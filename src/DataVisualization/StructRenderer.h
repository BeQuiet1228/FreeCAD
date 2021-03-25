#pragma once
#ifndef _STRUCTURERENDERER_H_
#define _STRUCTURERENDERER_H_
#include <Renderer.h>
#include "structureData.h"
#include<QVector>
class StructureRenderer :public Renderer{
public:
	StructureRenderer(std::shared_ptr<structureData> data);
	~StructureRenderer();
private:
	Data::Rang xRang, yRang;
	std::mutex xRangMutex, yRangMutex;
public:
	//渲染
	virtual bool drawImage() override;
	virtual bool addListRang(std::list<Data::Rang> listRang) override;
	virtual bool drawPointImage() override;
	virtual bool setDefaultRang() override;
	virtual void dataInit() override;
private:
	//将数据坐标转换为图片上的坐标
	float transitionX(const float& x, const float& xScale, const Data::Rang& xr);
	float transitionY(const float& y, const float& yScale, const Data::Rang& yr);
	void transitionPoint(QPointF& point, const float& xScale, const Data::Rang& xr, const float& yScale, Data::Rang& yr);
	void transitionRectF(QRectF& _rectf, const float& sScale, const Data::Rang& xr, const float& yScale,Data::Rang& yr);
	//初始化数据与图片坐标的缩放比例
	bool getTransitionScale(float& xScale, float& yScale);

public:
	//真空坐标
	QVector<QRectF> vacuo_vector; 
	//导管坐标
	QVector<QRectF> conduit_vector;
	//特殊属性坐标
	QVector<QRectF> specificproperty_vector;

};

#endif
