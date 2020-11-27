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
#include "openLog.h"
#include "ContorlDataBar.h"
#include "ContorlButtonBar.h"
#include "LocalEimtter.h"
ChipicManager::ChipicManager()
{
	auto getter = JsonMessageGetter::GetInstance();
#ifndef SERVICE
	connect(getter.get(), SIGNAL(hasNewMessage()), this, SLOT(hasNewMessage()));
#endif // !SERVICE

	loadingDialog = new LoadingDialog;
	connect(loadingDialog, SIGNAL(dialogClose()), this, SLOT(loadDialogClose()));
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
	if (chipic == chipicMap.end())
		return;

	//如果是当前chipic信息更新，则发送更新信息。
	if (!CurrentChipic)
		return;
	if (CurrentChipic->threadID != threadId)
		return;
	//如果dailog还在显示状态，说明chipic还没有解析完文本
	//则所有的提示信息都在提示框中显示
	if (loadingDialog->isShow)
	{
		loadingDialog->setText(CurrentChipic->title);
	}else{
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
* @brief ChipicManager::chipicWorkFinished chipic计算完成
* @return void
*/
void ChipicManager::chipicWorkFinished()
{
	//获取信号发送者
	auto sender = this->sender();
	auto chipic = dynamic_cast<Chipic *>(sender);
	if (!chipic)
		return;
	emit finishChipicM3dPath(chipic->threadID);
	showWorkFinishedBox();
	chipic->closeChipic();
}

/**
* @brief ChipicManager::chipicAnalysisFinished chipic解析完成槽
* @return void
*/
void ChipicManager::chipicAnalysisFinished()
{
	loadingDialog->close();
}

/**
* @brief ChipicManager::loadDialogClose load提示框被关闭
* @return void
*/
void ChipicManager::loadDialogClose()
{
	this->runButtonClicked();
}

/**
* @brief ChipicManager::closeAllChipic
* @return void
*/
void ChipicManager::closeAllChipic()
{
	for (auto i = chipicMap.begin(); i != chipicMap.end(); i++)
	{
		i->second->closeChipic();
	}
	chipicMap.clear();
}

void ChipicManager::closeChipic(const unsigned long threadID)
{
	auto chipic = chipicMap.find(threadID);
	if (chipic == chipicMap.end())
		return;
	chipic->second->closeChipic();
}
/**
* @brief ChipicManager::initMessageSender
* @return void
*/
void ChipicManager::initMessageSender()
{
	//初始化消息发射器
	auto sender = MessageSender::GetInstance();
	sender->setEmitter(new LocalEmitter);
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
			std::string errorCode = "0";
			MessageTransition::getErrorCOde(jsonObject,errorCode);
			disposeCloseChipicMessage(id,std::stoi(errorCode));
			return true;
		}else if(cmd  == "startFinished"){
			dispoesStartChipicMessage(json);
			return true;
		}
	}

	return false;
}


/**
* @brief ChipicManager::disposeCloseChipicMessage 处理chipic关闭消息
* @param const DWORD & threadId
* @param const int & errorCode 错误代码  从json消息中获取
* @return bool
*/
bool ChipicManager::disposeCloseChipicMessage(const DWORD& threadId, const int& errorCode)
{
	//如果id为0则清理掉所有的chipic对象
	if (threadId == 0)
	{
		//更改所有chipic的运行状态
		for (auto i = chipicMap.begin(); i != chipicMap.end(); i++)
		{
			i->second->runState = false;
		}
		chipicMap.clear();
		CurrentChipic.reset();
		emit currentChipicStateUpdate();
		return true;
	}
	/*
		如果id不为0 则寻找对应的chipic关闭
		判断错误代码。
		这个错误代码主要针对chipic在非正常退出的情况下。
		0 为正常退出
		1 为异常结束 异常结束的时候需要chipic管理器对象发送关闭消息释放监听器。
		因为在释放监听器的时候 监听器还会返回一个关闭消息，所以这里就先不处理关闭消息。
	*/
	auto  chipic = chipicMap.find(threadId);
	if (chipic == chipicMap.end())
		return false;
	//设置chipic运行状态
	chipic->second->runState = false;
	//正常退出
	if (errorCode == 0)
	{
		//移除chipic对象
		if (CurrentChipic.get() == chipic->second.get())
		{
			CurrentChipic.reset();
		}
		chipicMap.erase(chipic);
			
		emit currentChipicStateUpdate();
		loadingDialog->close();
	}else if (errorCode == 1){
		showDailLog("提示", "chipic异常退出");
		chipic->second->closeChipic();
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
	//新建chipic对象
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

	//根据运行模式 设置是否处理看图消息
	if (runType == AUTO)
		newChipic->setIsAuto(true);

	//将对象放入map
	chipicMap.insert(std::map<DWORD, std::shared_ptr<Chipic>>::value_type(newChipic->threadID, newChipic));
	//链接数据更新槽
	connect(newChipic.get(), SIGNAL(stateUpdate(DWORD)), this, SLOT(chipicStateUpdate(DWORD)));
	//链接计算完成槽
	connect(newChipic.get(), SIGNAL(workFinished()), this, SLOT(chipicWorkFinished()));
	//链接解析完成槽
	connect(newChipic.get(), SIGNAL(analysisFinished()), this, SLOT(chipicAnalysisFinished()));

	CurrentChipic = newChipic;
	newChipic.reset();
	emit currentChipicStateUpdate();

	//发送chipic启动完成信号
	emit chipicStartFinished(threadId);

	return true;
}

/**
* @brief ChipicManager::showLoadDailog 显示载入的提示框
* @return void
*/
void ChipicManager::showLoadDailog()
{
	//显示loading提示框
	if (runType == AUTO)
		return;
	loadingDialog->setText("CHIPIC正在启动中");
	loadingDialog->show();

		
}

/**
* @brief ChipicManager::showWorkFinishedBox 弹出计算完成提示框
* @return void
*/
void ChipicManager::showWorkFinishedBox()
{
	//判断是否显示提示框
	if (runType == AUTO)
		return;
	QMessageBox box;
	box.setWindowTitle(MessageTransition::gbkStdstringToQstring("提示框"));
	box.setText(MessageTransition::gbkStdstringToQstring("计算程序已完成计算，自动退出！"));
	box.exec();
}

/**
* @brief ChipicManager::showDailLog
* @param const std::string & title
* @param const std::string & content
* @return void
*/
void ChipicManager::showDailLog(const std::string& title, const std::string& content)
{
	if (runType == AUTO)
		return;
	QMessageBox box;
	box.setWindowTitle(MessageTransition::gbkStdstringToQstring(title));
	box.setText(MessageTransition::gbkStdstringToQstring(content));
	box.exec();
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
	//设置当前log文件的路径
	auto log = OpenLog::GetInstance();
	log->setCurrentChipicM3dPath(path,threadCount);
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

	showLoadDailog();

}

/**
* @brief ChipicManager::getM3dpathForThreadID 根据线程id获取一个 chipic的m3d路径
* @param unsigned long threadID
* @return QString
*/
QString ChipicManager::getM3dpathForThreadID(unsigned long threadID)
{
	auto chipic = chipicMap.find(threadID);
	if (chipic == chipicMap.end())
		return "";
	auto temp = chipic->second->m3dPath;
	
	QString result = QString::fromStdString(temp);
	return result;
}

#ifndef MY_QTCMY_DEBUG
#include "moc_ChipicManager.cpp"
#endif
