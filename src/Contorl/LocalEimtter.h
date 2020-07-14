#pragma once
#include "EmitterInterface.h"
#include <map>
#include "RunChipic3dListener.h"
#include <memory>
using RunChipic3dListenerPtr = std::shared_ptr<RunChipic3dListener>;
using RunChipic3dListenerMap = std::map<DWORD, RunChipic3dListenerPtr>;

class LocalEmitter:public EmitterInterface
{
public:
	LocalEmitter();
	~LocalEmitter();

public:
	void sendMessage(const std::string& json) override;
private:
	//处理chipic启动消息
	bool disposRunChipicJsonMessage(const std::string& json);
	//处理cihpic关闭消息
	bool disposeCloseChipicJsonMessage(const std::string& json);
	//启动m3d
	void runChipic(const std::string& m3dPath, const int& threadCount);
	//发送winMessage
	void sendWinMessage(const std::string& json);
private:
	//winmessage消息管理器集合
	RunChipic3dListenerMap listenerMap;

};
