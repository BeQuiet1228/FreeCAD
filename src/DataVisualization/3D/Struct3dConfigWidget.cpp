#include "Struct3dConfigWidget.h"
#include "ui_Struct3dConfigWidget.h"
#include "../CustomConfig.h"
#include "../C_encoding.h"
#include "XmlGroup3D.h"
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
	XmlData::Struct3dXml xmlInfo;
	XmlData::loadXmlInfo(xmlInfo);
	setButtonColor(ui->btnColor,xmlInfo.color);
}

void DV3D::Struct3dConfigWidget::saveConfig()
{
	XmlData::Struct3dXml xmlInfo;
	xmlInfo.color = getButtonColor(ui->btnColor);
	XmlData::saveXmlInfo(xmlInfo);
}

void DV3D::Struct3dConfigWidget::initUi()
{
	this->setWindowTitle(DV::GetEncodingstr("3ά�ṹͼ", ENCODING_GB2312));
	SETPERPORE(ui->btnColor, btnClicked());
}

void DV3D::Struct3dConfigWidget::btnClicked()
{
	auto button = dynamic_cast<QPushButton*>(sender());
	setButtonColor(button);
}
