#include "TimeMultiplePlotAdapter.h"
#include "TimeRenderer.h"
#include "RenderThreadManager.h"
#include <QtConcurrentRun>
#include <QFuture>
#include <QApplication>

QPointF findPoint(const QPointF& point, std::shared_ptr<DV::TimeRenderer> timeRender)
{
	return timeRender->findPoint(point);
}

DV::TimeMultiplePlotAdapter::TimeMultiplePlotAdapter(std::list<std::shared_ptr<Renderer>> renders)
	:TimePlotAdapter(renders)
{

}

/**
* 实现多个时间图同时显示时的点查找功能
* @brief DV::TimeMultiplePlotAdapter::findPointRender
* @param const float & x
* @param const float & y
* @return void
*/
void DV::TimeMultiplePlotAdapter::findPointRender(const float& x, const float& y)
{
	std::vector<QFuture<QPointF>> futuers;
	std::vector<std::shared_ptr<TimeRenderer>> renderers;

	//搜集所有的时间图渲染器
	{
		auto rd = std::dynamic_pointer_cast<TimeRenderer>(mainRenderer);
		if (rd)
			renderers.push_back(rd);
	}
	for (auto iter = subRenderers.begin(); iter != subRenderers.end(); iter++)
	{
		auto rd = std::dynamic_pointer_cast<TimeRenderer>(*iter);
		if (rd)
			renderers.push_back(rd);
	}

	//获取每张图中最近的点
	QPointF point(x, y);
	for (auto iter = renderers.begin(); iter != renderers.end(); iter++)
	{
		QFuture<QPointF> futuer = QtConcurrent::run(findPoint, point, *iter);
	}
	bool isFinished = false;
	while (!isFinished)
	{
		//执行一次事件循环
		QApplication::processEvents();
		//查看是否所有线程都完成
		isFinished = true;
		for (auto iter = futuers.begin(); iter != futuers.end(); iter++)
		{
			isFinished = isFinished && iter->isFinished();
		}
	}
	
	//获取离点击坐标最近的点
	int minIndex = 0;
	double minDistance = 999999999;
	//如果只有一个渲染器，那么默认为0

	for (int i = 1; i < renderers.size(); i++)
	{
		double distance = renderers[i]->getDistance(futuers[i].result(), point);
		if (distance < minDistance)
		{
			minDistance = distance;
			minIndex = i;
		}
	}

	renderers[minIndex]->setFindPosition(QPointF(x, y));
	RenderTask task(renderers[minIndex], RenderTask::FIND_POINT, Canvas::FIND_POINT_RENDER_RANK);
	renderManager->addTask(task);
	renderManager->start();
}

