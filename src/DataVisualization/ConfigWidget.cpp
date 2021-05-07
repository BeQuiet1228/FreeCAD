#include "ConfigWidget.h"
#include "ui_ConfigWidget.h"
#include "C_encoding.h"
#include <QDebug>
#include <QColorDialog>
#include <QPalette>
#include "C_encoding.h"
#include "CustomConfig.h"
#include<QPushButton>
#include <QRegExp>
/**
* @brief ConfigWidget::ConfigWidget
* @param QWidget* panter
*/
ConfigWidget::ConfigWidget(QWidget* panter) :QWidget(panter), ui(new Ui::ConfigWidget)
{
	ui->setupUi(this);
	initUI();
	loadxmlConfig();
}
/**
* @brief ConfigWidget::~ConfigWidget
*/
ConfigWidget::~ConfigWidget(){

}


/*
* @brief  ConfigWidget::initUI 初始化UI
* @return void  
*/
void ConfigWidget::initUI()
{
	//结构图
	connect(ui->perfectconductorColor, SIGNAL(clicked()), this, SLOT(perfectconductorClicked()));
	connect(ui->conductorNewColor, SIGNAL(clicked()),this,SLOT(conductornewClicked()));
	connect(ui->diolectricColor, SIGNAL(clicked()), this, SLOT(diolectricClicked()));
	connect(ui->permeabilityColor, SIGNAL(clicked()), this, SLOT(permeabilityClicked()));
	connect(ui->vacuoColor, SIGNAL(clicked()), this, SLOT(vacuoClicked()));
	connect(ui->perfectconductorlineColor, SIGNAL(clicked()), this, SLOT(perfectconductorlineClicked()));
	connect(ui->conductorNewlineColor, SIGNAL(clicked()), this, SLOT(conductornewlineClicked()));
	connect(ui->diolectriclineColor, SIGNAL(clicked()), this, SLOT(diolectriclineClicked()));
	connect(ui->permeabilitylineColor, SIGNAL(clicked()), this, SLOT(permeabilitylineClicked()));
	connect(ui->vacuolineColor, SIGNAL(clicked()), this, SLOT(vacuolineClicked()));
	this->SetAllreRender(ui->perfectconductorColor);
	this->SetAllreRender(ui->conductorNewColor);
	this->SetAllreRender(ui->diolectricColor);
	this->SetAllreRender(ui->permeabilityColor);
	this->SetAllreRender(ui->vacuoColor);
	this->SetAllreRender( ui->perfectconductorlineColor);
	this->SetAllreRender( ui->conductorNewlineColor);
	this->SetAllreRender( ui->diolectriclineColor);
	this->SetAllreRender( ui->permeabilitylineColor);
	this->SetAllreRender( ui->vacuolineColor);
	this->SetAllreRender(ui->vecColor);
	this->SetAllreRender(ui->lineColor);
	this->SetAllreRender(ui->axisColor);
	this->SetAllreRender(ui->axisvalColor);
	this->SetAllreRender(ui->partcleColor);
	//时间图
	connect(ui->lineColor, SIGNAL(clicked()), this, SLOT(linecolorClicked()));
	//矢量图
	connect(ui->vecColor, SIGNAL(clicked()), this, SLOT(veccolorClicked()));
	//保存
	connect(ui->applicButtom, SIGNAL(clicked()), this, SLOT(saveclicked()));
	//刻度
	connect(ui->axisColor, SIGNAL(clicked()), this, SLOT(axisColorclicked()));
	connect(ui->axisvalColor, SIGNAL(clicked()), this,SLOT(axisValColorclicked()));
	//粒子图
	connect(ui->partcleColor, SIGNAL(clicked()), this, SLOT(partcleColorclicked()));
	//限制只能输入整数
	QRegExp rx("^(\\d{0,2})$");
	QValidator * validator = new QRegExpValidator(rx, this);
	ui->partcleEdit->setValidator(validator);
}

