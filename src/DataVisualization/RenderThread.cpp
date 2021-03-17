#include "RenderThread.h"
#include "Renderer.h"
RenderThread::RenderThread(QObject* parent /*= nullptr*/)
	:QThread(parent), finishedFlag(true)
{

}

RenderThread::~RenderThread()
{
	QThread::quit();
	QThread::wait();
}

/**
* @brief RenderThread::addTask 添加渲染任务 非线程安全
* @param const std::list<RenderTask> & tasks
* @return void
*/
void RenderThread::addTask(const std::list<RenderTask>& tasks)
{
	for (auto i = tasks.begin(); i != tasks.end(); i++)
	{
		this->tasks.push_back(*i);
	}
}

/**
* @brief RenderThread::renderMap 渲染图表
* @param const RenderTask & task
* @return void
*/
void RenderThread::renderMap(RenderTask& task)
{
	auto renderer = task.getRenderer();

	renderer->drawPixmap();
	CanvasItem item;
	item.rank = task.rank;
	item.setPixmap(renderer->getPixmap());

	Q_EMIT renderFinished(item);
}

/**
* @brief RenderThread::findPoint 取点
* @param const RenderTask & task
* @return void
*/
void RenderThread::findPoint(RenderTask& task)
{
	auto renderer = task.getRenderer();

	renderer->drawPointPixmap();
	CanvasItem item;
	item.rank = task.rank;
	item.setPixmap(renderer->getPixmap());

	Q_EMIT renderFinished(item);
}

void RenderThread::run()
{
	setFinishedFlag(false);

	for (auto taskIter = tasks.begin(); taskIter != tasks.end(); taskIter++){

		switch (taskIter->getTyepe()){
		case RenderTask::MAP:
			renderMap(*taskIter);
			break;

		case RenderTask::FIND_POINT:
			findPoint(*taskIter);
			break;

		default:
			continue;
		}
	}
	setFinishedFlag(true);
	Q_EMIT threadFinished();
}


#include "moc_RenderThread.cpp"