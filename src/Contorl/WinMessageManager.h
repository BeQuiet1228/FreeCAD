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

struct Message;

class WinMessageManager
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
	DWORD mainThreadID;

private:
	//根据进程名获取所有线程的id
	int GetMainThreadIdFromName(LPCSTR szName, std::vector<DWORD>& threads);
	//获取主线程id
	void getMainThreadId(DWORD &_threadId);

};

