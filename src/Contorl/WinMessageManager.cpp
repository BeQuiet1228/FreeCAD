#include "WinMessageManager.h"
#include "lonelinessmode.h"
#include "MessageTransition.h"
#include "JsonMessageGetter.h"

WinMessageManager::WinMessageManager()
{
	workThreadFlag = false;
}


WinMessageManager::~WinMessageManager()
{
	sendMessage(0, 0, 0);
	//等待线程发送出关闭内核程序的消息
	Sleep(30);
	workThreadOff();
}
/**
* @brief WinMessageManager::GetMainThreadIdFromName 根据进程名称获取进程下所有线程id
* @param szName 进程名
* @param threads 线程id容器
* @return  进程中线程的数量
*/
int WinMessageManager::GetMainThreadIdFromName(LPCSTR szName, std::vector<DWORD>& threads)
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
* @brief WinMessageManager::getMainThreadId 获取主线程id
* @param threadId 主线程id
*/
void WinMessageManager::getMainThreadId(DWORD &_threadId) {
	std::vector<DWORD>threads;
	//std::cout << "Wait For Fortran Program Chipic3d.exe ..." << std::endl;
	_threadId = 0;
	while (_threadId == 0)
	{
		Sleep(1000);
		threads.clear();
		//通过进程名查找线程Id
		int ret = GetMainThreadIdFromName("Chipic3d.exe", threads);
#ifdef _DEBUG
		if (ret == 0)
		{
			std::cerr << "not found chipic3d thread" << std::endl;
		}
#endif
		//发送本线程的Id
		for (size_t i = 0; i < threads.size(); i++)
		{
			auto b = ::PostThreadMessage(threads[i], WM_USER + 10, GetCurrentThreadId(), 1);

#ifdef _DEBUG
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
	}
}

/**
* @brief WinMessageManager::getMessageForDeque 从消息队列中获取要发送的消息
* @param Message & msg
* @return bool 如果队列中没有消息则返回false
*/
bool WinMessageManager::getMessageForDeque(Message& msg)
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
* @brief WinMessageManager::workThreadOn 开启工作线程循环
* @return void
*/
void WinMessageManager::workThreadOn()
{
	setWorkThreadFlag(true);
	this->start();
}

void WinMessageManager::workThreadOff()
{
	setWorkThreadFlag(false);
	this->wait();
}

/**
* @brief WinMessageManager::setWorkThreadFlag
* @param const bool & flag
* @return void
*/
void WinMessageManager::setWorkThreadFlag(const bool& flag)
{
	workThreadMutex.lock();
	workThreadFlag = flag;
	workThreadMutex.unlock();
}

/**
* @brief WinMessageManager::getWorkThreadFlag
* @return bool
*/
bool WinMessageManager::getWorkThreadFlag()
{
	workThreadMutex.lock();
	bool temp = workThreadFlag;
	workThreadMutex.unlock();

	return temp;
}

void WinMessageManager::run()
{
	this->init();
	while (getWorkThreadFlag())
	{
		//每次循环睡眠50ms,避免cpu被占用
		Sleep(50);
		Message msg;
		//接收winmessga
		while (receiveMessage(msg,0))
		{
			msg.threadId = this->mainThreadID;
			std::string json = MessageTransition::winMessageTojson(msg);
			auto messageGetter = JsonMessageGetter::GetInstance();		
			messageGetter->addJsonMessage(json);
		}
		while (getMessageForDeque(msg))
		{
			sendMessage(msg.Msg, msg.wParam, msg.lParam);
		}
	}
}

/**
* @brief WinMessageManager::sendMessage 发送消息
* @param msg 消息类型
* @param wParam 短参数
* @param lParam 长参数
* @return 发送消息是否成功
*/
bool WinMessageManager::sendMessage(UINT Msg, WPARAM wParam, LPARAM lParam)
{
	auto b = (PostThreadMessage(this->mainThreadID, Msg + WM_USER, wParam, lParam));
#ifdef _DEBUG
	if (!b)
	{
        std::cerr << "message send erro,thread ID:" << this->mainThreadID
                  << "  windows erro code:" << GetLastError() << std::endl;
    }else {
        std::cerr << "message send finish,Thread ID:" << this->mainThreadID
                  << ",msg: WM_USER + " << Msg - WM_USER
                  << ",wParaw: " << wParam
                  << ",lParaw: " << lParam << std::endl;
    }
#endif // _DEBUG
	return b;
}

/**
* @brief WinMessageManager::sendMessage 发送消息，实际是将消息放入队列，等待工作线程发送
* @param const Message & msg
* @return void
*/
void WinMessageManager::sendMessage(const Message& msg)
{
	sendMessageDequeMutex.lock();
	sendMessageDeque.push_back(msg);
	sendMessageDequeMutex.unlock();
}

/**
* @brief 初始化
*/
void WinMessageManager::init(){
	getMainThreadId(mainThreadID);
}
/**
* @brief WinMessageManager::receiveMessage 接收消息
* @param msg 消息容器
* @param ms 接收消息前等待多少毫秒 默认为100ms
* @return 是否接收到消息
*/
bool WinMessageManager::receiveMessage(Message &msg,const int &ms){

    MSG m;
	Sleep(ms);
    if (::PeekMessage(&m, NULL, 0, 0, PM_REMOVE))
	{
        msg.Msg = m.message - WM_USER;
        msg.wParam = m.wParam;
        msg.lParam = m.lParam;
#ifdef _DEBUG
		std::cerr << "WinMessageManager::receiveMessage,Msg:" << msg.Msg <<
			",wParam:" << msg.wParam << ",lParam:" << msg.lParam << std::endl;
#endif // _DEBUG

		return true;
	}
	else
	{
//#ifdef _DEBUG
//		std::cout << "接收消息失败" << std::endl;
//#endif
		return false;
    }
}
/**
 * @brief WinMessageManager::testSendMessage 测试发送消息是否成功
 * @return 如果发送消息失败，且返回错误代码1444 则返回false 说明chipic已经不再运行
 */
bool WinMessageManager::testSendMessage()
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
