#include "RenderThreadManager.h"
#include <RenderThread.h>
#include <iostream>
RenderThreadManager::RenderThreadManager()
	:runMode(THREAD_ONCE)
{

}

RenderThreadManager::~RenderThreadManager()
{

}

/**
* @brief RenderThreadManager::start 开始处理当前的tasks之前，会先调用stop清理掉未完成的任务，如果有。。。
* @return void
*/
void RenderThreadManager::start()
{
	stop();
	//暂时实现一个线程渲染
	if (runMode != THREAD_ONCE)
		return;
	
	std::shared_ptr<RenderThread> th(new RenderThread);
	threads.push_back(th);
	th->addTask(this->tasks);
	tasks.clear();
	connect(th.get(), SIGNAL(renderFinished(CanvasItem)), this, SLOT(renderFinished(CanvasItem)));
	connect(th.get(), SIGNAL(threadFinished()), this, SLOT(threadWorkFinished()));
	th->start();
}

void RenderThreadManager::stop()
{
	for (auto i = threads.begin(); i != threads.end(); i++)
	{
		disconnect(i->get(), SIGNAL(renderFinished(CanvasItem)), this, SLOT(renderFinished(CanvasItem)));
		disconnect(i->get(), SIGNAL(threadFinished()), this, SLOT(threadWorkFinished()));
		i = threads.erase(i);
	}
}

/**
* @brief RenderThreadManager::takeResut 拿走结果 
* @return std::list<CanvasItem>
*/
std::list<CanvasItem> RenderThreadManager::takeResut()
{
	std::list<CanvasItem> re;
	re.splice(re.begin(), results);
	re.sort();
	return re;
}

/**
* @brief RenderThreadManager::clearFinishedThread 清理已完成任务的线程资源
* @return void
*/
void RenderThreadManager::clearFinishedThread()
{
	for (auto i = threads.begin(); i != threads.end(); i++)
	{
		if (!(*i)->getFinishedFlag())
			continue;
		disconnect(i->get(),SIGNAL(renderFinished(CanvasItem)), this, SLOT(renderFinished(CanvasItem)));
		disconnect(i->get(), SIGNAL(finished()), this, SLOT(threadWorkFinished()));
		i = threads.erase(i);
	}
}

void RenderThreadManager::renderFinished(CanvasItem item)
{
	results.push_back(item);
}

/**
* @brief RenderThreadManager::threadWorkFinished 线程完成槽 主要用于释放已完成工作的线程资源
* @return void
*/
void RenderThreadManager::threadWorkFinished()
{
	clearFinishedThread();
	auto re = takeResut();
	for (auto i = re.begin(); i != re.end(); i++)
	{
		std::cerr << i->rank << std::endl;
	}
}

#include "moc_RenderThreadManager.cpp"