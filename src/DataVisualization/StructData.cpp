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
		_ctype = C_TYPE::CARTESIAN;
		switch (_type)
		{
		case X_Y:
		case X_Z:
		case Y_Z:
			m_Type = _type; break;
		default:
			m_Type = X_Y; break;
		}
	}
		break;
	case Hdf5Data::CYLINDER:
	{
		//当前为cylindrical
		_ctype = C_TYPE::CYLINDRICAL;
		switch (_type)
		{
		case R_Z:
		case R_THETA:
			m_Type = _type; break;
		default:
			m_Type = R_Z; break;

		}
	}
		break;
	case Hdf5Data::POLAR:
	{
		//当前为polar
		_ctype = C_TYPE::POLAR;
		switch (_type)
		{
		case R_Z:
		case R_THETA:
			m_Type = _type; break;
		default:
			m_Type = R_Z; break;
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
		_ctype = C_TYPE::POLAR;
		//极坐标系  R pin Z
		switch (res)
		{
		case 1:
		case 2:
			m_Type = R_Z; break;
		case 3:
			m_Type = R_THETA; break;
		}
	}break;
	case  Hdf5Data::CYLINDER:
	{
		//当前为cylindrical
		_ctype = C_TYPE::CYLINDRICAL;//z_R_the
		switch (res)
		{
		case 1:
			m_Type = R_THETA; break;
		case 2:
		case 3:
			m_Type = R_Z; break;
		}
	}break;
	case Hdf5Data::CARTESIAN:
	{
		//当前为cartexian
		_ctype = C_TYPE::CARTESIAN;
		switch (res)
		{
		case 1:
			m_Type = Y_Z; break;
		case 2:
			m_Type = X_Z; break;
		case 3:
			m_Type = X_Y; break;
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
	switch (_ctype)
	{
	case POLAR:
		return loadPoint_polar();
	case CYLINDRICAL:
		return loadPoint_cylindrical();
	case CARTESIAN:
		return loadPoint_cartesian();
	}
}
/**
* @brief StructData::loadPoint_cartesian 加载点位-cartesian坐标系
* @return bool 
*/
bool StructData::loadPoint_cartesian()
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
	switch (m_Type)
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
* @brief StructData::loadPoint_cylindrical 加载点位-cylindrical坐标系
* @return bool
*/
bool StructData::loadPoint_cylindrical()
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
	switch (m_Type)
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
* @brief StructData::loadPoint_polar 加载点位--polar坐标系
* @return bool
*/
bool StructData::loadPoint_polar()
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
	switch (m_Type)
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
	switch (_ctype)
	{
	case POLAR:
		loadroom_polar(); break;
	case CYLINDRICAL:
		 loadroom_cylindrical();break;
	case CARTESIAN:
		loadroom_cartesian(); break;
	}
#ifdef MY_DEBUG
	QueryPerformanceCounter(&endTime);
	auto interval = ((double)endTime.QuadPart - (double)startTime.QuadPart) / (double)cpufer.QuadPart;
	qDebug() << "processingData(interval):" << interval;
#endif
	return true;
}
/**
* @brief StructData::loadroom_polar 转换成绘制数据-polar坐标系
* @return bool
*/
bool StructData::loadroom_polar(){
	
	switch (m_Type)
	{
	case R_Z:
		return loadroom_polar_R_Z();
	case R_THETA:
		return loadroom_polar_R_THETA();
	}
	return false;
}
/**
* @brief StructData::loadroom_cylindrical 转换成绘制数据-cylindrical坐标系
* @return bool
*/
bool StructData::loadroom_cylindrical(){
	switch (m_Type)
	{
	case R_Z:
		return loadroom_cylindrical_r_z();
	case R_THETA:
		return loadroom_cylindrical_r_theta();
	}
	return false;
}
/**
* @brief StructData::loadroom_cartesian 转换成绘制数据-cartesian坐标
* @return bool
*/
bool StructData::loadroom_cartesian(){
	switch (m_Type)
	{
	case X_Y:
		return loadroom_cartesian_x_y();
	case X_Z:
		return loadroom_cartesian_x_z();
	case Y_Z:
		return loadroom_cartesian_y_z();
	}
	return false;
}
/**
* @brief StructData::loadroom_polar_R_Z 转换成绘制数据-polar坐标系-R_Z方向
* @return bool 
*/
bool StructData::loadroom_polar_R_Z()
{
	if (pointXSize<2||pointYSize<2)
		return false;
#if 0
	allcutroom = fileproperty_polar_R_Z(GetAllCurspace_polar_R_Z(), GetdatasetKmt_polar_R_Z());
#else
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
			float curdistance = abs(*(IM2X->begin() + i) - _face_point_index);
			if (curdistance<distancemin)
			{
				distancemin = curdistance;
				index_min = i + 1;
			}
		}
		index = index_min;
	}
	QMap<int, QVector<QRectF>> allinfo;
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
	}
	allcutroom.swap(allinfo);
