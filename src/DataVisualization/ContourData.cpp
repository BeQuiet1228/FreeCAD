#include "ContourData.h"
#include <qvector.h>
#include <QRegExp>
#include <math.h>
#include <QRegExp>
#include <DataInformationGetter.h>
#include <qnumeric.h>
namespace DV {
	ContourData::ContourData(Hdf5Data& h5Data, const RunMod& mod /*= SINGLE_THREAD*/)
		:DirData(h5Data, mod), height(0), width(0)
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

		//判断方向是否跟结构图一样
		//不一样则调整方向
		if (isTruedir())
		{
			xg = *listValuesIter;
			listValuesIter++;
			yg = *listValuesIter;
			listValuesIter++;
			vg = *listValuesIter;
		}
		else {
			yg = *listValuesIter;
			listValuesIter++;
			xg = *listValuesIter;
			listValuesIter++;
			vg = *listValuesIter;
		}


		if (xg->size() == 0 || yg->size() == 0 || vg->size() == 0)
			return false;

		//预分配空间
		grids.clear();
		grids.reserve(xg->size() * yg->size());

		auto xIter = xg->begin();
		auto yIter = yg->begin();
		auto vIter = vg->begin();
		width = xg->size();
		height = yg->size();

		Rang vr;
		vr.min = vr.max = *vIter;
		Grid tempGrid;
		if (isTruedir()) {

			for (; yIter != yg->end() && vIter != vg->end(); yIter++)
			{
				for (xIter = xg->begin(); xIter != xg->end() && vIter != vg->end(); xIter++)
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
		}
		else {
			for (int h = 0; h < yg->size(); h++)
			{

				for (int w = 0; w < xg->size(); w++)
				{
					//生成网格信息
					tempGrid.x = xg->at(w);
					tempGrid.y = yg->at(h);
					tempGrid.value = vg->at(w * yg->size() + h);
					grids.push_back(tempGrid);

					//生成value范围信息
					if (tempGrid.value > vr.max)
						vr.max = tempGrid.value;
					else if (tempGrid.value < vr.min)
						vr.min = tempGrid.value;
				}
			}
		}

		xScale = *(xg.get());
		yScale = *(yg.get());
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
			if (grid->x > (w * xBlock + xr.min) && grid->y > (h * yBlock + yr.min))
			{
				data.append(grid->value);
				i++;
			}
			else {
				grid++;
			}
#else
			data.append(grid->value);
			grid++;
#endif			
		}
		//QwtMatrixRasterData *rasterData = new QwtMatrixRasterData;
		DefineMatrixRasterData* rasterData = new DefineMatrixRasterData;
		rasterData->setXScale(xScale);
		rasterData->setYScale(yScale);

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

		/*
			2022.7.5 更新
			之前判断索引数据大于取点数据时，使用该索引，这个逻辑会导致最前面的一个点永远无法取到。
			修改为判断大于之后，在判断前后的距离，取最近的距离
		*/
		//获取宽度索引
		for (; w < width; w++)
		{
			grid = grids.at(w);
			if (grid.x < x)
				continue;
			if(w == 0)
				break;
			auto agrid = grids.at(w - 1);
			w = abs(grid.x - x) < abs(agrid.x - x) ? w : w - 1;
			break;
		}
		//获取高度索引
		for (; h < height - 1; h++)
		{
			grid = grids.at(h * width);
			if (grid.y < y)
				continue;
			if(h == 0)
				break;
			auto agrid = grids.at((h - 1)*width);
			h = abs(grid.y - y) < abs(agrid.y - y) ? h : h - 1;
			break;
		}

