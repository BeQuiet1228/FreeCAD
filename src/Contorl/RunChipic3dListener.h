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
#include <memory>
/**
* @brief 消息结构类
*/
struct  Message
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
class RunChipic3d;
class  RunChipic3dListener:public QThread
{
private:
	RunChipic3dListener();
public:
	virtual ~RunChipic3dListener();

	void init();
	//发送消息
	bool sendMessage(UINT Msg, WPARAM wParam, LPARAM lParam);
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
public:
	static std::shared_ptr<RunChipic3dListener> runChipic3d(const std::string &m3dpath, const int &count,const std::string userName = "default_userName");
	static std::shared_ptr<RunChipic3dListener> runChipicFix(const std::string& m3dpath, const int& count, const std::string userName = "default_userName");
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
	//接收消息
	bool receiveMessage(Message &msg, const int &ms = 100);
	//测试发送消息是否成功
	bool testSendMessage();
	//gbk转utf8
	QString GBK2UTF8(const std::string &inStr);

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
	//chipic线程id
	DWORD mainThreadID;
	//chipic程序的process对象
	std::shared_ptr<RunChipic3d> runchipic3dPtr;
	//m3d路径
	std::string m3dPath;
	//chipic运行线程数
	int threadCount;
	//chipic所属用户的用户名，主要用于服务器有多个链接时判断chipic的归属
	std::string userName;
	//发送消息失败次数
	unsigned int sendMsgFailedCount;
protected:
	void run() override;

};

