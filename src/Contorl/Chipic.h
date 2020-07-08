#pragma once
#include <QObject>
#include <Windows.h>
#include <QWidget>
#include <QLabel>
#include <QPushButton>
#include "WinMessageManager.h"
#include "HintDailog.h"
class Chipic:public QObject
{
	class Time{
	public:
		int hour = 0;
		int minute = 0;
		int second = 0;
		//生成字符串
		std::string toString(){
			return std::to_string(hour) + ":" +
				std::to_string(minute) + ":" +
				std::to_string(second);
		}
	};

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
private:
	//处理迭代步数消息
	bool disposIterationCountMessage(const Message& msg);
	//处理cpu消耗时间消息
	bool disposUsedTimeMessage(const Message& msg);
	//处理粒子数目消息
	bool disposParticleMessage(const Message& msg);
	//处理迭代时间消息
	bool disposeIterationTimeMessage(const Message& msg);
	//处理定时器状态消息
	bool disposeChipicTimerState(const Message& msg);
	//处理chipic暂停状态消息
	bool disposeChipicIsPause(const Message& msg);
	//处理提示信息消息
	bool disposHintMessage(const Message& msg);
public:
	//运行状态
	bool runState;
	//暂停状态
	bool pausState;
	//定时器状态
	bool timerSate;
	//迭代次数、当前迭代次数
	int iterationCount, currentIteration;
	//粒子数目
	int particleCount;
	//消耗时间
	std::string iterationTimeInt,iterationTimeFloat;
	//总迭代时间、当前迭代时间
	Time UsedTime, currentUsedTime;
	//线程id
	DWORD threadID;
	//计算程序，提示信息
	std::string titile,titleNumber;
	//提示框
	HintDailog hintDailog;
public:
	void disposJsonMessage(const std::string& json);
	
signals:
	void stateUpdate(DWORD);

public slots:
	void buttonClicked();
};
