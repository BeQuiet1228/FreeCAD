#include "Contorl.h"
#include <qdebug.h>
#include "MessageSender.h"
#include "MessageTransition.h"
#include "ChipicManager.h"
#include "LocalEimtter.h"
#include "Chipic.h"
#include "LoadingDialog.h"
#include "NetworkEmitter.h"
#include "openLog.h"

#ifndef SERVICE
	#include <FCConfig.h>
	#include <Base\Interpreter.h>
#endif

Contorl::Contorl(QWidget *parent)
	: QMainWindow(parent)
{
	ui.setupUi(this);
	
	//初始化ui
	contorlButtonBar = new ContorlButtonBar;
	contorlDataBar = new ContorlDataBar;

	connect(&chipicManager, SIGNAL(currentChipicStateUpdate()), this, SLOT(chipicStateUpdate()));
	connectButtonBar();
	//初始化消息发射器
	auto sender = MessageSender::GetInstance();
	sender->setEmitter(new LocalEmitter);

	//LoadingDialog *d = new LoadingDialog;
	//d->show();
#ifdef _CONTORL_EXE_
	this->m3dPath = "C:/Users/Administrator/Desktop/m2d/beam(1).m3d";
#endif // _CONTORL_EXE_

	
}

Contorl::~Contorl()
{
	//delete contorlButtonBar;
	//delete contorlDataBar;
}

void Contorl::getM3dPathForRunPython()
{
#ifndef _CONTORL_EXE_ //判断是否以exe的形式生成模块

#ifndef SERVICE //判断是否是以服务器模式生成模块
	Base::InterpreterSingleton python;
	python.runString("FreeCAD.setM3dPath()");
	python.runString("import Visualization.VisualizationCommand.VisualizationTree as VT");
	python.runStringArg("VT.showPlotTree(\"%s\")", m3dPath.c_str());
#endif

#endif
}

/**
* @brief Contorl::changeConnectionWay 切换连接方式
* @return void
*/
void Contorl::changeConnectionWay()
{
	auto sender = MessageSender::GetInstance();
	EmitterInterface *emitter;
	if (sender->getEmitterTypeID() == 1)
	{
		emitter = new NetworkEmitter;
	}
	else if (sender->getEmitterTypeID() == 2){
		emitter = new LocalEmitter;
	}
	sender->setEmitter(emitter);
	contorlButtonBar->setConnectionWayIcon(sender->getEmitterTypeID());
}

/**
* @brief Contorl::getConnectWay 获取控制模块的连接方式
* @return int 1=本地连接 2=网络连接
*/
int Contorl::getConnectWay()
{
	auto sender = MessageSender::GetInstance();
	return sender->getEmitterTypeID();
}

/**
* @brief Contorl::openLog
* @return void
*/
void Contorl::openLog()
{
	auto log = OpenLog::GetInstance();
	log->openLog();
}

/**
* @brief Contorl::showTreeWidget 显示看图的树控件、前提是已经获取了m3d路径
* @return void
*/
void Contorl::showTreeWidget()
{
#ifndef _CONTORL_EXE_ //判断是否以exe的形式生成模块

#ifndef SERVICE //判断是否是以服务器模式生成模块
	Base::InterpreterSingleton python;
	python.runString("import Visualization.VisualizationCommand.VisualizationTree as VT");
	python.runStringArg("VT.showPlotTree(\"%s\")", m3dPath.c_str());
#endif

#endif
}

/**
* @brief Contorl::closePlot 关闭绘图窗口
* @return void
*/
void Contorl::closePlot()
{
#ifdef _SMART_CONTORL_
	return;
#endif
#ifdef _CONTORL_DLL_
	Base::InterpreterSingleton python;
	python.runString("import Visualization");
	python.runString("Visualization.VisualizationCommand.VisualizationPlot.vPlot.closePlot()");
#endif // _CONTORL_DLL_

}

void Contorl::on_pushButton_clicked()
{
	auto messageManager = MessageSender::GetInstance();
	messageManager->sendJsonMessage(MessageTransition::creatRunChipicJsonMessage(this->ui.lineEdit->text().toStdString(), 1));

}

void Contorl::chipicStateUpdate()
{
	auto chipic = chipicManager.CurrentChipic;
	if (!chipic)
	{
		contorlButtonBar->chipicClose();
		contorlDataBar->chipicClose();
		return;
	}
	contorlDataBar->setChipicData(chipic);
	contorlButtonBar->setChipicData(chipic);
}

void Contorl::buttonClinked(int buttonType)
{
	switch (ContorlButtonBar::ButtonType(buttonType))
	{
	case ContorlButtonBar::RUN:
		//获取m3d路径
		getM3dPathForRunPython();
		//运行m3d
		chipicManager.runButtonClicked(m3dPath);
		//显示树控件
		showTreeWidget();
		break;
	case ContorlButtonBar::PARALLE_RUN:
		//获取m3d路径
		getM3dPathForRunPython();
		//运行m3d
		if(chipicManager.ButtonParalleRunClicked(m3dPath))
			showTreeWidget();
		break;
	case ContorlButtonBar::REFREASH:
		chipicManager.CurrentChipic->refreshButtonClicked();
		break;
	case ContorlButtonBar::PAUSE:
		chipicManager.CurrentChipic->pausButtonClicked();
		break;
	case ContorlButtonBar::TIMER:
		chipicManager.CurrentChipic->timerButtonClicked();
		break;
	case ContorlButtonBar::LOG:
	 	this->openLog();
		break;
	case ContorlButtonBar::CONNECTION_WAY:
		changeConnectionWay();
		break;
	default:
		break;
	}
}

/**
* @brief Contorl::connectButtonBar 连接按钮条的信号跟槽
* @return void
*/
void Contorl::connectButtonBar()
{
	connect(contorlButtonBar, SIGNAL(buttonClicked(int)), this, SLOT(buttonClinked(int)));
}

#include "moc_Contorl.cpp"