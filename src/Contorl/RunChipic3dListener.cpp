#include "RunChipic3dListener.h"
#include "MessageTransition.h"
#include "JsonMessageGetter.h"
#include "runchipic3d.h"
#include <QByteArray>
#include <QString>
RunChipic3dListener::RunChipic3dListener()
{
	workThreadFlag = false;
	mainThreadID = 0;
	sendMsgFailedCount = 0;
}


RunChipic3dListener::~RunChipic3dListener()
{
	workThreadOff();
}
/**
* @brief RunChipic3dListener::GetMainThreadIdFromName 根据进程名称获取进程下所有线程id
* @param szName 进程名
* @param threads 线程id容器
* @return  进程中线程的数量
*/
int RunChipic3dListener::GetMainThreadIdFromName(LPCSTR szName, std::vector<DWORD>& threads)
{
	//std::vector<DWORD> idThread;         // 进程ID
	std::vector<DWORD> idProcess;        // 主线程ID

	// 获取进程ID
	PROCESSENTRY32 pe;      // 进程信息
	pe.dwSize = sizeof(PROCESSENTRY32);
	HANDLE hSnapshot = CreateToolhelp32Snapshot(0x02, 0); // 获取系统进程列表
	if (Process32First(hSnapshot, &pe))      // 返回系统中第一个进程的信息
	{
		do
		{
			if (0 == _stricmp(pe.szExeFile, szName)) // 不区分大小写比较
			{
				idProcess.push_back(pe.th32ProcessID);
				//break;
			}
		} while (Process32Next(hSnapshot, &pe));      // 下一个进程
	}
	CloseHandle(hSnapshot); // 删除快照
	if (idProcess.size() == 0)
	{
		return 0;
	}

	// 获取进程的主线程ID
	THREADENTRY32 te;       // 线程信息
	te.dwSize = sizeof(THREADENTRY32);
	HANDLE hSnapshot2 = CreateToolhelp32Snapshot(0x04, 0); // 系统所有线程快照
	if (Thread32First(hSnapshot2, &te))       // 第一个线程
	{
		do
		{
			for (auto itr = idProcess.begin(); itr != idProcess.end(); ++itr)
			{
				if (*itr == te.th32OwnerProcessID)      // 认为找到的第一个该进程的线程为主线程
				{
					threads.push_back(te.th32ThreadID);
					idProcess.erase(itr);
					break;
				}
			}
		} while (Thread32Next(hSnapshot2, &te));           // 下一个线程
	}
	CloseHandle(hSnapshot2); // 删除快照
	return threads.size();
}
/**
* @brief RunChipic3dListener::getMainThreadId 获取主线程id
* @param threadId 主线程id
*/
void RunChipic3dListener::getMainThreadId(DWORD &_threadId) {
	std::vector<DWORD>threads;
	//std::cerr << "Wait For Fortran Program Chipic3d.exe ..." << std::endl;
	_threadId = 0;
	while (_threadId == 0)
	{
		Sleep(1000);
		threads.clear();
		//通过进程名查找线程Id
		int ret = GetMainThreadIdFromName("Chipic3d.exe", threads);
#ifdef MY_DEBUG
		if (ret == 0)
		{
			std::cerr << "not found chipic3d thread" << std::endl;
		}
#endif
		//发送本线程的Id
		for (size_t i = 0; i < threads.size(); i++)
		{
			auto b = ::PostThreadMessage(threads[i], WM_USER + 10, GetCurrentThreadId(), 1);

#ifdef MY_DEBUG
			if (!b)
			{
				auto er = ::GetLastError();
				std::cerr << "message send erro,thread ID:" << threads[i] << "。windows erro code:" << er << std::endl;

			}
#endif 
			Sleep(100);
			MSG  msg;
			if (::PeekMessage(&msg, NULL, 0, 0, PM_REMOVE))
			{
				if (msg.message == WM_USER + 20)
				{
                    _threadId = (DWORD)msg.wParam;	
					break;
				}
			}
		}
		//如果线程已即将被关闭，那么不在寻找线程id
		//解决长时间没有找到chipic应用程序导致界面,导致的this内存释放不掉的bug
		if (!getWorkThreadFlag())
			return;
	}
}

/**
* @brief RunChipic3dListener::getMessageForDeque 从消息队列中获取要发送的消息
* @param Message & msg
* @return bool 如果队列中没有消息则返回false
*/
bool RunChipic3dListener::getMessageForDeque(Message& msg)
{
	sendMessageDequeMutex.lock();
	if (sendMessageDeque.empty())
	{
		sendMessageDequeMutex.unlock();
		return false;
	}
	msg = sendMessageDeque.front();
	sendMessageDeque.pop_front();
	sendMessageDequeMutex.unlock();

	return true;
}

