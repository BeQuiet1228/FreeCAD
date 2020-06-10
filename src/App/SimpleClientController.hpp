#pragma once
#include "ISessionCreateListener.hpp"
 namespace PicNet
{

	class SimpleClientController : public ISessionCreateListener
	{


	public:
		void TestStart(){

			char* text = "\0";
			while (true)
			{
				int type = 0;
				int msgId = 0;
				printf_s("type and id:");
				scanf_s("%d %d", &type, &msgId);
				printf_s("\n");

				if (_sessionWeakPtr.expired())
				{
					break;
				}

				if (type == NetMsgHeader::MsgType::ID_COMMAD)
				{
					_sessionWeakPtr.lock()->Send(NetMsg::Create(NetMsgHeader::ID_COMMAD, msgId, sizeof(text), text, Usercode));
				}
				if (type == NetMsgHeader::MsgType::MSG_COMMAD)
				{
					int w = 0;
					int l = 0;
					scanf_s("%d %d", &w, &l);
					WinMsgInfo info;
					info.wParam = w;
					info.lParam = l;

					_sessionWeakPtr.lock()->Send(NetMsg::Create(NetMsgHeader::MSG_COMMAD, msgId, sizeof(info), (char*)&info, Usercode));
				}
				if (type == NetMsgHeader::MsgType::FILE_CONENT)
				{
					char path[256];
					char name[256];
					scanf_s("%s %s", path, 256, name, 256);
					FILE* fp;
					errno_t err;
					if (err = fopen_s(&fp, path, "rb"))
					{
						printf_s("无法打开此文件\n");
					}
					else{
						_sessionWeakPtr.lock()->SendFile(NetMsg::CreateByFile(msgId, name, Usercode, fp), fp);
					}

				}
				if (type == NetMsgHeader::MsgType::STRING)
				{
					char str[256];

					scanf_s("%s", str, 256);

					_sessionWeakPtr.lock()->Send(NetMsg::Create(NetMsgHeader::STRING, msgId, sizeof(str), str, Usercode));
				}

				while (getchar() != '\n')
				{

				}

				Sleep(1000);
			}

		}

		virtual ~SimpleClientController(){};

		bool IsEnable()
		{
			return !_sessionWeakPtr.expired();
		}

		bool ExistReceiveMsg()
		{
			return IsEnable() && _sessionWeakPtr.lock()->ExistReceiveMsg();
		}

		MsgPtr GetMsg()
		{
			if (ExistReceiveMsg())
			{
				return _sessionWeakPtr.lock()->Get();
			}
			return nullptr;
		}

		bool SendIdMsg(int msgId)
		{
			if (IsEnable())
			{
				int i = 0;
				_sessionWeakPtr.lock()->Send(NetMsg::Create(NetMsgHeader::MsgType::ID_COMMAD, msgId, sizeof(i), (char*)&i, Usercode));
				return true;
			}
			return false;
		}


		bool SendWinMsg(int msgId, int wParam, int lParam)
		{
			if (IsEnable())
			{
				WinMsgInfo info;
				info.wParam = wParam;
				info.lParam = lParam;

				_sessionWeakPtr.lock()->Send(NetMsg::Create(NetMsgHeader::MsgType::MSG_COMMAD, msgId, sizeof(info), (char*)&info, Usercode));
				return true;
			}
			return false;
		}

		bool SendStrMsg(int msgId, std::string str)
		{
			if (IsEnable())
			{
				str = str + '\0';
				_sessionWeakPtr.lock()->Send(NetMsg::Create(NetMsgHeader::STRING, msgId, str.length(), str.c_str(), Usercode));

				return true;
			}
			return false;
		}

		bool SendFile( int msgId, std::string path, std::string name)
		{
			if (IsEnable())
			{
				FILE* fp;
				errno_t err;
				if (err = fopen_s(&fp, path.c_str(), "rb"))
				{
					printf_s("无法打开此文件\n");
					return false;
				}
				else{
					_sessionWeakPtr.lock()->SendFile(NetMsg::CreateByFile(msgId, name, Usercode, fp), fp);
					return true;
				}
			}
			return false;
		}

		float GetTransmissionRate()
		{
			if (IsEnable())
			{
				float f = _sessionWeakPtr.lock()->GetTransmissionRate();
				return f;
			}
			return 0;
		}

		void virtual OnSessionCreated(SessionWeakPtr sessionWeakPtr) {
			_sessionWeakPtr = sessionWeakPtr;
		}
		int Usercode;

	private:
		SessionWeakPtr _sessionWeakPtr;
		
	};

}