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

std::string MessageSender::getEmitterTypeID()
{
	return typeid(emitter).name();
}

