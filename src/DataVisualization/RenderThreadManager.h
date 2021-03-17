#pragma once
#include <list>
#include <memory.h>
#include "RenderTask.h"
#include "Canvas.h"
#include <QObject>
class RenderThread;
class RenderThreadManager:public QObject{
	Q_OBJECT
	using RenderThreadPtr = std::shared_ptr<RenderThread>;
public:
	enum RunMode {
		THREAD_ONCE = 0,
		THREAD_MULTIPLE
	};
public:
	RenderThreadManager();
	~RenderThreadManager();

public:
	//开始运行
	void start();
	//停止
	void stop();
	//获取结果
	std::list<CanvasItem> takeResut();
	//添加渲染任务
	void addTask(const RenderTask& task){
		this->tasks.push_back(task);
	}
	//设置运行模式
	void setRunMode(const RunMode& mode){
		this->runMode = mode;
	}
	RunMode getRunMode(){
		return runMode;
	}
private:
	//线程集
	std::list<RenderThreadPtr> threads;
	//任务集
	std::list<RenderTask> tasks;
	//运行模式
	RunMode runMode;
	//结果集
	std::list<CanvasItem> results;

private:
	void clearFinishedThread();
public Q_SLOTS:
	//渲染完成槽
	void renderFinished(CanvasItem item);
	//完成运行槽
	void threadWorkFinished();
};