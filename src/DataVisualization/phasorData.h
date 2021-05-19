#pragma once
#ifndef _PHASORDATA_H_
#define _PHASORDATA_H_
#include "DirData.h"
#include <QRectF>
#include <QVector>
typedef struct phasorinfo 
{
public:
	QRectF phasor_room;
	unsigned int room_property;//属性，真空0，导管1
	//向量
	QPointF p1;
	QPointF p2;
	phasorinfo() :p1(0.0, 0.0), p2(0.0, 0.0), phasor_room(0.0, 0.0, 0.0, 0.0), room_property(0){}
	void SetRectF(QRectF _rectf){
		phasor_room = _rectf;
	}
}PIF;

class phasorData :public DirData
{
public:
	phasorData(Hdf5Data& heData,const RunMod& mod=SINGLE_THREAD);
	~phasorData();
	enum DISMODE{
		sizeToLen,
		sizeToColor = 1,
	};
protected:

	virtual void restorDeriveData() override;
	//初始化xy的取值范围
	virtual bool initXYRang();
	//初始化相关数据
	bool initData();
	//计算出向量数据
	bool initVectorData();
	//计算出向量数据2
	bool initVectorData2();
	//获取坐标的刻度
	std::vector<qreal> getaxis_x();
	std::vector<qreal> getaxis_y();
public:
	virtual bool loadPoint();
	virtual unsigned int findIndexFromXValueL(const float& x) override;
	QPointF findindexlen_coef(int index);
	QPointF findindexP1(int index);
	
	//获取信息
	std::string getInformationTitle();

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
	//设置取值范围
	void setXRang(const Rang& xr)
	{
		std::lock_guard<std::mutex> am(xRangMutex);
		xRang = xr;
	}
	void setYRang(const Rang& yr){
		std::lock_guard<std::mutex> am(yRangMutex);
		yRang = yr;
	}
	
	QVector<QRectF> getAllCutRoom();
	QVector<QPointF> Getp1Point();
	QVector<QPointF> Getp2Point();
	float GetVecXScale();
	float GetVecYScale();
	DISMODE GetdisMode(){
		return disMode;
	}
	std::vector<float> getScaleVal(){
		return sizeScale;
	}
	void setdisMode(DISMODE a){
		disMode = a;
	}
	//2021年5月19日---新增加
	Data::Rang getdefXrang()
	{
		return defXrang;
	}
	Data::Rang getdefYrang()
	{
		return defYrang;
	}
	int getXsize()
	{
		return posxSize;
	}
	int getYsize()
	{
		return posySize;
	}
private:
	//xy的范围
	Rang xRang, yRang;
	std::mutex xRangMutex, yRangMutex;
	//坐标的个数
	int posxSize;
	int posySize;
	QVector<QRectF> mPiflist_rect;
	QVector<QPointF> p1;//箭头起点
	QVector <QPointF> p2;//箭头终点
	QVector<QPointF> len_coef;//长度系数
	std::vector<float> sizeScale;//大小系数
	//获取x,y的缩放
	DISMODE disMode;
	bool istrue;
	Rang defXrang, defYrang;
};
#endif