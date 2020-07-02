#pragma once
#include <QObject>
#include <Windows.h>
class Chipic:public QObject
{
	Q_OBJECT
public:
	Chipic();
	Chipic(DWORD threadID);
	~Chipic();

public:
	//运行按钮被点击
	void runButtonClicked();
	//暂停按钮被点击
	void pausButtonClicked();
	//刷新界面显示被点击
	void refreshButtonClicked();
	//定时器按钮被点击
	void timerButtonClicked();
public:
	//运行状态
	bool runState;
	//暂停状态
	bool pausState;
	//迭代次数、当前迭代次数
	int iterationCount, currentIteration;
	//粒子数目
	int particleCount;
	//消耗时间
	std::string usedTime;
	//总迭代时间、当前迭代时间
	std::string iterationTime, currentIterationTime;
	//线程id
	DWORD threadID;
public:
	void disposJsonMessage(const std::string& json);
	
signals:
	void stateUpdate();
};
