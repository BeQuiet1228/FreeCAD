#pragma once
#ifndef _PHASORRENDERERE_H_
#define _PHASORRENDERERE_H_
#include "Renderer.h"
#include "phasorData.h"
#include <QColor>
class phasorRenderer :public Renderer,public RendererValueRangeInterface
{
public:
	phasorRenderer(std::shared_ptr<phasorData> data);
	~phasorRenderer();
private:
	Data::Rang xRang, yRang;
	std::mutex xRangMutex, yRangMutex;
public:
	virtual bool drawImage() override;
	virtual bool addListRang(std::list<Data::Rang> listRang) override;
	virtual bool drawPointImage() override;
	virtual bool setDefaultRang() override;
	virtual void dataInit() override;
	virtual void loadconfig() override;
	virtual bool setDefaultRang(QSize& ) override;
	virtual Data::Rang getValueRange() override;
private:
	QPointF GetarrowTop(QPointF endpoint,QPointF startpoint);
	QPointF GetarrowBottom(QPointF endpoint,QPointF startpoint);
	float transitionX(const float& x, const float& xScale, const Data::Rang xr)
	{
		return (x - xr.min)*xScale;
	}
	float transitionY(const float& y, const float& yScale, const Data::Rang yr)
	{
		return (y - yr.min)*yScale;
	}
	void transitionpointF(QPointF & p,const float& xScale,const float& yScale,const Data::Rang xr,const Data::Rang yr);
	void transitionRectF(QRectF& _rectf, const float& xScale, const float& yScale, Data::Rang xr, Data::Rang yr){
		_rectf.setLeft(transitionX(_rectf.left(),xScale,xr));
		_rectf.setRight(transitionX(_rectf.right(), xScale, xr));
		_rectf.setTop(transitionY(_rectf.top(), yScale, yr));
		_rectf.setBottom(transitionY(_rectf.bottom(), yScale, yr));
	}
	void transionVector(QPointF& endpoint, QPointF startpoint, const float& xScale, const float& yScale);
	void transionVector(QPointF& endipoint,QPointF startpoint,const float& lenScale);
	QVector<QRectF> GetRectF_Scene();
	QVector<QLineF> findVecLines(QVector<QRectF> scene_rect,QVector<QPointF> p1,QVector<QPointF> p2);
	bool drawImageScence();
	int findApoint(QPointF A_point);
private:
	unsigned __int32 penSize;
	QColor penColor;
	bool isAA;
	unsigned long long colormapsite;
	unsigned long long lastcolormapsite;
};
#endif