#include "ContourData.h"
#include <qvector.h>
#include <QRegExp>
#include <math.h>
#include <QRegExp>
#include <DataInformationGetter.h>
ContourData::ContourData(Hdf5Data& h5Data, const RunMod& mod /*= SINGLE_THREAD*/)
	:XYData(h5Data, mod), height(0), width(0)
{

}

ContourData::~ContourData()
{

}

void ContourData::restorDeriveData()
{

}

bool ContourData::initXYRang()
{
	return true;
}

/**
* @brief ContourData::loadPoint 载入点数据
* @return bool
*/
bool ContourData::loadPoint()
{
	Data::ListValuesPtr listValues;
	bool ok = autoModGetSourceData(listValues);

	if (!ok || !listValues || listValues->size() != 3)
		return false;

	//获取网格数据
	ValuesPtr xg, yg, vg;
	auto listValuesIter = listValues->begin();
	xg = *listValuesIter;
	listValuesIter++;
	yg = *listValuesIter;
	listValuesIter++;
	vg = *listValuesIter;

	if (xg->size() == 0 || yg->size() == 0 || vg->size() == 0)
		return false;

	//预分配空间
	grids.clear();
	grids.reserve(xg->size()*yg->size());

	auto xIter = xg->begin();
	auto yIter = yg->begin();
	auto vIter = vg->begin();

	width = xg->size();
	height = yg->size();

	Rang vr;
	vr.min = vr.max = *vIter;
	Grid tempGrid;
	for (; yIter != yg->end() && vIter != vg->end(); yIter++)
	{
		for (xIter = xg->begin(); xIter != xg->end() && vIter != vg->end() ; xIter++)
		{
			//生成网格信息
			tempGrid.x = *xIter;
			tempGrid.y = *yIter;
			tempGrid.value = *vIter;
			grids.push_back(tempGrid);

			//生成value范围信息
			if (*vIter > vr.max)
				vr.max = *vIter;
			else if (*vIter < vr.min)
				vr.min = *vIter;
			vIter++;
		}
	
	}

	//初始化数据范围
	setValueRang(vr);
	Rang xr, yr;
	
	xr.min = *(xg->begin());
	xIter = xg->end();
	xIter--;
	xr.max = *xIter;

	yr.min = *(yg->begin());
	yIter = yg->end();
	yIter--;
	yr.max = *yIter;

	setXRang(xr);
	setYRang(yr);
	
	setXYRange();
}

/**
* @brief ContourData::getQwtMatrixRasterData 获取一个rasterData对象
* @return QwtMatrixRasterData*
*/
QwtMatrixRasterData* ContourData::getQwtMatrixRasterData()
{
	QVector<double> data;
	Rang xr = getXRang();
	Rang yr = getYRang();


	float xBlock = xr.length() / width;
	float yBlock = yr.length() / height;

	auto grid = grids.begin();
	for (int i = 0; i < grids.size() && grid != grids.end(); )
	{
#if 0 //是否处理非均匀网格
		int w = i % width;
		int h = i / width;
		if (grid->x > (w*xBlock + xr.min) && grid->y > (h*yBlock + yr.min))
		{
			data.append(grid->value);
			i++;
		}else{
			grid++;
		}
#else
		data.append(grid->value);
		grid++;
#endif			
	}
	QwtMatrixRasterData *rasterData = new QwtMatrixRasterData;
	rasterData->setValueMatrix(data, width);

	rasterData->setInterval(Qt::XAxis,
		QwtInterval(xr.min, xr.max, QwtInterval::ExcludeMaximum));
	rasterData->setInterval(Qt::YAxis,
		QwtInterval(yr.min, yr.max, QwtInterval::ExcludeMaximum));

	Rang vr = getVlaueRange();
	rasterData->setInterval(Qt::ZAxis, QwtInterval(vr.min, vr.max));
	rasterData->setResampleMode(QwtMatrixRasterData::BilinearInterpolation);
	return rasterData;
}

/**
* @brief ContourData::findGrid 根据坐标寻找网格
* @param const float & x
* @param const float & y
* @return ContourData::Grid
*/
ContourData::Grid ContourData::findGrid(const float& x, const float& y)
{
	int w(0), h(0);

	Grid grid;

	//获取宽度索引
	for (unsigned int index = width / 2; index > 0 && index < width ;)
	{
		grid = grids.at(index + w);
		if (grid.x < x)
		{
			w += index;
		}
		index = index / 2;
	}
	//获取高度索引
	for (unsigned int index = height / 2; index > 0 && index < height;)
	{
		grid = grids.at(index*width + h*width);
		if (grid.y < y)
		{
			h += index;
		}
		index = index / 2;
	}

	int index = w + h*width;
#ifdef MY_DEBUG
	if (index > grids.size())
	{
		std::cerr << "ContourData::findGrid index out of range" << std::endl;
		Grid g;
		return g;
	}
#endif
	return grids.at(index);
}

