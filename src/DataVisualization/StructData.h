#pragma once 
#ifndef _STRUCT_DATA_H_
#define _STRUCT_DATA_H_
#include "Data.h"
#include <QVector>
#include <QMap>
#include <QRectF>
#include <QlineF>
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
	int operator ==(const _3DPointf& that) const
	{
		if (this->_1st == that._1st&&this->_2rd != that._2rd&&this->_3th != that._3th)
			return 1;
		else if (this->_2rd == that._2rd&&this->_1st != that._1st&&this->_3th != that._3th)
			return 2;
		else if (this->_3th == that._3th&&this->_1st != that._1st&&this->_2rd != that._2rd)
			return 3;
		return 0;
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
	enum PROPERTYPE{
		RECTPROPER,
		LINEPROPER
	};
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
	struct CutCir{
		//内圆的切点
		QPointF inner1;
		QPointF inner2;
		//外圆的切点
		QPointF excir1;
		QPointF excir2;
		//开始角度，结束角度
		qreal startAngle;
		qreal endAngle;
		//内圈半径，外圈半径
		qreal R_inner;
		qreal R_excir;
	};
	struct  structpoint
	{
		structpoint() :x(0.0), y(0.0), d1(0.0), d2(0.0){}
		float x, y;//直角坐标系下的数据
		float d1, d2;//原始数据
	};
	enum structType
	{
		//理想导体
		PERFECTCONDUCTOR = 3,
		//电导新材料
		CONDUCTORNEW = 8,
		//介质
		DIOLECTRIC = 4,
		//电介质和电导
		DIELECTIRANDCONDUCTANCE = 16,
		//磁导率
		PERMEABILITY = 32,
		//自由空间
		FREESPACE = 64,
		//电阻
		FOIL = 128,
		//
		PORT,
		DRIVER,
		INDUCTOR
	};
	StructData(Hdf5Data& heData, DirectionType _type,const RunMod& mod=SINGLE_THREAD);
	StructData(Hdf5Data& heData,_3DPointf startpoint,_3DPointf endpoint,const RunMod& mod=SINGLE_THREAD);
public:
	virtual bool loadPoint();
	DirectionType GetDirectionType()
	{
		return mType;
	}
	C_TYPE GetC_TYPE()
	{
		return mCtype;
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
	std::map<int, std::vector<QRectF>>GetAllcutInfo()
	{
		return allcutroom;
	}
	std::map<int, std::vector<CutCir>> GetAllcurInfo_cir()
	{
		return allcutroomcir;
	}
	std::map<unsigned __int64, std::vector<QLineF>> GetProperLines()
	{
		return allLines;
	}
	void segloadRoom(unsigned  __int64 site1,unsigned __int64 site2);
protected:
	virtual bool initXYRang(){ return 0; }
	virtual void restorDeriveData() override{}
	bool loadPointPolar();
	bool loadPointCylindrical();
	bool loadPointCartesian();	
	//加载3维空间切割空间
	bool loadroomPolar();
	bool loadroomPolarRz();
	bool loadroomPolarRtheta();
	bool loadroomCylindrical();
	bool loadroomCylindricalRz();
	bool loadroomCylindricalRtheta();
	bool loadroomCartesian(); 
	bool loadroomCartesianXy();
	bool loadroomCartesianXz();
	bool loadroomCartesianYz();
	std::vector<DaTaKmt> GetdatasetKmtPolar();
	std::vector<DaTaKmt> GetdatasetKmtCylindrical();
	bool createLines(std::map<int, std::vector<QPoint>> &points,const Data::ValuesPtr &IMX, const Data::ValuesPtr &IMY);
	std::list<unsigned __int64> isAnAttritbute(unsigned __int64, PROPERTYPE);
private:
	//全部切割空间
	std::map<int, std::vector<QRectF>>	allcutroom;
	std::map<int, std::vector<CutCir>> allcutroomcir;
	std::map<unsigned __int64, std::vector<QLineF>> allLines;
	int pointXSize, pointYSize;
	DirectionType mType;
	C_TYPE mCtype;
	bool istrue;
	_3DPointf mstartpoint;
	_3DPointf mendpoint;
	Rang xRang, yRang;
	std::mutex xRangMutex, yRangMutex;
	//确定面的索引
	float _face_point_index;
	//因为重复处理会消耗时间，所以设定开关，防止重复读取
	bool isloadRoom;
};
#endif