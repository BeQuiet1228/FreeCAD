#include "StructData.h"
StructData::StructData(Hdf5Data& heData, DirectionType _type, const RunMod& mod):XYData(heData,mod),istrue(false){
	m_Type = _type;
	std::vector<std::string> headerlist = autoHeaderInfo();
	auto headeriter = headerlist.end() - 1;
	if (headeriter->find("polar") != std::string::npos)
	{
		//当前为polar
		_ctype = C_TYPE::POLAR;
	}
	else if (headeriter->find("cylindrical") != std::string::npos)
	{
		//当前为cylindrical
		_ctype = C_TYPE::CYLINDRICAL;
	}
	else if (headeriter->find("cartesian") != std::string::npos)
	{
		//当前为cartexian
		_ctype = C_TYPE::CARTESIAN;
	}
}

StructData::StructData(Hdf5Data& heData, _3DPointf startpoint, _3DPointf endpoint, const RunMod& mod):XYData(heData,mod),istrue(true),mstartpoint(startpoint),mendpoint(endpoint){
	std::vector<std::string> headerlist = autoHeaderInfo();
	int res = (startpoint == endpoint);
	auto headeriter = headerlist.end() - 1;
	if (headeriter->find("polar") != std::string::npos)
	{
		//当前为polar
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
	}
	else if (headeriter->find("cylindrical") != std::string::npos)
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
	}
	else if (headeriter->find("cartesian") != std::string::npos)
	{
		//当前为cartexian
		_ctype = C_TYPE::CARTESIAN;//X_Y_Z
		switch (res)
		{
		case 1:
			m_Type = Y_Z;break;
		case 2:
			m_Type = X_Z; break;
		case 3:
			m_Type = X_Y; break;
		}
	}

}

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

bool StructData::loadroom()
{
	switch (_ctype)
	{
	case POLAR:
		return loadroom_polar();
	case CYLINDRICAL:
		return loadroom_cylindrical();
	case CARTESIAN:
		return loadroom_cartesian();
	}
}

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
bool StructData::loadroom_polar_R_Z()
{
	if (pointXSize<2||pointYSize<2)
		return false;
	Data::ListValuesPtr listValues;
	bool ok = autoModGetSourceData(listValues);//获取原始数据
	if (!ok && !listValues && listValues->size() == 0)
		return false;
	auto it = (listValues->begin());
	//获取全部切割
	std::vector<QRectF> list= GetAllCurspace_polar_R_Z();
	//获取datasetKmt的信息
	std::vector<DaTaKmt> datainfolist = GetdatasetKmt_polar_R_Z();
	//填充
	QMap<int, QVector<QRectF>>allKmtInfo=fileproperty_polar_R_Z(list, datainfolist);
	allcutroom.swap(allKmtInfo);
}
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
	QMap<int, QVector<QRectF>> allinfo;
	for each (DaTaKmt var in datainfo)
	{
		if (var.point3==1&&var.point1<pointXSize-1)
		{
			allinfo[var.pointproperty].push_back(list[(var.point1 - 1)*(pointYSize - 1) + var.point2 - 1]);
		}
	}
	return allinfo;
}

bool StructData::loadroom_polar_R_THETA()
{
	if (pointXSize < 2 || pointYSize < 2)
		return false;
	Data::ListValuesPtr listValues;
	bool ok = autoModGetSourceData(listValues);//获取原始数据
	if (!ok && !listValues && listValues->size() == 0)
		return false;
	auto it = (listValues->begin());
	std::map<int, std::vector<CutCir>> temp = filecir_polar_R_THETA();
	allcutroom_cir.swap(temp);
	return true;
}
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
	int CutNum = rand_val.size() - 1;
	std::vector<DaTaKmt> datakmtinfo =GetdatasetKmt_polar_R_THETA();
	for each (DaTaKmt var in datakmtinfo)
	{
		if (var.point1==1&&var.point3<rand_val.size())
		{
			listcir[var.pointproperty].push_back(_CutCirlist[(var.point2 - 1)*CutNum + (var.point3 - 1)]);
		}
	}
