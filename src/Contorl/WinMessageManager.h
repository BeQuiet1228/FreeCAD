#pragma once
#undef   UNICODE
#include <windows.h>
#include <cstdio>
#include <process.h>
#include <iostream>
#include <tlhelp32.h>
#include <tchar.h>
#include <stdio.h>
#include <io.h>
#include <direct.h>
#include <fstream>
#include <vector>
#include <process.h>
#include <string.h>
#include <iostream>
#include <qstring.h>
#include <QThread>
#include <mutex>
#include <deque>
/**
* @brief 消息结构类
*/
struct Message
{
	Message(UINT msg = WM_USER, WPARAM wParam = 0, LPARAM lParam = 0) {
		this->Msg = msg;
		this->wParam = wParam;
		this->lParam = lParam;
		this->text = "";
		this->threadId = 0;
	}
	//消息类型
	UINT Msg;
	//短参数
	WPARAM wParam;
	//长参数
	LPARAM lParam;
	//文本信息
	std::string text;
	//线程id
	DWORD threadId;

};

class WinMessageManager:public QThread
{
public:
	WinMessageManager();
	virtual ~WinMessageManager();


	void init();
	//发送消息
	bool sendMessage(UINT Msg, WPARAM wParam, LPARAM lParam);
	//接收消息
    bool receiveMessage(Message &msg,const int &ms = 100);
    //测试发送消息是否成功
    bool testSendMessage();
	//chipic线程id
	DWORD mainThreadID;
	//添加发送消息
	void sendMessage(const Message& msg);
	//开启工作线程
	void workThreadOn();
	//关闭工作线程
	void workThreadOff();
	//获取线程ID
	DWORD getThreadId();
	//设置线程id
	void setThreadId(const DWORD& id);
private:
	//根据进程名获取所有线程的id
	int GetMainThreadIdFromName(LPCSTR szName, std::vector<DWORD>& threads);
	//获取主线程id
	void getMainThreadId(DWORD &_threadId);
	//获取消息队列中的消息
	bool getMessageForDeque(Message& msg);
	//设置工作线程循环标志
	void setWorkThreadFlag(const bool& flag);
	//获取工作线程循环标志
	bool getWorkThreadFlag();
	//接收字符串消息
	void receiveStringMessage(Message &msg);
private:
	//消息队列
	std::deque<Message> sendMessageDeque;
	//消息队列锁
	std::mutex sendMessageDequeMutex;
	//工作线程循环锁
	std::mutex workThreadMutex;
	//工作线程循环标志
	bool workThreadFlag;
	//线程id锁
	std::mutex threadIdMutex;

protected:
	void run() override;

};

