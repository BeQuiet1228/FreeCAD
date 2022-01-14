#include "ParticleConfigWidget.h"
#include "ui_ParticleConfigWidget.h"
#include "QPushButton"
#include "CustomConfig.h"
#include "C_encoding.h"
#include "XmlGroup.h"
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
	/*

	*/
	XmlData::ParticleXml xmlinfo;
	xmlinfo.loadXml();
	setButtonColor(ui->partcleColor, xmlinfo.color.value);
	ui->partcleEdit->setText(QString::number(xmlinfo.size.value));
	ui->partclecheckBox->setCheckState(xmlinfo.AlisAttitude.value ? Qt::Checked : Qt::Unchecked);
}

void DV::ParticleConfigWidget::saveConfig()
{
	XmlData::ParticleXml xmlinfo;
	xmlinfo.size = ui->partcleEdit->text().toInt();
	xmlinfo.color = getButtonColor(ui->partcleColor);
	xmlinfo.AlisAttitude = ((ui->partclecheckBox->checkState() == Qt::Checked) ? 1 : 0);
	xmlinfo.saveXml();
}

void DV::ParticleConfigWidget::initUi()
{
	this->setWindowTitle(GetEncodingstr("Á£×ÓÍ¼", ENCODING_GB2312));
	SETPERPORE(ui->partcleColor, btnClicked());
}

void DV::ParticleConfigWidget::btnClicked()
{
	auto button = dynamic_cast<QPushButton*>(sender());
	auto color = setButtonColor(button);
}

#include "moc_ParticleConfigWidget.cpp"