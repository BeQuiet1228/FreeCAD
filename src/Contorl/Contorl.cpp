#include "Contorl.h"
#include <qdebug.h>
#include "LonelinessMode.h"
#include "MessageSender.h"
#include "MessageTransition.h"
#include "ChipicManager.h"
#include "LocalEimtter.h"
Contorl::Contorl(QWidget *parent)
	: QMainWindow(parent)
{
	ui.setupUi(this);
	
	connect(&contorlButtonBar, SIGNAL(buttonClicked(int)), this, SLOT(buttonClinked(int)));
	connect(&chipicManager, SIGNAL(currentChipicStateUpdate()), this, SLOT(chipicStateUpdate()));

	contorlButtonBar.show();
	contorlDataBar.show();
	auto sender = MessageSender::GetInstance();
	sender->setEmitter(new LocalEmitter);

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
		chipicManager.runButtonClicked(m3dPath);
		break;
	case ContorlButtonBar::PARALLE_RUN:
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