#pragma endregion 
	/**************************************/
	return listcir;
}
std::vector<StructData::DaTaKmt> StructData::GetdatasetKmt_polar_R_THETA(){
	return GetdatasetKmt_polar_R_Z();
}
bool StructData::loadroom_cylindrical_r_z(){
	if (pointXSize < 2 || pointYSize < 2)
		return false;
	Data::ListValuesPtr listValues;
	bool ok = autoModGetSourceData(listValues);//获取原始数据
	if (!ok && !listValues && listValues->size() == 0)
		return false;
	auto it = (listValues->begin());
	//获取全部切割
	std::vector<QRectF> list = GetAllCurspace_cylindrical_R_Z();
	//获取datasetKmt的信息
	std::vector<DaTaKmt> datainfolist = GetdatasetKmt_cylindrical_R_Z();
	//填充
	QMap<int, QVector<QRectF>>allKmtInfo = fileproperty_cylindrical_R_Z(list, datainfolist);
	allcutroom.swap(allKmtInfo);
	return true;
}
bool StructData::loadroom_cylindrical_r_theta(){
	if (pointXSize < 2 || pointYSize < 2)
		return false;
	Data::ListValuesPtr listValues;
	bool ok = autoModGetSourceData(listValues);//获取原始数据
	if (!ok && !listValues && listValues->size() == 0)
		return false;
	auto it = (listValues->begin());
	std::map<int, std::vector<CutCir>> temp = filecir_cylindrical_R_THETA();
	allcutroom_cir.swap(temp);
	return true;
}

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
	for each (DaTaKmt var in datainfo)
	{
		if (var.point3 == 1 && var.point1 < pointXSize - 1)
		{
			allinfo[var.pointproperty].push_back(list[(var.point1 - 1)*(pointYSize - 1) + var.point2 - 1]);
		}
	}
	return allinfo;
}
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
	int CutNum = rand_val.size() - 1;
	std::vector<DaTaKmt> datakmtinfo = GetdatasetKmt_cylindrical_R_THETA();
	for each (DaTaKmt var in datakmtinfo)
	{
		if (var.point1 == 1 && var.point3 < rand_val.size())
		{
			listcir[var.pointproperty].push_back(_CutCirlist[(var.point2 - 1)*CutNum + (var.point3 - 1)]);
		}
	}
#pragma endregion 
	/**************************************/
	return listcir;
}

std::vector<StructData::DaTaKmt> StructData::GetdatasetKmt_cylindrical_R_THETA(){
	return GetdatasetKmt_cylindrical_R_Z();
}
bool StructData::loadroom_cartesian_x_y(){
	if (pointXSize < 2 || pointYSize < 2)
		return false;
	//获取全部切割
	std::vector<QRectF> list = GetAllCurspace_cartesian_x_y();
	//获取datasetKmt的信息
	std::vector<DaTaKmt> datainfolist = GetdatasetKmt_cartesian_x_y();
	//填充
	QMap<int, QVector<QRectF>>allKmtInfo = fileproperty_cartesian_x_y(list, datainfolist);
	allcutroom.swap(allKmtInfo);
	return true;
}
bool StructData::loadroom_cartesian_x_z(){
	if (pointXSize < 2 || pointYSize < 2)
		return false;
	//获取全部切割
	std::vector<QRectF> list = GetAllCurspace_cartesian_x_z();
	//获取datasetKmt的信息
	std::vector<DaTaKmt> datainfolist = GetdatasetKmt_cartesian_x_z();
	//填充
	QMap<int, QVector<QRectF>>allKmtInfo = fileproperty_cartesian_x_z(list, datainfolist);
	allcutroom.swap(allKmtInfo);
	return true;
}
bool StructData::loadroom_cartesian_y_z(){
	if (pointXSize < 2 || pointYSize < 2)
		return false;
	//获取全部切割
	std::vector<QRectF> list = GetAllCurspace_cartesian_y_z();
	//获取datasetKmt的信息
	std::vector<DaTaKmt> datainfolist = GetdatasetKmt_cartesian_y_z();
	//填充
	QMap<int, QVector<QRectF>>allKmtInfo = fileproperty_cartesian_y_z(list, datainfolist);
	allcutroom.swap(allKmtInfo);
	return true;
}
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
	QMap<int, QVector<QRectF>> allinfo;
	for each (DaTaKmt var in datainfo)
	{
		if (var.point3 == IM3X->size()/2 && var.point1 < pointXSize - 1)
		{
			allinfo[var.pointproperty].push_back(list[(var.point1 - 1)*(pointYSize - 1) + var.point2 - 1]);
		}
	}
	return allinfo;
}
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
std::vector<StructData::DaTaKmt> StructData::GetdatasetKmt_cartesian_y_z()
{
	return GetdatasetKmt_cartesian_x_y();
}
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
	for each (DaTaKmt var in datainfo)
	{
		if (var.point1 == IM1X->size()/2 && var.point2 < pointXSize - 1)
		{
			allinfo[var.pointproperty].push_back(list[(var.point2 - 1)*(pointYSize - 1) + var.point3 - 1]);
		}
	}
	return allinfo;
}
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
std::vector<StructData::DaTaKmt> StructData::GetdatasetKmt_cartesian_x_z()
{
	return GetdatasetKmt_cartesian_x_y();
}
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
	for each (DaTaKmt var in datainfo)
	{
		if (var.point2 == IM2X->size()/2 && var.point1 < pointXSize - 1)
		{
			allinfo[var.pointproperty].push_back(list[(var.point1 - 1)*(pointYSize - 1) + var.point3 - 1]);
		}
	}
	return allinfo;
}