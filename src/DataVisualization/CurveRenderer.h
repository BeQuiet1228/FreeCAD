#pragma once
#include "TimeRenderer.h"
#include "CurveData.h"
#include <memory>

namespace DV {
	class CurveRenderer :public TimeRenderer{
	public:
		CurveRenderer(const std::shared_ptr<CurveData> data);
		~CurveRenderer();
	public:
		virtual void dataInit() override;
		virtual bool drawImage() override;
		virtual bool drawPointImage() override;
		//get set
		void setPointColor(const QColor& color);
		QColor getPointColor();
		QPointF findPoint(const QPointF& point,int &index);
	private:
		QColor pointColor;
	};

}