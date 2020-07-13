#pragma once
#include <memory>
#include <mutex>
#include "EmitterInterface.h"
class MessageSender
{
public:
	~MessageSender();
	static std::shared_ptr<MessageSender> GetInstance(){
		static std::once_flag flag;
		std::call_once(flag, [&](){
			_instance.reset(new MessageSender);
		});

		return _instance;
	}
private:
	MessageSender();
	static std::shared_ptr<MessageSender> _instance;
	MessageSender(const MessageSender&) = delete;
	MessageSender operator=(const MessageSender&) = delete;

public:
	//发送Json消息
	void sendJsonMessage(const std::string& json);
	//设置消息发射器
	void setEmitter(EmitterInterface *em);

private:
	EmitterInterface * emitter = nullptr;
};
