#include "AxisConfigWidget.h"
#include "ui_AxisConfigWidget.h"
#include "SysInfo.h"
#include "CustomConfig.h"
#include "C_encoding.h"
DV::AxisConfigWidget::AxisConfigWidget(QWidget* parent/*=nullptr*/)
	:QWidget(parent),ui(new Ui::AxisConfigWidget)
{
	ui->setupUi(this);
	initUi();
}

DV::AxisConfigWidget::~AxisConfigWidget()
{

}

void DV::AxisConfigWidget::loadConfig()
{
	Config::GetInstance()->loadConfig();
	auto Group = Config::GetInstance()->getRootGroup();
	{
		auto Axisgroup = Group.getGroup("axis");
		setButtonColor(ui->axisColor, Axisgroup.getGroup("axisColor").getValue("value"));
		//axisinfo._3th = QString::fromStdString(Axisgroup.getGroup("axisColor").getValue("value"));
		setButtonColor(ui->axisvalColor, Axisgroup.getGroup("axisvalColor").getValue("value"));
		//axisinfo._4th = QString::fromStdString(Axisgroup.getGroup("axisvalColor").getValue("value"));
		QString axisSize = QString::fromStdString(Axisgroup.getGroup("axisSize").getValue("value"));
		toComboxIndex(ui->fontSize, axisSize);
		toComboxIndex(ui->axisvalSize, QString::fromStdString(Axisgroup.getGroup("axisvalSize").getValue("value")));
		int infoshow = atoi(Axisgroup.getGroup("infoShow").getValue("value").c_str());
		if (infoshow)
		{
			ui->infoshow->setChecked(true);
			ui->infohide->setChecked(false);
		}
		else
		{
			ui->infoshow->setChecked(false);
			ui->infohide->setChecked(true);
		}
		std::string mfont = Axisgroup.getGroup("font").getValue("value");
		QString sfont = QString::fromStdString(mfont);
		//遍历
		for (auto i = 0; i < ui->fontStyle->count(); i++)
		{
			if (ui->fontStyle->itemText(i) == sfont)
			{
				ui->fontStyle->setCurrentIndex(i);
				break;
			}

		}
	}
}

void DV::AxisConfigWidget::saveConfig()
{
	Config::GetInstance()->loadConfig();
	ConfigGroup Group = Config::GetInstance()->getRootGroup();
	auto Axisgroup = Group.getGroup("axis");
	auto AxisUnitSize = (ui->fontSize->itemText(ui->fontSize->currentIndex())).toStdString();
	Axisgroup.getGroup("axisSize").setSetting("value", AxisUnitSize);
	//Axisgroup.getGroup("axisColor").setSetting("value", axisinfo._3th.toStdString());
	Axisgroup.getGroup("axisColor").setSetting("value", getButtonColorstr(ui->axisColor));
	//Axisgroup.getGroup("axisvalColor").setSetting("value", axisinfo._4th.toStdString());
	Axisgroup.getGroup("axisvalColor").setSetting("value", getButtonColorstr(ui->axisvalColor));
	auto axisvalSize = (ui->axisvalSize->itemText(ui->axisvalSize->currentIndex())).toStdString();
	Axisgroup.getGroup("axisvalSize").setSetting("value", axisvalSize);
	if (ui->infoshow->isChecked())Axisgroup.getGroup("infoShow").setSetting("value", "1");
	else
		Axisgroup.getGroup("infoShow").setSetting("value", "0");
	//存储字体
	std::string mfont = ui->fontStyle->itemText(ui->fontStyle->currentIndex()).toStdString();
	Axisgroup.getGroup("font").setSetting("value", mfont);
	//Axisgroup.getGroup("font").setSetting("value");
	Config::GetInstance()->saveFile();
}

void DV::AxisConfigWidget::initUi()
{
	this->setWindowTitle(GetEncodingstr("综合",ENCODING_GB2312));
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
	SETPERPORE(ui->axisColor, axisColorclicked());
	SETPERPORE(ui->axisvalColor, axisValColorclicked());
}

void DV::AxisConfigWidget::btnClicked()
{
	auto button = dynamic_cast<QPushButton*>(sender());
	setButtonColor(button);
}

#include "moc_AxisConfigWidget.cpp"