		int index = w + h * width;
		if (index >= grids.size())
		{
			std::cerr << "ContourData::findGrid index out of range" << std::endl;
			Grid g;
			return g;
		}

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
		const std::string end = "  ";
		title += "观察时间:";
		title += DataInformationGetter::getObserveTime(headList.at(12)) + end;
		title += "观察分量:";
		title += DataInformationGetter::getObserveObejct(headList.at(2));
		//获取观察分量单位
		{
			if (headList.size() >= 15)
			{
				auto str = QString::fromStdString(headList.at(14)).simplified();
				auto lstr = str.split(" ");
				title += lstr.at(lstr.size() -1).toStdString();
			}
		}
		title +=end + "观测面:";
		title += DataInformationGetter::getObserveFace(headList.at(16)) + end;

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
		}
		else {
			xr = getAxisRangeFromName(xAxisName);
			yr = getAxisRangeFromName(yAxisName);
		}

		//判断方向是否正常，不正常则颠倒范围
		if (isTruedir())
		{
			setXRang(xr);
			setYRang(yr);
		}
		else {
			setXRang(yr);
			setYRang(xr);
		}



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
			}
			else {
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

	DefineMatrixRasterData::DefineMatrixRasterData()
	{

	}

	DefineMatrixRasterData::~DefineMatrixRasterData()
	{

	}

	double DefineMatrixRasterData::value(double x, double y) const
	{
		if ((!isInScal(xScale, x)) || (!isInScal(yScale, y)))
			return qQNaN();

		double value;

		switch (d_data->resampleMode)
		{
		case BilinearInterpolation:
		{
			int col1 = findIndex(xScale, x);;
			int row1 = findIndex(yScale, y);;
			int col2 = col1 + 1;
			int row2 = row1 + 1;

			double xp, yp;
			xp = (x - xScale.at(col1)) / (xScale.at(col2) - xScale.at(col1));
			yp = (y - yScale.at(row1)) / (yScale.at(row2) - yScale.at(row1));

			double v1, v2, v3, v4;
			v1 = d_data->value(row1, col1);
			v2 = d_data->value(row1, col2);
			v3 = d_data->value(row2, col1);
			v4 = d_data->value(row2, col2);

			double vi1, vi2;
			vi1 = v1 + (v2 - v1) * xp;
			vi2 = v3 + (v4 - v3) * xp;
			value = vi1 + (vi2 - vi1) * yp;

			break;
		}
		case NearestNeighbour:
		default:
		{
			int row = findIndex(yScale, y);
			int col = findIndex(xScale, x);

			// In case of intervals, where the maximum is included
			// we get out of bound for row/col, when the value for the
			// maximum is requested. Instead we return the value
			// from the last row/col

			if (row >= d_data->numRows)
				row = d_data->numRows - 1;

			if (col >= d_data->numColumns)
				col = d_data->numColumns - 1;

			value = d_data->value(row, col);
		}
		}

		return value;
	}

	/**
	* @brief DefineMatrixRasterData::findIndex 根据位置查找在标尺中所在的索引
	* @param const std::vector<float> & scale 标尺
	* @param const float & pos 位置
	* @return int 索引
	*/
	int DefineMatrixRasterData::findIndex(const std::vector<float>& scale, const double& pos) const
	{



#if 0
		int i;

		for (int index = 0; index < scale.size(); index++)
		{
			if (pos < scale.at(index)) {
				//return index - 1;
				i = index - 1;
				break;
			}

		}

		unsigned int index = scale.size() / 2;

		float p;
		unsigned int add = 0;
		for (; index > 0 && index < scale.size();)
		{
			p = scale.at(index + add);
			if (p < pos)
			{
				add += index;
			}
			index = index / 2;
		}

		if (add != i)
		{
			int a;
			a++;
		}

		return add;
#else
		unsigned int fm, am;
		fm = 0;
		am = scale.size() - 1;
		unsigned int index;

		if (pos < scale.at(fm) || pos > scale.at(am))
			return -1;
		while ((am - fm) > 1) {
			index = (am - fm) / 2;
			scale.at(index + fm) > pos ? am = index + fm : fm += index;
		}
		return fm;
#endif
	}

	bool DefineMatrixRasterData::isInScal(const std::vector<float>& scale, const double& pos) const
	{
		if (scale.size() < 2)
			return false;

		return pos >= *scale.begin() && pos <= *scale.rbegin();
	}
	void ContourData::setValueRang(const Rang& r) {
		std::lock_guard<std::mutex> am(ValueRangMutex);
		valueRang = r;
	}
	Data::Rang ContourData::getVlaueRange() {
		std::lock_guard<std::mutex> am(ValueRangMutex);
		return valueRang;
	}
	void DefineMatrixRasterData::setXScale(const std::vector<float>& xScale) {
		this->xScale = xScale;
	}
	void DefineMatrixRasterData::setYScale(const std::vector<float>& yscale) {
		this->yScale = yscale;
	}
	/*********************************/
	ContourData::Grid::Grid() :x(0.0), y(0.0), value(0.0) {}

	std::vector<ContourData::Grid>& ContourData::getGrids()
	{
		return grids;
	}
	unsigned int ContourData::getWidth()
	{
		return width;
	}
	unsigned int ContourData::getHeight()
	{
		return height;
	}
};
