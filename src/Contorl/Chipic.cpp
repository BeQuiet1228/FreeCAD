#include "Chipic.h"
#include <QLabel>
#include <QPushButton>
#include "CJsonObject.hpp"
#include <QString>
#include <Qt>
#include <iostream>
#include <QVBoxLayout>
#include "MessageTransition.h"
#include "MessageSender.h"
#include <QFileInfo>
#include <QProcess>
#include <QMessageBox>

#ifndef SERVICE
#include <FCConfig.h>
#include <Base\Interpreter.h>
#endif // !SERVICE



Chipic::Chipic(DWORD threadID)
{
	this->threadID = threadID;
	init();
	connect(&hintDailog, SIGNAL(buttonClicked(int)), this, SLOT(buttonClicked(int)));

	timer = new QTimer;
	connect(timer, SIGNAL(timeout()), this, SLOT(timerOut()));

	//开启定时器刷新
	timer->start(5 * 1000);
}

Chipic::~Chipic()
{
	delete timer;
}

/**
* @brief Chipic::pausButtonClicked 暂停按钮被点击
* @return void
*/
void Chipic::pausButtonClicked()
{
	if (pausState)
	{
		sendMessage(101, 0, 0);
	}
	else
	{
		sendMessage(102, 0, 0);
	}
}

/**
* @brief Chipic::refreshButtonClicked
* @return void
*/
void Chipic::refreshButtonClicked()
{
	this->sendMessage(104, 0, 0);
	this->sendMessage(105, 0, 0);

}

/**
* @brief Chipic::timerButtonClicked
* @return void
*/
void Chipic::timerButtonClicked()
{
	if (timerSate)
	{
		sendMessage(103, 1, 0);
	}
	else
	{
		sendMessage(103, 0, 0);
	}
}

/**
* @brief Chipic::init
* @return void
*/
void Chipic::init()
{
	//运行状态
	runState = false;
	//暂停状态
	pausState = true;
	//定时器状态
	timerSate = false;
	//迭代次数、当前迭代次数
	iterationCount = 1;
	currentIteration = 1;
	//粒子数目
	particleCount = 0;

	threadCount = 1;

}


/**
* @brief Chipic::sendMessage 发送消息
* @param const UINT & type 消息类型 自动加WM_USER
* @param const WPARAM & wParam 参数
* @param const LPARAM & lParam 参数
* @param const DWORD & thradId 线程id，默认为0，则使用当前对象的threadID
* @return void
*/
void Chipic::sendMessage(const UINT& type, const WPARAM& wParam, const LPARAM& lParam, const DWORD& thradId /*= 0*/)
{
	Message msg;
	if (thradId == 0)
	{
		msg.threadId = this->threadID;
	}else{
		msg.threadId = threadID;
	}
	msg.Msg = type;
	msg.wParam = wParam;
	msg.lParam = lParam;
	std::string json = MessageTransition::winMessageTojson(msg);
	auto messageManager = MessageSender::GetInstance();
	messageManager->sendJsonMessage(json);
}


/**
* @brief Chipic::closeChipic
* @return void
*/
void Chipic::closeChipic()
{
	auto msg = MessageTransition::creatCloseChipicJsonMessage(threadID);
	auto sender = MessageSender::GetInstance();
	sender->sendJsonMessage(msg);
}

/**
* @brief Chipic::openLogFile 打开log文件
* @return void
*/
void Chipic::openLogFile()
{
	auto  path = QString::fromStdString(this->m3dPath);
	path = "notepad.exe " + path.left(path.size() - 4) + ".LOG";

	QProcess process;
	process.start(path);
	process.waitForFinished();

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
		iterationTime = msg.lParam;
		return true;
	}
	else if (msg.wParam == 11)
	{
		iterationTime += (float)msg.lParam / 1000;
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
	if (msg.Msg  == 203)
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
	if (msg.Msg != 201
		&& msg.Msg != 202
		&& msg.Msg != 205)
		return false;

	if (msg.Msg == 201)
		pausState = false;
	if (msg.Msg  == 202)
		pausState = true;
	//同样的功能的消息定义了两次，所以需要处理两次，不知何意
	if (msg.Msg  == 205)
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
		title = titleStr =msg.text;
		break;
	case 2:
		this->titleNumber = std::to_string(msg.lParam);
		title = titleStr + titleNumber;
		break;
	case 3:
		//如果为自动运行模式，则直接发送继续消息
		if (getIsAuto())
		{
			sendMessage(108, 3, -2);
			break;
		}
		hintDailog.setText(msg.text);
		hintDailog.showForMode1();
		break;
	case 4:
		//如果为自动运行模式，则直接发送继续消息
		if (getIsAuto())
		{
			closeChipic();
			break;
		}
		hintDailog.setText(msg.text);
		hintDailog.showForMode3();
		break;
	case 9:
	case 8:
		//如果为自动运行模式，则直接发送继续消息
		if (getIsAuto())
		{
			sendMessage(108, 3, -2);
			break;
		}
		hintDailog.setText(msg.text);
		hintDailog.showForMode2();
		break;
	default:
		return false;
	}
	return true;
}

