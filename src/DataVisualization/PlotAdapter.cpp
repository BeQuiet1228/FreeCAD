#include "PlotAdapter.h"
#include "Renderer.h"
#include "RenderTask.h"
#include "RenderThreadManager.h"
#include "Plot.h"
#include "C_encoding.h"
PlotAdapter::PlotAdapter()
{
	renderManager.reset(new RenderThreadManager);
}

PlotAdapter::~PlotAdapter()
{

}

void PlotAdapter::reRender(const QSize& size)
{
	//创建坐标轴网格渲染任务
	//creatGridRenderTask();

	if (mainRenderer)
	{
		std::cerr << "reRender" << std::endl;
		mainRenderer->setSize(size);
		RenderTask task(mainRenderer);
		renderManager->addTask(task);
	}
	unsigned int rank = Canvas::SUB_RENDER_START_RANK;
	for (auto rdIter = subRenderers.begin(); rdIter != subRenderers.end(); rdIter++)
	{
		(*rdIter)->setSize(size);
		RenderTask task(*rdIter, RenderTask::MAP, rank);
		renderManager->addTask(task);
		rank++;
	}

	renderManager->start();
}

/**
* @brief PlotAdapter::addSubRenderer 添加附属渲染器 渲染一些附加内容，这些内容会自动覆盖到主渲染器渲染的内容之上（层级按照添加顺序覆盖）。
* @param const std::shared_ptr<Renderer> & rd
* @return void
*/
void PlotAdapter::addSubRenderer(const std::shared_ptr<Renderer>& rd)
{
	rd->dataInit();
	rd->loadconfig();

	if (mainRenderer)
	{
		Data::Rang xr, yr;
		xr = mainRenderer->getXRang();
		yr = mainRenderer->getYRang();
		rd->setXRang(xr);
		rd->setYRang(yr);
	}
	else {
		//rd->setDefaultRang(canvas->size());
		rd->setDefaultRang();
	}

	subRenderers.push_back(rd);
}

void PlotAdapter::setMainRenderer(const std::shared_ptr<Renderer>& rd)
{
	//初始化数据
	rd->loadconfig();
	rd->dataInit();
	rd->setDefaultRang();
	mainRenderer = rd;
	autoMaxRender();
}

/**
* @brief PlotAdapter::addRenderer 添加渲染器 这个操作会清空之前的渲染器，第一个渲染器默认为主渲染器。
* @param const std::list<std::shared_ptr<Renderer>> & listRender
* @return void
*/
void PlotAdapter::addRenderer(const std::list<std::shared_ptr<Renderer>>& listRender)
{
	if (listRender.size() < 1)
		return;
	clearSubRenderer();
	auto iter = listRender.begin();
	auto mRedner = *iter;
	iter++;
	for (; iter != listRender.end(); iter++)
	{
		addSubRenderer(*iter);
	}
	setMainRenderer(mRedner);
}

void PlotAdapter::autoMaxRender()
{
	if (!mainRenderer)
		return;

	//获取渲染器中最大的默认渲染范围
	//mainRenderer->setDefaultRang(canvas->size());
	mainRenderer->setDefaultRang();
	auto xr = mainRenderer->getXRang();
	auto yr = mainRenderer->getYRang();

	for (auto rder = subRenderers.begin(); rder != subRenderers.end(); rder++)
	{
		(*rder)->setDefaultRang();
		Data::Rang sxr = (*rder)->getXRang();
		Data::Rang syr = (*rder)->getYRang();

		xr.max = sxr.max > xr.max ? sxr.max : xr.max;
		xr.min = sxr.min < xr.min ? sxr.min : xr.min;

		yr.max = syr.max > yr.max ? syr.max : yr.max;
		yr.min = syr.min < yr.min ? syr.min : yr.min;
	}

	setRenderRange(xr.min, xr.max, yr.min, yr.max);
}

void PlotAdapter::updateGridLine()
{
	//creatGridRenderTask();
	//renderManager->start();
}

void PlotAdapter::findPointRender(const float& x, const float& y)
{
	//这里的size应该跟之前渲染的size没有区别，所以应该不用重新设置
	//mainRenderer->setSize(canvas->size());
	mainRenderer->setFindPosition(QPointF(x, y));
	RenderTask task(mainRenderer,RenderTask::FIND_POINT, Canvas::FIND_POINT_RENDER_RANK);
	renderManager->addTask(task);
	renderManager->start();
}

Data::Rang PlotAdapter::getXRange()
{
	if (!mainRenderer)
		return Data::Rang();
	return mainRenderer->getXRang();
}

Data::Rang PlotAdapter::getYRange()
{
	if (!mainRenderer)
		return Data::Rang();
	return mainRenderer->getYRang();
}

void PlotAdapter::initPlot(Plot& plot)
{
	Plot::connect(renderManager.get(), SIGNAL(allWorkFinished()), &plot, SLOT(renderFinished()));
}

std::list<QAction*> PlotAdapter::getActions()
{
	return std::list<QAction*>();
}

std::list<CanvasItem> PlotAdapter::takeResut()
{
	return renderManager->takeResut();
}

QString PlotAdapter::getInformationTitile()
{
	if (!mainRenderer)
		return "";
	return GetEncodingstr(mainRenderer->getInformationTitile().c_str(), ENCODING_GB2312);
}

void PlotAdapter::setRenderRange(const float& xMin, const float xMax, const float& yMin, const float& yMax)
{
	Data::Rang xr(xMin, xMax), yr(yMin, yMax);
	mainRenderer->setXRang(xr);
	mainRenderer->setYRang(yr);
	//设置其他渲染器的范围
	for (auto iter = subRenderers.begin(); iter != subRenderers.end(); iter++)
	{
		(*iter)->setYRang(yr);
		(*iter)->setXRang(xr);
	}
}

void PlotAdapter::setRenderXRange(const float& min, const float& max)
{
	if (!mainRenderer)
		return;
	auto yr = mainRenderer->getYRang();
	setRenderRange(min, max, yr.min, yr.max);
}

void PlotAdapter::setRenderYRange(const float& min, const float& max)
{
	if (!mainRenderer)
		return;
	auto xr = mainRenderer->getXRang();
	setRenderRange(xr.min, xr.max, min, max);
}

void PlotAdapter::loadConfig()
{
	if (!mainRenderer)
		return;
	mainRenderer->loadconfig();
	for (auto iter = subRenderers.begin(); iter != subRenderers.end(); iter++)
		(*iter)->loadconfig();
}

