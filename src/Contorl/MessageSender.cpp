#include "MessageSender.h"
#include "CJsonObject.hpp"
#include "runchipic3d.h"
#include <QString>
#include "MessageTransition.h"
std::shared_ptr<MessageSender> MessageSender::_instance;

MessageSender::MessageSender()
{
	
}
MessageSender::~MessageSender()
{
	if (emitter != nullptr)
		delete emitter;
}

/**
* @brief MessageSender::sendJsonMessage 发送json消息
* @param const std::string & json
* @return void
*/
void MessageSender::sendJsonMessage(const std::string& json)
{
	if (emitter == nullptr)
	{
#ifdef MY_LOG
		std::cerr << "MessageSender::sendJsonMessage emitter is null,send msg is failed!" << std::endl;
#endif // MY_LOG
		return;
	}
	emitter->sendMessage(json);
}

/**
* @brief MessageSender::setEmitter 设置消息发射器
* @param EmitterInterface * em
* @return void
*/
void MessageSender::setEmitter(EmitterInterface *em)
{
	if (emitter != nullptr)
		delete emitter;
	emitter = em;
}

int MessageSender::getEmitterTypeID()
{
	return emitter->getEmitterId();
}

