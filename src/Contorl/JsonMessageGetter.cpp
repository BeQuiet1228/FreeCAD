#include "JsonMessageGetter.h"
#include <iostream>

std::shared_ptr<JsonMessageGetter> JsonMessageGetter::_instance;

JsonMessageGetter::~JsonMessageGetter()
{

}

JsonMessageGetter::JsonMessageGetter()
{

}

/**
* @brief JsonMessageGetter::hasMessage 判断是否有消息
* @return bool true代表有消息
*/
bool JsonMessageGetter::hasMessage()
{
	jsonDequeMutex.lock();
	bool ok = jsonDeque.size();
	jsonDequeMutex.unlock();
	return ok;
}

/**
* @brief JsonMessageGetter::getJsonMessage 获取一个消息
* @param std::string & json 消息
* @return bool 是否获取成功
*/
bool JsonMessageGetter::getJsonMessage(std::string& json)
{
	jsonDequeMutex.lock();
	if (jsonDeque.size() <= 0)
	{
		jsonDequeMutex.unlock();
		return false;

	}	
	json = jsonDeque.front();
	jsonDeque.pop_front();
	jsonDequeMutex.unlock();

	return true;

}

/**
* @brief JsonMessageGetter::addJsonMessage 添加一个消息
* @param const std::string & json 消息
* @return void
*/
void JsonMessageGetter::addJsonMessage(const std::string& json)
{
#if MY_DEBUG
	std::cerr << "JsonMessageGetter::addJsonMessage,Json:" << json << std::endl;
#endif // MY_DEBUG

	jsonDequeMutex.lock();
	jsonDeque.push_back(json);
	jsonDequeMutex.unlock();

	emit hasNewMessage();
}

#ifndef MY_QTCMY_DEBUG
#include "moc_JsonMessageGetter.cpp"
#endif