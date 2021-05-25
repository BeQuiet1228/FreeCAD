#include "StructData.h"
#ifdef MY_DEBUG
#include<windows.h>
#include <QDebug>
#endif
/**
* @brief StructData::StructData 构造函数
* @param Hdf5Data& heData
* @param DirectionType _type 方向
* @param const RunMod& mod
*/
StructData::StructData(Hdf5Data& heData, DirectionType _type, const RunMod& mod):XYData(heData,mod),istrue(false){
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
StructData::StructData(Hdf5Data& heData, _3DPointf startpoint, _3DPointf endpoint, const RunMod& mod):XYData(heData,mod),istrue(true),mstartpoint(startpoint),mendpoint(endpoint){
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
#ifdef MY_DEBUG
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
#ifdef MY_DEBUG
	QueryPerformanceCounter(&endTime);
	auto interval = ((double)endTime.QuadPart - (double)startTime.QuadPart) / (double)cpufer.QuadPart;
	qDebug() << "processingData(interval):" << interval;
#endif
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
	int index = IM2X->size() / 2;
	if (istrue)
	{
		int index_min = 1;
		float distancemin = 10000.0f;
		for (auto i = 0; i < IM3X->size(); i++)
		{
			float curdistance = abs(*(IM3X->begin() + i) - _face_point_index);
			if (curdistance<distancemin)
			{
				distancemin = curdistance;
				index_min = i + 1;
			}
		}
		index = index_min;
	}
	std::map<int, std::vector<QRectF>> allinfo;
	auto intervalV = *(IM3X->begin()+1)-*(IM3X->begin());
	auto intervalH = *(IM1X->begin() + 1) - *(IM1X->begin());
	for(auto itersetkmt=datasetkmt->begin();itersetkmt!=datasetkmt->end();)
	{
		auto x1=*itersetkmt;itersetkmt++;
		auto x2=*itersetkmt;itersetkmt++;
		auto x3=*itersetkmt;itersetkmt++;
		auto proper=*itersetkmt;itersetkmt++;
		if (x2 == index&&x3<IM3X->size()&&x1<IM1X->size())
		{
			QRectF rect;
			rect.setLeft(*(IM3X->begin() + x3 - 1));
			rect.setRight(*(IM3X->begin() + x3));
			rect.setBottom(*(IM1X->begin() + x1 - 1));
			rect.setTop(*(IM1X->begin() + x1));
			allinfo[proper].push_back(rect);
		}
		//增加越界处理
		else if (x2==index&& x3==IM3X->size()&&x1<IM1X->size())
		{
			QRectF rect;
			rect.setLeft(*(IM3X->begin() + x3 - 1));
			rect.setBottom(*(IM1X->begin()+x1-1));
			rect.setRight(rect.left() + intervalV);
			rect.setTop(*(IM1X->begin() + x1));
			allinfo[proper].push_back(rect);

		}
		else if (x2==index&& x3<IM3X->size()&&x1==IM1X->size())
		{
			QRectF rect;
			rect.setLeft(*(IM3X->begin()+x3-1));
			rect.setRight(*(IM3X->begin()+x3));
			rect.setBottom(*(IM1X->begin()+x1-1));
			rect.setTop(rect.bottom()+intervalH);
			allinfo[proper].push_back(rect);
		}
	}
	allcutroom.swap(allinfo);
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
				//内圈半径
				tempCurcir.R_inner = r_val[index_R];
				//外圈半径
				tempCurcir.R_excir = r_val[index_R + 1];
				//内圈切点
				tempCurcir.inner1 = QPointF(
					tempCurcir.R_inner*cos(rand_val[index_rand]) + p0.x(),
					p0.y() - tempCurcir.R_inner*sin(rand_val[index_rand]));
				tempCurcir.inner2 = QPointF(
					tempCurcir.R_inner*cos(rand_val[index_rand + 1]) + p0.x(),
					p0.y() - tempCurcir.R_inner*sin(rand_val[index_rand + 1]));
				//外圈切点
				tempCurcir.excir1 = QPointF(
					tempCurcir.R_excir*cos(rand_val[index_rand] + p0.x()),
					p0.y() - tempCurcir.R_excir*sin(rand_val[index_rand]));
				tempCurcir.excir2 = QPointF(
					tempCurcir.R_excir*cos(rand_val[index_rand + 1] + p0.x()),
					p0.y() - tempCurcir.R_excir*sin(rand_val[index_rand + 1]));
				//开始角度，结束角度
				tempCurcir.startAngle = rand_val[index_rand];
				tempCurcir.endAngle = rand_val[index_rand + 1];
				CutCirlist.push_back(tempCurcir);
			}
		}
