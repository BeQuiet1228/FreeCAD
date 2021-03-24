#include "ParticleRenderer.h"
#include "ParticleData.h"
#include <QPen>
#include <QPainter>
ParticleRenderer::ParticleRenderer(std::shared_ptr<ParticleData> data)
	:Renderer(std::dynamic_pointer_cast<Data>(data))
{

}

ParticleRenderer::~ParticleRenderer()
{

}

bool ParticleRenderer::drawImage()
{
	//获取坐标缩放比例
	float yScale(0.0), xScale(0.0);
	if (!getTransitionScale(xScale, yScale))
		return false;
	std::shared_ptr<ParticleData> d = std::dynamic_pointer_cast<ParticleData>(data);
	if (!d)
	{
#if LOG
		std::cerr << "ParticleRenderer::drawImage() data dynamic cast failed!" << std::endl;
#endif
		return false;
	}

	//获取起始点,因为图表的刻度不一定是从零开始的。
	auto xr = getXRang();
	auto yr = getYRang();

	//获取数据索引的范围
	int startIndex(0), endIndex(0);
	startIndex = d->findIndexFromXValueL(xr.min);
	endIndex = d->findIndexFromXValueL(xr.max);

	//新建画布 画笔
	QImage img(getSize(), QImage::Format_ARGB32);
	img.fill(qRgba(0, 0, 0, 0));
	QPen pen(Qt::red);
	pen.setWidth(1);
	QPainter painter(&img);
	painter.setPen(pen);

	ParticleData::Particle p;
	for (int index = startIndex + 1; index < endIndex; index++)
	{
		p = d->particles.at(index);
		p.x = transitionDataToScreen(p.x, xScale, xr);
		p.y = transitionDataToScreen(p.y, yScale, yr);
		painter.drawPoint(p.x,p.y);
	}
	//因为qpainter的屏幕坐标系原点在左上角，所以需要翻转图片才能得到我们想要的结果
	auto nImg = img.mirrored(false, true);
	setImage(nImg);

}

/**
* @brief ParticleRenderer::setDefaultRang 设置默认的渲染范围
* @return bool
*/
bool ParticleRenderer::setDefaultRang()
{
	auto particleData = std::dynamic_pointer_cast<ParticleData>(data);
	setXRang(particleData->getXRang());
	setYRang(particleData->getYRang());
	return true;
}

void ParticleRenderer::dataInit()
{
	Renderer::dataInit();
	auto pData = std::dynamic_pointer_cast<ParticleData>(data);
	if (!pData)
		return;
	pData->loadPoint();
}

