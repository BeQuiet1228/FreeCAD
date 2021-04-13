#pragma once
#include "Renderer.h"
#include "ContourData.h"
#include "ContourRender.h"
#include <memory>
class ContourRenderPolar :public ContourRender{
public:
	ContourRenderPolar(std::shared_ptr<ContourData> data);
	~ContourRenderPolar();

public:
	bool drawImage() override;
	bool addListRang(std::list<Data::Rang> listRang) override;
	bool drawPointImage() override;
	bool setDefaultRang() override;
	void dataInit() override;
	//获取value范围
	Data::Rang getValueRange();
private:
	//绘制提示框
	void drawDisplayPoint(QPainter& painter, const QPointF& position, const ContourData::Grid& grid);


protected:
	void renderTile(const QwtScaleMap &xMap, const QwtScaleMap &yMap,
		const QRect &tile, QImage *) const;
	QImage renderImage(const QwtScaleMap &xMap, const QwtScaleMap &yMap, const QRectF &area, const QSize &imageSize)const override;

	QPointF transiton(const QwtScaleMap &xMap, const QwtScaleMap &yMap, const double& x, const double& y) const;

	QSize size;

};