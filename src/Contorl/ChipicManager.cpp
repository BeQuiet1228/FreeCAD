#include "ChipicManager.h"
#include "JsonMessageGetter.h"
#include "CJsonObject.hpp"
#include <iostream>
#include "JsonMessageGetter.h"
ChipicManager::ChipicManager()
{
	auto getter = JsonMessageGetter::GetInstance();
	connect(getter.get(), SIGNAL(hasNewMessage()), this, SLOT(hasNewMessage()));
}

ChipicManager::~ChipicManager()
{

}

/**
* @brief ChipicManager::hasNewMessage 获取json消息获取器中的消息  然后交给对应chipic对象处理
* @return void
*/
void ChipicManager::hasNewMessage()
{
	/*
	*[1] 获取消息获取器中的消息
	*[2] 获取消息中的线程id
	*[3] 通过线程id寻找chipic对象，如果未找到对应的chipic对象，则创建对应的chipic对象
	*[4] 将json对应给到对应的chipic对象处理
	*/
	auto msgGetter = JsonMessageGetter::GetInstance();

	std::string jsonMsg;
	//[1]
	if (msgGetter->getJsonMessage(jsonMsg))
	{
		neb::CJsonObject jsonObject(jsonMsg);
		std::string temp;
		//[2]
		if (!jsonObject.Get("threadID", temp))
		{
#if _DEBUG
			std::cerr << "ChipicManager hasNewMessgae jsonObject get threadid faild" << std::endl;
#endif // _DEBUG

			return;
		}
		//[3]
		DWORD threadID = std::stol(temp);
		auto chipicIterator = chipicMap.find(threadID);
		
		std::shared_ptr<Chipic> chipic;

		if (chipicIterator == chipicMap.end())
		{
			chipic.reset(new Chipic(threadID));
			chipicMap.insert(std::map<DWORD, std::shared_ptr<Chipic>>::value_type(chipic->threadID, chipic));
		}
		else
		{
			chipic = chipicIterator->second;
		}

		//[4]
		chipic->disposJsonMessage(jsonMsg);

	}
}

#ifndef MY_QTC_DEBUG
#include "moc_ChipicManager.cpp"
#endif
