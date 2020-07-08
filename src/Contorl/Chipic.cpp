#include "Chipic.h"
#include <QLabel>
#include <QPushButton>
#include "CJsonObject.hpp"
#include <QString>
#include <Qt>
#include <iostream>
#include <QVBoxLayout>
#include "LonelinessMode.h"
#include "MessageTransition.h"
#include "MessageManager.h"
Chipic::Chipic(DWORD threadID)
{
	this->threadID = threadID;
}

Chipic::~Chipic()
{

}

/**
* @brief Chipic::pausButtonClicked 暂停按钮被点击
* @return void
*/
void Chipic::pausButtonClicked()
{
	Message msg;
	msg.threadId = threadID;
	msg.Msg = 101;
	std::string json = MessageTransition::winMessageTojson(msg);
	
	auto messageManager = MessageManager::GetInstance();
	messageManager->sendJsonMessage(json);
}

/**
* @brief Chipic::refreshButtonClicked
* @return void
*/
void Chipic::refreshButtonClicked()
{
	Message msg;
	msg.threadId = threadID;
	msg.Msg = 104;
	std::string json = MessageTransition::winMessageTojson(msg);

	auto messageManager = MessageManager::GetInstance();
	messageManager->sendJsonMessage(json);

}

/**
* @brief Chipic::timerButtonClicked
* @return void
*/
void Chipic::timerButtonClicked()
{

}

/**
* @brief Chipic::disposIterationCountMessage 处理迭代时间消息
* @param const Message & msg
* @return bool
*/
bool Chipic::disposIterationCountMessage(const Message& msg)
{
	if (msg.Msg != 204)
		return false;

	if (msg.wParam == 1)
	{
		this->currentIteration = msg.lParam;
		return true;
	}
	else if (msg.wParam == 2)
	{
		this->iterationCount = msg.lParam;
		return true;
	}
		
	return false;
}

/**
* @brief Chipic::disposUsedTimeMessage 处理消耗时间消息
* @param const Message & msg
* @return bool
*/
bool Chipic::disposUsedTimeMessage(const Message& msg)
{
	if (msg.Msg != 204)
		return false;
	switch (msg.wParam)
	{
	case 3:
		this->currentUsedTime.hour = msg.lParam;
		return true;
	case 4:
		this->currentUsedTime.minute = msg.lParam;
		return true;
	case 5:
		this->currentUsedTime.second = msg.lParam;
		return true;
	case 6:
		this->UsedTime.hour = msg.lParam;
		return true;
	case 7:
		this->UsedTime.minute = msg.lParam;
		return true;
	case 8:
		this->UsedTime.second = msg.lParam;
		return true;
	}
	return false;
}

/**
* @brief Chipic::disposParticleMessage 处理粒子数目
* @param const Message & msg
* @return bool
*/
bool Chipic::disposParticleMessage(const Message& msg)
{
	if (msg.Msg != 204)
		return false;
	if (msg.wParam == 9)
	{
		this->particleCount = msg.lParam;
		return true;
	}
	return false;
}

/**
* @brief Chipic::disposeIterationTimeMessage 处理迭代时间
* @param const Message & msg
* @return bool
*/
bool Chipic::disposeIterationTimeMessage(const Message& msg)
{
	if (msg.Msg != 204)
		return false;
	if (msg.wParam == 10)
	{
		iterationTimeInt = msg.lParam;
		return true;
	}
	else if (msg.wParam == 11)
	{
		iterationTimeFloat = msg.lParam;
		return true;
	}

	return false;
}

/**
* @brief Chipic::disposeChipicTimerState 处理定时器状态消息
* @param const Message & msg
* @return bool
*/
bool Chipic::disposeChipicTimerState(const Message& msg)
{
	if (msg.Msg - WM_USER == 203)
	{
		if (msg.wParam == 1)
			timerSate = true;
		else {
			timerSate = false;
		}
		return true;
	}
	return false;
}

/**
* @brief Chipic::disposeChipicIsPause 处理chipic暂停状态消息
* @param const Message & msg
* @return bool
*/
bool Chipic::disposeChipicIsPause(const Message& msg)
{
	//如果不是对应的消息，则返回false
	if (msg.Msg - WM_USER != 201
		&& msg.Msg - WM_USER != 202
		&& msg.Msg - WM_USER != 205)
		return false;

	if (msg.Msg - WM_USER == 201)
		pausState = false;
	if (msg.Msg - WM_USER == 202)
		pausState = true;
	//同样的功能的消息定义了两次，所以需要处理两次，不知何意
	if (msg.Msg - WM_USER == 205)
	{
		if (msg.wParam == 0)
			pausState = true;
		else {
			pausState = false;
		}
	}
	return  true;
}

/**
* @brief Chipic::disposHintMessage 处理提示信息消息
* @param const Message & msg
* @return bool
*/
bool Chipic::disposHintMessage(const Message& msg)
{
	if (msg.Msg != 208)
		return false;
	switch (msg.wParam)
	{
	case 1:
	case 5:
	case 6:
	case 7:
		this->titile = msg.text;
		break;
	case 2:
		this->titleNumber = std::to_string(msg.lParam);
		break;
	case 3:
		hintDailog.setText(msg.text);
		hintDailog.showForMode1();
		break;
	case 4:
		hintDailog.setText(msg.text);
		hintDailog.showForMode3();
		break;
	case 8:
		hintDailog.setText(msg.text);
		hintDailog.showForMode2();
		break;
	}
	return true;
}

void Chipic::disposJsonMessage(const std::string& json)
{
	Message msg = MessageTransition::jsonToWinMessage(json);

	//处理迭代步数消息
	if (disposIterationCountMessage(msg))
		return;
	//处理cpu消耗时间消息
	if(disposUsedTimeMessage(msg))
		return;
	//处理粒子数目消息
	if(disposParticleMessage(msg))
		return;
	//处理迭代时间消息
	if(disposeIterationTimeMessage(msg))
		return;
	//处理定时器状态消息
	if(disposeChipicTimerState(msg))
		return;
	//处理chipic暂停状态消息
	if(disposeChipicIsPause(msg))
		return;
	//处理提示消息
	if (disposHintMessage(msg))
	{
		emit stateUpdate(this->threadID);
		return;
	}

}

void Chipic::buttonClicked()
{
	std::cerr << "mmm" << std::endl;
	pausButtonClicked();
}

#ifndef MY_QTC_DEBUG
#include "moc_Chipic.cpp"
#endif