/**
* @brief RunChipic3dListener::workThreadOn 开启工作线程循环,线程阻塞，直到获取到计算程序线程id
* @return void
*/
void RunChipic3dListener::workThreadOn()
{
	setWorkThreadFlag(true);
	this->start();
}

void RunChipic3dListener::workThreadOff()
{
	sendMessage(0, 0, 0);
	setWorkThreadFlag(false);
	Sleep(10);
	this->wait();
}

/**
* @brief RunChipic3dListener::getThreadId 获取线程id
* @return DWORD
*/
DWORD RunChipic3dListener::getThreadId()
{
	threadIdMutex.lock();
	DWORD id = mainThreadID;
	threadIdMutex.unlock();

	return id;
}

/**
* @brief RunChipic3dListener::setThreadId 设置线程id
* @param const DWORD & id
* @return void
*/
void RunChipic3dListener::setThreadId(const DWORD& id)
{
	threadIdMutex.lock();
	mainThreadID = id;
	threadIdMutex.unlock();
}

/**
* @brief RunChipic3dListener::runChipic3d 运行chipic 并返回一个监听器指针  这个指针需要在外部释放
* @param const std::string & m3dpath 路径
* @param const int & count 线程数
* @param const std::string userName chipic所属用户名，这个参数主要用于服务器有多个用户链接时判断chipic的归属
* @return std::shared_ptr<RunChipic3dListener::RunChipic3dListener> 监听器
*/
std::shared_ptr<RunChipic3dListener> RunChipic3dListener::runChipic3d(const std::string &m3dpath, const int &count, const std::string userName /*= "default_userName"*/)
{
	std::shared_ptr<RunChipic3d> chipic3d(new RunChipic3d());
	chipic3d->run(m3dpath, count);

	std::shared_ptr<RunChipic3dListener> listener(new RunChipic3dListener);

	listener->runchipic3dPtr = chipic3d;
	listener->m3dPath = m3dpath;
	listener->threadCount = count;
	listener->userName = userName;
	listener->workThreadOn();

	return listener;
}

std::shared_ptr<RunChipic3dListener> RunChipic3dListener::runChipicFix(const std::string& m3dpath, const int& count, const std::string userName /*= "default_userName"*/)
{
	std::shared_ptr<RunChipic3d> chipic3d(new RunChipic3d());
	chipic3d->runfix(m3dpath);

	std::shared_ptr<RunChipic3dListener> listener(new RunChipic3dListener);

	listener->runchipic3dPtr = chipic3d;
	listener->m3dPath = m3dpath;
	listener->threadCount = count;
	listener->userName = userName;
	listener->workThreadOn();

	return listener;
}

/**
* @brief RunChipic3dListener::setWorkThreadFlag
* @param const bool & flag
* @return void
*/
void RunChipic3dListener::setWorkThreadFlag(const bool& flag)
{
	workThreadMutex.lock();
	workThreadFlag = flag;
	workThreadMutex.unlock();
}

/**
* @brief RunChipic3dListener::getWorkThreadFlag
* @return bool
*/
bool RunChipic3dListener::getWorkThreadFlag()
{
	workThreadMutex.lock();
	bool temp = workThreadFlag;
	workThreadMutex.unlock();

	return temp;
}

/**
* @brief RunChipic3dListener::receiveStringMessage 循环接收字符串消息
* @param Message & msg
* @return void
*/
void RunChipic3dListener::receiveStringMessage(Message &msg)
{
	//判断消息是否为消息头
	if (msg.Msg == 208
		&&msg.wParam != 2
		&&msg.lParam == 111111)
	{
		QByteArray buffer;
		int failedCount = 0;//接收失败次数，超过最大值则停止接收该字符串消息
		const int failedCountMax = 10000;
		//循环接收字符串，直到接收到消息尾
		do 
		{
			Message temp;
			if (receiveMessage(temp,0))
			{
				if (temp.Msg != 208||temp.wParam == 2)
				{
					msg = temp;
					break;
				}
				//接收到消息尾，则停止接收
				if (temp.lParam == 999999)
				{
					msg.text = buffer.data();
					//替换其中的特殊字符为空格
				//	QString temp = QString::fromStdString(msg.text.c_str());
				//	temp.replace("@#$","\n");
				//	msg.text = temp.toStdString();
					break;
				}
				buffer.append(temp.lParam);

			}else
			{
				failedCount++;
			}
		} while (failedCount < failedCountMax);
	}
}