/**
* @brief Chipic::disposeStructMapMessage 处理结构图消息
* @param const Message & msg
* @return bool
*/
bool Chipic::disposeStructMapMessage(const Message& msg)
{
	if (msg.Msg != 208)
		return false;
	if (msg.wParam != 100 || msg.lParam != 0)
		return false;
#ifndef _CONTORL_EXE_

#ifndef SERVICE
	if (!getIsAuto())
	{
		std::string fileName = this->makePath("_Temp.h5");
		fileName = MessageTransition::utf8StdstringToGbkStdstring(fileName);
		Base::InterpreterSingleton python;
		python.runString("import Control.controlCommand.LonelinessCmd");
		python.runString("lonemod = Control.controlCommand.LonelinessCmd.LonelinessCmd()");
		python.runStringArg("lonemod.openStruct(\'%s\')", fileName.c_str());
	}
	//刷新一下数据
	this->refreshButtonClicked();
	//发送解析完成信号
	emit analysisFinished();
#endif

#endif


	return false;
}

/**
* @brief Chipic::disposResultMapMessage 处理结果图消息
* @param const Message & msg
* @return bool
*/
bool Chipic::disposResultMapMessage(const Message& msg)
{
	if (getIsAuto())
		return false;

	if (msg.Msg == 209)
	{
		if (msg.wParam != -1000 && msg.lParam != -1000)
		{
#ifndef SERVICE
			std::string fileName = this->makePath("_Temp.h5");
			fileName = MessageTransition::utf8StdstringToGbkStdstring(fileName);
			Base::InterpreterSingleton python;
			python.runString("import Control.controlCommand.LonelinessCmd");
			python.runString("lonemod = Control.controlCommand.LonelinessCmd.LonelinessCmd()");
			python.runStringArg("lonemod.openMap(\'%s\',%d,%d)", fileName.c_str(), msg.wParam, msg.lParam);
#endif // !SERVICE
			return  true;
		}
	}

	return false;
}

/**
* @brief Chipic::makePath 按照固定格式 生成文件路径
* @param const std::string & fileName
* @return std::string
*/
std::string Chipic::makePath(const std::string& fileName)
{
	//将winmsg消息转换为文件消息
	//使Python代码直接打开文件
	std::string filePath;
	//去掉文件名的后缀
	QString temp = QString::fromStdString(m3dPath);
	QFileInfo fileInfo(temp);
	QString name = fileInfo.fileName();
	name = name.left(name.size() - 4);
	//将qstring转换为stdstring
	//直接tostdstring中文转换会有问题
	std::string m3dFileName = std::string(name.toLocal8Bit());
	std::string path = std::string(fileInfo.absolutePath().toLocal8Bit());
	if (threadCount > 1)
	{
		filePath = path + "/1/" + m3dFileName + fileName;
	}else if (threadCount == 1) {
		filePath = path + "/" + m3dFileName + fileName;
	}

	return filePath;
}

/**
* @brief Chipic::disposChipicCloseMessage 处理chipic关闭消息
* @param const std::string & json
* @return bool
*/
bool Chipic::disposChipicCloseMessage(const std::string& json)
{
	neb::CJsonObject jsonObject(json);
	std::string cmd = "";
	if (jsonObject.Get("cmd", cmd))
	{
		if (cmd == "CloseChipic")
		{
			runState = false;
			return true;
		}
	}

	return false;
}

/**
* @brief Chipic::disposChipicSendMessagePauseMessage 因为消息队列有大小限制，在消息比较多的时候，计算程序会先发送一部分消息，然后暂停，等待处理完消息 
* @param const Message & msg
* @return bool
*/
bool Chipic::disposChipicSendMessagePauseMessage(const Message& msg)
{
	if (msg.Msg == 250 && msg.wParam == 1)
	{
		if (msg.lParam == 0)
		{
			sendMessage(150, 0, 0);
			this->pausState = true;
		}else{
			this->pausState = false;
		}

		return true;
	}

	return false;
}

/**
* @brief Chipic::disposChipicFinished 处理计算完成消息
* @param const Message & msg
* @return bool
*/
bool Chipic::disposChipicFinished(const Message& msg)
{
	if (msg.Msg != 300)
		return false;
	if (msg.wParam != 200)
		return false;
	if (msg.lParam != 0)
		return false;
	if (timer != nullptr)
		timer->stop();
	//完成的时候就将状态设置为未运行，这里主要可以避免关闭时和异常退出检测发生冲突
	this->runState = false;
	emit workFinished();
	return true;
}

