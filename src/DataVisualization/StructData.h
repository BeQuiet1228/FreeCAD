#pragma once 
#ifndef _STRUCT_DATA_H_
#define _STRUCT_DATA_H_
#include "Data.h"
#include <QVector>
#include <QMap>
#include <QRectF>
enum C_TYPE
{
	POLAR=0,
	CYLINDRICAL,
	CARTESIAN,
};
struct _3DPointf
{
	float _1st;
	float _2rd;
	float _3th;
	_3DPointf() :_1st(0.0f), _2rd(0.0f), _3th(0.0f){}
	int operator ==(const _3DPointf& that)
	{
		if (this->_1st == that._1st&&this->_2rd != that._2rd&&this->_3th != that._3th)
			return 1;
		else if (this->_2rd == that._2rd&&this->_1st != that._1st&&this->_3th != that._3th)
			return 2;
		else if (this->_3th == that._3th&&this->_1st != that._1st&&this->_2rd != that._2rd)
			return 3;
		return -1;
	}
	float operator [](int index)
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
};

class StructData:public XYData
{
public:
	typedef struct DaTaKmt
	{
		//坐标1
		int point1;
		//坐标2
		int point2;
		//坐标3
		int point3;
		//属性
		int pointproperty;
	}DATAKMT;

	StructData(Hdf5Data& heData, DirectionType _type,const RunMod& mod=SINGLE_THREAD);
	StructData(Hdf5Data& heData,_3DPointf startpoint,_3DPointf endpoint,const RunMod& mod=SINGLE_THREAD);
public:
	virtual bool loadPoint();
	DirectionType GetDirectionType()
	{
		return m_Type;
	}
	C_TYPE GetC_TYPE()
	{
		return _ctype;
	}
	QMap<int, QVector<QRectF>> GetAllKMTInfo(){
		return allkmtInfo;
	}
	bool loadroom();
	void setXRang(const Rang& rg)
	{
		std::lock_guard<std::mutex> am(xRangMutex);
		xRang = rg;
	}
	void setYRang(const Rang& rg)
	{
		std::lock_guard<std::mutex> am(yRangMutex);
		yRang = rg;
	}
	Rang getXRang()
	{
		std::lock_guard<std::mutex> am(xRangMutex);
		return xRang;
	}
	Rang getYRang()
	{
		std::lock_guard<std::mutex> am(yRangMutex);
		return yRang;
	}
protected:
	virtual bool initXYRang(){ return 0; }
	virtual void restorDeriveData() override{}
	bool loadPoint_polar();
	bool loadPoint_cylindrical();
	bool loadPoint_cartesian();
	
	//加载3维空间切割空间
	bool loadroom_polar();
	bool loadroom_cylindrical();
	bool loadroom_cartesian();
	//
	bool loadroom_polar_R_Z();
private:
	int pointXSize, pointYSize;
	DirectionType m_Type;
	C_TYPE _ctype;
	bool istrue;
	_3DPointf mstartpoint;
	_3DPointf mendpoint;
	QMap<int, QVector<QRectF>> allkmtInfo;
	//
	Rang xRang, yRang;
	std::mutex xRangMutex, yRangMutex;
};
#endif