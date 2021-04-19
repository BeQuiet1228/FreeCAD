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
	Data::ValuesPtr IM1X = *it; it++;
	Data::ValuesPtr IM2X = *it; it++;
	Data::ValuesPtr IM3X = *it; it++;
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
		xr.max = *(IM2X->end()-1);
		xr.min = *(IM2X->begin());
		yr.max = *(IM1X->end() - 1);
		yr.min = *(IM1X->begin());
		setXRang(xr);
		setYRang(yr);
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
	Data::ValuesPtr IM1X = *it; it++;
	Data::ValuesPtr IM2X = *it; it++;
	Data::ValuesPtr IM3X = *it; it++;
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
		yr.min = *(IM3X->begin());
		yr.max = *(IM3X->end()-1);
		setXRang(xr);
		setYRang(yr);
	}
		break;
	case R_THETA:
	{
		//设置X_Y的范围
		Rang xr;
		Rang yr;
		xr.max = *(IM1X->end() - 1);
		xr.min = -xr.max;
		yr = xr;
		setXRang(xr); 
		setYRang(yr);
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
		return false;
	}
}
bool StructData::loadroom_cylindrical(){
	return true;
}
bool StructData::loadroom_cartesian(){
	return true;
}

//

bool StructData::loadroom_polar_R_Z()
{
	Data::ListValuesPtr listValues;
	bool ok = autoModGetSourceData(listValues);//获取原始数据
	if (!ok && !listValues && listValues->size() == 0)
		return false;
	auto it = (listValues->begin());
	Data::ValuesPtr IM2X = *it; it++;//R
	Data::ValuesPtr IM3X = *it; it++;//THETA
	Data::ValuesPtr IM1X = *it; it++;//Z
	Data::ValuesPtr datasetkmt = *it;//datasetkmt
	pointXSize = IM1X->size();
	pointYSize=IM2X->size();
	//R_THETA_Z
	//获取切割空间
	auto iterleft = IM1X->begin();
	auto iterRight = IM1X->begin() + 1;
	auto iterTop = IM2X->begin();
	auto iterbottom = IM2X->begin() + 1;
	std::vector<QRectF> list;
	for (auto x = 0; x < pointXSize-1; x++)
	{
		iterTop = IM2X->begin();
		iterbottom = IM2X->begin() + 1;
		for (auto y = 0; y < pointYSize - 1; y++)
		{
			QRectF temp;
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
	//获取到全部切割空间
	//获取datasetkmt中的数据
	std::vector<DaTaKmt> datakmtlist;
	auto iterkmt = datasetkmt->begin();
	for (;iterkmt!=datasetkmt->end();)
	{
		DaTaKmt temp;
		temp.point2 = *iterkmt; iterkmt++;
		temp.point3 = *iterkmt; iterkmt++;
		temp.point1 = *iterkmt; iterkmt++;
		temp.pointproperty = *iterkmt; iterkmt++;
		datakmtlist.push_back(temp);
	}


	int _theta, rmin, rmax, zmin, zmax;
	if (auto res = (mstartpoint == mendpoint)!=-1)
	{
		//THETA
		for (auto  i = 0; i < IM2X->size(); i++)
		{
			auto iter = IM2X->begin() + i;
			if (*iter==mstartpoint[res])
			{
				_theta = i;
				break;
			}
		}
		//R
		for (auto i = 0; i < IM1X->size();i++)
		{
			auto iter = IM1X->begin()+i;
			if (*iter == mstartpoint[1])
				rmin = i;
			if (*iter == mendpoint[1])
				rmax = i;
		}
		//Z
		for (auto i = 0; i < IM2X->size();i++)
		{
			auto iter = IM2X->begin() + i;
			if (*iter == mstartpoint[3])
				zmin = i;
			if (*iter == mendpoint[3])
				zmax = i;
		}
	}
	else
	{
		_theta = 1;
		rmin = 1;
		rmax = IM1X->size();
		zmin = 1;
		zmax = IM3X->size();
	}
	for each (DaTaKmt var in datakmtlist)
	{
		if (var.point3 == _theta&& var.point1<zmax-1 && var.point1>zmin && var.point2 < rmax-1&&var.point2>rmin)
		{
			allkmtInfo[var.pointproperty].push_back(list[(var.point1 - 1)*(rmax-1) + var.point2 - 1]);
		}
	}
}