/**
* @brief  ConfigWidget::perfectconductorClicked
* @return void  
*/
void ConfigWidget::perfectconductorClicked(){ structInfoClicked(Mas::Perfect_Conductor, ui->perfectconductorColor); }
/**
* @brief  ConfigWidget::conductornewClicked
* @return void  
*/
void ConfigWidget::conductornewClicked(){structInfoClicked(Mas::Conductor_New, ui->conductorNewColor);}
/**
* @brief  ConfigWidget::diolectricClicked
* @return void  
*/
void ConfigWidget::diolectricClicked(){	structInfoClicked(Mas::Diolectric, ui->diolectricColor);}
/**
* @brief  ConfigWidget::permeabilityClicked
* @return void  
*/
void ConfigWidget::permeabilityClicked(){structInfoClicked(Mas::Permeability, ui->permeabilityColor);}
/**
* @brief  ConfigWidget::vacuoClicked
* @return void  
*/
void ConfigWidget::vacuoClicked(){ structInfoClicked(Mas::Vacuo, ui->vacuoColor); }
/**
* @brief  ConfigWidget::structInfoClicked
* @param  int _property  
* @param  QPushButton * button  
* @return void  
*/
void ConfigWidget::structInfoClicked(int _property, QPushButton* button)
{
	
	QColor color= QColorDialog::getColor(Qt::white, this, "pick Color", QColorDialog::ShowAlphaChannel);
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
/*
* @brief  saveclicked 应用按钮
* @return void  
*/
void ConfigWidget::saveclicked()
{
	ui->applicButtom->setEnabled(false);
	Config::GetInstance()->loadConfig();
	ConfigGroup Group = Config::GetInstance()->getRootGroup();
	//结构图参数
	{
		auto StructGroup = Group.getGroup("struct");
		for (auto iter = structColor.begin(); iter != structColor.end(); iter++)
			StructGroup.setSetting(iter->first.toStdString(), iter->second.toStdString());
		//auto StructGroup2 = Group.getGroup("structline");
		for (auto iter = structlineColor.begin(); iter != structlineColor.end();iter++)
			StructGroup.setSetting(iter->first.toStdString(), iter->second.toStdString());
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
		auto AxisUnitSize = (ui->fontSize->itemText(ui->fontSize->currentIndex())).toStdString();
		Axisgroup.setSetting("axisSize", AxisUnitSize);
		Axisgroup.setSetting("axisColor", axisinfo._3th.toStdString());
		Axisgroup.setSetting("axisvalColor",axisinfo._4th.toStdString());
		auto axisvalSize = (ui->axisvalSize->itemText(ui->axisvalSize->currentIndex())).toStdString();
		Axisgroup.setSetting("axisvalSize",axisvalSize);
	}
	//相空间图
	{
		auto particlegroup = Group.getGroup("particle");
		auto particleSize = ui->partcleEdit->text().toStdString();
		particlegroup.setSetting("size",particleSize);
		particlegroup.setSetting("color", partcleConfig._2nd.toStdString());
	}
	Config::GetInstance()->saveFile();
	ui->applicButtom->setEnabled(true);

#ifdef MY_DEBUG
	printf("saveclicked\n");
#endif
}
//时间图

/**
* @brief  ConfigWidget::linecolorClicked 时间图颜色选择
* @return void  
*/
void ConfigWidget::linecolorClicked()
{
	QColor color = setbuttomColor(ui->lineColor);
	timeConfig._2nd = QColorToQstring(color);
}
/**
* @brief ConfigWidget::veccolorClicked 矢量图颜色选择
* @return void
*/
void ConfigWidget::veccolorClicked()
{
	QColor color=setbuttomColor(ui->vecColor);
	vecconfig._2nd = QColorToQstring(color);
}
/**
* @brief  ConfigWidget::SetAllreRender
* @param  QPushButton * buttom  
* @return void  
*/void ConfigWidget::SetAllreRender(QPushButton* buttom)
{
	buttom->setAutoFillBackground(true);
	buttom->setFlat(true);
}



/**
* @brief  ConfigWidget::axisColorclicked 刻度相关的
* @return void  
*/
void ConfigWidget::axisColorclicked(){
	QColor color = setbuttomColor(ui->axisColor);
	axisinfo._3th = QColorToQstring(color);
}

/**
* @brief  ConfigWidget::setbuttomColor 刻度颜色选择
* @param  QPushButton * button  
* @return QT_NAMESPACE::QColor  
*/

QColor ConfigWidget::setbuttomColor(QPushButton* button)
{
	QColor color=QColorDialog::getColor(Qt::white, this, "pick Color", QColorDialog::ShowAlphaChannel);
	QPalette qpalette =button->palette();
	qpalette.setColor(QPalette::Button, color);
	button->setPalette(qpalette);
	button->setText(QString("#%1").arg(QColorToQstring(color)));
	return color;
}

/**
* @brief  ConfigWidget::axisValColorclicked 刻度数值颜色选择
* @return void  
*/
void ConfigWidget::axisValColorclicked()
{
	QColor color = setbuttomColor(ui->axisvalColor);
	axisinfo._4th = QColorToQstring(color);
}

/**
* @brief  ConfigWidget::perfectconductorlineClicked 
* @return void  
*/void ConfigWidget::perfectconductorlineClicked(){ structinfolineClicked(Mas::Perfect_Conductor, ui->perfectconductorlineColor); }

/**
* @brief  ConfigWidget::conductornewlineClicked
* @return void  
*/void ConfigWidget::conductornewlineClicked(){ structinfolineClicked(Mas::Conductor_New, ui->conductorNewlineColor); }

/**
* @brief  ConfigWidget::diolectriclineClicked
* @return void  
*/void ConfigWidget::diolectriclineClicked(){ structinfolineClicked(Mas::Diolectric, ui->diolectriclineColor); }
/**
* @brief  ConfigWidget::permeabilitylineClicked
* @return void  
*/
void ConfigWidget::permeabilitylineClicked(){ structinfolineClicked(Mas::Permeability, ui->permeabilitylineColor); }
/**
* @brief  ConfigWidget::vacuolineClicked
* @return void  
*/
void ConfigWidget::vacuolineClicked(){ structinfolineClicked(Mas::Vacuo, ui->vacuolineColor); }
/**
* @brief  ConfigWidget::structinfolineClicked
* @param  int _property  
* @param  QPushButton * button  
* @return void  
*/
void ConfigWidget::structinfolineClicked(int _property, QPushButton* button){
	QColor color = QColorDialog::getColor(Qt::white, this, "pick Color", QColorDialog::ShowAlphaChannel);
	QPalette qpalette = button->palette();
	qpalette.setColor(QPalette::Button, color);
	button->setPalette(qpalette);
	button->setText(QString("#%1").arg(QColorToQstring(color)));
	switch (_property)
	{
	case Mas::Conductor_New:
		structlineColor["Conductor_Newline"] = QColorToQstring(color); break;
	case Mas::Diolectric:
		structlineColor["Diolectricline"] = QColorToQstring(color); break;
	case Mas::Perfect_Conductor:
		structlineColor["Perfect_Conductorline"] = QColorToQstring(color); break;
	case Mas::Permeability:
		structlineColor["Permeabilityline"] = QColorToQstring(color); break;
	case Mas::Vacuo:
		structlineColor["Vacuoline"] = QColorToQstring(color); break;

	}
}
/**
* @brief  ConfigWidget::partcleColorclicked
* @return void  
*/
void ConfigWidget::partcleColorclicked(){
	QColor color=setbuttomColor(ui->partcleColor);
	partcleConfig._2nd = QColorToQstring(color);
}
/**
* @brief  ConfigWidget::loadxmlConfig 读取xml配置信息
* @return void  
*/
void ConfigWidget::loadxmlConfig(){
	Config::GetInstance()->loadConfig();
	auto Group = Config::GetInstance()->getRootGroup();
	//结构图
	{
		auto StructGroup = Group.getGroup("struct");
		fileeButtom(ui->diolectricColor, StructGroup.getValue("Diolectric"));
		structColor["Diolectric"] = QString::fromStdString(StructGroup.getValue("Diolectric"));
		fileeButtom(ui->vacuoColor, StructGroup.getValue("Vacuo"));
		structColor["Vacuo"] = QString::fromStdString(StructGroup.getValue("Vacuo"));
		fileeButtom(ui->permeabilityColor, StructGroup.getValue("Permeability"));
		structColor["Permeability"] = QString::fromStdString(StructGroup.getValue("Permeability"));
		fileeButtom(ui->perfectconductorColor, StructGroup.getValue("Perfect_Conductor"));
		structColor["Perfect_Conductor"] = QString::fromStdString(StructGroup.getValue("Perfect_Conductor"));
		fileeButtom(ui->conductorNewColor, StructGroup.getValue("Conductor_New"));
		structColor["Conductor_New"] = QString::fromStdString(StructGroup.getValue("Conductor_New"));

		fileeButtom(ui->vacuolineColor, StructGroup.getValue("Vacuoline"));
		structlineColor["Vacuoline"] = QString::fromStdString(StructGroup.getValue("Vacuoline"));
		fileeButtom(ui->permeabilitylineColor, StructGroup.getValue("Permeabilityline"));
		structlineColor["Permeabilityline"] = QString::fromStdString(StructGroup.getValue("Permeabilityline"));
		fileeButtom(ui->perfectconductorlineColor, StructGroup.getValue("Perfect_Conductorline"));
		structlineColor["Perfect_Conductorline"] = QString::fromStdString(StructGroup.getValue("Perfect_Conductorline"));
		fileeButtom(ui->diolectriclineColor, StructGroup.getValue("Diolectricline"));
		structlineColor["Diolectricline"] = QString::fromStdString(StructGroup.getValue("Diolectricline"));
		fileeButtom(ui->conductorNewlineColor, StructGroup.getValue("Conductor_Newline"));
		structlineColor["Conductor_Newline"] = QString::fromStdString(StructGroup.getValue("Conductor_Newline"));
	}
	//时间图
	{
		auto timeGroup = Group.getGroup("observe");
		fileeButtom(ui->lineColor, timeGroup.getValue("lineColor"));
		timeConfig._2nd = QString::fromStdString(timeGroup.getValue("lineColor"));
		QString linesize = QString::fromStdString(timeGroup.getValue("lineSize"));
		int index = -1;
		for (int i = 0; i < ui->linesSizeEdit->count(); i++)
		{
			if (ui->linesSizeEdit->itemText(i)==linesize)
			{
				ui->linesSizeEdit->setCurrentIndex(i);
				break;
			}
		}
	}
	//矢量图
	{
		auto vectorGroup = Group.getGroup("vector");
		fileeButtom(ui->vecColor, vectorGroup.getValue("vectorColor"));
		vecconfig._2nd = QString::fromStdString(vectorGroup.getValue("vectorColor"));
		QString vectorsize = QString::fromStdString(vectorGroup.getValue("vectorsize"));
		int index = -1;
		for (int i = 0; i < ui->vectorSize->count(); i++)
		{
			if (ui->vectorSize->itemText(i) == vectorsize)
			{
				ui->vectorSize->setCurrentIndex(i);
				break;
			}
		}
	}
	//刻度
	{
		auto Axisgroup = Group.getGroup("axis");
		fileeButtom(ui->axisColor, Axisgroup.getValue("axisColor"));
		axisinfo._3th = QString::fromStdString(Axisgroup.getValue("axisColor"));
		fileeButtom(ui->axisvalColor, Axisgroup.getValue("axisvalColor"));
		axisinfo._4th = QString::fromStdString(Axisgroup.getValue("axisvalColor"));
		QString axisSize = QString::fromStdString(Axisgroup.getValue("axisSize"));
		int index = -1;
		for (int i = 0; i < ui->fontSize->count(); i++)
		{
			if (ui->fontSize->itemText(i) == axisSize)
			{
				ui->fontSize->setCurrentIndex(i);
				break;
			}
		}
	}
	{
		auto particlegroup = Group.getGroup("particle");
		fileeButtom(ui->partcleColor, particlegroup.getValue("color"));
		partcleConfig._2nd = QString::fromStdString(particlegroup.getValue("color"));
		auto size = atoi(particlegroup.getValue("size").c_str());
		if (0 == size)size = 1;
		ui->partcleEdit->setText(QString::number(size));
	}
}
/**
* @brief  ConfigWidget::fileeButtom 按钮填充
* @param  QPushButton * button  
* @param  std::string color  
* @return void  
*/
void ConfigWidget::fileeButtom(QPushButton* button, std::string color) 
{
	QColor rgba = QStringToQColor(QString::fromStdString(color));
	QPalette qpalette = button->palette();
	qpalette.setColor(QPalette::Button, rgba);
	button->setPalette(qpalette);
	button->setText(QString("#%1").arg(QString::fromStdString(color)));
}
/**
* @brief  Mas::Setconfig::Setconfig
* @return   
*/
Mas::Setconfig::Setconfig()
	:_1st("1"), _2nd("1"), _3th("1"), _4th("1")
{

}

#include "moc_ConfigWidget.cpp"

