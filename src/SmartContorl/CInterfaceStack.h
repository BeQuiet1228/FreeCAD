#pragma once
#include "SmartContorl.h"
#include "HDF5Reader/hdf5io.h"
class CInterfaceStack{

public:
	CInterfaceStack(){};
	~CInterfaceStack(){};

public:
	//当前运算结果
	ChipicRunDataPtr activeRunData;
	//当前图的h5d对象
	Hdf5Data activeH5Data;
	//当前数据
	VectorF activeValues;

public:
	//清理数据
	void clear(){
		this->activeRunData.reset();
		Hdf5Data d;
		this->activeH5Data = d;
		this->activeValues.clear();
	}
};