#pragma once
#include <Renderer.h>
#include "TimeData.h"
class TimeRenderer:public Renderer{
public:
	TimeRenderer(std::shared_ptr<TimeData> data);
	~TimeRenderer();

private:
	Data::Rang xRang, yRang;
	std::mutex xRangMutex, yRangMutex;
public:
	//渲染
	virtual bool drawImage() override;
	virtual bool addListRang(std::list<Data::Rang> listRang) override;
	virtual bool drawPointImage() override{ return true; };

public:
	//操作范围
	void setXRang(const Data::Rang& rang);
	Data::Rang getXRang();
	void setYRang(const Data::Rang& rang);
	Data::Rang getYRang();

private:
	//将数据坐标转换为图片上的坐标
	float transitionX(const float& x,const float& xScale,const Data::Rang& xr);
	float transitionY(const float& y,const float& yScale,const Data::Rang& yr);
	void transitionPoint(QPointF& point, const float& xScale, const Data::Rang& xr, const float& yScale, Data::Rang& yr);
	//初始化数据与图片坐标的缩放比例
	bool getTransitionScale(float& xScale,float& yScale);
};