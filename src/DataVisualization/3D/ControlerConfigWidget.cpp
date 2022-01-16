#include"ControlerConfigWidget.h"
#include"ui_ControlerConfigWidget.h"
#include "XmlGroup3D.h"
#include "QSlider"
//QSlider;
DV3D::ControlerConfigWidget::ControlerConfigWidget(QWidget* parent)
	:QWidget(parent), ui(new Ui::ControlerConfigWidget())
{
	ui->setupUi(this);
	initUi();
}

DV3D::ControlerConfigWidget::~ControlerConfigWidget()
{

}

void DV3D::ControlerConfigWidget::initUi()
{
	parentGroup = "";
	/*
	*	初始化滑动条
	*/
	ui->alphaSlider->setMinimum(0);
	ui->alphaSlider->setMaximum(100);
	ui->alphaSlider->setSingleStep(1);
	connect(ui->alphaSlider, SIGNAL(valueChanged(int )),this,SLOT(slotSliderChange(int)));
}
void DV3D::ControlerConfigWidget::loadConfig(XmlData::ControlerXml& xmlinfo)
{
	xmlinfo.loadXml();
	ui->centerX->setText(QString::number(xmlinfo.centerPoint.x()));
	ui->centerY->setText(QString::number(xmlinfo.centerPoint.y()));
	ui->centerZ->setText(QString::number(xmlinfo.centerPoint.z()));
	ui->normalX->setText(QString::number(xmlinfo.normalPoint.x()));
	ui->normalY->setText(QString::number(xmlinfo.normalPoint.y()));
	ui->normalZ->setText(QString::number(xmlinfo.normalPoint.z()));

	int per = xmlinfo.alpha.value * 100;
	ui->alphaSlider->setValue(per);
	ui->clipCheckBox->setCheckable(xmlinfo.clipEnable.value?Qt::Checked:Qt::Unchecked);
	ui->gridCheckBox->setCheckState(xmlinfo.gridEnable.value?Qt::Checked:Qt::Unchecked);
}
void DV3D::ControlerConfigWidget::saveConfig(XmlData::ControlerXml& xmlinfo)
{
	xmlinfo.alpha = ui->alphaEdit->text().toDouble();
	xmlinfo.clipEnable = (ui->clipCheckBox->checkState() == Qt::Checked ? 1 : 0);
	xmlinfo.gridEnable = (ui->gridCheckBox->checkState() == Qt::Checked ? 1 : 0);
	xmlinfo.centerPoint.setX(ui->centerX->text().toDouble());
	xmlinfo.centerPoint.setY(ui->centerY->text().toDouble());
	xmlinfo.centerPoint.setZ(ui->centerZ->text().toDouble());

	xmlinfo.normalPoint.setX(ui->normalX->text().toDouble());
	xmlinfo.normalPoint.setY(ui->normalX->text().toDouble());
	xmlinfo.normalPoint.setZ(ui->normalX->text().toDouble());
	//XmlData::saveXmlInfo(xmlinfo, parentGroup);
	xmlinfo.saveXml();
}

void DV3D::ControlerConfigWidget::setParentGroup(std::string val)
{
	parentGroup = val;
}

void DV3D::ControlerConfigWidget::slotSliderChange(int value)
{
	float p = value / 100.0;
	ui->alphaEdit->setText(QString::number(p));
}
