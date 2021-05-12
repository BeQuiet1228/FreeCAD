#pragma  once
#include "Renderer.h"
#include <memory>
#include "ParticleData.h"
#include <QPointF>
#include <QColor>
class ParticleRenderer :public Renderer{
public:
	ParticleRenderer(std::shared_ptr<ParticleData> data);
	~ParticleRenderer();
public:
	bool drawImage() override;
	bool setDefaultRang() override;
	void dataInit() override;
	bool drawPointImage() override;
	//新增加
	virtual void loadconfig() override;
	virtual bool setDefaultRang(QSize&) override;
private:
	ParticleData::Particle findParticle(const QPointF& point);
	//绘制显示信息，暂时保留，未使用了
	void drawDisplayPoint(QPainter& painter, const QPointF& position, const QPointF& d);
	//将数据转换为屏幕坐标
	QPointF transitionPoint(const QPointF& point);
private:
	QColor particleColor;
	int particleSize;
	bool isAA;
};