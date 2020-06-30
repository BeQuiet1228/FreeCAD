#include "Contorl.h"
#include <qdebug.h>
#include "LonelinessMode.h"
Contorl::Contorl(QWidget *parent)
	: QMainWindow(parent)
{
	ui.setupUi(this);
}

void Contorl::on_pushButton_clicked()
{
	auto lonelineMode = LonelinessMode::getIntance();
	lonelineMode->lonelinessModeOff();
	lonelineMode->startChipic3d(this->ui.lineEdit->text().toStdString());
}
#include "moc_Contorl.cpp"