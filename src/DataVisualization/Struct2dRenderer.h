#pragma once
#ifndef _STRUCT_2D_RENDERER_H_
#define _STRUCT_2D_RENDERER_H_
#include "Renderer.h"
#include "Struct2dData.h"
#include <QMap>
#include <QColor>
class Struct2DRenderer :public Renderer
{
public:
	Struct2DRenderer(std::shared_ptr<Struct2dData> data);
	~Struct2DRenderer();
private:
	Data::Rang xRang, yRang;
	std::mutex xRangMutex, yRangMutex;
public:
	virtual bool drawImage() override;
	virtual bool addListRang(std::list<Data::Rang> listRang) override;
	virtual bool drawPointImage() override;
	virtual bool setDefaultRang() override;
	virtual void dataInit() override;
private:
	void transitionPoint(QPointF& point, const float& xScale, const Data::Rang& xr, const float& yScale, const Data::Rang& yr)
	{
		point.setX(transitionX(point.x(), xScale, xr));
		point.setY(transitionY(point.y(), yScale, yr));
	}
	float transitionX(const float& x, const float& xScale, const Data::Rang& xr)
	{
		return (x - xr.min)*xScale;
	}
	float transitionY(const float& y, const float& yScale, const Data::Rang& yr)
	{
		return (y - yr.min)*yScale;
	}
private:
	QMap<int, QColor> color_tab;
};
#endif