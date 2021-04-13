#pragma once 
#ifndef _STRUCTUREDATA_H_
#define _STRUCTUREDATA_H_
#include "Data.h"
#include <vector>
#include <mutex>
#include <QVector>
#include <QRectF>
#include <QMap>
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

enum StructTexture
{
	//理想导体
	Perfect_Conductor=3,
	//电导新材料
	Conductor_New=8,
	//介质
	Diolectric=4,
	//磁导率
	Permeability=16,
	//真空
	Vacuo=1024,
};
class structureData :public XYData{
public:
	//Z-R坐标系
	struct  structpoint
	{
		structpoint():x(0.0),y(0.0),d1(0.0),d2(0.0){}
		float x, y;//直角坐标系下的数据
		float d1, d2;//原始数据
	};

	//圆环坐标系
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

	structureData(Hdf5Data& heData, const RunMod& mod = SINGLE_THREAD);
	~structureData();
protected:
	virtual void restorDeriveData() override;
public:
	//载入数据
	virtual bool loadPoint();
	virtual unsigned int findIndexFromXValueL(const float& x){ return 0; }
	bool loadrectpoint();
	//释放中间参数
	bool Dropout_value();
	QMap<int, QVector<QRectF>> GetAllKMTInfo()
	{
		return allKmtInfo;
	}
	QMap<int, QVector<CutCir>> GetAllKMTInfo_Cir()
	{
		return allKmtinfo_cir;
	}
	QVector<qreal> Get_R_val();
	QVector<qreal> Get_rand_val();
	//获取取值范围
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
protected:
	//初始化xy的取值范围
	virtual bool initXYRang();
	//获取切割的空间
	QVector<QRectF> GetAllCutspace();
	//获取dataSetkmt的全部数据
	QVector<DaTaKmt> GetdatasetKmt();
	
	//填充相关属性的队列
	void fileproperty(QVector<QRectF> list);
	//填充圆柱坐标系需要的信息
	void fileCylindrical_info();
private:
	//横向点的个数
	int pointXSize;
	//纵向点的个数
	int pointYsize;
	//datasetkmt的数据采集
	QVector<DaTaKmt> datakmtinfo;

	QMap<int, QVector<QRectF>> allKmtInfo;
	QMap<int, QVector<CutCir>> allKmtinfo_cir;
	//xy的范围
	Rang xRang, yRang;
	//圆柱坐标系的取值范围
	QVector<qreal> R_val;
	QVector<qreal> rand_val;
	std::mutex xRangMutex, yRangMutex;
};
#endif