void RunChipic3dListener::run()
{
	//初始化chipic程序
	this->init();
	//发送初始化完成消息
	{
		std::string json = MessageTransition::creatChipicStartfinishedJsonMessage(this->m3dPath, this->getThreadId(), this->threadCount,this->userName);
		auto messageGetter = JsonMessageGetter::GetInstance();
		messageGetter->addJsonMessage(json);
	}

	while (getWorkThreadFlag())
	{
		/*
			为了能尽快的接收消息，又能在接收时兼顾发送，并且空闲时不占用cpu大量资源。
			如果有未发送的消息，或者接收消息未失败，则一直循环接收。
			否则跳出循环，休眠一会儿再接收或者发送。
		*/

		bool ok = true;
		while (ok)
		{
			Message msg;
			//接收winmessga
			if (receiveMessage(msg, 0))
			{
				receiveStringMessage(msg);
				msg.threadId = this->mainThreadID;
				std::string json = MessageTransition::winMessageTojson(msg);
				auto messageGetter = JsonMessageGetter::GetInstance();
				messageGetter->addJsonMessage(json);
			}else{
				ok = false;
			}
			//发送winMessage
			if (getMessageForDeque(msg))
			{
				sendMessage(msg.Msg, msg.wParam, msg.lParam);
			}else{
				ok = false || ok;
			}

			if (!getWorkThreadFlag())
				return;
		}
		//每次循环睡眠10ms,避免cpu被占用
		Sleep(10);
	}
}

/**
* @brief RunChipic3dListener::sendMessage 发送消息
* @param msg 消息类型
* @param wParam 短参数
* @param lParam 长参数
* @return 发送消息是否成功
*/
bool RunChipic3dListener::sendMessage(UINT Msg, WPARAM wParam, LPARAM lParam)
{
	auto b = (PostThreadMessage(this->mainThreadID, Msg + WM_USER, wParam, lParam));
#ifdef  MY_DEBUG
	if (!b)
	{
        std::cerr << "message send erro,thread ID:" << this->mainThreadID
                  << "  windows erro code:" << GetLastError() << std::endl;
    }else {
        std::cerr << "message send finish,Thread ID:" << this->mainThreadID
                  << ",msg: WM_USER + " << Msg
                  << ",wParaw: " << wParam
                  << ",lParaw: " << lParam << std::endl;
    }
#endif // MY_DEBUG

	//判断消息发送失败的错误代码是否是程序已关闭  如果程序已关闭则发送关闭消息 释放管理器对象。
	if (b)
		return b;
	auto erroCode = GetLastError();
	if (erroCode != 1444)
		return b;
	sendMsgFailedCount++;
	if (sendMsgFailedCount < 3)
		return b;

	//回执一个chipic关闭消息，通知管理器释放对象
	std::string aj = MessageTransition::creatCloseChipicJsonMessage(getThreadId(),1);
	auto getter = JsonMessageGetter::GetInstance();
	getter->addJsonMessage(aj);

	return b;
}

/**
* @brief RunChipic3dListener::sendMessage 发送消息，实际是将消息放入队列，等待工作线程发送
* @param const Message & msg
* @return void
*/
void RunChipic3dListener::sendMessage(const Message& msg)
{
	sendMessageDequeMutex.lock();
	sendMessageDeque.push_back(msg);
	sendMessageDequeMutex.unlock();
}

/**
* @brief 初始化
*/
void RunChipic3dListener::init(){
	DWORD id;
#ifdef MY_DEBUG
	std::cerr << "parallel run start find main thread ID!" << std::endl;
#endif // MY_LOG
	getMainThreadId(id);
#ifdef MY_DEBUG
	std::cerr << "find main thread ID finished,ID: " << id << std::endl;
#endif
	setThreadId(id);
}
/**
* @brief RunChipic3dListener::receiveMessage 接收消息
* @param msg 消息容器
* @param ms 接收消息前等待多少毫秒 默认为100ms
* @return 是否接收到消息
*/
bool RunChipic3dListener::receiveMessage(Message &msg,const int &ms){

    MSG m;
	Sleep(ms);
    if (::PeekMessage(&m, NULL, 0, 0, PM_REMOVE))
	{
        msg.Msg = m.message - WM_USER;
        msg.wParam = m.wParam;
        msg.lParam = m.lParam;
#ifdef MY_DEBUG
		std::cerr << "RunChipic3dListener::receiveMessage,Msg:" << msg.Msg <<
			",wParam:" << msg.wParam << ",lParam:" << msg.lParam << std::endl;
#endif // MY_DEBUG

		return true;
	}
	else
	{
//#ifdef MY_DEBUG
//		std::cerr << "接收消息失败" << std::endl;
//#endif
		return false;
    }
}
/**
 * @brief RunChipic3dListener::testSendMessage 测试发送消息是否成功
 * @return 如果发送消息失败，且返回错误代码1444 则返回false 说明chipic已经不再运行
 */
bool RunChipic3dListener::testSendMessage()
{
    auto b = (PostThreadMessage(this->mainThreadID, WM_USER + 666, 0, 0));
    if(!b)
    {
        auto erroCode = GetLastError();
        if(erroCode == 1444)
        {
            return false;
        }
    }

    return true;
}