#endif
}
/**
* @brief StructData::GetAllCurspace_polar_R_Z 获取所有网格的-polar坐标系-R_Z方向
* @return std::vector<QRectF>
*/
std::vector<QRectF> StructData::GetAllCurspace_polar_R_Z()
{
	std::vector<QRectF> list;
	//获取全部切割空间
	//获取从H5F文件中的数据
	Data::ListValuesPtr listValues;
	bool ok = autoModGetSourceData(listValues);//获取原始数据
	if (!ok && !listValues && listValues->size() == 0)
		return list;
	auto it = (listValues->begin());
	//polar_R_Z
	Data::ValuesPtr IM2X = *it; it++;
	Data::ValuesPtr IM3X = *it; it++;
	Data::ValuesPtr IM1X = *it; it++;
	Data::ValuesPtr datasetkmt = *it;
	//开始获取
	auto iterleft = IM1X->begin();
	auto iterRight = IM1X->begin() + 1;
	auto iterTop = IM2X->begin();
	auto iterbottom = IM2X->begin() + 1;
#if 1
	for (auto x = 0; x < pointXSize-1; x++)
	{
		iterTop = IM2X->begin();
		iterbottom = IM2X->begin() + 1;
		for (auto y = 0; y < pointYSize-1; y++)
		{
			QRectF temp;//介值
			temp.setLeft(*iterleft);
			temp.setRight(*iterRight);
			temp.setTop(*iterTop);
			temp.setBottom(*iterbottom);
			list.push_back(temp);
			iterTop++;
			iterbottom++;
		}
		iterleft++;
		iterRight++;
	}
#endif
	return list;
}
/**
* @brief StructData::GetdatasetKmt_polar_R_Z 获取datasetkmt的数据-polar坐标系-R_Z方向
* @return std::vector<StructData::DaTaKmt>
*/
std::vector<StructData::DaTaKmt> StructData::GetdatasetKmt_polar_R_Z()
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
* @brief StructData::fileproperty_polar_R_Z 跟具不同属性放入字典
* @param std::vector<QRectF>& list 所有的网格
* @param std::vector<StructData::DaTaKmt>& datainfo datasetkmt的信息
* @return QMap<int, QVector<QRectF>>
*/
QMap<int, QVector<QRectF>> StructData::fileproperty_polar_R_Z(std::vector<QRectF>& list, std::vector<StructData::DaTaKmt>& datainfo)
{
	Data::ListValuesPtr listValues;
	autoModGetSourceData(listValues);//获取原始数据
	//获取dataSetKmt里的全部数据
	auto it = listValues->begin();
	Data::ValuesPtr IM2X = *it; it++;
	Data::ValuesPtr IM3X = *it; it++;
	Data::ValuesPtr IM1X = *it; it++;
	Data::ValuesPtr datasetkmt = *it;
	int index = IM3X->size()/2;
	if (istrue)
	{
		int index_min = 1;
		float distancemin = 10000.0f;
		_face_point_index;
		for (auto i = 0; i < IM3X->size();i++)
		{
			float curdistance = abs(*(IM3X->begin() + i) - _face_point_index);
			if (curdistance<distancemin)
			{
				distancemin = curdistance;
				index_min = i+1;
			}
		}
		index = index_min;
	}
	QMap<int, QVector<QRectF>> allinfo;
	for each (DaTaKmt var in datainfo)
	{
		if (var.point3==index&&var.point1<pointXSize)
		{
			allinfo[var.pointproperty].push_back(list[(var.point1 - 1)*(pointYSize - 1) + var.point2 - 1]);
		}
	}
	return allinfo;
}
/**
* @brief StructData::loadroom_polar_R_THETA 转换成绘制信息-polar坐标系-R_THETA方向
* @return bool
*/
bool StructData::loadroom_polar_R_THETA()
{
	if (pointXSize < 2 || pointYSize < 2)
		return false;
	allcutroom_cir= filecir_polar_R_THETA();
	return true;
}
/**
* @brief StructData::filecir_polar_R_THETA 根据不同属性分类R_THETA信息-polar坐标系-R_THETA方向
* @return std::map<int, std::vector<StructData::CutCir>>
*/
std::map<int, std::vector<StructData::CutCir>> StructData::filecir_polar_R_THETA()
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
	for (auto iter2mx = IM2X->begin(); iter2mx != IM2X->end();iter2mx++)
		r_val.push_back(*iter2mx);
	for (auto iter3mx = IM3X->begin(); iter3mx != IM3X->end(); iter3mx++)
		rand_val.push_back(*iter3mx);
