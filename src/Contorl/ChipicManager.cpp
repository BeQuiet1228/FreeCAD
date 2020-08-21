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
#include "ContorlDataBar.h"
#include "LoadingDialog.h"
#include "NetworkClient.h"
ChipicManager::ChipicManager()
{
	auto getter = JsonMessageGetter::GetInstance();
#ifndef SERVICE
	connect(getter.get(), SIGNAL(hasNewMessage()), this, SLOT(hasNewMessage()));
#endif // !SERVICE

	loadingDialog = new LoadingDialog;
}

ChipicManager::~ChipicManager()
{
	delete loadingDialog;
}

/**
* @brief ChipicManager::hasNewMessage 获取json消息获取器中的消息  然后交给对应chipic对象处理
* @return void
*/
void ChipicManager::hasNewMessage()
{
	/*
	*[1] 获取消息获取器中的消息
	*[2] 处理消息cmd消息，如果是cmd消息则不往下执行
	*[3] 获取消息中的线程id
	*[4] 通过线程id寻找chipic对象,未找到对象就不处理
	*[5] 将json对应给到对应的chipic对象处理
	*/
	auto msgGetter = JsonMessageGetter::GetInstance();

	std::string jsonMsg;
	//[1]
	while (msgGetter->getJsonMessage(jsonMsg))
	{
		//[2]
		if (disposeMessage(jsonMsg))
			return;

		neb::CJsonObject jsonObject(jsonMsg);
		std::string temp;
		//[3]
		if (!jsonObject.Get("threadID", temp))
		{
#if MY_DEBUG
			std::cerr << "ChipicManager hasNewMessgae jsonObject get threadid faild" << std::endl;
#endif // MY_DEBUG

			return;
		}
		//[4]
		DWORD threadID = std::stol(temp);
		auto chipicIterator = chipicMap.find(threadID);
		
		std::shared_ptr<Chipic> chipic;

		if (chipicIterator == chipicMap.end())
		{
			return;

		}else{
			chipic = chipicIterator->second;
		}

		//[5]
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
		if (CurrentChipic.get() == chipic->second.get())
			emit currentChipicStateUpdate();
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
		sendStartChipicMessage(m3dPath, 1);
	}else{
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
		//获取并行线程
		int threadCount = 1;
		ThreadCountDialog dialog;
		dialog.exec();
		if (!dialog.okBuutonClicked)
			return;
		threadCount = dialog.threadCount;
		
		sendStartChipicMessage(m3dPath, threadCount);

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

/**
* @brief ChipicManager::disposeMessage
* @param const std::string & json
* @return bool
*/
bool ChipicManager::disposeMessage(const std::string& json)
{
	neb::CJsonObject jsonObject(json);
	std::string cmd = "";
	if (jsonObject.Get("cmd", cmd))
	{
		std::string threadID;
		if (!jsonObject.Get("threadID", threadID))
			return false;
		long int id = std::stol(threadID);

		if (cmd == "CloseChipic")
		{
			disposeCloseChipicMessage(id);
			return true;
		}else if(cmd  == "startFinished"){
			dispoesStartChipicMessage(json);
			return true;
		}
	}

	return false;
}

/**
* @brief ChipicManager::disposeCloseChipicMessage
* @param const DWORD & threadId
* @return bool
*/
bool ChipicManager::disposeCloseChipicMessage(const DWORD& threadId)
{
	auto  chipic = chipicMap.find(threadId);
	if (chipic != chipicMap.end())
	{
		if (CurrentChipic.get() == chipic->second.get())
		{
			CurrentChipic.reset();
		}
		chipicMap.erase(chipic);
		emit currentChipicStateUpdate();
	}

	return true;
}

/**
* @brief ChipicManager::dispoesStartChipicMessage 处理chipic启动完成消息
* @param const std::string json
* @return bool
*/
bool ChipicManager::dispoesStartChipicMessage(const std::string json)
{
	loadingDialog->close();

	//新建计算程序，用于启动时未获取线程id时暂存
	std::shared_ptr<Chipic> newChipic(new Chipic);
	//获取chipic的各种信息
	neb::CJsonObject jsonObject(json);
	std::string temp;

	jsonObject.Get("threadID", temp);
	DWORD threadId = std::stol(temp);

	MessageTransition::getPath(jsonObject, temp);
	std::string m3dPath = temp;

	jsonObject.Get("threadCount", temp);
	int threadCount = std::stoi(temp);

	newChipic->threadID = threadId;
	newChipic->runState = true;
	newChipic->m3dPath = m3dPath;
	newChipic->threadCount = threadCount;
	chipicMap.insert(std::map<DWORD, std::shared_ptr<Chipic>>::value_type(newChipic->threadID, newChipic));
	connect(newChipic.get(), SIGNAL(stateUpdate(DWORD)), this, SLOT(chipicStateUpdate(DWORD)));
	CurrentChipic = newChipic;
	newChipic.reset();
	emit currentChipicStateUpdate();

	return true;
}

/**
* @brief ChipicManager::sendStartChipicMessage 发送chipic启动消息
* @param const std::string & path
* @param const int & threadCount
* @return void
*/
void ChipicManager::sendStartChipicMessage(const std::string& path, const int& threadCount)
{
	//判断路径是否存在
	if (!detectionFilePathUTF8(path))
		return;
	//发送启动消息
	auto sender = MessageSender::GetInstance();
	
	//如果消息发射器为网络发射器 则需要判断客户端是否已是登录状态
	if (sender->getEmitterTypeID() == 2)
	{
		auto client = NetworkClient::GetInstance();
		//如果客户端处于未登录状态 则显示登录提示框
		if (!client->login)
		{
			client->showLocginDialog();
			return;
		}
	}
	sender->sendJsonMessage(MessageTransition::creatRunChipicJsonMessage(path, threadCount));

	//显示loading提示框
	loadingDialog->show();
}

#ifndef MY_QTCMY_DEBUG
#include "moc_ChipicManager.cpp"
#endif
