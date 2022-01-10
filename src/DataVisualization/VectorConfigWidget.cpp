#include "VectorConfigWidget.h"
#include "ui_VectorConfigWidget.h"
#include "QPushButton"
#include "CustomConfig.h"
#include "C_encoding.h"
DV::VectorConfigWidget::VectorConfigWidget(QWidget* parent /*= nullptr*/)
	:QWidget(parent), ui(new Ui::VectorConfigWidget)
{
	ui->setupUi(this);
	initUi();
}

DV::VectorConfigWidget::~VectorConfigWidget()
{

}

void DV::VectorConfigWidget::loadConfig()
{
	Config::GetInstance()->loadConfig();
	auto Group = Config::GetInstance()->getRootGroup();
	auto vectorGroup = Group.getGroup("vector");
	setButtonColor(ui->vecColor, vectorGroup.getGroup("vectorColor").getValue("value"));
	//vecconfig._2nd = QString::fromStdString(vectorGroup.getGroup("vectorColor").getValue("value"));
	QString vectorsize = QString::fromStdString(vectorGroup.getGroup("vectorsize").getValue("value"));
	toComboxIndex(ui->vectorSize, vectorsize);
	ui->veccheckBox->setCheckState((QString::fromStdString(vectorGroup.getGroup("AlisAttitude").getValue("isAlis")).toInt()) ? Qt::Checked : Qt::Unchecked);
	ui->disMode->setCheckState((QString::fromStdString(vectorGroup.getGroup("disMode").getValue("value")).toInt()) ? Qt::Checked : Qt::Unchecked);
}

void DV::VectorConfigWidget::saveConfig()
{
	Config::GetInstance()->loadConfig();
	ConfigGroup Group = Config::GetInstance()->getRootGroup();
	auto vectorGroup = Group.getGroup("vector");
	auto vecsizestr = (ui->vectorSize->itemText(ui->vectorSize->currentIndex())).toStdString();
	vectorGroup.getGroup("vectorsize").setSetting("value", vecsizestr);
	//vectorGroup.setSetting("vectorsize", vecsizestr);
	
	//vectorGroup.getGroup("vectorColor").setSetting("value", vecconfig._2nd.toStdString());
	vectorGroup.getGroup("vectorColor").setSetting("value", getButtonColorstr(ui->vecColor));
	//vectorGroup.setSetting("vectorColor", vecconfig._2nd.toStdString());

	(ui->veccheckBox->checkState() == Qt::Checked) ? vectorGroup.getGroup("AlisAttitude").setSetting("isAlis", "1") :
		vectorGroup.getGroup("AlisAttitude").setSetting("isAlis", "0");

	(ui->disMode->checkState() == Qt::Checked) ? vectorGroup.getGroup("disMode").setSetting("value", "1") :
		vectorGroup.getGroup("disMode").setSetting("value", "0");
	Config::GetInstance()->saveFile();
}

void DV::VectorConfigWidget::initUi()
{
	SETPERPORE(ui->vecColor, btnClicked());
}

void DV::VectorConfigWidget::btnClicked()
{
	auto button = dynamic_cast<QPushButton*>(sender());
	auto color = setButtonColor(button);
}

#include "moc_VectorConfigWidget.cpp"