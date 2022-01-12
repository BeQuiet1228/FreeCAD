#include "Particle3dConfigWidget.h"
#include "ui_Particle3dConfigWidget.h"
#include "../CustomConfig.h"
#include "../C_encoding.h"
DV3D::Particle3dConfigWidget::Particle3dConfigWidget(QWidget* parent/*=nullptr*/)
	:QWidget(parent),ui(new Ui::Particle3dConfigWidget)
{
	ui->setupUi(this);
	initUi();
}
DV3D::Particle3dConfigWidget::~Particle3dConfigWidget()
{

}
void DV3D::Particle3dConfigWidget::loadConfig()
{
	DV::Config::GetInstance()->loadConfig();
	auto Group = DV::Config::GetInstance()->getRootGroup();
	auto particleGroup = Group.getGroup("particle3d");
	std::string particleColor = particleGroup
		.getGroup("particleColor")
		.getValue("value");
	std::string particleSize = particleGroup
		.getGroup("particleSize")
		.getValue("value");
	setButtonColor(ui->particleColor,particleColor);
	ui->particleSize->setText(QString::fromStdString(particleSize));
}
void DV3D::Particle3dConfigWidget::saveConfig()
{
	DV::Config::GetInstance()->loadConfig();
	DV::ConfigGroup Group = DV::Config::GetInstance()->getRootGroup();
	auto particleGroup = Group.getGroup("particle3d");
	/*
		相空间图相关参数
	*/
	//粒子大小
	auto particleSize=ui->particleSize->text().toDouble();
	//std::string particleSizeStr = "" + particleSize;
	particleGroup
		.getGroup("particleSize")
		.setSetting("value", std::to_string(particleSize));
	//粒子颜色
	ui->particleColor;
	particleGroup
		.getGroup("particleColor")
		.setSetting("value",getButtonColorstr(ui->particleColor));
	DV::Config::GetInstance()->saveFile();
}
void DV3D::Particle3dConfigWidget::initUi()
{
	this->setWindowTitle(DV::GetEncodingstr("3维粒子图",ENCODING_GB2312));
	SETPERPORE(ui->particleColor,btnClicked());
}

void DV3D::Particle3dConfigWidget::btnClicked()
{
	auto button = dynamic_cast<QPushButton*>(sender());
	setButtonColor(button);
}
