#include "Struct3dConfigWidget.h"
#include "ui_Struct3dConfigWidget.h"
#include "../CustomConfig.h"
#include "../C_encoding.h"
#include "XmlGroup3D.h"
#include "ControlerConfigWidget.h"
#include "QFormLayout"
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
	xmlInfo.loadXml();
	setButtonColor(ui->btnColor,xmlInfo.color.value);
	ui->rotationEdit->setText(QString::number(xmlInfo.Rotation.value));
	controlerConfigWidget->loadConfig(xmlInfo.controlerXml);
}

void DV3D::Struct3dConfigWidget::saveConfig()
{
	XmlData::Struct3dXml xmlInfo;
	xmlInfo.color = getButtonColor(ui->btnColor);
	xmlInfo.Rotation = ui->rotationEdit->text().toInt();
	//XmlData::saveXmlInfo(xmlInfo);
	controlerConfigWidget->saveConfig(xmlInfo.controlerXml);
	xmlInfo.saveXml();
}

void DV3D::Struct3dConfigWidget::initUi()
{
	this->setWindowTitle(DV::GetEncodingstr("3ά�ṹͼ", ENCODING_GB2312));
	SETPERPORE(ui->btnColor, btnClicked());
	QFormLayout* layout = new QFormLayout;
	layout->setSpacing(0);
	ui->topWidget->setLayout(layout);
	controlerConfigWidget = new ControlerConfigWidget(ui->topWidget);
	controlerConfigWidget->setParentGroup("struct3d");
	layout->addWidget(controlerConfigWidget);	
}

void DV3D::Struct3dConfigWidget::btnClicked()
{
	auto button = dynamic_cast<QPushButton*>(sender());
	setButtonColor(button);
}
