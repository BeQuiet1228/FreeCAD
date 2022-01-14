#include "Particle3dConfigWidget.h"
#include "ui_Particle3dConfigWidget.h"
#include "../CustomConfig.h"
#include "../C_encoding.h"
#include "XmlGroup3D.h"
#include "ControlerConfigWidget.h"
#include "QFormLayout"
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
	XmlData::Particle3dXml xmlinfo;
	XmlData::loadXmlInfo(xmlinfo);
	setButtonColor(ui->particleColor,xmlinfo.particleColor);
	ui->particleSize->setText(QString::number(xmlinfo.particleSize));
	controlerConfigWidget->loadConfig();
}
void DV3D::Particle3dConfigWidget::saveConfig()
{
	XmlData::Particle3dXml xmlInfo;
	xmlInfo.particleColor = getButtonColor(ui->particleColor);
	xmlInfo.particleSize = ui->particleSize->text().toDouble();
	XmlData::saveXmlInfo(xmlInfo);
	controlerConfigWidget->saveConfig();
}
void DV3D::Particle3dConfigWidget::initUi()
{
	this->setWindowTitle(DV::GetEncodingstr("3Î¬Á£×ÓÍ¼",ENCODING_GB2312));
	SETPERPORE(ui->particleColor,btnClicked());

	QFormLayout* layout = new QFormLayout;
	ui->topWidget->setLayout(layout);
	controlerConfigWidget = new ControlerConfigWidget(ui->topWidget);
	controlerConfigWidget->setParentGroup("particle3d");
	layout->addWidget(controlerConfigWidget);
}

void DV3D::Particle3dConfigWidget::btnClicked()
{
	auto button = dynamic_cast<QPushButton*>(sender());
	setButtonColor(button);
}
