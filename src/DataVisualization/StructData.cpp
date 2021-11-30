#include "StructData.h"
#include <QPoint>
#include<thread>
#ifdef MY_DEBUG
#include <QDebug>
#endif
#include<windows.h>
#define THRESHOLD (1000000)  //限定门限
#include <process.h>
//#include <math.h>

namespace threadSites{

	typedef struct lps
	{
		unsigned __int64 site1;
		unsigned __int64 site2;
		StructData* lp;
	};
	HANDLE threadEvent = nullptr;
};
unsigned int __stdcall functhread(void*);
/**
* @brief StructData::StructData 构造函数
* @param Hdf5Data& heData
* @param DirectionType _type 方向
* @param const RunMod& mod
*/
StructData::StructData(Hdf5Data& heData, DirectionType _type, const RunMod& mod):XYData(heData,mod),istrue(false),
isloadRoom(false){
	switch (heData.coordinateSystem)
	{
	case Hdf5Data::CARTESIAN:
	{
		//当前为cartexian
		mCtype = C_TYPE::CARTESIAN;
		switch (_type)
		{
		case X_Y:
		case X_Z:
		case Y_Z:
			mType = _type; break;
		default:
			mType = X_Y; break;
		}
	}
		break;
	case Hdf5Data::CYLINDER:
	{
		//当前为cylindrical
		mCtype = C_TYPE::CYLINDRICAL;
		switch (_type)
		{
		case R_Z:
		case R_THETA:
			mType = _type; break;
		default:
			mType = R_Z; break;

		}
	}
		break;
	case Hdf5Data::POLAR:
	{
		//当前为polar
		mCtype = C_TYPE::POLAR;
		switch (_type)
		{
		case R_Z:
		case R_THETA:
			mType = _type; break;
		default:
			mType = R_Z; break;
		}
	}
		break;
	}
}
/**
* @brief StructData::StructData 构造函数
* @param Hdf5Data& heData
* @param _3DPointf startpoint  三维点位1
* @param _3DPointf endpoint 三维点位2
* @parame const RunMod& mod
*/
StructData::StructData(Hdf5Data& heData, _3DPointf startpoint, _3DPointf endpoint, const RunMod& mod):
XYData(heData,mod),istrue(true),mstartpoint(startpoint),mendpoint(endpoint),isloadRoom(false){
	//std::vector<std::string> headerlist = autoHeaderInfo();
	int res = (startpoint == endpoint);
	_face_point_index = startpoint[res];
	//auto headeriter = headerlist.begin()+3;
	switch (heData.coordinateSystem)
	{
	case Hdf5Data::POLAR:
	{
		mCtype = C_TYPE::POLAR;
		//极坐标系  R pin Z
		switch (res)
		{
		case 1:
		case 2:
			mType = R_Z; break;
		case 3:
			mType = R_THETA; break;
		}
	}break;
	case  Hdf5Data::CYLINDER:
	{
		//当前为cylindrical
		mCtype = C_TYPE::CYLINDRICAL;//z_R_the
		switch (res)
		{
		case 1:
			mType = R_THETA; break;
		case 2:
		case 3:
			mType = R_Z; break;
		}
	}break;
	case Hdf5Data::CARTESIAN:
	{
		//当前为cartexian
		mCtype = C_TYPE::CARTESIAN;
		switch (res)
		{
		case 1:
			mType = Y_Z; break;
		case 2:
			mType = X_Z; break;
		case 3:
			mType = X_Y; break;
		}
	}break;
	}
}
/**
* @brief StructData::loadPoint  加载点位信息
* @return bool 
*/
bool StructData::loadPoint()
{
	setXYTag(mType);
	switch (mCtype)
	{
	case POLAR:
		return loadPointPolar();
	case CYLINDRICAL:
		return loadPointCylindrical();
	case CARTESIAN:
		return loadPointCartesian();
	}
	
}
/**
* @brief StructData::loadPointCartesian 加载点位-cartesian坐标系
* @return bool 
*/
bool StructData::loadPointCartesian()
{
	Data::ListValuesPtr listValues;
	bool ok = autoModGetSourceData(listValues);//获取原始数据
	if (!ok && !listValues && listValues->size() == 0)
		return false;
	auto it = (listValues->begin());
	Data::ValuesPtr IM1X = *it; it++;//x
	Data::ValuesPtr IM2X = *it; it++;//y
	Data::ValuesPtr IM3X = *it; it++;//z
	Data::ValuesPtr datasetkmt = *it;
	//X_Y_Z
	switch (mType)
	{
	case X_Y:
	{
		//设置X_Y的范围
		Rang xr;
		xr.max = *(IM1X->end() - 1);
		xr.min = *(IM1X->begin());
		Rang yr;
		yr.min = *(IM2X->begin());
		yr.max = *(IM2X->end() - 1);
		setXRang(xr);
		setYRang(yr);
		pointXSize = IM1X->size();
		pointYSize = IM2X->size();
	}
		break;
	case Y_Z:
	{
		//设置X_Y的范围
		Rang xr;
		Rang yr;
		xr.max = *(IM2X->end()-1);
		xr.min = *(IM2X->begin());
		yr.max = *(IM3X->end() - 1);
		yr.min = *(IM3X->begin());
		setXRang(xr);
		setYRang(yr);
		pointXSize = IM2X->size();
		pointYSize = IM3X->size();
	}
		break;
	case X_Z:
	{
		Rang xr, yr;
		xr.max = *(IM1X->end()-1);
		xr.min = *(IM1X->begin());
		yr.max = *(IM3X->end() - 1);
		yr.min = *(IM3X->begin());
		setXRang(xr);
		setYRang(yr);
		pointXSize = IM1X->size();
		pointYSize = IM3X->size();
	}
		break;
	}
	return true;
}
/**
* @brief StructData::loadPointCylindrical 加载点位-cylindrical坐标系
* @return bool
*/
bool StructData::loadPointCylindrical()
{
	Data::ListValuesPtr listValues;
	bool ok = autoModGetSourceData(listValues);//获取原始数据
	if (!ok && !listValues && listValues->size() == 0)
		return false;
	auto it = (listValues->begin());
	Data::ValuesPtr IM1X = *it; it++;
	Data::ValuesPtr IM2X = *it; it++;
	Data::ValuesPtr IM3X = *it; it++;
	Data::ValuesPtr datasetkmt = *it;
	//Z_R_THETA
	switch (mType)
	{
	case R_Z:
	{
		//设置X_Y的范围
		Rang xr, yr;
		xr.max = *(IM1X->end()-1);
		xr.min = *(IM1X->begin());
		yr.max = *(IM2X->end() - 1);
		yr.min = *(IM2X->begin());
		setXRang(xr);
		setYRang(yr);
		pointXSize = IM1X->size();
		pointYSize = IM2X->size();
	}
		break;
	case R_THETA:
	{
		//设置X_Y的范围
		Rang xr;
		Rang yr;
		xr.max = *(IM2X->end() - 1);
		xr.min = -xr.max;
		yr = xr;
		setXRang(xr);
		setYRang(yr);
		pointXSize = IM2X->size();
		pointYSize = IM2X->size();
	}
		break;
	}
	return true;
}
/**
* @brief StructData::loadPointPolar 加载点位--polar坐标系
* @return bool
*/
bool StructData::loadPointPolar()
{
	Data::ListValuesPtr listValues;
	bool ok = autoModGetSourceData(listValues);//获取原始数据
	if (!ok && !listValues && listValues->size() == 0)
		return false;
	auto it = (listValues->begin());

	Data::ValuesPtr IM2X = *it; it++;//R
	Data::ValuesPtr IM3X = *it; it++;//THETA
	Data::ValuesPtr IM1X = *it; it++;//Z
	Data::ValuesPtr datasetkmt = *it;
	//R_THETA_Z
	switch (mType)
	{
	case R_Z:
	{
		//设置X_Y的范围
		Rang xr;
		xr.max= *(IM1X->end() - 1);
		xr.min =*(IM1X->begin());
		Rang yr;
		yr.min = *(IM2X->begin());
		yr.max = *(IM2X->end()-1);
		setXRang(xr);
		setYRang(yr);
		pointXSize = IM1X->size();
		pointYSize = IM2X->size();
	}
		break;
	case R_THETA:
	{
		//设置X_Y的范围
		Rang xr;
		Rang yr;
		xr.max = *(IM2X->end() - 1);
		xr.min = -xr.max;
		yr = xr;
		setXRang(xr); 
		setYRang(yr);
		pointXSize = IM2X->size();
		pointYSize = IM2X->size();
	}
		break;
	}
	return true;
}
/**
* @brief StructData::loadroom 获取信息
* @return bool
*/
bool StructData::loadroom()
{
	if (isloadRoom)
		return true;
#if MY_DEBUG
	//测试数据生成时间
	LARGE_INTEGER startTime;
	LARGE_INTEGER endTime;
	LARGE_INTEGER cpufer;
	QueryPerformanceFrequency(&cpufer);
	QueryPerformanceCounter(&startTime);
#endif
	switch (mCtype)
	{
	case POLAR:
		loadroomPolar(); break;
	case CYLINDRICAL:
		 loadroomCylindrical();break;
	case CARTESIAN:
		loadroomCartesian(); break;
	}
#if MY_DEBUG
	QueryPerformanceCounter(&endTime);
	auto interval =(static_cast<double>(endTime.QuadPart) - static_cast<double>(startTime.QuadPart)) / static_cast<double>(cpufer.QuadPart);
	qDebug() << "processingData(interval):" << interval;
#endif
	isloadRoom = true;
	return true;
}
/**
* @brief StructData::loadroomPolar 转换成绘制数据-polar坐标系
* @return bool
*/
bool StructData::loadroomPolar(){
 
	switch (mType)
	{
	case R_Z:
		return loadroomPolarRz();
	case R_THETA:
		return loadroomPolarRtheta();
	}
	return false;
}
/**
* @brief StructData::loadroomCylindrical 转换成绘制数据-cylindrical坐标系
* @return bool
*/
bool StructData::loadroomCylindrical(){
	switch (mType)
	{
	case R_Z:
		return loadroomCylindricalRz();
	case R_THETA:
		return loadroomCylindricalRtheta();
	}
	return false;
}
/**
* @brief StructData::loadroomCartesian 转换成绘制数据-cartesian坐标
* @return bool
*/
bool StructData::loadroomCartesian(){
	switch (mType)
	{
	case X_Y:
		return loadroomCartesianXy();
	case X_Z:
		return loadroomCartesianXz();
	case Y_Z:
		return loadroomCartesianYz();
	}
	return false;
}
/**
* @brief StructData::loadroomPolarRz 转换成绘制数据-polar坐标系-R_Z方向
* @return bool 
*/
bool StructData::loadroomPolarRz()
{
	if (pointXSize<2||pointYSize<2)
		return false;
	//简化数据处理流程----通过打印处理时间比之前的快1/3
	Data::ListValuesPtr listValues;
	autoModGetSourceData(listValues);//获取原始数据
	//获取dataSetKmt里的全部数据
	auto it = listValues->begin();
	Data::ValuesPtr IM1X = *it; it++;
	Data::ValuesPtr IM2X = *it; it++;
	Data::ValuesPtr IM3X = *it; it++;
	Data::ValuesPtr datasetkmt = *it;
	//默认取中间位置
	int index = IM2X->size() / 2+IM2X->size()%2;
	if (istrue)
	{
		int index_min = 1;
		float distancemin = 10000.0f;
		for (auto i = 0; i < IM2X->size(); i++)
		{
			float curdistance = abs(*(IM2X->begin() + i) - _face_point_index);
			if (curdistance<distancemin)
			{
				distancemin = curdistance;
				index_min = i + 1;
			}
		}
		index = index_min;
	}
	std::map<int, std::vector<QRectF>> allinfo;
	std::map<int, std::vector<QPoint>> pointlist;//用来判断线段
	for(auto itersetkmt=datasetkmt->begin();itersetkmt!=datasetkmt->end();)
	{
		unsigned __int64 x1=*itersetkmt;itersetkmt++;
		unsigned __int64 x2=*itersetkmt;itersetkmt++;
		unsigned __int64 x3=*itersetkmt;itersetkmt++;
		unsigned __int64 proper=*itersetkmt;itersetkmt++;
		//qDebug() << "x1:" << x1 << "x2:" << x2 << "x3:" << x3 << "proper:" << proper;
		if (x2 == index&&x3 <= IM3X->size() && x1 <= IM1X->size())
		{
			std::list<unsigned __int64> rectpro = isAnAttritbute(proper, RECTPROPER);
			std::list<unsigned __int64> linepro = isAnAttritbute(proper, LINEPROPER);
			if (!linepro.empty())
			{
				for each (auto  var in linepro)
				{
					pointlist[var].push_back(QPoint(x3 - 1, x1 - 1));
				}
			}
			if (!rectpro.empty())
			{
				//添加限定条件
				if (x3 == IM3X->size() || x1 == IM1X->size())
					continue;
				QRectF rect;
				rect.setLeft(*(IM3X->begin() + x3 - 1));
				rect.setRight(*(IM3X->begin() + x3));
				rect.setBottom(*(IM1X->begin() + x1 - 1));
				rect.setTop(*(IM1X->begin() + x1));
				for each (auto  var in rectpro)
				{
					allinfo[var].push_back(rect);
				}
			}
			
		}
	}
	//开始生成线段
	createLines(pointlist, IM3X, IM1X);
	allcutroom.swap(allinfo);
	return true;
}
/**
* @brief StructData::GetdatasetKmtPolar 获取datasetkmt的数据-polar坐标系-R_Z方向
* @return std::vector<StructData::DaTaKmt>
*/
std::vector<StructData::DaTaKmt> StructData::GetdatasetKmtPolar()
{
	std::vector<DaTaKmt> list;
	Data::ListValuesPtr listValues;
	bool ok = autoModGetSourceData(listValues);//获取原始数据
	//获取dataSetKmt里的全部数据
	auto it = listValues->begin();
	Data::ValuesPtr IM2X = *it; it++;
	Data::ValuesPtr IM3X = *it; it++;
	Data::ValuesPtr IM1X = *it; it++;
	Data::ValuesPtr datasetkmt = *it;
	for (auto iterkmt = datasetkmt->begin(); iterkmt != datasetkmt->end();)
	{
		//polar
		DaTaKmt temp;
		temp.point2 = *iterkmt;	iterkmt++;
		temp.point3 = *iterkmt;	iterkmt++;
		temp.point1 = *iterkmt;	iterkmt++;
		temp.pointproperty = *iterkmt; iterkmt++;
		list.push_back(temp);
	}
	return list;
}
/**
* @brief StructData::loadroomPolarRtheta 转换成绘制信息-polar坐标系-R_THETA方向
* @return bool
*/
bool StructData::loadroomPolarRtheta()
{
	if (pointXSize < 2 || pointYSize < 2)
		return false;
	{
		std::map<int, std::vector<CutCir>> listcir;
		std::vector<float> r_val;
		std::vector<float> rand_val;
		Data::ListValuesPtr listValues;
		bool ok = autoModGetSourceData(listValues);//获取原始数据
		auto it = listValues->begin();
		Data::ValuesPtr IM2X = *it; it++;
		Data::ValuesPtr IM3X = *it; it++;
		Data::ValuesPtr IM1X = *it; it++;
		Data::ValuesPtr datasetkmt = *it;
		//原点
		QPointF p0 = QPointF(0.0, 0.0);
		//获取所有半径
		for (auto iter2mx = IM2X->begin(); iter2mx != IM2X->end(); iter2mx++)
			r_val.push_back(*iter2mx);
		for (auto iter3mx = IM3X->begin(); iter3mx != IM3X->end(); iter3mx++)
			rand_val.push_back(*iter3mx);
#pragma region 遍历所有切割圆环
		std::vector<CutCir> CutCirlist;
		for (auto index_R = 0; index_R < r_val.size() - 1; index_R++)
		{
			for (auto index_rand = 0; index_rand < rand_val.size() - 1; index_rand++)
			{
				CutCir tempCurcir;
				float startAngle = rand_val[index_rand];
				float endAngle = rand_val[index_rand + 1];
				//内圈半径
				tempCurcir.R_inner = r_val[index_R];
				//外圈半径
				tempCurcir.R_excir = r_val[index_R + 1];
				//内圈切点
				tempCurcir.inner1 = QPointF(
					(tempCurcir.R_inner * cos(startAngle)),
					(tempCurcir.R_inner * sin(startAngle)));
				tempCurcir.inner2 = QPointF(
					(tempCurcir.R_inner * cos(endAngle)),
					(tempCurcir.R_inner * sin(endAngle)));
				//外圈切点
				tempCurcir.excir1 = QPointF(
					(tempCurcir.R_excir * cos(startAngle)),
					(tempCurcir.R_excir * sin(startAngle)));
				tempCurcir.excir2 = QPointF(
					(tempCurcir.R_excir * cos(endAngle)),
					(tempCurcir.R_excir * sin(endAngle)));
				//开始角度，结束角度
				tempCurcir.startAngle = startAngle;
				tempCurcir.endAngle = endAngle;
				CutCirlist.push_back(tempCurcir);
			}
		}
#pragma endregion
#pragma region 筛选属性
		//默认取中间位置
		int index = IM1X->size() / 2+IM1X->size()%2;
		if (istrue)
		{
			int index_min = 1;
			float distancemin = 10000.0f;
			for (auto i = 0; i < IM1X->size(); i++)
			{
				float curdistance = abs(*(IM1X->begin() + i) - _face_point_index);
				if (curdistance < distancemin)
				{
					distancemin = curdistance;
					index_min = i + 1;
				}
			}
			index = index_min;
		}
		int CutNum = rand_val.size() - 1;
		std::vector<DaTaKmt> datakmtinfo = GetdatasetKmtPolar();
		for each (DaTaKmt var in datakmtinfo)
		{
			if (var.point1 == index&&var.point3 < rand_val.size())
			{

				__int64 cutCirSize = (var.point2 - 1) * CutNum + (var.point3 - 1);
				if (cutCirSize < CutCirlist.size())
				{
					listcir[var.pointproperty].push_back(CutCirlist[(var.point2 - 1) * CutNum + (var.point3 - 1)]);
				}
			}
		}
#pragma endregion 
		allcutroomcir.swap(listcir);
	}
	return true;
}
/**
* @brief StructData::loadroomCylindricalRz 转换成绘制信息-cylindrical坐标系-R_Z方向
* @return bool
*/
bool StructData::loadroomCylindricalRz(){
	if (pointXSize < 2 || pointYSize < 2)
		return false;
	//简化数据处理流程----通过打印处理时间比之前的快1/3
	Data::ListValuesPtr listValues;
	autoModGetSourceData(listValues);//获取原始数据
	//获取dataSetKmt里的全部数据
	auto it = listValues->begin();
	Data::ValuesPtr IM1X = *it; it++;
	Data::ValuesPtr IM2X = *it; it++;
	Data::ValuesPtr IM3X = *it; it++;
	Data::ValuesPtr datasetkmt = *it;
	QMap<int, QVector<QRectF>> allinfo;
	//默认取中间位置
	int index = IM3X->size() / 2+IM3X->size()%2;
	if (istrue)
	{
		int index_min = 1;
		float distancemin = 10000.0f;
		_face_point_index;
		for (auto i = 0; i < IM3X->size(); i++)
		{
			float curdistance = abs(*(IM3X->begin() + i) - _face_point_index);
			if (curdistance < distancemin)
			{
				distancemin = curdistance;
				index_min = i + 1;
			}
		}
		index = index_min;
	}
#ifdef MY_DEBUG
	qDebug() << datasetkmt->size();
#endif
	allcutroom.clear();
	std::map<int, std::vector<QPoint>> pointlist;//用来暂时存储线段的所有点
	for (auto itersetkmt = datasetkmt->begin(); itersetkmt != datasetkmt->end();)
	{
		unsigned __int64 x1 = *itersetkmt; itersetkmt++;
		unsigned __int64 x2 = *itersetkmt; itersetkmt++;
		unsigned __int64 x3 = *itersetkmt; itersetkmt++;
		unsigned __int64 proper = *itersetkmt; itersetkmt++;
		if (x3 == index&& x1 <=IM1X->size()&&x2<=IM2X->size())
		{
			std::list<unsigned __int64> rectPro = isAnAttritbute(proper,RECTPROPER);
			std::list<unsigned __int64> linePro = isAnAttritbute(proper, LINEPROPER);
			if (!linePro.empty())
			{
				int x = x1 - 1, y = x2 - 1;
				for each (auto var in linePro)
				{
					pointlist[var].push_back(QPoint(x, y));
				}
			}
			if (!rectPro.empty())
			{
				if (x1 == IM1X->size() || x2 == IM2X->size())
					continue;
				QRectF rect;
				rect.setLeft(*(IM1X->begin() + x1 - 1));
				rect.setRight(*(IM1X->begin() + x1));
				rect.setBottom(*(IM2X->begin() + x2 - 1));
				rect.setTop(*(IM2X->begin() + x2));
				for each (auto var in rectPro)
				{
					allcutroom[var].push_back(rect);
				}
			}
			
		}
	}
	createLines(pointlist, IM1X,IM2X);
	return true;
}
/**
* @brief StructData::loadroomCylindricalRtheta 获取绘制信息-cylindrical坐标系-R_THETA方向
* @return bool
*/
bool StructData::loadroomCylindricalRtheta(){
	//qreal pi = 3.141592653589793;
	if (pointXSize < 2 || pointYSize < 2)
		return false;
	{
		std::map<int, std::vector<CutCir>> listcir;
		std::vector<float> r_val;
		std::vector<float> rand_val;
		Data::ListValuesPtr listValues;
		bool ok = autoModGetSourceData(listValues);//获取原始数据
		auto it = listValues->begin();
		Data::ValuesPtr IM1X = *it; it++;
		Data::ValuesPtr IM2X = *it; it++;
		Data::ValuesPtr IM3X = *it; it++;
		Data::ValuesPtr datasetkmt = *it;
		//默认取中间位置
		int index = IM1X->size() / 2 + IM1X->size() % 2;
		//		int index = 4;
		if (istrue)
		{
			int index_min = 1;
			float distancemin = 10000.0f;
			_face_point_index;
			for (auto i = 0; i < IM1X->size(); i++)
			{
				float curdistance = abs(*(IM1X->begin() + i) - _face_point_index);
				if (curdistance < distancemin)
				{
					distancemin = curdistance;
					index_min = i + 1;
				}
			}
			index = index_min;
		}
		//原点
		QPointF p0 = QPointF(0.0, 0.0);
		//获取所有半径
		for (auto iter2mx = IM2X->begin(); iter2mx != IM2X->end(); iter2mx++)
			r_val.push_back(*iter2mx);
		for (auto iter3mx = IM3X->begin(); iter3mx != IM3X->end(); iter3mx++)
			rand_val.push_back(*iter3mx);
#pragma region 遍历所有切割圆环
		std::vector<CutCir> CutCirlist;
		for (auto index_R = 0; index_R < r_val.size() - 1; index_R++)
		{
			for (auto index_rand = 0; index_rand < rand_val.size() - 1; index_rand++)
			{
				qreal startangle = rand_val[index_rand];
				qreal endangle = rand_val[index_rand + 1];
				CutCir tempCurcir;
				//内圈半径
				tempCurcir.R_inner = r_val[index_R];
				//外圈半径
				tempCurcir.R_excir = r_val[index_R + 1];
				//内圈切点
				tempCurcir.inner1 = QPointF(
					(tempCurcir.R_inner * cos(startangle)),
					(tempCurcir.R_inner * sin(startangle)));
				tempCurcir.inner2 = QPointF(
					(tempCurcir.R_inner * cos(endangle)),
					(tempCurcir.R_inner * sin(endangle)));
				//外圈切点
				tempCurcir.excir1 = QPointF(
					(tempCurcir.R_excir * cos(startangle)),
					(tempCurcir.R_excir * sin(startangle)));
				tempCurcir.excir2 = QPointF(
					(tempCurcir.R_excir * cos(endangle)),
					(tempCurcir.R_excir * sin(endangle)));
				//开始角度，结束角度
				tempCurcir.startAngle = startangle;
				tempCurcir.endAngle = endangle;
				CutCirlist.push_back(tempCurcir);
			}
		}
#pragma endregion
#pragma region 筛选属性
		int CutNum = rand_val.size() - 1;
		std::vector<DaTaKmt> datakmtinfo = GetdatasetKmtCylindrical();
		for each (DaTaKmt var in datakmtinfo)
		{
			if (var.point1 == index && var.point3 < rand_val.size())
			{

				__int64 cutCirSize = (var.point2 - 1) * CutNum + (var.point3 - 1);
				if (cutCirSize < CutCirlist.size())
				{
					listcir[var.pointproperty].push_back(CutCirlist[(var.point2 - 1) * CutNum + (var.point3 - 1)]);
				}
			}
		}
#pragma endregion 
		/**************************************/
		allcutroomcir.swap(listcir);
	}
	return true;
}
/**
* @brief StructData::GetdatasetKmtCylindrical 获取datasetkmt信息-cylindrical坐标系-R_Z方向
* @return std::vector<StructData::DaTaKmt>
*/
std::vector<StructData::DaTaKmt> StructData::GetdatasetKmtCylindrical(){
	std::vector<DaTaKmt> list;
	Data::ListValuesPtr listValues;
	bool ok = autoModGetSourceData(listValues);//获取原始数据
	//获取dataSetKmt里的全部数据
	auto it = listValues->begin();
	Data::ValuesPtr IM1X = *it; it++;
	Data::ValuesPtr IM2X = *it; it++;
	Data::ValuesPtr IM3X = *it; it++;
	Data::ValuesPtr datasetkmt = *it;
	for (auto iterkmt = datasetkmt->begin(); iterkmt != datasetkmt->end();)
	{
		//polar
		DaTaKmt temp;
		temp.point1 = *iterkmt;	iterkmt++;
		temp.point2 = *iterkmt;	iterkmt++;
		temp.point3 = *iterkmt;	iterkmt++;
		temp.pointproperty = *iterkmt; iterkmt++;
		list.push_back(temp);
	}
	return list;
}

