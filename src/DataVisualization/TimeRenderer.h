#pragma once
#include <Renderer.h>
#include "TimeData.h"
#include <QPainter>

namespace DV {
	class TimeRenderer :public Renderer {
	public:
		TimeRenderer(std::shared_ptr<TimeData> data);
		~TimeRenderer();
	public:
		//渲染
		virtual bool drawImage() override;
		virtual bool addListRang(std::list<Data::Rang> listRang) override;
		virtual bool drawPointImage() override;
		virtual bool setDefaultRang() override;
		virtual void dataInit() override;
		//加载配置
		virtual void loadconfig() override;
		//在原始数据中寻找点
		virtual QPointF findPoint(const QPointF& point);
		virtual QPointF findPoint(const QPointF& point, std::shared_ptr<TimeData> timeData);
		double getDistance(const QPointF& point1, const QPointF& point2);
		//设置画笔颜色
		void setColor(const QColor& color);
	protected:
		//将数据坐标转换为图片上的坐标
		float transitionX(const float& x, const float& xScale, const Data::Rang& xr);
		float transitionY(const float& y, const float& yScale, const Data::Rang& yr);
		void transitionPoint(QPointF& point);
		void transitionPoint(QPointF& point, const float& xScale, const Data::Rang& xr, const float& yScale, Data::Rang& yr);
		//绘制显示信息---目前没有使用，重新实现在Renderer中的通用方法--暂时保留
		void drawDisplayPoint(QPainter& painter, const QPointF& position, const QPointF& d);
	protected:
		//新增--画笔大小,颜色
		unsigned __int32 pensize;
		QColor penColor;
		bool isAA;
	};
};
