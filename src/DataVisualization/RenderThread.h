#pragma once
#include <QThread>
#include <QObject>
#include "Canvas.h"
#include <mutex>
#include "RenderTask.h"
#include <list>
class Renderer;
class RenderThread :public QThread{
	Q_OBJECT
public:
	RenderThread(QObject* parent = nullptr);
	~RenderThread();

public:
	//获取完成标志
	bool getFinishedFlag(){
		std::lock_guard<std::mutex> am(finishedFlagMutex);
		return finishedFlag;
	}
	//操作渲染任务 非线程安全
	void addTask(const RenderTask& task){
		this->tasks.push_back(task);
	}
	void addTask(const std::list<RenderTask>& tasks);
private:
	//执行渲染图任务
	void renderMap(RenderTask& task);
	//执行取点任务
	void findPoint(RenderTask& task);
	//设置完成标值
	void setFinishedFlag(const bool& flag){
		std::lock_guard<std::mutex> am(finishedFlagMutex);
		this->finishedFlag = flag;
	}
private:
	//是否运行完成
	bool  finishedFlag;
	std::mutex finishedFlagMutex;
	//渲染任务 不提供线程安全操作函数！！！！！！！！！
	std::list<RenderTask> tasks;
protected:
	void run() override;

Q_SIGNALS:
	void renderFinished(CanvasItem item);
	void threadFinished();

};