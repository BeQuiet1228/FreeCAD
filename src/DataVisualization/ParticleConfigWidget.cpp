#include "ParticleConfigWidget.h"
#include "ui_ParticleConfigWidget.h"
#include "QPushButton"
#include "CustomConfig.h"
#include "C_encoding.h"
DV::ParticleConfigWidget::ParticleConfigWidget(QWidget* parent /*= nullptr*/)
	:QWidget(parent), ui(new Ui::ParticleConfigWidget)
{
	ui->setupUi(this);
	initUi();
}

DV::ParticleConfigWidget::~ParticleConfigWidget()
{

}

void DV::ParticleConfigWidget::loadConfig()
{
	Config::GetInstance()->loadConfig();
	auto Group = Config::GetInstance()->getRootGroup();
	auto particlegroup = Group.getGroup("particle");
	setButtonColor(ui->partcleColor, particlegroup.getGroup("color").getValue("value"));
	//partcleConfig._2nd = QString::fromStdString(particlegroup.getGroup("color").getValue("value"));
	auto size = atoi(particlegroup.getGroup("size").getValue("value").c_str());
	if (0 == size)size = 1;
	ui->partcleEdit->setText(QString::number(size));
	ui->partclecheckBox->setCheckState((QString::fromStdString(particlegroup.getGroup("AlisAttitude").getValue("isAlis")).toInt()) ? Qt::Checked : Qt::Unchecked);
}

void DV::ParticleConfigWidget::saveConfig()
{
	Config::GetInstance()->loadConfig();
	ConfigGroup Group = Config::GetInstance()->getRootGroup();
	auto particlegroup = Group.getGroup("particle");
	auto particleSize = ui->partcleEdit->text().toStdString();
	particlegroup.getGroup("size").setSetting("value", particleSize);
	particlegroup.getGroup("color").setSetting("value", getButtonColorstr(ui->partcleColor));
	(ui->partclecheckBox->checkState() == Qt::Checked) ? particlegroup.getGroup("AlisAttitude").setSetting("isAlis", "1") : particlegroup.getGroup("AlisAttitude").setSetting("isAlis", "0");
	Config::GetInstance()->saveFile();
}

void DV::ParticleConfigWidget::initUi()
{
	this->setWindowTitle(GetEncodingstr("Á£×ÓÍ¼",ENCODING_GB2312));
	SETPERPORE(ui->partcleColor, btnClicked());
}

void DV::ParticleConfigWidget::btnClicked()
{
	auto button = dynamic_cast<QPushButton*>(sender());
	auto color = setButtonColor(button);
}

#include "moc_ParticleConfigWidget.cpp"