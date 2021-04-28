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
	this->SetAllreRender(ui->perfectconductorColor);
	this->SetAllreRender(ui->conductorNewColor);
	this->SetAllreRender(ui->diolectricColor);
	this->SetAllreRender(ui->permeabilityColor);
	this->SetAllreRender(ui->vacuoColor);
	this->SetAllreRender(ui->vecColor);
	this->SetAllreRender(ui->lineColor);
	this->SetAllreRender(ui->axisColor);
	//时间图
	connect(ui->lineColor, SIGNAL(clicked()), this, SLOT(linecolorClicked()));
	//矢量图
	connect(ui->vecColor, SIGNAL(clicked()), this, SLOT(veccolorClicked()));
	//保存
	connect(ui->applicButtom, SIGNAL(clicked()), this, SLOT(saveclicked()));
	//刻度
	connect(ui->axisColor, SIGNAL(clicked()), this, SLOT(fontColorclicked()));
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
		structColor["Conductor_New"] = QColorToQstring(color); break;
	case Mas::Diolectric:
		structColor["Diolectric"] = QColorToQstring(color); break;
	case Mas::Perfect_Conductor:
		structColor["Perfect_Conductor"] = QColorToQstring(color); break;
	case Mas::Permeability:
		structColor["Permeability"] = QColorToQstring(color); break;
	case Mas::Vacuo:
		structColor["Vacuo"] = QColorToQstring(color); break;
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
			StructGroup.setSetting(iter->first.toStdString(), iter->second.toStdString());
		}
	}
	//时间图
	{
		auto timeGroup = Group.getGroup("observe");
		QString pensize = ui->linesSizeEdit->itemText(ui->linesSizeEdit->currentIndex());
		timeGroup.setSetting("lineSize", pensize.toStdString());
		timeGroup.setSetting("lineColor", timeConfig._2nd.toStdString());
	}
	//矢量图
	{
		auto vectorGroup = Group.getGroup("vector");
		auto vecsizestr = (ui->vectorSize->itemText(ui->vectorSize->currentIndex())).toStdString();
		vectorGroup.setSetting("vectorsize", vecsizestr);
		vectorGroup.setSetting("vectorColor", vecconfig._2nd.toStdString());
	}
	//刻度
	{
		auto Axisgroup = Group.getGroup("axis");
		auto AxisSize = (ui->fontSize->itemText(ui->vectorSize->currentIndex())).toStdString();
		Axisgroup.setSetting("axisSize", AxisSize);
		Axisgroup.setSetting("axisColor", axisinfo._3th.toStdString());
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
	QColor color = setbuttomColor(ui->lineColor);
	timeConfig._2nd = QColorToQstring(color);
}
//矢量图
void ConfigWidget::veccolorClicked()
{
	QColor color=setbuttomColor(ui->vecColor);
	vecconfig._2nd = QColorToQstring(color);
}
void ConfigWidget::SetAllreRender(QPushButton* buttom)
{
	buttom->setAutoFillBackground(true);
	buttom->setFlat(true);
}
void ConfigWidget::fontColorclicked(){
	QColor color = setbuttomColor(ui->axisColor);
	axisinfo._3th = QColorToQstring(color);
}
QColor ConfigWidget::setbuttomColor(QPushButton* button)
{
	QColor color = QColorDialog::getColor(Qt::white, this);
	QPalette qpalette =button->palette();
	qpalette.setColor(QPalette::Button, color);
	button->setPalette(qpalette);
	button->setText(QString("#%1").arg(QColorToQstring(color)));
	return color;
}
#include "moc_ConfigWidget.cpp"