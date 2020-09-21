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

	connect(contorlButtonBar, SIGNAL(buttonClicked(int)), this, SLOT(buttonClinked(int)));
	connect(&chipicManager, SIGNAL(currentChipicStateUpdate()), this, SLOT(chipicStateUpdate()));

	//初始化消息发射器
	auto sender = MessageSender::GetInstance();
	sender->setEmitter(new LocalEmitter);

	//LoadingDialog *d = new LoadingDialog;
	//d->show();

	//this->m3dPath = "E:/lingshiwenjianjia/MILO_D/MILO_D.m3d";
}

Contorl::~Contorl()
{

}

void Contorl::getM3dPathForRunPython()
{
#ifndef SERVICE
	Base::InterpreterSingleton python;
	python.runString("import Control.controlCommand.LonelinessCmd");
	python.runString("lonemod = Control.controlCommand.LonelinessCmd.LonelinessCmd()");
	python.runString("lonemod.setM3dPath()");
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
* @brief Contorl::openLog
* @return void
*/
void Contorl::openLog()
{
	auto log = OpenLog::GetInstance();
	log->openLog();
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
		break;
	case ContorlButtonBar::PARALLE_RUN:
		//获取m3d路径
		getM3dPathForRunPython();
		//运行m3d
		chipicManager.ButtonParalleRunClicked(m3dPath);
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

#include "moc_Contorl.cpp"