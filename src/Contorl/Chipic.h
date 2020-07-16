#pragma once
#include <QObject>
#include <Windows.h>
#include <QWidget>
#include <QLabel>
#include <QPushButton>
#include "RunChipic3dListener.h"
#include "HintDailog.h"
#include "ContorlConfig.hpp"
class CONTROL_EXPORT Chipic:public QObject
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
	Chipic(DWORD threadID = 0);
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
	//初始化变量
	void init();
	//发送消息
	void sendMessage(const UINT& type, const WPARAM& wParam, const LPARAM& lParam,const DWORD& thradId = 0);
	//关闭chipic
	void closeChipic();
	//打开log文件
	void openLogFile();
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
	//处理结构图消息
	bool disposeStructMapMessage(const Message& msg);
	//处理结果图消息
	bool disposResultMapMessage(const Message& msg);
	//按照固定格式生成文件路径
	std::string makePath(const std::string& fileName);
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
	//总迭代时间的整数部分和小数部分
	std::string iterationTimeInt,iterationTimeFloat;
	//预估消耗时间、当前消耗时间
	Time UsedTime, currentUsedTime;
	//线程id
	DWORD threadID;
	//计算程序，提示信息
	std::string title,titleStr,titleNumber;
	//提示框
	HintDailog hintDailog;
	//线程数
	int threadCount;
	//文件路径
	std::string m3dPath;
public:
	void disposJsonMessage(const std::string& json);
	
Q_SIGNALS:
	void stateUpdate(DWORD);

public Q_SLOTS:
	void buttonClicked(int clickType);
};
