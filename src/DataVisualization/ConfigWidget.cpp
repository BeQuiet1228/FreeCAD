#include "ConfigWidget.h"
#include "ui_ConfigWidget.h"
#include "C_encoding.h"
#include <QDebug>
#include <QColorDialog>
#include <QPalette>
#include "C_encoding.h"
#include "CustomConfig.h"
ConfigWidget::ConfigWidget(QWidget* panter) :QWidget(panter), ui(new Ui::ConfigWidget)
{
	ui->setupUi(this);
	initUI();
}
ConfigWidget::~ConfigWidget(){

}
void ConfigWidget::initUI()
{
	//结构图
	connect(ui->perfectconductorColor, SIGNAL(clicked()), this, SLOT(perfectconductorClicked()));
	connect(ui->conductorNewColor, SIGNAL(clicked()),this,SLOT(conductornewClicked()));
	connect(ui->diolectricColor, SIGNAL(clicked()), this, SLOT(diolectricClicked()));
	connect(ui->permeabilityColor, SIGNAL(clicked()), this, SLOT(permeabilityClicked()));
	connect(ui->vacuoColor, SIGNAL(clicked()), this, SLOT(vacuoClicked()));
	ui->perfectconductorColor->setAutoFillBackground(true);
	ui->perfectconductorColor->setFlat(true);
	ui->conductorNewColor->setAutoFillBackground(true);
	ui->conductorNewColor->setFlat(true);
	ui->diolectricColor->setAutoFillBackground(true);
	ui->diolectricColor->setFlat(true);
	ui->permeabilityColor->setAutoFillBackground(true);
	ui->permeabilityColor->setFlat(true);
	ui->vacuoColor->setAutoFillBackground(true);
	ui->vacuoColor->setFlat(true);
	//时间图
	connect(ui->lineColor, SIGNAL(clicked()), this, SLOT(linecolorClicked()));
	ui->lineColor->setAutoFillBackground(true);
	ui->lineColor->setFlat(true);
	//矢量图
	connect(ui->vecColor, SIGNAL(clicked()), this, SLOT(veccolorClicked()));
	ui->vecColor->setAutoFillBackground(true);
	ui->vecColor->setFlat(true);
	//保存
	connect(ui->applicButtom, SIGNAL(clicked()), this, SLOT(saveclicked()));
}
void ConfigWidget::perfectconductorClicked(){
#ifdef MY_DEBUG
	printf("perfectconductorClicked\n");
#endif
	structInfoClicked(Mas::Perfect_Conductor, ui->perfectconductorColor);
}
void ConfigWidget::conductornewClicked(){
#ifdef MY_DEBUG
	printf("conductornewClicked\n");
#endif
	structInfoClicked(Mas::Conductor_New, ui->conductorNewColor);
}
void ConfigWidget::diolectricClicked(){
#ifdef MY_DEBUG
	printf("diolectricClicked\n");
#endif
	structInfoClicked(Mas::Diolectric, ui->diolectricColor);
}
void ConfigWidget::permeabilityClicked(){
#ifdef MY_DEBUG
	printf("permeabilityClicked\n");
#endif
	structInfoClicked(Mas::Permeability, ui->permeabilityColor);
}
void ConfigWidget::vacuoClicked(){
#ifdef MY_DEBUG
	printf("vacuoClicked\n");
#endif
	structInfoClicked(Mas::Vacuo, ui->vacuoColor);
}
void ConfigWidget::structInfoClicked(int _property, QPushButton* button)
{
	QColor color = QColorDialog::getColor(Qt::white, this);
#ifdef MY_DEBUG
	printf("structInfoClicked\n");
	qDebug() << color;
#endif
	QPalette qpalette = button->palette();
	qpalette.setColor(QPalette::Button,color);
	button->setPalette(qpalette);
	button->setText(QString("#%1").arg(QColorToQstring(color)));
	switch (_property)
	{
	case Mas::Conductor_New:
		structColor["Conductor_New"] =QColorToQstring(color);
	case Mas::Diolectric:
		structColor["Diolectric"] = QColorToQstring(color);
	case Mas::Perfect_Conductor:
		structColor["Perfect_Conductor"] = QColorToQstring(color);
	case Mas::Permeability:
		structColor["Permeability"] = QColorToQstring(color);
	case Mas::Vacuo:
		structColor["Vacuo"] = QColorToQstring(color);
	}
}
void ConfigWidget::saveclicked()
{
	ui->applicButtom->setEnabled(false);
	
	Config::GetInstance()->loadConfig();
	ConfigGroup Group = Config::GetInstance()->getRootGroup();
	//结构图参数
	{
		auto StructGroup = Group.getGroup("struct");
		for (auto iter = structColor.begin(); iter != structColor.end(); iter++)
		{
			std::string resstr = StructGroup.getValue(iter->first.toStdString());
			if (StructGroup.getValue(iter->first.toStdString()) != "")
				StructGroup.setSetting(iter->first.toStdString(), iter->second.toStdString());
			else
				StructGroup.addSetting(iter->first.toStdString(), iter->second.toStdString());
		}
	}
	//时间图
	{
		auto timeGroup = Group.getGroup("observe");
		//获取当前大小
		QString pensize = ui->linesSizeEdit->itemText(ui->linesSizeEdit->currentIndex());
		if (timeGroup.getValue("lineSize") != "")
			timeGroup.setSetting("lineSize", pensize.toStdString());
		else
			timeGroup.addSetting("lineSize", pensize.toStdString());

		if (timeGroup.getValue("lineColor") != "")
			timeGroup.setSetting("lineColor", timeConfig._2nd.toStdString());
		else
			timeGroup.addSetting("lineColor", timeConfig._2nd.toStdString());
	}
	//矢量图
	{
		auto vectorGroup = Group.getGroup("vector");
		auto vecsizestr = (ui->vectorSize->itemText(ui->vectorSize->currentIndex())).toStdString();
		if (vectorGroup.getValue("vectorsize")!="") 
			vectorGroup.setSetting("vectorsize", vecsizestr);
		else 
			vectorGroup.addSetting("vectorsize", vecsizestr);
		if (vectorGroup.getValue("vectorColor") != "")
			vectorGroup.setSetting("vectorColor", vecconfig._2nd.toStdString());
		else
			vectorGroup.addSetting("vectorColor", vecconfig._2nd.toStdString());
	}
	
	Config::GetInstance()->saveFile();
	ui->applicButtom->setEnabled(true);

#ifdef MY_DEBUG
	printf("saveclicked\n");
#endif
}
//时间图
void ConfigWidget::linecolorClicked()
{
	QColor color = QColorDialog::getColor(Qt::white, this);
#ifdef MY_DEBUG
	printf("linecolorClicked\n");
	qDebug() << color;
#endif // MY_DEBUG
	QPalette qpalette = ui->lineColor->palette();
	qpalette.setColor(QPalette::Button, color);
	ui->lineColor->setPalette(qpalette);
	ui->lineColor->setText(QString("#%1").arg(QColorToQstring(color)));
	timeConfig._2nd = QColorToQstring(color);
}
//矢量图
void ConfigWidget::veccolorClicked()
{
	QColor color = QColorDialog::getColor(Qt::white, this);
#ifdef MY_DEBUG
	printf("linecolorClicked\n");
	qDebug() << color;
#endif // MY_DEBUG
	QPalette qpalette = ui->vecColor->palette();
	qpalette.setColor(QPalette::Button, color);
	ui->vecColor->setPalette(qpalette);
	ui->vecColor->setText(QString("#%1").arg(QColorToQstring(color)));
	vecconfig._2nd = QColorToQstring(color);
}
#include "moc_ConfigWidget.cpp"