#include "LocalEimtter.h"
#include "CJsonObject.hpp"
#include "MessageTransition.h"
LocalEmitter::LocalEmitter()
{

}

LocalEmitter::~LocalEmitter()
{

}

/**
* @brief LocalEmitter::sendMessage 发送消息,在发送之前会预先处理非winmessage消息
* @param const std::string& json
* @return void
*/
void LocalEmitter::sendMessage(const std::string& json)
{
	neb::CJsonObject jsonObject(json);
	std::string cmd = "";
	if (jsonObject.Get("cmd", cmd))
	{
		if (cmd == "RunChipic")
		{
			disposRunChipicJsonMessage(json);
		}
		else if (cmd == "CloseChipic")
		{
			disposeCloseChipicJsonMessage(json);
		}
	}
	else
	{
		sendWinMessage(json);
	}

}

/**
* @brief LocalEmitter::disposRunChipicJsonMessage 判断消息是否为chipic启动消息，是则启动chipic 并返回true
* @param const std::string & json
* @return bool 
*/
bool LocalEmitter::disposRunChipicJsonMessage(const std::string& json)
{
	neb::CJsonObject jsonObject(json);
	std::string runChipicParm, temp;
	if (jsonObject.Get("Text", runChipicParm))
	{
		neb::CJsonObject parmJsonObject(runChipicParm);
		std::string m3dPath;
		int threadCount;

		parmJsonObject.Get("m3dPath", m3dPath);
		parmJsonObject.Get("threadCount", temp);
		threadCount = std::stoi(temp);
		runChipic(m3dPath, threadCount);

		return true;
	}

	return false;
}

/**
* @brief LocalEmitter::disposeCloseChipicJsonMessage 关闭chipic
* @param const std::string json
* @return bool
*/
bool LocalEmitter::disposeCloseChipicJsonMessage(const std::string& json)
{
	neb::CJsonObject jsonObject(json);
	std::string temp;
	if (jsonObject.Get("threadID", temp))
	{
		DWORD threadId = std::stoi(temp);
		auto listener = listenerMap.find(threadId);
		if (listener != listenerMap.end())
		{
			listenerMap.erase(listener);
		}
		else
		{
#if MY_DEBUG
			std::cerr << "LocalEmitter::disposeCloseChipicJsonMessage get RunChipic3dListener failde" << std::endl;
#endif // MY_DEBUG
			return false;
		}
	}
	else
	{
#if MY_DEBUG
		std::cerr << "LocalEmitter::disposeCloseChipicJsonMessage get ThreadId failed!" << std::endl;
#endif // MY_DEBUG
		return false;
	}

	return true;
}

/**
* @brief LocalEmitter::runChipic 启动chipic
* @param const std::string & m3dPath 文件路径
* @param const int & threadCount 线程数
* @return void
*/
void LocalEmitter::runChipic(const std::string& m3dPath, const int& threadCount)
{
	auto  listener = RunChipic3dListener::runChipic3d(m3dPath, threadCount);

	listenerMap.insert(RunChipic3dListenerMap::value_type(listener->getThreadId(), listener));
}

/**
* @brief LocalEmitter::sendWinMessage 将win消息发给对应的线程
* @param const std::string & json
* @return void
*/
void LocalEmitter::sendWinMessage(const std::string& json)
{
	neb::CJsonObject jsonObject(json);
	std::string temp;
	if (jsonObject.Get("threadID", temp))
	{
		DWORD threadId = std::stoi(temp);
		auto listener = listenerMap.find(threadId);
		if (listener != listenerMap.end())
		{
			Message msg = MessageTransition::jsonToWinMessage(json);
			listener->second->sendMessage(msg);
		}
		else
		{
#if MY_DEBUG
			std::cerr << "LocalEmitter::sendWinMessage get RunChipic3dListener failde" << std::endl;
#endif // MY_DEBUG

		}
	}
	else
	{
#if MY_DEBUG
		std::cerr << "LocalEmitter::sendWinMessage get ThreadId failed!" << std::endl;
#endif // MY_DEBUG

	}
}
