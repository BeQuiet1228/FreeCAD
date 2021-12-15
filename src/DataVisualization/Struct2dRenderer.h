#pragma once
#ifndef _STRUCT_2D_RENDERER_H_
#define _STRUCT_2D_RENDERER_H_
#include "Renderer.h"
#include "Struct2dData.h"
#include <QMap>
#include <QColor>
#include <QPen>

namespace DV {
	struct linepen
	{
		QPen pen;
		QLineF line;
	};
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
		virtual void loadconfig() override;
	public:
	private:
		QVector<QLineF> Getlines(std::vector<QPointF> points);
		void drawDisplayPoint(QPainter& painter, const QPointF& position, const QPointF& d);
		void transitionLineF(QLineF& line, const float& xScale, const float& yScale, const Data::Rang& xr, const Data::Rang& yr);
		void DrawLine(QPainter& painter, QLineF& line, int mPorper);
		void transitionPoint(QPointF& point, const float& xScale, const Data::Rang& xr, const float& yScale, const Data::Rang& yr)
		{
			point.setX(transitionX(point.x(), xScale, xr));
			point.setY(transitionY(point.y(), yScale, yr));
		}
		float transitionX(const float& x, const float& xScale, const Data::Rang& xr)
		{
			return (x - xr.min) * xScale;
		}
		float transitionY(const float& y, const float& yScale, const Data::Rang& yr)
		{
			return (y - yr.min) * yScale;
		}
		QPointF GetApos(QPointF& A_pos);
		QVector<QLineF> GetCurLine_x();
		QVector<QLineF> GetCutLine_y();
		QImage createImg(std::map<int, std::vector<QPointF>>::iterator& it,
			Data::Rang& xr,
			Data::Rang& yr,
			float& xScale,
			float& yScale);
		void clipImg(QImage& img, QPolygonF& polyon);
		void drawPolygons(
			QPainter& painter, std::vector<QPointF>& points);
	private:
		QMap<int, QColor> color_tab;
		QMap<int, QColor> color_pen;
		std::map<unsigned __int64, QPixmap> pixmap;
		bool isAA;
	};
}
#endif