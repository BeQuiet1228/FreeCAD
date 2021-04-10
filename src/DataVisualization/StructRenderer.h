#pragma once
#ifndef _STRUCTURERENDERER_H_
#define _STRUCTURERENDERER_H_
#include <Renderer.h>
#include "structureData.h"
#include<QVector>
enum Coordinate_Dir{
	cylindrical_coordinate,
	polar_coordinate,
	Z_R_coordinater,
};//坐标系方向
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
	void SetCoordinateDir(Coordinate_Dir);
	Coordinate_Dir getCurCoordinateDir();
	void SetColor(int Material_index, QColor& _color)
	{
		//color_tab[Material_index] =QColor(_color.red,_color.green,_color.blue,_color.alpha);
	}
private:
	//将数据坐标转换为图片上的坐标
	float transitionX(const float& x, const float& xScale, const Data::Rang& xr);
	float transitionY(const float& y, const float& yScale, const Data::Rang& yr);
	void transitionPoint(QPointF& point, const float& xScale, const Data::Rang& xr, const float& yScale, Data::Rang& yr);
	void transitionRectF(QRectF& _rectf, const float& sScale, const Data::Rang& xr, const float& yScale,Data::Rang& yr);

	QVector<QRectF> GetCylindricalRect(QVector<qreal> _r_rang);
	//初始化数据与图片坐标的缩放比例
	bool getTransitionScale(float& xScale, float& yScale);
	bool drawImage_Z_R();
	bool drawImage_Polar_coordinate();
	bool drawImage_Cylindrical_Coordinate();
	//渲染取点
	bool drawPointImage_Cylindrical();
	bool drawPointImage_polar();
	bool drawPointImage_Z_R();
	//获取圆柱图需要切割的线段
	QVector<QLineF> Getlines(QPointF p0,QVector<QRectF> RAxis,QVector<qreal> randlist);
	//获取接近点
	structureData::structpoint findApoint_Z_R(QPointF _curpostion);
	structureData::structpoint findApoint_Cylindrical(QPointF _curpoint);
	//计算距离
	float GetDistance(QPointF p1,QPointF p2);
	//绘制需要显示的信息
	void drawDisplayPoint(QPainter& painter, const QPointF& position, const QPointF& d);
public:
private:
	Coordinate_Dir m_Coordinate_Dir;
	QMap<int, QColor> color_tab;
};

#endif