/**
* @brief StructData::loadroomCartesianXy 转换绘制信息-cartesian坐标系-X_Y方向
* @return bool
*/
bool StructData::loadroomCartesianXy(){
	if (pointXSize < 2 || pointYSize < 2)
		return false;
	//简化了数据处理流程,通过打印时间比之前的处理方式快了1/3。后续会做替换
	Data::ListValuesPtr listValues;
	autoModGetSourceData(listValues);//获取原始数据
	//获取dataSetKmt里的全部数据
	auto it = listValues->begin();
	Data::ValuesPtr IM1X = *it; it++;
	Data::ValuesPtr IM2X = *it; it++;
	Data::ValuesPtr IM3X = *it; it++;
	Data::ValuesPtr datasetkmt = *it;
	//默认取中间位置
	int index = IM3X->size() / 2+IM3X->size()%2;
	if (istrue)
	{
		int index_min = 1;
		float distancemin = 10000.0f;
		for (auto i = 0; i < IM3X->size(); i++)
		{
			float curdistance = abs(*(IM3X->begin() + i) - _face_point_index);
			if (curdistance < distancemin)
			{
				distancemin = curdistance;
				index_min = i + 1;
			}
		}
		index = index_min;
	}
#ifdef MY_DEBUG
	qDebug() << datasetkmt->size();
#endif
#if 0
	//这是尝试使用线程分段处理数据
	//开始分段操作100万为单位
	std::vector<HANDLE> thlist;
	if (datasetkmt->size()>THRESHOLD)
	{
		threadSites::threadEvent = CreateEvent(nullptr,true,true,nullptr);
		for (auto index = 0; index < datasetkmt->size() / THRESHOLD;index++)
		{
			unsigned __int64 site1 = index*THRESHOLD;
			unsigned __int64 site2 = (index + 1)*THRESHOLD;
			WaitForSingleObject(threadSites::threadEvent,INFINITY)		
			ResetEvent(threadSites::threadEvent);
			threadSites::lps llps;
			llps.lp = this;	llps.site1 = site1;	llps.site2 = site2;
			HANDLE header = (HANDLE)_beginthreadex(nullptr, 0, functhread, &llps, 0, nullptr);
			thlist.push_back(header);
			
		}
		if (datasetkmt->size()%THRESHOLD)
		{
			unsigned __int64 site1=(datasetkmt->size()/THRESHOLD)*THRESHOLD;
			unsigned __int64 site2=datasetkmt->size();
			threadSites::lps* llps = new threadSites::lps();
			llps->lp = this;llps->site1 = site1;llps->site2 = site2;
			HANDLE header = (HANDLE)_beginthreadex(nullptr,1,functhread,llps,0,nullptr);
			thlist.push_back(header);
		}
		while (!thlist.empty())
		{
			for (auto index = 0; index < thlist.size();index++)
			{
				if (WaitForSingleObject(thlist[index],20)!=WAIT_TIMEOUT)
				{
					CloseHandle(thlist[index]);
					thlist[index] = nullptr;
					thlist.erase(thlist.begin() + index);
				}
			}
		}

#ifdef MY_DEBUG
		qDebug("prodatasuccess\n");
#endif // MY_DEBUG

	}

#else 
	std::map<int, std::vector<QRectF>> allinfo;
	std::map<int, std::vector<QPoint>> pointList;
	for (auto itersetkmt = datasetkmt->begin(); itersetkmt != datasetkmt->end();)
	{
		unsigned __int64 x1 = *itersetkmt; itersetkmt++;
		unsigned __int64 x2 = *itersetkmt; itersetkmt++;
		unsigned __int64 x3 = *itersetkmt; itersetkmt++;
		unsigned __int64 proper = *itersetkmt; itersetkmt++;
		if (x3 == index&& x1 <= IM1X->size()&& x2<=IM2X->size())
		{
			std::list<unsigned __int64> rectPro = isAnAttritbute(proper, RECTPROPER);
			std::list<unsigned __int64> linePro = isAnAttritbute(proper, LINEPROPER);
			if (!linePro.empty())
			{
				int x = x1 - 1, y = x2 - 1;
				for each (auto  var in linePro)
				{
					pointList[var].push_back(QPoint(x, y));
				}
			}
			if (!rectPro.empty())
			{
				if (x1 == IM1X->size() || x2 == IM2X->size())
					continue;
				QRectF rect;
				rect.setLeft(*(IM1X->begin() + (x1 - 1)));
				rect.setRight(*(IM1X->begin() + x1));
				rect.setBottom(*(IM2X->begin() + (x2 - 1)));
				rect.setTop(*(IM2X->begin() + x2));
				for each (auto  var in rectPro)
				{
					allinfo[var].push_back(rect);
				}
			}
			
		}
	}
	allcutroom.swap(allinfo);
	createLines(pointList, IM1X, IM2X);
#endif
	return true;
}
/**
* @brief StructData::loadroomCartesianXz 获取绘制信息-cartesian坐标系-X_Z方向
* @return bool
*/
bool StructData::loadroomCartesianXz(){
	if (pointXSize < 2 || pointYSize < 2)
		return false;
	//简化了数据处理流程,通过打印时间比之前的处理方式快了1/3。后续会做替换
	Data::ListValuesPtr listValues;
	autoModGetSourceData(listValues);//获取原始数据
	//获取dataSetKmt里的全部数据
	auto it = listValues->begin();
	Data::ValuesPtr IM1X = *it; it++;
	Data::ValuesPtr IM2X = *it; it++;
	Data::ValuesPtr IM3X = *it; it++;
	Data::ValuesPtr datasetkmt = *it;
	//默认取中间位置
	int index = IM2X->size() / 2+IM2X->size()%2;
	if (istrue)
	{
		int index_min = 1;
		float distancemin = 10000.0f;
		for (auto i = 0; i < IM2X->size();i++)
		{
			float curdistance = abs(*(IM2X->begin()+i)-_face_point_index);
			if (curdistance<distancemin)
			{
				index_min = i + 1;
				distancemin = curdistance;
			}
		}
		index = index_min;
	}
#ifdef MY_DEBUG
	qDebug() << datasetkmt->size();
#endif
	allcutroom.clear();
	std::map<int, std::vector<QPoint>> pointList;
	for (auto itersetkmt = datasetkmt->begin(); itersetkmt != datasetkmt->end();)
	{
		unsigned __int64 x1 = *itersetkmt; itersetkmt++;
		unsigned __int64 x2 = *itersetkmt; itersetkmt++;
		unsigned __int64 x3 = *itersetkmt; itersetkmt++;
		unsigned __int64 proper = *itersetkmt; itersetkmt++;
		if (x2 == index && x1 <= IM1X->size()&&x3<=IM3X->size())
		{
			std::list<unsigned __int64> rectPro=isAnAttritbute(proper,RECTPROPER);
			std::list<unsigned __int64> linePro=isAnAttritbute(proper,LINEPROPER);
			if (!linePro.empty()) {
				int x = x1 - 1, y = x3 - 1;
				for each (auto var in linePro)	pointList[var].push_back(QPoint(x, y));
			}
			if(!rectPro.empty()){
				if (x1 == IM1X->size() || x3 == IM3X->size())
					continue;
				QRectF rect;
				rect.setLeft(*(IM1X->begin() + (x1 - 1)));
				rect.setRight(*(IM1X->begin() + x1));
				rect.setBottom(*(IM3X->begin() + (x3 - 1)));
				rect.setTop(*(IM3X->begin() + x3));
				for each (auto var in rectPro)	allcutroom[var].push_back(rect);
			}
			
		}
	}
	createLines(pointList, IM1X, IM3X);
	return true;
}
/**
* @brief StructData::loadroomCartesianYz 获取绘制信息-caryesian坐标系-Y_Z方向
* @return bool
*/
bool StructData::loadroomCartesianYz(){
	if (pointXSize < 2 || pointYSize < 2)
		return false;
	//简化了数据处理流程,通过打印时间比之前的处理方式快了1/3。后续会做替换
	Data::ListValuesPtr listValues;
	autoModGetSourceData(listValues);//获取原始数据
	//获取dataSetKmt里的全部数据
	auto it = listValues->begin();
	Data::ValuesPtr IM1X = *it; it++;
	Data::ValuesPtr IM2X = *it; it++;
	Data::ValuesPtr IM3X = *it; it++;
	Data::ValuesPtr datasetkmt = *it;
	//默认取中间位置
	int index = IM1X->size() / 2+IM1X->size()%2;
	if (istrue)
	{
		int index_min = 1;
		float distancemin = 10000.0f;
		for (auto i = 0; i < IM1X->size();i++)
		{
			float curdistance = abs(*(IM1X->begin()+i)-_face_point_index);
			if (curdistance<distancemin)
			{
				distancemin = curdistance;
				index_min = i + 1;
			}
		}
		index = index_min;
	}
#ifdef MY_DEBUG
	qDebug() << datasetkmt->size();
#endif
	allcutroom.clear();
	std::map<int, std::vector<QPoint>> pointList;
	for (auto itersetkmt = datasetkmt->begin(); itersetkmt != datasetkmt->end();)
	{
		unsigned __int64 x1 = *itersetkmt; itersetkmt++;
		unsigned __int64 x2 = *itersetkmt; itersetkmt++;
		unsigned __int64 x3 = *itersetkmt; itersetkmt++;
		unsigned __int64 proper = *itersetkmt; itersetkmt++;
		if (x1 == index &&x2 <=IM2X->size()&&x3<=IM3X->size())
		{
			std::list<unsigned __int64> rectPro=isAnAttritbute(proper,RECTPROPER);
			std::list<unsigned __int64> linePro=isAnAttritbute(proper,LINEPROPER);
			if (!linePro.empty())
			{
				int x = x2 - 1, y = x3 - 1;
				for each (auto  var in linePro)
				{
					pointList[var].push_back(QPoint(x, y));
				}
			}
			if (!rectPro.empty())
			{
				if (x2 == IM2X->size() || x3 == IM3X->size())
					continue;
				QRectF rect;
				rect.setLeft(*(IM2X->begin() + (x2 - 1)));
				rect.setRight(*(IM2X->begin() + (x2)));
				rect.setBottom(*(IM3X->begin() + (x3 - 1)));
				rect.setTop(*(IM3X->begin() + x3));
				for each (auto var in rectPro)
				{
					allcutroom[var].push_back(rect);
				}
			}
			
		}
	}
	createLines(pointList, IM2X, IM3X);
	return true;
}
std::list<unsigned __int64> StructData::isAnAttritbute(unsigned __int64 p, PROPERTYPE sp)
{
	std::list<unsigned __int64> list;
#define CPM(a,b)\
	if((a)&(b)) list.push_back(b);
	switch (sp)
	{
	case StructData::RECTPROPER:
	{
		unsigned __int64 rectPro = p & 0xff;
		list.clear();
		CPM(rectPro, PERFECTCONDUCTOR);
		CPM(rectPro, CONDUCTORNEW);
		CPM(rectPro, DIOLECTRIC);
		CPM(rectPro, DIELECTIRANDCONDUCTANCE);
		CPM(rectPro, PERMEABILITY);
		CPM(rectPro, FREESPACE);
		CPM(rectPro, FOIL);
		if (0 == rectPro)
		{
			list.push_back(0);
		}
		return list;
	}
	case StructData::LINEPROPER:
	{
		list.clear();
		unsigned __int64 linePro = p & 0xff00;
		CPM(linePro,256);
		CPM(linePro, 512);
		CPM(linePro, 1024);
		CPM(linePro, 2048);
		CPM(linePro, 4096);
		CPM(linePro, 8192);
		CPM(linePro, 16384);
		CPM(linePro, 32768);
		CPM(linePro, 65536);
		return list;
	}
	}
#undef CPM(a,b)
}

