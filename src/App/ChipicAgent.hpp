#pragma once

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
#include <boost/thread/mutex.hpp>
#include"Config.hpp"
#include <string>
namespace PicNet
{
	//各类消息回调
	class ChipicAgentListener {
	public:
		virtual ~ChipicAgentListener(){};
		virtual  void OnReceiveLocalWinMsg(DWORD id, int w, int l){};
	};

	//管理代理类
	class ChipicAgent {
	public:
		//构造函数，需要得到Distributer
		ChipicAgent(ChipicAgentListener* listener) :_listener(listener), _threadId(0){
		}

		int Start(int count, std::string userDir, std::string filePath)
		{
			boost::unique_lock<boost::mutex> lock(_mutex);

			std::string exepath = ConfigSingleton::GetInstance()->Get<std::string>("exepath");
			_userDir = userDir;
			if (count == 1)
			{
				auto cmd = exepath + " \"" + filePath + "\"";

				auto x = CreateProcess((TCHAR*)cmd.c_str());
				std::cout << cmd << "\n" << GetLastError();
			}
			else if (count > 1) {
				std::cout << "Paiallel : " << count << " Loading..." << std::endl;
				//生成文件，如果存在删除重来
				std::ofstream file(userDir + "\\cfg.txt", std::ios::trunc);

				for (size_t i = 1; i <= count; i++)
				{
					std::string path = userDir + "\\%d";
					std::string newFile = path + "\\" + filePath.substr(filePath.find_last_of('\\') + 1);
					_mkdir(path.c_str());
					if (!CopyFile(filePath.c_str(), newFile.c_str(), FALSE))
					{
						return -1;
					}
					file << "-n 1 -wdir";
					file << " ";
					file << path;
					file << " ";
					file << exepath;
					file << " ";
					file << newFile;
					file << "\n";
				}
				file.close();

				_cmdThread = new boost::thread(boost::bind(&ChipicAgent::RunCmd, this));
			}
			std::vector<DWORD>threads;
			std::cout << "Wait For Fortran Program Chipic3d.exe ..." << std::endl;
			_threadId = 0;
			while (_threadId == 0)
			{
				Sleep(1000);
				threads.clear();
				//通过进程名查找线程Id
				int ret = GetMainThreadIdFromName("Chipic3d.exe", threads);

				//发送本线程的Id
				for (size_t i = 0; i < threads.size(); i++)
				{
					auto currentThreadId = GetCurrentThreadId();
					::PostThreadMessage(threads[i], WM_USER + 10, GetCurrentThreadId(), 111);
					Sleep(100);
					MSG  msg;
					if (::PeekMessage(&msg, NULL, 0, 0, PM_REMOVE))
					{
						if (msg.message == WM_USER + 20)
						{
							_threadId = msg.wParam;
							break;
						}
					}
				}
			}
			Sleep(500);

			return 0;
		}

		void ReceiveNetWinMsg(DWORD id, int w, int l)
		{
			if (id == WM_USER)
			{
				std::cout << "ReceiveNetWinMsg Quit" << std::endl;
				//发送关闭消息
				::PostThreadMessage(_threadId, WM_QUIT, 0, GetCurrentThreadId());
			}
			else {
				std::cout << "ReceiveNetWinMsg WM_USER+" << id - WM_USER << std::endl;
				//发送关闭消息
				::PostThreadMessage(_threadId, id, w, l);
			}
		}

		void ReceiveLocalWinMsg(DWORD id, int w, int l)
		{

		}

		void Update()
		{
			MSG  msg;
			if (::PeekMessage(&msg, NULL, 0, 0, PM_REMOVE))
			{
				ReceiveLocalWinMsg(msg.message, msg.wParam, msg.lParam);
			}
		}
		void Finalize()
		{
			if (_threadId != 0)
			{
				//发送关闭消息
				::PostThreadMessage(_threadId, WM_QUIT, 0, GetCurrentThreadId());
			}

		}
	private:
		ChipicAgentListener * _listener;
		boost::thread* _cmdThread;
		DWORD _threadId = 0;
		std::string _userDir;
		//静态变量
		boost::mutex _mutex;

		// 由进程名获取进程ID(需要头文件tlhelp32.h)
		// 失败返回0
		DWORD GetProcessIDFromName(LPCSTR szName)
		{
			DWORD id = 0;       // 进程ID
			PROCESSENTRY32 pe;  // 进程信息
			pe.dwSize = sizeof(PROCESSENTRY32);
			HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0); // 获取系统进程列表
			if (Process32First(hSnapshot, &pe))      // 返回系统中第一个进程的信息
			{
				do
				{
					if (0 == _stricmp(pe.szExeFile, szName)) // 不区分大小写比较
					{
						id = pe.th32ProcessID;
						break;
					}
				} while (Process32Next(hSnapshot, &pe));      // 下一个进程
			}
			CloseHandle(hSnapshot);     // 删除快照
			return id;
		}

		// 由进程名获取主线程ID(需要头文件tlhelp32.h)
		// 失败返回0
		int GetMainThreadIdFromName(LPCSTR szName, std::vector<DWORD>& threads)
		{
			//std::vector<DWORD> idThread;         // 进程ID
			std::vector<DWORD> idProcess;        // 主线程ID

			// 获取进程ID
			PROCESSENTRY32 pe;      // 进程信息
			pe.dwSize = sizeof(PROCESSENTRY32);
			HANDLE hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0); // 获取系统进程列表
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
			HANDLE hSnapshot2 = CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0); // 系统所有线程快照
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

		void RunCmd()
		{
			WinExec("smpd -d -0", SW_HIDE);
			std::string cmd = "mpiexec.exe -configfile \"" + _userDir + "cfg.txt\" -phrase 0";
			system(cmd.c_str());
		}

		int CreateProcess(TCHAR  szCommandLine[])
		{
			STARTUPINFO si;
			PROCESS_INFORMATION pi;
			ZeroMemory(&si, sizeof(si));
			si.cb = sizeof(si);
			ZeroMemory(&pi, sizeof(pi));

			si.dwFlags = STARTF_USESHOWWINDOW;  // 指定wShowWindow成员有效
			si.wShowWindow = TRUE;          // 此成员设为TRUE的话则显示新建进程的主窗口，
			// 为FALSE的话则不显示
			BOOL bRet = ::CreateProcess(
				NULL,           // 不在此指定可执行文件的文件名
				szCommandLine,      // 命令行参数
				NULL,           // 默认进程安全性
				NULL,           // 默认线程安全性
				FALSE,          // 指定当前进程内的句柄不可以被子进程继承
				CREATE_NEW_CONSOLE, // 为新进程创建一个新的控制台窗口
				NULL,           // 使用本进程的环境变量
				NULL,           // 使用本进程的驱动器和目录
				&si,
				&pi);

			if (bRet)
			{
				//WaitForSingleObject(pi.hProcess, INFINITE);
				// 既然我们不使用两个句柄，最好是立刻将它们关闭
				::CloseHandle(pi.hThread);
				::CloseHandle(pi.hProcess);

				//	printf(" 新进程的进程ID号：%d \n", pi.dwProcessId);
				//	printf(" 新进程的主线程ID号：%d \n", pi.dwThreadId);
				return pi.dwThreadId;
			}
			return 0;
		}
	};

}