#pragma region 遍历所有切割圆环
	std::vector<CutCir> _CutCirlist;
	for (auto index_R = 0; index_R < r_val.size() - 1; index_R++)
	{
		for (auto index_rand = 0; index_rand < rand_val.size() - 1; index_rand++)
		{
			CutCir _curcir;
			//内圈半径
			_curcir.R_inner = r_val[index_R];
			//外圈半径
			_curcir.R_excir = r_val[index_R + 1];
			//内圈切点
			_curcir.inner1 = QPointF(
				_curcir.R_inner*cos(rand_val[index_rand]) + p0.x(),
				p0.y() - _curcir.R_inner*sin(rand_val[index_rand]));
			_curcir.inner2 = QPointF(
				_curcir.R_inner*cos(rand_val[index_rand + 1]) + p0.x(),
				p0.y() - _curcir.R_inner*sin(rand_val[index_rand + 1]));
			//外圈切点
			_curcir.excir1 = QPointF(
				_curcir.R_excir*cos(rand_val[index_rand] + p0.x()),
				p0.y() - _curcir.R_excir*sin(rand_val[index_rand]));
			_curcir.excir2 = QPointF(
				_curcir.R_excir*cos(rand_val[index_rand + 1] + p0.x()),
				p0.y() - _curcir.R_excir*sin(rand_val[index_rand + 1]));
			//开始角度，结束角度
			_curcir.startAngle = rand_val[index_rand];
			_curcir.endAngle = rand_val[index_rand + 1];
			_CutCirlist.push_back(_curcir);
		}
	}
#pragma endregion
#pragma region 筛选属性
	int index = IM1X->size()/2;
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
				index_min = i+1;
			}
		}
		index = index_min;
	}
	int CutNum = rand_val.size()-1;
	std::vector<DaTaKmt> datakmtinfo =GetdatasetKmt_polar_R_THETA();
	for each (DaTaKmt var in datakmtinfo)
	{
		if (var.point1==index&&var.point3<rand_val.size())
		{
			listcir[var.pointproperty].push_back(_CutCirlist[(var.point2 - 1)*CutNum + (var.point3 - 1)]);
		}
	}
