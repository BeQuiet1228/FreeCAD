#pragma once
#include <QObject>
#include <Windows.h>
#include <QWidget>
#include <QLabel>
#include <QPushButton>
#include "RunChipic3dListener.h"
#include "HintDailog.h"
#include <QTimer>
class  Chipic:public QObject
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
	//发送关闭消息
	void sendCloseChipicMessage();
	//打开log文件
	void openLogFile();
	//获取运行结果数据路径
	std::string getResultPath();
	//设置是否为auto运行模式
	void setIsAuto(const bool& a){
		this->isAuto = a;
	}
	bool getIsAuto(){
		return this->isAuto;
	}
	//设置是否有数据更新
	void setIsUpdate(const bool& b){
		this->isUpdate = b;
	}
	//获取是否有数据更新
	bool getIsUpdate(){
		return this->isUpdate;
	}
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
	//处理chipic关闭消息
	bool disposChipicCloseMessage(const std::string& json);
	//处理发送消息中的暂停消息
	bool disposChipicSendMessagePauseMessage(const Message& msg);
	//处理计算完成消息
	bool disposChipicFinished(const Message& msg);
	//处理chipic输出图繁忙消息
	bool disposChipicBusy(const Message& msg);
	//处理chipic关闭消息
	bool disposChipicCloseWinMessage(const Message& msg);
	//重启状态检测定时器
	void restartTimeoutTimer();
public:
	//是否为等待关闭的状态
	bool isWaitclose;
	//运行状态
	bool runState;
	//暂停状态
	bool pausState;
	//定时器状态
	bool timerSate;
	/*
	* 2023.9.8修改了chipic关闭的逻辑，
	* 现在以任何方式关闭程序都需要程序回执关闭信息才能真正的关闭
	* 所以需要先记录运行状态，然后再程序关闭后处理文件操作 
	*/
	//是否已完成计算
	bool chipicIsFinish;
	/*
	* 关闭消息可能重复发送，记录处理标志，如果已经处理过了就不再处理了
	*/
	bool isDisposCloseMessage;
	//迭代次数、当前迭代次数
	int iterationCount, currentIteration;
	//粒子数目
	int particleCount;
	//总迭代时间的整数部分和小数部分
	float iterationTime = 0;
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
	//定时检查内核是否还在运行
	QTimer * timer;
public:
	void disposJsonMessage(const std::string& json);
	
Q_SIGNALS:
	void stateUpdate(DWORD);
	//计算完成信号
	void workFinished();
	//解析完成信号
	void analysisFinished();
	//输出新的结果图
	void newResultFile(unsigned long);
	//输出结构图
	void outputStructFile(unsigned long);
public Q_SLOTS:
	void buttonClicked(int clickType);
	void timerOut();

private:
	//是否运行模式为auto
	bool isAuto = false;
	//数据是否有更新
	bool isUpdate = false;
};
