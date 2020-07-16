#include "Contorl.h"
#include <qdebug.h>
#include "LonelinessMode.h"
#include "MessageSender.h"
#include "MessageTransition.h"
#include "ChipicManager.h"
#include "LocalEimtter.h"
#include <FCConfig.h>
#include <Base\Interpreter.h>
Contorl::Contorl(QWidget *parent)
	: QMainWindow(parent)
{
	ui.setupUi(this);
	
	connect(&contorlButtonBar, SIGNAL(buttonClicked(int)), this, SLOT(buttonClinked(int)));
	connect(&chipicManager, SIGNAL(currentChipicStateUpdate()), this, SLOT(chipicStateUpdate()));

	auto sender = MessageSender::GetInstance();
	sender->setEmitter(new LocalEmitter);

}

void Contorl::getM3dPathForRunPython()
{
	Base::InterpreterSingleton python;
	python.runString("import Control.controlCommand.LonelinessCmd");
	python.runString("lonemod = Control.controlCommand.LonelinessCmd.LonelinessCmd()");
	python.runString("lonemod.setM3dPath()");
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
		return;
	contorlDataBar.setChipicData(chipic);
	contorlButtonBar.setChipicData(chipic);
}

void Contorl::buttonClinked(int buttonType)
{
	switch (ContorlButtonBar::ButtonType(buttonType))
	{
	case ContorlButtonBar::RUN:
		getM3dPathForRunPython();
		chipicManager.runButtonClicked(m3dPath);
		break;
	case ContorlButtonBar::PARALLE_RUN:
		getM3dPathForRunPython();
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
		break;
	default:
		break;
	}
}

#include "moc_Contorl.cpp"