#pragma endregion 
	return listcir;
}
/**
* @brief StructData::GetdatasetKmt_polar_R_THETA 获取datasetkmt信息-polar坐标系-R_THETA方向
* @return std::vector<StructData::DaTaKmt>
*/
std::vector<StructData::DaTaKmt> StructData::GetdatasetKmt_polar_R_THETA(){
	return GetdatasetKmt_polar_R_Z();
}
/**
* @brief StructData::loadroom_cylindrical_r_z 转换成绘制信息-cylindrical坐标系-R_Z方向
* @return bool
*/
bool StructData::loadroom_cylindrical_r_z(){
	if (pointXSize < 2 || pointYSize < 2)
		return false;
#if 0
	allcutroom = fileproperty_cylindrical_R_Z(GetAllCurspace_cylindrical_R_Z(), GetdatasetKmt_cylindrical_R_Z());
#else
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
	for (auto itersetkmt = datasetkmt->begin(); itersetkmt != datasetkmt->end();)
	{
		auto x1 = *itersetkmt; itersetkmt++;
		auto x2 = *itersetkmt; itersetkmt++;
		auto x3 = *itersetkmt; itersetkmt++;
		auto proper = *itersetkmt; itersetkmt++;
		if (x3 == index&& x1 < IM1X->size()&&x2<IM2X->size())
		{
			QRectF rect;
			rect.setLeft(*(IM1X->begin()+x1-1));
			rect.setRight(*(IM1X->begin() + x1));
			rect.setBottom(*(IM2X->begin()+x2-1));
			rect.setTop(*(IM2X->begin() + x2));
			allcutroom[proper].push_back(rect);
		}
	}
#endif
	return true;
}
/**
* @brief StructData::loadroom_cylindrical_r_theta 获取绘制信息-cylindrical坐标系-R_THETA方向
* @return bool
*/
bool StructData::loadroom_cylindrical_r_theta(){
	if (pointXSize < 2 || pointYSize < 2)
		return false;
	allcutroom_cir = filecir_cylindrical_R_THETA();
	return true;
}
/**
* @brief StructData::GetAllCurspace_cylindrical_R_Z 获取网格数据-cylindrical坐标系-R_Z方向
* @return std::vector<QRectF>
*/
std::vector<QRectF> StructData::GetAllCurspace_cylindrical_R_Z()
{
	std::vector<QRectF> list;
	//获取全部切割空间
	//获取从H5F文件中的数据
	Data::ListValuesPtr listValues;
	bool ok = autoModGetSourceData(listValues);//获取原始数据
	if (!ok && !listValues && listValues->size() == 0)
		return list;
	auto it = (listValues->begin());
	//cylindrical_R_Z
	Data::ValuesPtr IM1X = *it; it++;
	Data::ValuesPtr IM2X = *it; it++;
	Data::ValuesPtr IM3X = *it; it++;
	Data::ValuesPtr datasetkmt = *it;
	//开始获取
	auto iterleft = IM1X->begin();
	auto iterRight = IM1X->begin() + 1;
	auto iterTop = IM2X->begin();
	auto iterbottom = IM2X->begin() + 1;
	for (auto x = 0; x < pointXSize - 1; x++)
	{
		iterTop = IM2X->begin();
		iterbottom = IM2X->begin() + 1;
		for (auto y = 0; y < pointYSize - 1; y++)
		{
			QRectF temp;//介值
			temp.setLeft(*iterleft);
			temp.setRight(*iterRight);
			temp.setTop(*iterTop);
			temp.setBottom(*iterbottom);
			list.push_back(temp);
			iterTop++;
			iterbottom++;
		}
		iterleft++;
		iterRight++;
	}
	return list;
}
/**
* @brief StructData::GetdatasetKmt_cylindrical_R_Z 获取datasetkmt信息-cylindrical坐标系-R_Z方向
* @return std::vector<StructData::DaTaKmt>
*/
std::vector<StructData::DaTaKmt> StructData::GetdatasetKmt_cylindrical_R_Z(){
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
* @brief StructData::fileproperty_cylindrical_R_Z 根据属性分类信息-cylindrical坐标系-R_Z方向
* @param std::vector<QRectF>& list
* @param std::vector<DaTaKmt>& datainfo
* @return QMap<int, QVector<QRectF>>
*/
QMap<int, QVector<QRectF>> StructData::fileproperty_cylindrical_R_Z(std::vector<QRectF>& list, std::vector<DaTaKmt>& datainfo){
	Data::ListValuesPtr listValues;
	autoModGetSourceData(listValues);//获取原始数据
	//获取dataSetKmt里的全部数据
	auto it = listValues->begin();
	Data::ValuesPtr IM1X = *it; it++;
	Data::ValuesPtr IM2X = *it; it++;
	Data::ValuesPtr IM3X = *it; it++;
	Data::ValuesPtr datasetkmt = *it;
	QMap<int, QVector<QRectF>> allinfo;
	int index = IM3X->size()/2;
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
				index_min = i+1;
			}
		}
		index = index_min;
	}
	for each (DaTaKmt var in datainfo)
	{
		if (var.point3 == index && var.point1 < pointXSize)
		{
			allinfo[var.pointproperty].push_back(list[(var.point1 - 1)*(pointYSize - 1) + var.point2 - 1]);
		}
	}
	return allinfo;
}
/**
* @brief StructData::filecir_cylindrical_R_THETA 填充圆柱坐标系的数据-cylindrial坐标系-R_THETA方向
* @return std::map<int, std::vector<StructData::CutCir>>
*/
std::map<int, std::vector<StructData::CutCir>> StructData::filecir_cylindrical_R_THETA()
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
	std::vector<CutCir> _CutCirlist;
	for (auto index_R = 0; index_R < r_val.size() - 1; index_R++)
	{
		for (auto index_rand = 0; index_rand < rand_val.size() - 1; index_rand++)
		{
			CutCir _curcir;
			//内圈半径
			_curcir.R_inner = r_val[index_R];
			//外圈半径
			_curcir.R_excir = r_val[index_R + 1];
			//内圈切点
			_curcir.inner1 = QPointF(
				_curcir.R_inner*cos(rand_val[index_rand]) + p0.x(),
				p0.y() - _curcir.R_inner*sin(rand_val[index_rand]));
			_curcir.inner2 = QPointF(
				_curcir.R_inner*cos(rand_val[index_rand + 1]) + p0.x(),
				p0.y() - _curcir.R_inner*sin(rand_val[index_rand + 1]));
			//外圈切点
			_curcir.excir1 = QPointF(
				_curcir.R_excir*cos(rand_val[index_rand] + p0.x()),
				p0.y() - _curcir.R_excir*sin(rand_val[index_rand]));
			_curcir.excir2 = QPointF(
				_curcir.R_excir*cos(rand_val[index_rand + 1] + p0.x()),
				p0.y() - _curcir.R_excir*sin(rand_val[index_rand + 1]));
			//开始角度，结束角度
			_curcir.startAngle = rand_val[index_rand];
			_curcir.endAngle = rand_val[index_rand + 1];
			_CutCirlist.push_back(_curcir);
		}
	}
