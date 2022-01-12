#include "AxisConfigWidget.h"
#include "ui_AxisConfigWidget.h"
#include "SysInfo.h"
#include "CustomConfig.h"
#include "C_encoding.h"
#include "XmlGroup.h"
DV::AxisConfigWidget::AxisConfigWidget(QWidget* parent/*=nullptr*/)
	:QWidget(parent), ui(new Ui::AxisConfigWidget)
{
	ui->setupUi(this);
	initUi();
}

DV::AxisConfigWidget::~AxisConfigWidget()
{

}

void DV::AxisConfigWidget::loadConfig()
{
	AxisXmlGroup axisGroup;
	auto xmlinfo = axisGroup.loadXmlInfo();
	setButtonColor(ui->axisColor, xmlinfo.axisColor);
	setButtonColor(ui->axisvalColor, xmlinfo.axisvalColor);
	toComboxIndex(ui->fontSize, QString::number(xmlinfo.axisSize));
	toComboxIndex(ui->axisvalSize, QString::number(xmlinfo.axisvalSize));
	for (auto i = 0; i < ui->fontStyle->count(); ++i)
		if (ui->fontStyle->itemText(i) == xmlinfo.font)
		{
			ui->fontStyle->setCurrentIndex(i);
			break;
		}
	if (xmlinfo.infoShow)
	{
		ui->infoshow->setChecked(true);
		ui->infohide->setChecked(false);
	}
	else
	{
		ui->infoshow->setChecked(false);
		ui->infohide->setChecked(true);
	}
}

void DV::AxisConfigWidget::saveConfig()
{
	/*
		封装
	*/
	AxisXmlGroup group;
	DV::AxisXmlGroup::AxisXml axisXml;
	axisXml.axisColor = getButtonColor(ui->axisColor);
	axisXml.axisSize = (ui->fontSize->itemText(ui->fontSize->currentIndex())).toInt();
	axisXml.axisvalColor = getButtonColor(ui->axisvalColor);
	axisXml.axisvalSize = (ui->axisvalSize->itemText(ui->axisvalSize->currentIndex())).toInt();
	axisXml.infoShow = ((ui->infoshow->isChecked()) ? 1 : 0);
	axisXml.font = ui->fontStyle->itemText(ui->fontStyle->currentIndex());
	group.saveXmlInfo(axisXml);
}

void DV::AxisConfigWidget::initUi()
{
	this->setWindowTitle(GetEncodingstr("综合", ENCODING_GB2312));
	/*
		字体
	*/
	std::vector<QString> fonts = SysInfo::GetInstance()->getfonts();
	for (auto iter = fonts.begin(); iter != fonts.end(); iter++)
	{
		ui->fontStyle->addItem(*iter);
	}
	/*
		刻度
	*/
	SETPERPORE(ui->axisColor, btnClicked());
	SETPERPORE(ui->axisvalColor, btnClicked());
}

void DV::AxisConfigWidget::btnClicked()
{
	auto button = dynamic_cast<QPushButton*>(sender());
	setButtonColor(button);
}

#include "moc_AxisConfigWidget.cpp"