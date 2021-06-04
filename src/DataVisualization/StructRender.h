#pragma once
#ifndef _STRUCT_RENDER_H_
#define _STRUCT_RENDER_H_
#include "Renderer.h"
#include "StructData.h"
#include <QColor>
enum StructTexture
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
class StructRender :public Renderer
{
public:
	StructRender(std::shared_ptr<StructData> data);
	~StructRender();
	virtual void loadconfig()override;
	virtual bool drawImage() override;
	virtual bool addListRang(std::list<Data::Rang> listRang) override;
	virtual bool drawPointImage() override;
	virtual bool setDefaultRang() override;
	virtual void dataInit() override;
	virtual bool setDefaultRang(QSize&) override;
private:
	bool drawImageRectspace();
	bool drawImageRandspace();
	float transitionX(const float& x, const float& xScale, const Data::Rang& xr);
	float transitionY(const float& y, const float& yScale, const Data::Rang& yr);
	void transitionPoint(QPointF& point, const float& xScale, const Data::Rang& xr, const float& yScale, const Data::Rang& yr);
	void transitionRectF(QRectF& _rectf, const float& sScale, const Data::Rang& xr, const float& yScale, Data::Rang& yr);
	void transitionLineF(QLineF& line, const float& xScale, const float& yScale,const Data::Rang &xr,const Data::Rang& yr);
	bool getTransitionScale(float& xScale, float& yScale);
	QVector<QPainterPath> StructRender::GetPath(std::vector<StructData::CutCir>& _vector, const Data::Rang& xr, const Data::Rang& yr, const float& xScale, const float& yScale);
	StructData::structpoint findApointZr(QPointF _curpostion);
	float GetDistance(QPointF p1, QPointF p2);
	bool drawPointRect();
	bool drawPointCir();
	StructData::structpoint findApointCylindrical(QPointF _curpoint);
	void DrawLine(QPainter& painter,QVector<QLineF>& lines,int mPorper);
private:
	QMap<int, QColor> color_tab;
	QMap<int, QColor> color_pen;
	std::map<int, QPixmap> pixmap;
	Data::Rang xRang, yRang;
	std::mutex xRangMutex, yRangMutex;
	bool isAA;
};

#endif
