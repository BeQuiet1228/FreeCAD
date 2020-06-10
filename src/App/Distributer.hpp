#pragma once
#include<unordered_map>
#include<vector>
#include <windows.h>

#include"NetMsg.hpp"
#include"ChipicAgent.hpp"
#include"Config.hpp"

namespace PicNet
{
	//消息分发类，
	//根据不同的消息对ChipicAgent进行不同操作
	class Distributer : ChipicAgentListener{


	public:

		typedef void (Distributer::*MsgHandle)(MsgPtr);

		Distributer() :_agent(this)
		{
			//string类型数据
			_stringHandleMap[1] = &Distributer::NeedFile;

			//文件类型数据
			_fileHandleMap[1] = &Distributer::StartRunM3d;
		}

		void Finalize(){
			_agent.Finalize();
		}

		//根据函数内容执行
		void InputNet(MsgPtr msg)
		{
			if (msg->GetType() == NetMsgHeader::MsgType::MSG_COMMAD)
			{
				//这里是直接转发
				_agent.ReceiveNetWinMsg(msg->GetId() + WM_USER,
					msg->CastBody<WinMsgInfo*>()->wParam, msg->CastBody<WinMsgInfo*>()->lParam);
				return;
			}
			else if (msg->GetType() == NetMsgHeader::MsgType::ID_COMMAD)
			{
				auto pair = _idHandleMap.find(msg->GetId());
				if (pair != _idHandleMap.end())
				{
					auto f = pair->second;
					(this->*f)(msg);
				}
			}

			else if (msg->GetType() == NetMsgHeader::MsgType::STRING){
				auto pair = _stringHandleMap.find(msg->GetId());
				if (pair != _stringHandleMap.end())
				{
					auto f = pair->second;
					(this->*f)(msg);
				}
			}

			else if (msg->GetType() == NetMsgHeader::MsgType::FILE_CONENT){
				auto pair = _fileHandleMap.find(msg->GetId());
				if (pair != _fileHandleMap.end())
				{
					auto f = pair->second;
					(this->*f)(msg);
				}
			}
		}

		//需要发送某个文件名的文件
		void NeedFile(MsgPtr msg)
		{
			std::string userdir = ConfigSingleton::GetInstance()->Get<std::string>("workpath");
			userdir = userdir + std::to_string(msg->GetRealUserCode()) + "\\";
			std::string path = userdir + msg->CastBody<char*>();
			FILE* fp;
			errno_t err;
			if (err = fopen_s(&fp, path.c_str(), "rb"))
			{
				printf_s("无法打开此文件\n");
			}
			else{
				AddSend(NetMsg::CreateByFile(msg->GetId(), msg->CastBody<char*>(), 123, fp), fp);
			}
		}

		//开始运行一个m3d文件
		void StartRunM3d(MsgPtr msg)
		{
			std::string userdir = ConfigSingleton::GetInstance()->Get<std::string>("workpath");
			userdir = userdir + std::to_string(msg->GetRealUserCode()) + "\\";
			_agent.Start(1, userdir, userdir + msg->CastBody<FileInfo*>()->Name);
		}

		//更新，并且把需要发的消息发出去
		void Update(std::vector<MsgPtr>& msgs, std::vector<FILE*>& files)
		{
			_agent.Update();

			msgs.insert(msgs.begin(), _currentOutputs.begin(), _currentOutputs.end());
			files.insert(files.begin(), _currentFileOutputs.begin(), _currentFileOutputs.end());

			_currentOutputs.clear();
			_currentFileOutputs.clear();
		}


		//-----以下是函数回调，供ChipicAgent使用
		virtual void OnReceiveLocalWinMsg(DWORD id, int w, int l)
		{
			WinMsgInfo info;
			info.wParam = w;
			info.lParam = l;

			AddSend(NetMsg::Create(NetMsgHeader::MSG_COMMAD, (int)(id - WM_USER), sizeof(info), (char*)(&info), 123));
		}


	private:

		std::vector<MsgPtr> _currentOutputs;
		std::vector<FILE*> _currentFileOutputs;

		//分发函数
		std::map<int, MsgHandle> _idHandleMap;
		std::map<int, MsgHandle> _stringHandleMap;
		std::map<int, MsgHandle> _fileHandleMap;

		ChipicAgent _agent;
		int _userCode = 0;

		//添加到输出网络消息
		void AddSend(MsgPtr mptr)
		{
			_currentOutputs.push_back(mptr);
		}
		void AddSend(MsgPtr mptr, FILE* fp)
		{
			_currentOutputs.push_back(mptr);
			_currentFileOutputs.push_back(fp);
		}

	};
}