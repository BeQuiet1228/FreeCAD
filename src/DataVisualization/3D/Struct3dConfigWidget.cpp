#include "Struct3dConfigWidget.h"
#include "ui_Struct3dConfigWidget.h"
#include "../CustomConfig.h"
DV3D::Struct3dConfigWidget::Struct3dConfigWidget(QWidget* parent/*=nullptr*/)
	:QWidget(parent), ui(new Ui::Struct3dConfigWidget)
{
	ui->setupUi(this);
	initUi();
}

DV3D::Struct3dConfigWidget::~Struct3dConfigWidget()
{

}

void DV3D::Struct3dConfigWidget::loadConfig()
{
	DV::Config::GetInstance()->loadConfig();
	auto Group = DV::Config::GetInstance()->getRootGroup();
	auto StructGroup = Group.getGroup("struct3d");
	std::string structColor = StructGroup.getGroup("color").getValue("value");
	setButtonColor(ui->btnColor, structColor);
}

void DV3D::Struct3dConfigWidget::saveConfig()
{
	DV::Config::GetInstance()->loadConfig();
	DV::ConfigGroup Group = DV::Config::GetInstance()->getRootGroup();
	//结构图参数
	auto StructGroup = Group.getGroup("struct3d");
	//获取颜色
	std::string colorStr = getButtonColorstr(ui->btnColor);
	StructGroup.getGroup("color").setSetting("value", colorStr);
	DV::Config::GetInstance()->saveFile();
}

void DV3D::Struct3dConfigWidget::initUi()
{
	SetAllreRenderer(ui->btnColor);
	connect(ui->btnColor, SIGNAL(clicked()),this,SLOT(btnClicked()));
}

void DV3D::Struct3dConfigWidget::btnClicked()
{
	auto button =dynamic_cast<QPushButton*>(sender());
	setButtonColor(button);
}