/**
* @brief Chipic::disposChipicBusy
* @param const Message & msg
* @return bool
*/
bool Chipic::disposChipicBusy(const Message& msg)
{
	if (msg.Msg != 260)
		return false;
	QMessageBox box;
	box.setWindowTitle(MessageTransition::gbkStdstringToQstring("提示"));
	box.setText(MessageTransition::gbkStdstringToQstring("计算程序正在绘制其他图形，请勿频繁点击绘图按钮！"));
	box.exec();


	//清空树控件中显示的正在接收文件
#ifndef SERVICE
	std::string fileName = this->makePath("_Temp.h5");
	fileName = MessageTransition::utf8StdstringToGbkStdstring(fileName);
	Base::InterpreterSingleton python;
	python.runString("import Control.controlCommand.LonelinessCmd");
	python.runString("lonemod = Control.controlCommand.LonelinessCmd.LonelinessCmd()");
	python.runStringArg("lonemod.clearTree()");
#endif

	return  true;
}

void Chipic::disposJsonMessage(const std::string& json)
{
	Message msg = MessageTransition::jsonToWinMessage(json);
	//处理提示消息
	if (disposHintMessage(msg))
	{
		emit stateUpdate(this->threadID);
		setIsUpdate(true);
	//	if (msg.wParam == 3 || msg.wParam == 8)
	//		std::cerr << json << std::endl;
		return;
	}
	//处理迭代步数消息
	if (disposIterationCountMessage(msg))
	{
		emit stateUpdate(this->threadID);
		setIsUpdate(true);
		return;
	}
	//处理cpu消耗时间消息
	if (disposUsedTimeMessage(msg))
	{
		emit stateUpdate(this->threadID);
		setIsUpdate(true);
		return;
	}
	//处理粒子数目消息
	if (disposParticleMessage(msg))
	{
		emit stateUpdate(this->threadID);
		setIsUpdate(true);
		return;
	}
	//处理迭代时间消息
	if(disposeIterationTimeMessage(msg))
	{ 
		emit stateUpdate(this->threadID);
		setIsUpdate(true);
		return;
	}
	//处理chipic暂停状态消息
	if (disposeChipicIsPause(msg))
	{
		emit stateUpdate(this->threadID);
		setIsUpdate(true);
		return;
	}
	//输出除了提示消息以外的消息
	//std::cerr << json << std::endl;
	//处理chipic关闭消息
	if (disposChipicCloseMessage(json))
	{
		emit stateUpdate(threadID);
		setIsUpdate(true);
		return;
	}
	//处理器件结构消息
	if (disposeStructMapMessage(msg))
		return;
	//处理定时器状态消息
	if(disposeChipicTimerState(msg))
	{
		emit stateUpdate(this->threadID);
		setIsUpdate(true);
		return;
	}

	//处理发送消息中的暂停消息
	if (disposChipicSendMessagePauseMessage(msg))
	{
		emit stateUpdate(this->threadID);
		setIsUpdate(true);
		return;
	}
	//查看结果图
	if (disposResultMapMessage(msg))
		return;
	//计算程序计算完成
	if (disposChipicFinished(msg))
		return;
	if (disposChipicBusy(msg))
		return;
}


/**
* @brief Chipic::buttonClicked 提示框中的按钮被点击
* @param int clickType 点击类型
* @return void
*/
void Chipic::buttonClicked(int clickType)
{
	switch (HintDailog::ClinkeType(clickType))
	{
	case HintDailog::MODE1_EXIT:
		//sendMessage(108, 3, 4);
		closeChipic();
		break;
	case HintDailog::MODE1_LOSE:
		sendMessage(108, 3, 1);
		break;
	case HintDailog::MODE1_LOSE_ALL:
		sendMessage(108, 3, -1);
		break;
	case HintDailog::MODE1_CONTINUE:
		sendMessage(108, 3, 2);
		break;
	case HintDailog::MODE1_CONTINUE_ALL:
		sendMessage(108, 3, -2);
		break;
	case HintDailog::MODE2_EXIT:
		//sendMessage(108, 8, 3);
		closeChipic();
		break;
	case HintDailog::MODE2_CONTINUE:
		sendMessage(108, 8, 1);
		break;
	case HintDailog::MODE2_CONTINUE_ALL:
		sendMessage(108, 8, -1);
		break;
	case HintDailog::MODE3_EXIT:
		//sendMessage(108, 4, 0);
		closeChipic();
		break;
	case HintDailog::NULL_TYPE:
		break;
	}
}

/**
* @brief Chipic::timerOut 定时器超时
* @return void
*/
void Chipic::timerOut()
{
	/*
		定时发送一个消息出去，然后由消息发送是否成功判断chipic程序是否还在正常运行。
		该消息没有实际意义。
	*/
	/* 2020.12.22 更新
		加上宏判断，避免在生成exe做调试的时候输出过多的调试信息，影响判断
	*/
#ifndef _CONTORL_EXE_
	this->sendMessage(886, 886, 886, this->threadID);
#endif
}

#ifndef MY_QTCMY_DEBUG
#include "moc_Chipic.cpp"
#endif