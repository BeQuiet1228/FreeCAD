#include "Contorl.h"
#include <qdebug.h>
#include "LonelinessMode.h"
#include "MessageManager.h"
#include "MessageTransition.h"
#include "ChipicManager.h"
Contorl::Contorl(QWidget *parent)
	: QMainWindow(parent)
{
	ui.setupUi(this);
}

void Contorl::on_pushButton_clicked()
{
	auto messageManager = MessageManager::GetInstance();
	messageManager->sendJsonMessage(MessageTransition::creatRunChipicJsonMessage(this->ui.lineEdit->text().toStdString(), 1));
	auto manager = new ChipicManager;

}
#include "moc_Contorl.cpp"