std::vector<float> ContourData::getStructFace()
{
	if (headList.size() < 17)
		return std::vector<float>();
	
	QString qstr = QString::fromStdString(headList[16]);
	QStringList sl = qstr.split("TO");
	if (sl.size() != 2)
		return std::vector<float>();
	QString point1 = sl[0];
	QString point2 = sl[1];

	sl = point1.split("(");
	if (sl.size() != 2)
		return std::vector<float>();
	point1 = sl[1];

	sl = point1.split(")");
	if (sl.size() != 2)
		return std::vector<float>();
	point1 = sl[0];

	sl = point1.split(",");
	if (sl.size() < 2)
		return std::vector<float>();

	std::vector<float> values;
	for (auto iter = sl.begin(); iter != sl.end(); iter++)
	{
		values.push_back(iter->toFloat());
	}

	sl = point2.split("(");
	if (sl.size() != 2)
		return std::vector<float>();
	point2 = sl[1];

	sl = point2.split(")");
	if (sl.size() != 2)
		return std::vector<float>();
	point2 = sl[0];

	sl = point2.split(",");
	if (sl.size() < 2)
		return std::vector<float>();

	for (auto iter = sl.begin(); iter != sl.end(); iter++)
	{
		values.push_back(iter->toFloat());
	}

	return values;
}

std::string ContourData::getInformationTitle()
{
	std::string title;
	title += "观察时间:";
	title += DataInformationGetter::getObserveTime(headList.at(12)) + "\n";
	title += "观察分量:";
	title += DataInformationGetter::getObserveObejct(headList.at(2)) + "\n";
	title += "观测面:\n";
	title += DataInformationGetter::getObserveFace(headList.at(16)) + "\n";

	return title;
}

/**
* @brief ContourData::setXYRange 设置数据渲染范围，这里的范围能从数据中读取，会有误差，得从观测面中读取
* @return void
*/
void ContourData::setXYRange()
{
	std::vector<float> structFace = getStructFace();

	Data::Rang xr, yr;

	//建通2d等位图数据
	if (structFace.size() == 4) {
		xr.max = std::max(structFace[0], structFace[2]);
		xr.min = std::min(structFace[0], structFace[2]);
		yr.max = std::max(structFace[1], structFace[3]);
		yr.min = std::min(structFace[1], structFace[3]);
	}else {
		xr = getAxisRangeFromName(xAxisName);
		yr = getAxisRangeFromName(yAxisName);
	}


	setXRang(xr);
	setYRang(yr);

}

Data::Rang ContourData::getAxisRangeFromName(const std::string& name)
{
	std::vector<float> structFace = getStructFace();
	Data::Rang r;
	switch (stringToDirection(name))
	{
	default:
		return r;
		break;
	case X:
		r.min = std::min(structFace[0], structFace[3]);
		r.max = std::max(structFace[0], structFace[3]);
		break;
	case Y:
		r.min = std::min(structFace[1], structFace[4]);
		r.max = std::max(structFace[1], structFace[4]);
		break;
	case Z:
		if (h5Data.coordinateSystem != Hdf5Data::CYLINDER)
		{
			r.min = std::min(structFace[2], structFace[5]);
			r.max = std::max(structFace[2], structFace[5]);
		}else {
			r.min = std::min(structFace[0], structFace[3]);
			r.max = std::max(structFace[0], structFace[3]);
		}
		break;
	case R:
		if (h5Data.coordinateSystem != Hdf5Data::CYLINDER)
		{
			r.min = std::min(structFace[0], structFace[3]);
			r.max = std::max(structFace[0], structFace[3]);
		}
		else {
			r.min = std::min(structFace[1], structFace[4]);
			r.max = std::max(structFace[1], structFace[4]);
		}
		break;
	case THETA:
		if (h5Data.coordinateSystem != Hdf5Data::CYLINDER)
		{
			r.min = std::min(structFace[1], structFace[4]);
			r.max = std::max(structFace[1], structFace[4]);
		}
		else {
			r.min = std::min(structFace[2], structFace[5]);
			r.max = std::max(structFace[2], structFace[5]);
		}
		break;

	}
	return r;
}
