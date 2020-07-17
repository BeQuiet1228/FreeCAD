#include "ChipicManager.h"
#include "JsonMessageGetter.h"
#include "CJsonObject.hpp"
#include <iostream>
#include "JsonMessageGetter.h"
#include "MessageSender.h"
#include "MessageTransition.h"
#include "Chipic.h"
#include "ThreadCountDialog.h"
#include <QDir>
#include <QMessageBox>
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
	*[3] 通过线程id寻找chipic对象，如果未找到对应的chipic对象，则判断是否有未获取线程id的chipic对象，如有有则
	*	 赋值线程id，然后将对象加入map，并处理消息
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
			//如果存在未获取线程id的chipic对象
			if (newChipic)
			{
				newChipic->threadID = threadID;
				newChipic->runState = true;
				chipic = newChipic;
				newChipic.reset();
				chipicMap.insert(std::map<DWORD, std::shared_ptr<Chipic>>::value_type(chipic->threadID, chipic));
				connect(chipic.get(), SIGNAL(stateUpdate(DWORD)), this, SLOT(chipicStateUpdate(DWORD)));
				emit currentChipicStateUpdate();
			}else{
				return;
			}

		}else{
			chipic = chipicIterator->second;
		}

		//[4]
		chipic->disposJsonMessage(jsonMsg);

	}
}

/**
* @brief ChipicManager::chipicStateUpdate chipic状态更新槽
* @param DWORD threadId
* @return void
*/
void ChipicManager::chipicStateUpdate(DWORD threadId)
{
	auto  chipic = chipicMap.find(threadId);
	if (chipic != chipicMap.end())
	{
		//判断chipic的运行状态 如果没有在运行 则释放掉对象
		if (!(chipic->second->runState))
		{
			if (CurrentChipic.get() == chipic->second.get())
			{
				CurrentChipic.reset();
				emit currentChipicStateUpdate();	
			}
			chipicMap.erase(chipic);
		}else{
			if (CurrentChipic.get() == chipic->second.get())
				emit currentChipicStateUpdate();
		}
	}
}

/**
* @brief ChipicManager::runButtonClicked 运行按钮被点击
* @param const std::string & m3dPtah 路径
* @return void
*/
void ChipicManager::runButtonClicked(const std::string& m3dPath /*= ""*/)
{
	if (!CurrentChipic)
	{
		//判断路径是否存在
		if (!detectionFilePathUTF8(m3dPath))
			return;
		//暂存一个新建chipic对象，直到获取到线程id
		newChipic.reset(new Chipic(0));
		CurrentChipic = newChipic;
		newChipic->m3dPath = m3dPath;
		newChipic->threadCount = 1;
		auto messageManager = MessageSender::GetInstance();
		messageManager->sendJsonMessage(MessageTransition::creatRunChipicJsonMessage(m3dPath, 1));


	}
	else{
		CurrentChipic->closeChipic();
	}
}

void ChipicManager::closeCurrentChipic()
{

}

/**
* @brief ChipicManager::ButtonParalleRunClicked
* @param const std::string & m3dPath
* @param const int & threadCount
* @return void
*/
void ChipicManager::ButtonParalleRunClicked(const std::string& m3dPath)
{
	if (!CurrentChipic)
	{
		//判断路径是否存在
		if (!detectionFilePathUTF8(m3dPath))
			return;
		//获取并行线程
		int threadCount = 1;
		ThreadCountDialog dialog;
		dialog.exec();
		if (!dialog.okBuutonClicked)
			return;
		threadCount = dialog.threadCount;

		//暂存一个新建chipic对象，直到获取到线程id
		newChipic.reset(new Chipic(0));
		CurrentChipic = newChipic;
		newChipic->m3dPath = m3dPath;
		newChipic->threadCount = threadCount;
		auto messageManager = MessageSender::GetInstance();
		messageManager->sendJsonMessage(MessageTransition::creatRunChipicJsonMessage(m3dPath, threadCount));


	}else{

	}
}

/**
* @brief ChipicManager::detectionFilePathUTF8 检测路径是否存在 路径为utf8编码
* @param const std::string & path
* @return bool
*/
bool ChipicManager::detectionFilePathUTF8(const std::string& path)
{
	auto temp = QString::fromStdString(path);
	QDir dir;
	if (!dir.exists(temp))
	{
		QMessageBox box;
		box.setText(MessageTransition::gbkStdstringToQstring("路径不存在，路径: ") + temp);
		box.exec();
		return false;
	}

	return true;
}

#ifndef MY_QTCMY_DEBUG
#include "moc_ChipicManager.cpp"
#endif
