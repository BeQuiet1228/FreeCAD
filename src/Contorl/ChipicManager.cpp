#include "ChipicManager.h"
#include "JsonMessageGetter.h"
#include "CJsonObject.hpp"
#include <iostream>
#include "JsonMessageGetter.h"
#include "MessageSender.h"
#include "MessageTransition.h"
#include "Chipic.h"
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
#if MY_DEBUG
			std::cerr << "ChipicManager hasNewMessgae jsonObject get threadid faild" << std::endl;
#endif // MY_DEBUG

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
			connect(chipic.get(), SIGNAL(stateUpdate(DWORD)), this, SLOT(chipicStateUpdate(DWORD)));
			//切换到当前计算程序
			CurrentChipic = chipic;
		}
		else
		{
			chipic = chipicIterator->second;
		}

		//[4]
		chipic->disposJsonMessage(jsonMsg);

	}
}

void ChipicManager::chipicStateUpdate(DWORD threadId)
{
	auto  chipic = chipicMap.find(threadId);
	if (chipic != chipicMap.end())
	{
		if (CurrentChipic.get() == chipic->second.get())
			emit currentChipicStateUpdate();
	}
}

/**
* @brief ChipicManager::runButtonClicked 运行按钮被点击
* @param const std::string & m3dPtah 路径
* @return void
*/
void ChipicManager::runButtonClicked(const std::string& m3dPtah /*= ""*/)
{
	if (!CurrentChipic)
	{
		auto messageManager = MessageSender::GetInstance();
		messageManager->sendJsonMessage(MessageTransition::creatRunChipicJsonMessage(m3dPtah, 1));
	}
	else{
		CurrentChipic->closeChipic();

		//移除chipic对象
		for (auto i = chipicMap.begin(); i != chipicMap.end(); i++)
		{
			if (i->second == CurrentChipic)
			{
				chipicMap.erase(i);
				break;
			}
		}
		CurrentChipic.reset();
	}
}

void ChipicManager::closeCurrentChipic()
{

}

#ifndef MY_QTCMY_DEBUG
#include "moc_ChipicManager.cpp"
#endif
