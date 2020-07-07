#pragma once
#include <memory>
#include <mutex>
#include <map>
#include "WinMessageManager.h"

using WinMessageManagerPtr = std::shared_ptr<WinMessageManager>;
using WinMessageManagerMap = std::map<DWORD, WinMessageManagerPtr>;
class MessageManager
{
public:
	~MessageManager();
	static std::shared_ptr<MessageManager> GetInstance(){
		static std::once_flag flag;
		std::call_once(flag, [&](){
			_instance.reset(new MessageManager);
		});

		return _instance;
	}
private:
	MessageManager();
	static std::shared_ptr<MessageManager> _instance;
	MessageManager(const MessageManager&) = delete;
	MessageManager operator=(const MessageManager&) = delete;
private:
	//是否开启远程模式
	bool onlineMode;
	//winmessage消息管理器集合
	WinMessageManagerMap winMessageManagerMap;
public:
	//发送Json消息
	void sendJsonMessage(const std::string& json);

private:
	//处理chipic启动消息
	bool disposRunChipicJsonMessage(const std::string& json);
	//启动m3d
	void runChipic(const std::string& m3dPath, const int& threadCount);
	//发送winMessage
	void sendWinMessage(const std::string& json);
};
