#include "LocalEimtter.h"
#include "CJsonObject.hpp"
#include "MessageTransition.h"
#include "JsonMessageGetter.h"
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
* @brief LocalEmitter::getEmitterId 获取发射器id
* @return int
*/
int LocalEmitter::getEmitterId()
{
	return 1;
}

/**
* @brief LocalEmitter::disposRunChipicJsonMessage 判断消息是否为chipic启动消息，是则启动chipic 并返回true
* @param const std::string & json
* @return bool 
*/
bool LocalEmitter::disposRunChipicJsonMessage(const std::string& json)
{
	neb::CJsonObject jsonObject(json);
	std::string temp,m3dPath,userName = "defaultUser";

	MessageTransition::getPath(jsonObject, m3dPath);
	jsonObject.Get("threadCount", temp);
	int threadCount = std::stoi(temp);

	MessageTransition::getUserName(jsonObject, userName);
	runChipic(m3dPath, threadCount,userName);

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

		for (auto i = listenerList.begin(); i != listenerList.end(); i++)
		{
			if ((*i)->getThreadId() == threadId)
			{
				listenerList.erase(i);
				//回执一个chipic关闭消息，通知管理器释放对象
				std::string aj = MessageTransition::creatCloseChipicJsonMessage(threadId);
				auto getter = JsonMessageGetter::GetInstance();
				getter->addJsonMessage(aj);
				return true;
			}
		}
#if MY_DEBUG
			std::cerr << "LocalEmitter::disposeCloseChipicJsonMessage get RunChipic3dListener failde" << std::endl;
#endif // MY_DEBUG
			return false;
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
* @param const std::string & userName 账户名,服务器版本中使用
* @return void
*/
void LocalEmitter::runChipic(const std::string& m3dPath, const int& threadCount, const std::string& userName /*= "defaultUser"*/)
{
	auto  listener = RunChipic3dListener::runChipic3d(m3dPath, threadCount,userName);

	listenerList.push_back(listener);
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

		for (auto i = listenerList.begin(); i != listenerList.end(); i++)
		{
			if ((*i)->getThreadId() == threadId)
			{
				Message msg = MessageTransition::jsonToWinMessage(json);
				(*i)->sendMessage(msg);
				return;
			}
		}
#if MY_DEBUG
			std::cerr << "LocalEmitter::sendWinMessage get RunChipic3dListener failde" << std::endl;
#endif // MY_DEBUG

	}
	else
	{
#if MY_DEBUG
		std::cerr << "LocalEmitter::sendWinMessage get ThreadId failed!" << std::endl;
#endif // MY_DEBUG

	}
}
