#include "VectorConfigWidget.h"
#include "ui_VectorConfigWidget.h"
#include "QPushButton"
#include "CustomConfig.h"
#include "C_encoding.h"
#include "XmlGroup.h"
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
	XmlData::VectorXml xmlinf;
	xmlinf.loadXml();
	setButtonColor(ui->vecColor, xmlinf.vectorColor.value);
	toComboxIndex(ui->vectorSize, QString::number(xmlinf.vectorsize.value));
	ui->veccheckBox->setCheckState(xmlinf.AlisAttitude.value ? Qt::Checked : Qt::Unchecked);
	ui->disMode->setCheckState((xmlinf.disMode.value) ? Qt::Checked : Qt::Unchecked);

}

void DV::VectorConfigWidget::saveConfig()
{
	/*
	·â×°
	*/
	XmlData::VectorXml vecXml;
	vecXml.vectorsize = (ui->vectorSize->itemText(ui->vectorSize->currentIndex())).toInt();
	vecXml.vectorColor = getButtonColor(ui->vecColor);
	vecXml.AlisAttitude =((ui->veccheckBox->checkState() == Qt::Checked) ? 1 : 0);
	vecXml.disMode = ((ui->disMode->checkState() == Qt::Checked) ? 1 : 0);
	vecXml.saveXml();
}

void DV::VectorConfigWidget::initUi()
{
	this->setWindowTitle(GetEncodingstr("Ê¸Á¿Í¼", ENCODING_GB2312));
	SETPERPORE(ui->vecColor, btnClicked());
}

void DV::VectorConfigWidget::btnClicked()
{
	auto button = dynamic_cast<QPushButton*>(sender());
	auto color = setButtonColor(button);
}

#include "moc_VectorConfigWidget.cpp"