/**
* @brief  StructData::createLines 生成线段
* @param  std::map<int  
* @param  std::vector<QPoint>> & points  
* @param  const Data::ValuesPtr & IMX  
* @param  const Data::ValuesPtr & IMY  
* @return bool  
*/
bool StructData::createLines(std::map<int, std::vector<QPoint>>& points,const Data::ValuesPtr &IMX,const Data::ValuesPtr &IMY)
{
	//auto intervalx = *(IMX->begin() + 1) - *(IMX->begin());
	//auto intervaly = *(IMY->begin() + 1) - *(IMY->begin());
	allLines.clear();
	for (auto iter = points.begin(); iter != points.end(); iter++)
	{
		unsigned int difval = 1;
		std::vector<QPoint>::iterator startiter = iter->second.begin();
		for (auto itersecond = iter->second.begin() + 1; itersecond != iter->second.end(); itersecond++)
		{
			unsigned int distance = (itersecond->x() - startiter->x())*(itersecond->x() - startiter->x()) +
				(itersecond->y() - startiter->y())*(itersecond->y() - startiter->y());
			unsigned int sqareDifval = difval*difval;
			if (distance == sqareDifval)
			{
				difval += 1;
			}
			else
			{
				auto enditer = itersecond - 1;
				QPointF startPoint(*(IMX->begin() + startiter->x()), *(IMY->begin() + startiter->y()));
				QPointF endPoint(*(IMX->begin() + enditer->x()), *(IMY->begin() + enditer->y()));

				if (startPoint.x()==endPoint.x()&& IMY->size()>enditer->y()+1)	endPoint.setY(*(IMY->begin()+enditer->y()+1));
				else if(IMX->size()>enditer->x()+1)endPoint.setX(*(IMX->begin()+enditer->x()+1));
				allLines[iter->first].push_back(QLineF(startPoint, endPoint));
				startiter = itersecond;
				difval = 1;
			}
		}
		auto enditer = iter->second.end() - 1;
		QPointF startPoint(*(IMX->begin() + startiter->x()), *(IMY->begin() + startiter->y()));
		QPointF endPoint(*(IMX->begin() + enditer->x()), *(IMY->begin() + enditer->y()));
		if (startPoint.x() == endPoint.x()&& IMY->size()>enditer->y()+1)	endPoint.setY(*(IMY->begin()+enditer->y()+1));
		else if(IMX->size()>enditer->x()+1)endPoint.setX(*(IMX->begin()+enditer->x()+1));
		allLines[iter->first].push_back(QLineF(startPoint, endPoint));
	}
	return true;
}
/**
* @brief  StructData::segloadRoom 分段处理
* @param  unsigned __int64 site1  
* @param  unsigned __int64 site2  
* @return void  
*/
void StructData::segloadRoom(unsigned  __int64 site1, unsigned __int64 site2)
{
	//qDebug() << site1 << site2;
}
unsigned int __stdcall  functhread(void*lp)
{
	threadSites::lps* llp = reinterpret_cast<threadSites::lps*>(lp);
	SetEvent(threadSites::threadEvent);
	llp->lp->segloadRoom(llp->site1, llp->site2);
	return 0;
}
void StructData::setXYTag(DirectionType type)
{
	switch (type)
	{
	case X_Y:
	{
		setXTag("X(m)");
		setYTag("Y(m)");
	}
		break;
	case X_Z:
	{
		setXTag("X(m)");
		setYTag("Z(m)");
	}
		break;
	case Y_Z:
	{
		setXTag("Y(m)");
		setYTag("Z(m)");
	}
		break;
	case R_Z:
	{
		setXTag("Z(m)");
		setYTag("R(m)");
	}
		break;
	case R_THETA:
	{
		setXTag("R*cos(Pin)");
		setYTag("R*sin(Pin)");
	}
		break;
	}
}

