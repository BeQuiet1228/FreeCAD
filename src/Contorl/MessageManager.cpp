#include "MessageManager.h"
#include "CJsonObject.hpp"
#include "runchipic3d.h"
#include <QString>
std::shared_ptr<MessageManager> MessageManager::_instance;

MessageManager::MessageManager()
{
	this->onlineMode = false;
}

/**
* @brief MessageManager::sendJsonMessage 发送json消息
* @param const std::string & json
* @return void
*/
void MessageManager::sendJsonMessage(const std::string& json)
{
	if (disposRunChipicJsonMessage(json))
		return;
}

/**
* @brief MessageManager::disposRunChipicJsonMessage 处理启动chipic的json消息
* @param const std::string & json 
* @return bool 如果不是chipic启动消息则返回false
*/
bool MessageManager::disposRunChipicJsonMessage(const std::string& json)
{
	neb::CJsonObject jsonObject(json);
	std::string temp = "";
	jsonObject.Get("cmd", temp);
	if (temp == "" && temp != "RunChipic")
		return false;
	//判断是否开启远程模式
	if (this->onlineMode)
	{
	}
	else
	{
		std::string runChipicParm;
		if (jsonObject.Get("Text", runChipicParm))
		{
			neb::CJsonObject parmJsonObject(runChipicParm);
			std::string m3dPath;
			int threadCount;

			parmJsonObject.Get("m3dPath", m3dPath);
			parmJsonObject.Get("threadCount", temp);
			threadCount = std::stoi(temp);
			runChipic(m3dPath, threadCount);
		}
	}
	

	return true;
}
/**
* @brief MessageManager::runChipic 启动chipic
* @param const std::string & m3dPath m3d文件路径
* @param const int & threadCount 线程数
* @return void
*/
void MessageManager::runChipic(const std::string& m3dPath, const int& threadCount)
{
	RunChipic3d run(RunChipic3d::X32);
	run.run(m3dPath, threadCount);
	std::shared_ptr<WinMessageManager> manager(new WinMessageManager);
	manager->workThreadOn();

	winMessageManagerMap.insert(WinMessageManagerMap::value_type(manager->mainThreadID, manager));

}

MessageManager::~MessageManager()
{

}