#pragma endregion
#pragma region 筛选属性
		int index = IM1X->size() / 2;
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
				listcir[var.pointproperty].push_back(CutCirlist[(var.point2 - 1)*CutNum + (var.point3 - 1)]);
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
	int index = IM3X->size() / 2;
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
	allcutroom.clear();
	auto intervalV = *(IM1X->begin() + 1) - *(IM1X->begin());
	auto intervalH = *(IM2X->begin() + 1) - *(IM2X->begin());
	for (auto itersetkmt = datasetkmt->begin(); itersetkmt != datasetkmt->end();)
	{
		auto x1 = *itersetkmt; itersetkmt++;
		auto x2 = *itersetkmt; itersetkmt++;
		auto x3 = *itersetkmt; itersetkmt++;
		auto proper = *itersetkmt; itersetkmt++;
		if (x3 == index&& x1 <IM1X->size()&&x2<IM2X->size())
		{
			QRectF rect;
			rect.setLeft(*(IM1X->begin()+x1-1));
			rect.setRight(*(IM1X->begin() + x1));
			rect.setBottom(*(IM2X->begin()+x2-1));
			rect.setTop(*(IM2X->begin() + x2));
			allcutroom[proper].push_back(rect);
		}
		else if (x3==index&& x1==IM1X->size()&&x2<IM2X->size())
		{
			QRectF rect;
			rect.setLeft(*(IM1X->begin()+x1-1));
			rect.setRight(rect.left()+intervalV);
			rect.setBottom(*(IM2X->begin()+x2-1));
			rect.setTop(*(IM2X->begin()+x2));
			allcutroom[proper].push_back(rect);
		}
		//增加越界处理
		else if (x3==index&& x1<IM1X->size()&& x2==IM2X->size())
		{
			QRectF rect;
			rect.setLeft(*(IM1X->begin()+x1-1));
			rect.setRight(*(IM1X->begin()+x1));
			rect.setBottom(*(IM2X->begin()+x2-1));
			rect.setTop(rect.bottom()+intervalH);
			allcutroom[proper].push_back(rect);
		}
		else if (x3==index&& x1==IM1X->size()&& x2<IM2X->size())
		{
			QRectF rect;
			rect.setLeft(*(IM1X->begin()+x1-1));
			rect.setRight(rect.left() + intervalV);
			rect.setBottom(*(IM2X->begin()+x2-1));
			rect.setTop(*(IM2X->begin()+x2));
			allcutroom[proper].push_back(rect);
		}

	}
	return true;
}
/**
* @brief StructData::loadroomCylindricalRtheta 获取绘制信息-cylindrical坐标系-R_THETA方向
* @return bool
*/
bool StructData::loadroomCylindricalRtheta(){
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
				//内圈半径
				tempCurcir.R_inner = r_val[index_R];
				//外圈半径
				tempCurcir.R_excir = r_val[index_R + 1];
				//内圈切点
				tempCurcir.inner1 = QPointF(
					tempCurcir.R_inner*cos(rand_val[index_rand]) + p0.x(),
					p0.y() - tempCurcir.R_inner*sin(rand_val[index_rand]));
				tempCurcir.inner2 = QPointF(
					tempCurcir.R_inner*cos(rand_val[index_rand + 1]) + p0.x(),
					p0.y() - tempCurcir.R_inner*sin(rand_val[index_rand + 1]));
				//外圈切点
				tempCurcir.excir1 = QPointF(
					tempCurcir.R_excir*cos(rand_val[index_rand] + p0.x()),
					p0.y() - tempCurcir.R_excir*sin(rand_val[index_rand]));
				tempCurcir.excir2 = QPointF(
					tempCurcir.R_excir*cos(rand_val[index_rand + 1] + p0.x()),
					p0.y() - tempCurcir.R_excir*sin(rand_val[index_rand + 1]));
				//开始角度，结束角度
				tempCurcir.startAngle = rand_val[index_rand];
				tempCurcir.endAngle = rand_val[index_rand + 1];
				CutCirlist.push_back(tempCurcir);
			}
		}