DirectionType StructData::GetDirectionType()
{
	return mType;
}
C_TYPE StructData::GetC_TYPE()
{
	return mCtype;
}
void StructData::setXRang(const Rang& rg)
{
	std::lock_guard<std::mutex> am(xRangMutex);
	xRang = rg;
}
void StructData::setYRang(const Rang& rg)
{
	std::lock_guard<std::mutex> am(yRangMutex);
	yRang = rg;
}
Data::Rang StructData::getXRang()
{
	std::lock_guard<std::mutex> am(xRangMutex);
	return xRang;
}
Data::Rang StructData::getYRang()
{
	std::lock_guard<std::mutex> am(yRangMutex);
	return yRang;
}
std::map<int, std::vector<QRectF>> StructData::GetAllcutInfo()
{
	return allcutroom;
}
std::map<int, std::vector<StructData::CutCir>> StructData::GetAllcurInfo_cir()
{
	return allcutroomcir;
}
std::map<unsigned __int64, std::vector<QLineF>> StructData::GetProperLines()
{
	return allLines;
}
bool StructData::getIsface() {
	return istrue;
}
_3DPointf StructData::getStartPoint()
{
	return mstartpoint;
}
_3DPointf StructData::getEndPoint()
{
	return mendpoint;
}
/***************************************/
//struct _3DPointf
int _3DPointf::operator ==(const _3DPointf& that) const
{
	if (this->_1st == that._1st && this->_2rd != that._2rd && this->_3th != that._3th)
		return 1;
	else if (this->_2rd == that._2rd && this->_1st != that._1st && this->_3th != that._3th)
		return 2;
	else if (this->_3th == that._3th && this->_1st != that._1st && this->_2rd != that._2rd)
		return 3;
	return 0;
}
float _3DPointf::operator [](int index)
{
	switch (index)
	{
	case 1:
		return _1st;
	case 2:
		return _2rd;
	case 3:
		return _3th;
	default:
		return 0.0f;
	}
}
_3DPointf::_3DPointf() :_1st(0.0f), _2rd(0.0f), _3th(0.0f) {}