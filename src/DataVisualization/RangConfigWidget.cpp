#include "RangConfigWidget.h"
#include "ui_RangConfigWidget.h"
#include "QPushButton"
#include "CustomConfig.h"
#include "C_encoding.h"
DV::RangConfigWidget::RangConfigWidget(QWidget* parent /*= nullptr*/)
	:QWidget(parent), ui(new Ui::RangConfigWidget)
{
	ui->setupUi(this);
	initUi();
}

DV::RangConfigWidget::~RangConfigWidget()
{

}

void DV::RangConfigWidget::loadConfig()
{
	Config::GetInstance()->loadConfig();
	ConfigGroup Group = Config::GetInstance()->getRootGroup();
	auto timeGroup = Group.getGroup("observe");
	setButtonColor(ui->lineColor, timeGroup.getGroup("lineColor").getValue("value"));
	//timeConfig._2nd = QString::fromStdString(timeGroup.getGroup("lineColor").getValue("value"));
	QString linesize = QString::fromStdString(timeGroup.getGroup("lineSize").getValue("value"));
	toComboxIndex(ui->linesSizeEdit, linesize);
	ui->linescheckBox->setCheckState((QString::fromStdString(timeGroup.getGroup("AlisAttitude").getValue("isAlis")).toInt() == 1) ? Qt::Checked : Qt::Unchecked);
}

void DV::RangConfigWidget::saveConfig()
{
	Config::GetInstance()->loadConfig();
	ConfigGroup Group = Config::GetInstance()->getRootGroup();
	auto timeGroup = Group.getGroup("observe");
	QString pensize = ui->linesSizeEdit->itemText(ui->linesSizeEdit->currentIndex());
	timeGroup.getGroup("lineSize").setSetting("value", pensize.toStdString());
	//timeGroup.setSetting("lineSize", pensize.toStdString());
	
	timeGroup.getGroup("lineColor").setSetting("value", getButtonColorstr(ui->lineColor));
	//timeGroup.setSetting("lineColor", timeConfig._2nd.toStdString());
	//¿¹¾â³Ý
	auto AlisAttitude = timeGroup.getGroup("AlisAttitude");
	(ui->linescheckBox->checkState() == Qt::Checked) ? AlisAttitude.setSetting("isAlis", "1") : AlisAttitude.setSetting("isAlis", "0");
	Config::GetInstance()->saveFile();
}

void DV::RangConfigWidget::initUi()
{
	this->setWindowTitle(GetEncodingstr("Ê±¼äÍ¼",ENCODING_GB2312));
	SETPERPORE(ui->lineColor, btnClicked());
}

void DV::RangConfigWidget::btnClicked()
{
	auto button = dynamic_cast<QPushButton*>(sender());
	auto color = setButtonColor(button);
}
#include "moc_RangConfigWidget.cpp"