#pragma endregion
#pragma region 筛选属性
	int index = IM1X->size()/2;
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
				index_min = i+1;
			}
		}
		index = index_min;
	}
	int CutNum = rand_val.size()-1;
	std::vector<DaTaKmt> datakmtinfo = GetdatasetKmt_cylindrical_R_THETA();
	for each (DaTaKmt var in datakmtinfo)
	{
		if (var.point1 == index && var.point3 < rand_val.size())
		{
			listcir[var.pointproperty].push_back(_CutCirlist[(var.point2 - 1)*CutNum + (var.point3 - 1)]);
		}
	}
#pragma endregion 
	/**************************************/
	return listcir;
}
/**
* @brief StructData::GetdatasetKmt_cylindrical_R_THETA 获取datasetkmt的信息-cylindrical坐标系-R_THETA方向
* @return std::vector<StructData::DaTaKmt>
*/
std::vector<StructData::DaTaKmt> StructData::GetdatasetKmt_cylindrical_R_THETA(){
	return GetdatasetKmt_cylindrical_R_Z();
}
/**
* @brief StructData::loadroom_cartesian_x_y 转换绘制信息-cartesian坐标系-X_Y方向
* @return bool
*/
bool StructData::loadroom_cartesian_x_y(){
	if (pointXSize < 2 || pointYSize < 2)
		return false;
#if 0
	allcutroom = fileproperty_cartesian_x_y(GetAllCurspace_cartesian_x_y(), GetdatasetKmt_cartesian_x_y());
#else
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
	QMap<int, QVector<QRectF>> allinfo;
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
	}
	allcutroom.swap(allinfo);