#pragma endregion
#pragma region 筛选属性
		int index = IM1X->size() / 2;
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
		int CutNum = rand_val.size() - 1;
		std::vector<DaTaKmt> datakmtinfo = GetdatasetKmtCylindrical();
		for each (DaTaKmt var in datakmtinfo)
		{
			if (var.point1 == index && var.point3 < rand_val.size())
			{
				listcir[var.pointproperty].push_back(CutCirlist[(var.point2 - 1)*CutNum + (var.point3 - 1)]);
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
	int index = IM3X->size() / 2;
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
	auto intervalV = *(IM1X->begin()+1)-*(IM1X->begin());
	auto intervalH = *(IM2X->begin() + 1) - *(IM2X->begin());

	std::map<int, std::vector<QRectF>> allinfo;
	for (auto itersetkmt = datasetkmt->begin(); itersetkmt != datasetkmt->end();)
	{
		auto x1 = *itersetkmt; itersetkmt++;
		auto x2 = *itersetkmt; itersetkmt++;
		auto x3 = *itersetkmt; itersetkmt++;
		auto proper = *itersetkmt; itersetkmt++;
		if (x3 == index&& x1 < IM1X->size()&& x2<IM2X->size())
		{
			QRectF rect;
			rect.setLeft(*(IM1X->begin() + (x1 - 1)));
			rect.setRight(*(IM1X->begin() + x1));
			rect.setBottom(*(IM2X->begin() + (x2 - 1)));
			rect.setTop(*(IM2X->begin() + x2));
			allinfo[proper].push_back(rect);
		}
		//增加越界处理
		else if (x3==index&& x1==IM1X->size()&& x2<IM2X->size())
		{
			QRectF rect;
			rect.setLeft(*(IM1X->begin()+x1-1));
			rect.setRight(rect.left() + intervalV);
			rect.setBottom(*(IM2X->begin() + x2 - 1));
			rect.setTop(*(IM2X->begin()+x2));
			allinfo[proper].push_back(rect);
		}
		else if (x3==index&& x1<IM1X->size()&&x2==IM2X->size())
		{
			QRectF rect;
			rect.setLeft(*(IM1X->begin()+x1-1));
			rect.setRight(*(IM1X->begin()+x1));
			rect.setBottom(*(IM2X->begin()+x2-1));
			rect.setTop(rect.bottom()+intervalH);
			allinfo[proper].push_back(rect);
		}
	}
	allcutroom.swap(allinfo);
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
	int index = IM2X->size() / 2;
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
	}
	allcutroom.clear();
	auto intervalV = *(IM1X->begin() + 1) - *(IM1X->begin());
	auto intervalH = *(IM3X->begin()+1) - *(IM3X->begin());
	for (auto itersetkmt = datasetkmt->begin(); itersetkmt != datasetkmt->end();)
	{
		auto x1 = *itersetkmt; itersetkmt++;
		auto x2 = *itersetkmt; itersetkmt++;
		auto x3 = *itersetkmt; itersetkmt++;
		auto proper = *itersetkmt; itersetkmt++;
		if (x2 == index && x1 < IM1X->size()&&x3<IM3X->size())
		{
			QRectF rect;
			rect.setLeft(*(IM1X->begin() + (x1 - 1)));
			rect.setRight(*(IM1X->begin() + x1));
			rect.setBottom(*(IM3X->begin()+(x3-1)));
			rect.setTop(*(IM3X->begin() + x3));
			allcutroom[proper].push_back(rect);
		}
		//增加越界处理
		else if (x2==index && x1==IM1X->size()&& x3<IM3X->size())
		{
			QRectF rect;
			rect.setLeft(*(IM1X->begin()+x1-1));
			rect.setRight(rect.left()+intervalV);
			rect.setBottom(*(IM3X->begin()+x3-1));
			rect.setTop(*(IM3X->begin()+x3));
			allcutroom[proper].push_back(rect);
		}
		else if (x2==index&& x1<IM1X->size()&&x3==IM3X->size())
		{
			QRectF rect;
			rect.setLeft(*(IM1X->begin()+x1-1));
			rect.setRight(*(IM1X->begin()+x1));
			rect.setBottom(*(IM3X->begin()+x3-1));
			rect.setTop(rect.bottom()+intervalH);
			allcutroom[proper].push_back(rect);
		}
	}
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
	int index = IM1X->size() / 2;
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
	allcutroom.clear();
	auto intervalV = *(IM2X->begin() + 1) - *(IM2X->begin());
	auto intervalH = *(IM3X->begin() + 1) - *(IM3X->begin());
	for (auto itersetkmt = datasetkmt->begin(); itersetkmt != datasetkmt->end();)
	{
		auto x1 = *itersetkmt; itersetkmt++;
		auto x2 = *itersetkmt; itersetkmt++;
		auto x3 = *itersetkmt; itersetkmt++;
		auto proper = *itersetkmt; itersetkmt++;
		if (x1 == index &&x2 < IM2X->size()&&x3<IM3X->size())
		{
			QRectF rect;
			rect.setLeft(*(IM2X->begin() + (x2 - 1)));
			rect.setRight(*(IM2X->begin() + (x2)));
			rect.setBottom(*(IM3X->begin()+(x3-1)));
			rect.setTop(*(IM3X->begin()+x3));
			allcutroom[proper].push_back(rect);
		}
		//增加越界处理
		else if (x1==index&& x2==IM2X->size()&&x3<IM3X->size())
		{
			QRectF rect;
			rect.setLeft(*(IM2X->begin()+x2-1));
			rect.setRight(rect.left()+intervalV);
			rect.setBottom(*(IM3X->begin()+x3-1));
			rect.setTop(*(IM3X->begin() + x3));
			allcutroom[proper].push_back(rect);
		}
		else if (x1==index&&x2<IM2X->size()&& x3==IM3X->size())
		{
			QRectF rect;
			rect.setLeft(*(IM2X->begin()+x2-1));
			rect.setRight(*(IM2X->begin() + x2));
			rect.setBottom(*(IM3X->begin()+x3-1));
			rect.setTop(rect.bottom()+intervalH);
			allcutroom[proper].push_back(rect);
		}
	}
	return true;
}