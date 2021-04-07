#include "ContourData.h"

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
	//获取网格数据 并初始化网格范围
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

	setBoundingRect(QwtDoubleRect(xr.min,yr.min,xr.length(),yr.length()));
}

/**
* @brief ContourData::value 寻找等值线时获取网格的值
* @param double x
* @param double y
* @return double
*/
double ContourData::value(double x, double y) const
{
#if 0
	std::cerr << "x:" << x << ",y:" << y << std::endl;
#endif
	/**********插值算法******************

	a ******************* b
	*				 *
  e *_________ h     * f
	*		|		 *
	*		|		 *
	c ******************* d
			g
	已知a,b,c,d的值及坐标，和e,g的坐标。 坐标用大写表示。

	H = (A - C)/(E - C);
	W = (D - C)/(G - C);
	e = Hc + (1 - H)a;
	f = Hd + (1 - H)b;

	h = We + (1 - W)f;


	************************************/

	//获取点所在的网格范围（及abcd的值）

	auto vertex = getVertex(x, y);
	if (vertex.size() < 4)
		return 0.0;


	Grid A, B, C, D;
	A = vertex.at(0);
	B = vertex.at(1);
	C = vertex.at(2);
	D = vertex.at(3);

#if 0
	std::cerr << "X:" << x << ",Y:" << y << std::endl;
	for each (auto i in vertex)
	{
		std::cerr << i.x << "," << i.y << "," << i.value << std::endl;
	}
#endif

	float H = (A.y - C.y) / (A.y - y);
	float W = (D.x - C.x) / (D.x - x);
	float e = H*C.value + (1 - H)*A.value;
	float f = H*D.value + (1 - H)*B.value;
	float h = W*e + (1 - W)*f;
	return h;
}


QwtRasterData* ContourData::copy() const
{
	auto h5 = this->h5Data;
	ContourData *d = new ContourData(h5);
	d->loadPoint();
	return  d;
}

/**
* @brief ContourData::getVertex 根据位置信息获取所在网格的四个顶底点位置及值
* @param const double & x
* @param const double & y
* @return std::vector<ContourData::ContourData::Grid> 顶点顺序为 左上、右上、左下、右下
*/
std::vector<ContourData::Grid> ContourData::getVertex(const double& x, const double& y) const
{
	//获取行索引
	int rIndex = 1;
	for (; (rIndex*width)< grids.size(); rIndex++)
	{
		if (y < grids.at(rIndex*width).y)
			break;
	}
	//获取列索引
	int lIndex = 1;
	for (; lIndex < width; lIndex++)
	{
		if (x<grids.at(lIndex).x)
			break;
	}

	std::vector<Grid> vertex;
	if (lIndex > (grids.size() / height) || rIndex > (grids.size() / width))
		return vertex;

try
{
	Grid gd;
	gd = grids.at((rIndex)*width + lIndex - 1);
	vertex.push_back(gd);
	gd = grids.at((rIndex)*width + lIndex);
	vertex.push_back(gd);
	gd = grids.at((rIndex - 1)*width + lIndex - 1);
	vertex.push_back(gd);
	gd = grids.at((rIndex - 1)*width + lIndex);
	vertex.push_back(gd);
}
catch (...)
{
	return vertex;
}

	

	return vertex;
}

