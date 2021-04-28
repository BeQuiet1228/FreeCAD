#include "ContourRenderStateGetter.h"
#include "ContourRender.h"
#include <QPen>
ContourRenderStateGetter::ContourRenderStateGetter(Plot* p)
	:plot(p)
{

}

/**
* @brief ContourRenderStateGetter::enabled 判断getter是否可用 主要判断plot中的主渲染器是否是等位图渲染器
* @return bool
*/
bool ContourRenderStateGetter::enabled()
{
	auto rd = getContourRender();
	if (rd)
		return true;
	return false;
}

/**
* @brief ContourRenderStateGetter::getDisplayMod 获取等位图的渲染模式
* @return ContourRenderStateGetter::DisplayMod
*/
ContourRenderStateGetter::DisplayMod ContourRenderStateGetter::getDisplayMod()
{
	DisplayMod ImageMod = IMAGE, ContourMod = CONTOUR;
	auto rd = getContourRender();
	if (!rd->testDisplayMode(QwtPlotSpectrogram::DisplayMode::ImageMode))
	{
		ImageMod = NONE;
	}

	if (!rd->testDisplayMode(QwtPlotSpectrogram::DisplayMode::ContourMode)) 
	{
		ContourMod = NONE;
	}

	return DisplayMod(ImageMod | ContourMod);
}

/**
* @brief ContourRenderStateGetter::setDisplayMode 设置等位图的渲染模式
* @param const DisplayMod & mod
* @return void
*/
void ContourRenderStateGetter::setDisplayMode(const DisplayMod& mod)
{
	if (!enabled())
		return;

	auto rd = getContourRender();
	//创建一个空的画笔备用
	QPen pen;
	pen.setStyle(Qt::NoPen);

	switch (mod)
	{
	default:
		break;
	case IMAGE:
		rd->setDisplayMode(QwtPlotSpectrogram::DisplayMode::ImageMode, true);
		rd->setDisplayMode(QwtPlotSpectrogram::DisplayMode::ContourMode, false);
		break;
	case CONTOUR:
		rd->setDisplayMode(QwtPlotSpectrogram::DisplayMode::ImageMode, false);
		rd->setDisplayMode(QwtPlotSpectrogram::DisplayMode::ContourMode, true);

		//这里设置一个空的画笔，渲染器会根据等值线等级创建对应颜色的画笔。
		//用不同的颜色渲染不同等级的等值线。
		rd->setDefaultContourPen(pen);
		break;
	case IMAGE_AND_CONTOUR:
		rd->setDisplayMode(QwtPlotSpectrogram::DisplayMode::ImageMode, true);
		rd->setDisplayMode(QwtPlotSpectrogram::DisplayMode::ContourMode, true);
		break;
	}
}

std::shared_ptr<ContourRender> ContourRenderStateGetter::getContourRender()
{
	auto rd = plot->mainRenderer;
	std::shared_ptr<ContourRender> crd = std::dynamic_pointer_cast<ContourRender>(rd);
	return crd;
}