#endif
	return true;
}
/**
* @brief StructData::loadroom_cartesian_x_z 获取绘制信息-cartesian坐标系-X_Z方向
* @return bool
*/
bool StructData::loadroom_cartesian_x_z(){
	if (pointXSize < 2 || pointYSize < 2)
		return false;
#if 0
	allcutroom = fileproperty_cartesian_x_z(GetAllCurspace_cartesian_x_z(), GetdatasetKmt_cartesian_x_z());
#else
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
	}
#endif
	return true;
}
/**
* @brief StructData::loadroom_cartesian_y_z 获取绘制信息-caryesian坐标系-Y_Z方向
* @return bool
*/
bool StructData::loadroom_cartesian_y_z(){
	if (pointXSize < 2 || pointYSize < 2)
		return false;
#if 0
	allcutroom = fileproperty_cartesian_y_z(GetAllCurspace_cartesian_y_z(), GetdatasetKmt_cartesian_y_z());
#else
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
	}
#endif
	return true;
}
/**
* @brief StructData::GetAllCurspace_cartesian_x_y 获取网格-cartesian坐标系-X_Y方向
* @retrun std::vector<QRectF>
*/
std::vector<QRectF> StructData::GetAllCurspace_cartesian_x_y()
{
	std::vector<QRectF> list;
	//获取全部切割空间
	//获取从H5F文件中的数据
	Data::ListValuesPtr listValues;
	bool ok = autoModGetSourceData(listValues);//获取原始数据
	if (!ok && !listValues && listValues->size() == 0)
		return list;
	auto it = (listValues->begin());
	//cylindrical_R_Z
	Data::ValuesPtr IM1X = *it; it++;
	Data::ValuesPtr IM2X = *it; it++;
	Data::ValuesPtr IM3X = *it; it++;
	Data::ValuesPtr datasetkmt = *it;
	//开始获取
	auto iterleft = IM1X->begin();
	auto iterRight = IM1X->begin() + 1;
	auto iterTop = IM2X->begin();
	auto iterbottom = IM2X->begin() + 1;
	for (auto x = 0; x < pointXSize - 1; x++)
	{
		iterTop = IM2X->begin();
		iterbottom = IM2X->begin() + 1;
		for (auto y = 0; y < pointYSize - 1; y++)
		{
			QRectF temp;//介值
			temp.setLeft(*iterleft);
			temp.setRight(*iterRight);
			temp.setTop(*iterTop);
			temp.setBottom(*iterbottom);
			list.push_back(temp);
			iterTop++;
			iterbottom++;
		}
		iterleft++;
		iterRight++;
	}
	return list;
}
/**
* @brief StructData::GetdatasetKmt_cartesian_x_y 获取datasetkmt数据-cartesian坐标系-X_Y方向
* @return std::vector<StructData::DaTaKmt>
*/
std::vector<StructData::DaTaKmt> StructData::GetdatasetKmt_cartesian_x_y()
{
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
		temp.point1 = *iterkmt;	iterkmt++;//x
		temp.point2 = *iterkmt;	iterkmt++;//y
		temp.point3 = *iterkmt;	iterkmt++;//z
		temp.pointproperty = *iterkmt; iterkmt++;
		list.push_back(temp);
	}
	return list;
}
/**
* @brief StructData::fileproperty_cartesian_x_y 根据属性分类-cartesian坐标系-X_Y方向
* @param std::vector<QRectF>& list
* @param std::vector<StructData::DaTaKmt>& datainfo
* @return QMap<int, QVector<QRectF>>
*/
QMap<int, QVector<QRectF>> StructData::fileproperty_cartesian_x_y(std::vector<QRectF>& list, std::vector<StructData::DaTaKmt>& datainfo)
{
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
		_face_point_index;
		for (auto i = 0; i < IM3X->size(); i++)
		{
			float curdistance = abs(*(IM3X->begin() + i) - _face_point_index);
			if (curdistance < distancemin)
			{
				distancemin = curdistance;
				index_min = i+1;
			}
		}
		index = index_min;
	}
	QMap<int, QVector<QRectF>> allinfo;
	for each (DaTaKmt var in datainfo)
	{
		if (var.point3 ==index && var.point1 < pointXSize)
		{
			allinfo[var.pointproperty].push_back(list[(var.point1 - 1)*(pointYSize - 1) + var.point2 - 1]);
		}
	}
	return allinfo;
}
/**
* @brief StructData::GetAllCurspace_cartesian_y_z 获取所有网格数据-Cartesian坐标系-y_z方向
* @return std::vector<QRectF>
*/
std::vector<QRectF> StructData::GetAllCurspace_cartesian_y_z()
{
	std::vector<QRectF> list;
	//获取全部切割空间
	//获取从H5F文件中的数据
	Data::ListValuesPtr listValues;
	bool ok = autoModGetSourceData(listValues);//获取原始数据
	if (!ok && !listValues && listValues->size() == 0)
		return list;
	auto it = (listValues->begin());
	//cylindrical_R_Z
	Data::ValuesPtr IM1X = *it; it++;
	Data::ValuesPtr IM2X = *it; it++;
	Data::ValuesPtr IM3X = *it; it++;
	Data::ValuesPtr datasetkmt = *it;
	//开始获取
	auto iterleft = IM2X->begin();
	auto iterRight = IM2X->begin() + 1;
	auto iterTop = IM3X->begin();
	auto iterbottom = IM3X->begin() + 1;
	for (auto x = 0; x < pointXSize - 1; x++)
	{
		iterTop = IM3X->begin();
		iterbottom = IM3X->begin() + 1;
		for (auto y = 0; y < pointYSize - 1; y++)
		{
			QRectF temp;//介值
			temp.setLeft(*iterleft);
			temp.setRight(*iterRight);
			temp.setTop(*iterTop);
			temp.setBottom(*iterbottom);
			list.push_back(temp);
			iterTop++;
			iterbottom++;
		}
		iterleft++;
		iterRight++;
	}
	return list;
}
/**
* @brief StructData::GetdatasetKmt_cartesian_y_z 获取datasetkmt信息-cartesian坐标系-y_z方向
* @return std::vector<StructData::DaTaKmt>
*/
std::vector<StructData::DaTaKmt> StructData::GetdatasetKmt_cartesian_y_z()
{
	return GetdatasetKmt_cartesian_x_y();
}
/**
* @brief StructData::fileproperty_cartesian_y_z 跟具不同属性分类-cartesian坐标系-yz方向
* @param std::vector<QRectF>& list 网格信息
* @param std::vector<StructData::DaTaKmt>& datainfo datasetkmt数据
* @return QMap<int, QVector<QRectF>>
*/
QMap<int, QVector<QRectF>> StructData::fileproperty_cartesian_y_z(std::vector<QRectF>& list, std::vector<StructData::DaTaKmt>& datainfo)
{
	Data::ListValuesPtr listValues;
	autoModGetSourceData(listValues);//获取原始数据
	//获取dataSetKmt里的全部数据
	auto it = listValues->begin();
	Data::ValuesPtr IM1X = *it; it++;
	Data::ValuesPtr IM2X = *it; it++;
	Data::ValuesPtr IM3X = *it; it++;
	Data::ValuesPtr datasetkmt = *it;
	QMap<int, QVector<QRectF>> allinfo;
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
				index_min = i+1;
			}
		}
		index = index_min;
	}
	for each (DaTaKmt var in datainfo)
	{
		if (var.point1 ==index && var.point2 < pointXSize)
		{
			allinfo[var.pointproperty].push_back(list[(var.point2-1)*(pointYSize-1) + var.point3-1]);
		}
	}
	return allinfo;
}
/**
* @brief StructData::GetAllCurspace_cartesian_x_z  获取网格信息-cartesian坐标系xz方向
* @return std::vector<QRectF>
*/
std::vector<QRectF> StructData::GetAllCurspace_cartesian_x_z()
{
	std::vector<QRectF> list;
	//获取全部切割空间
	//获取从H5F文件中的数据
	Data::ListValuesPtr listValues;
	bool ok = autoModGetSourceData(listValues);//获取原始数据
	if (!ok && !listValues && listValues->size() == 0)
		return list;
	auto it = (listValues->begin());
	//cylindrical_R_Z
	Data::ValuesPtr IM1X = *it; it++;
	Data::ValuesPtr IM2X = *it; it++;
	Data::ValuesPtr IM3X = *it; it++;
	Data::ValuesPtr datasetkmt = *it;
	//开始获取
	auto iterleft = IM1X->begin();
	auto iterRight = IM1X->begin() + 1;
	auto iterTop = IM3X->begin();
	auto iterbottom = IM3X->begin() + 1;
	for (auto x = 0; x < pointXSize - 1; x++)
	{
		iterTop = IM3X->begin();
		iterbottom = IM3X->begin() + 1;
		for (auto y = 0; y < pointYSize - 1; y++)
		{
			QRectF temp;//介值
			temp.setLeft(*iterleft);
			temp.setRight(*iterRight);
			temp.setTop(*iterTop);
			temp.setBottom(*iterbottom);
			list.push_back(temp);
			iterTop++;
			iterbottom++;
		}
		iterleft++;
		iterRight++;
	}
	return list;
}
/**
* @brief StructData::GetdatasetKmt_cartesian_x_z 获取datasetkmt信息-cartesian坐标系-xz方向
* @return std::vector<StructData::DaTaKmt>
*/
std::vector<StructData::DaTaKmt> StructData::GetdatasetKmt_cartesian_x_z()
{
	return GetdatasetKmt_cartesian_x_y();
}
/**
* @brief StructData::fileproperty_cartesian_x_z 根据不同属性分类-cartesian坐标系-xz方向
* @param std::vector<QRectF>& list 网格信息
* @param std::vector<StructData::DaTaKmt>& datainfo datasetkmt数据
* @return QMap<int, QVector<QRectF>>
*/
QMap<int, QVector<QRectF>> StructData::fileproperty_cartesian_x_z(std::vector<QRectF>& list, std::vector<StructData::DaTaKmt>& datainfo){
	Data::ListValuesPtr listValues;
	autoModGetSourceData(listValues);//获取原始数据
	//获取dataSetKmt里的全部数据
	auto it = listValues->begin();
	Data::ValuesPtr IM1X = *it; it++;
	Data::ValuesPtr IM2X = *it; it++;
	Data::ValuesPtr IM3X = *it; it++;
	Data::ValuesPtr datasetkmt = *it;
	QMap<int, QVector<QRectF>> allinfo;
	int index = IM2X->size() / 2;
	if (istrue)
	{
		int index_min = 1;
		float distancemin = 10000.0f;
		_face_point_index;
		for (auto i = 0; i < IM2X->size(); i++)
		{
			float curdistance = abs(*(IM2X->begin() + i) - _face_point_index);
			if (curdistance < distancemin)
			{
				distancemin = curdistance;
				index_min = i+1;
			}
		}
		index = index_min;
	}
	for each (DaTaKmt var in datainfo)
	{
		if (var.point2 == index && var.point1 < pointXSize&& var.point3)
		{
			allinfo[var.pointproperty].push_back(list[(var.point1 - 1)*(pointYSize - 1) + var.point3 - 1]);
		}
	}
	return allinfo;
}