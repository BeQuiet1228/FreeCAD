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
#include<QStringList>
#include "qwt/qwt_scale_widget.h"
#include"qwt/qwt_scale_engine.h";
#include "ContourRender.h"
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
	{
		connect(ui->perfectconductorColor, SIGNAL(clicked()), this, SLOT(perfectconductorClicked()));
		connect(ui->conductorNewColor, SIGNAL(clicked()), this, SLOT(conductornewClicked()));
		connect(ui->diolectricColor, SIGNAL(clicked()), this, SLOT(diolectricClicked()));
		connect(ui->permeabilityColor, SIGNAL(clicked()), this, SLOT(permeabilityClicked()));
		connect(ui->vacuoColor, SIGNAL(clicked()), this, SLOT(vacuoClicked()));
		connect(ui->perfectconductorlineColor, SIGNAL(clicked()), this, SLOT(perfectconductorlineClicked()));
		connect(ui->conductorNewlineColor, SIGNAL(clicked()), this, SLOT(conductornewlineClicked()));
		connect(ui->diolectriclineColor, SIGNAL(clicked()), this, SLOT(diolectriclineClicked()));
		connect(ui->permeabilitylineColor, SIGNAL(clicked()), this, SLOT(permeabilitylineClicked()));
		connect(ui->vacuolineColor, SIGNAL(clicked()), this, SLOT(vacuolineClicked()));
	}
	
	//2维结构图
	{
		connect(ui->perfectconductorColor_2, SIGNAL(clicked()), this, SLOT(perfectconductorClicked_2()));
		connect(ui->conductorNewColor_2, SIGNAL(clicked()), this, SLOT(conductornewClicked_2()));
		connect(ui->diolectricColor_2, SIGNAL(clicked()), this, SLOT(diolectricClicked_2()));
		connect(ui->permeabilityColor_2, SIGNAL(clicked()), this, SLOT(permeabilityClicked_2()));
		connect(ui->vacuoColor_2, SIGNAL(clicked()), this, SLOT(vacuoClicked_2()));
	}
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
	this->SetAllreRender(ui->perfectconductorColor_2);
	this->SetAllreRender(ui->conductorNewColor_2);
	this->SetAllreRender(ui->diolectricColor_2);
	this->SetAllreRender(ui->permeabilityColor_2);
	this->SetAllreRender(ui->vacuoColor_2);
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
	{
		//等位图
		ui->equal_ratiovaltableWidget;
		ui->epuivalencevaltableWidget;
		ui->user_definedtableWidget;
		connect(ui->levelnumber, SIGNAL(currentIndexChanged(int)), this, SLOT(changeUser_defined(int)));
		ui->user_definedtableWidget->setEditTriggers(QAbstractItemView::CurrentChanged);
		ui->user_definedtableWidget->setColumnCount(1);
		QStringList header;
		header << GetEncodingstr("自定义取值区间",ENCODING_GB2312);
		ui->user_definedtableWidget->setHorizontalHeaderLabels(header);
		ui->user_definedtableWidget->resizeColumnsToContents();
		ui->user_definedtableWidget->setShowGrid(false);
		//等位图示例
		//gridLayout = new QGridLayout(ui->colorscale);
		boxLayout = new QBoxLayout(QBoxLayout::Direction::BottomToTop,ui->colorscale);
		scaleWIdget = new QwtScaleWidget(QwtScaleDraw::BottomScale, ui->colorscale);
		scaleWIdget->setColorBarEnabled(true);
		scaleWIdget->setColorBarWidth(20);
		scaleEngine = new QwtLinearScaleEngine;
		QwtInterval interval(0, 1);
		scaleWIdget->setColorMap(interval,new ColorMap);
		scaleWIdget->setScaleDiv(scaleEngine->divideScale(0,1,5,6,0));
		ui->colorscale->setLayout(boxLayout);
		boxLayout->addWidget(scaleWIdget);
		boxLayout->addWidget(new QWidget(ui->colorscale));
	}
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
		for (auto iter = structlineColor.begin(); iter != structlineColor.end();iter++)
			StructGroup.setSetting(iter->first.toStdString(), iter->second.toStdString());
		(ui->structcheckBox->checkState() == Qt::Checked)?StructGroup.setSetting("isAlis", "1"):StructGroup.setSetting("isAlis", "0");
	}
	//2维结构图参数
	{
		auto Struct2DGroup = Group.getGroup("struct2D");
#define SetSeting(x,y,z,w) (x):\
										{\
			Struct2DGroup.setSetting((#x+5),(y));\
		Struct2DGroup.setSetting(#x "type" + 5, (z->itemText(z->currentIndex())).toStdString());\
		Struct2DGroup.setSetting(#x "width" + 5, (w->itemText(w->currentIndex())).toStdString());\
				}\
		break
		for (auto iter = struct2dinfo.begin(); iter != struct2dinfo.end(); iter++)
		{
			switch (iter->first)
			{
				case SetSeting(Mas::Conductor_New, iter->second.toStdString(), ui->conductorNewtype, ui->conductorNewWidth);
				case SetSeting(Mas::Diolectric, iter->second.toStdString(), ui->diolectrictype, ui->diolectricWidth);
				case SetSeting(Mas::Perfect_Conductor, iter->second.toStdString(), ui->perfectconducttype, ui->perfectconductorWidth);
				case SetSeting(Mas::Vacuo, iter->second.toStdString(), ui->vacuotype, ui->vacuoWidth);
				case SetSeting(Mas::Permeability, iter->second.toStdString(), ui->permeabilitytype, ui->permeabilityWidth);
			}
#undef SetSeting(x,y)
		}
	}
	//时间图
	{
		auto timeGroup = Group.getGroup("observe");
		QString pensize = ui->linesSizeEdit->itemText(ui->linesSizeEdit->currentIndex());
		timeGroup.setSetting("lineSize", pensize.toStdString());
		timeGroup.setSetting("lineColor", timeConfig._2nd.toStdString());
		//抗锯齿
		(ui->linescheckBox->checkState() == Qt::Checked)?timeGroup.setSetting("isAlis", "1"):timeGroup.setSetting("isAlis", "0");
	}
	//矢量图
	{
		auto vectorGroup = Group.getGroup("vector");
		auto vecsizestr = (ui->vectorSize->itemText(ui->vectorSize->currentIndex())).toStdString();
		vectorGroup.setSetting("vectorsize", vecsizestr);
		vectorGroup.setSetting("vectorColor", vecconfig._2nd.toStdString());
		(ui->veccheckBox->checkState() == Qt::Checked)?vectorGroup.setSetting("isAlis", "1"):vectorGroup.setSetting("isAlis", "0");
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
		(ui->partclecheckBox->checkState() == Qt::Checked)?particlegroup.setSetting("isAlis", "1"):particlegroup.setSetting("isAlis", "0");
	}
	//等位图
	{
		auto contourGroup = Group.getGroup("Contour");
		(ui->concheckBox->checkState() == Qt::Checked) ? contourGroup.setSetting("isAlis", "1") : contourGroup.setSetting("isAlis", "0");
		contourGroup.setSetting("valtype",ui->contourvalType->itemText(ui->contourvalType->currentIndex()).toStdString());
		contourGroup.setSetting("vallevel", ui->levelnumber->itemText(ui->levelnumber->currentIndex()).toStdString());
		//等比
		auto equl_ratioGroup = contourGroup.getGroup("equl_ratio");
		equl_ratioGroup.setSetting("equal_ratioval", ui->equal_ratioval->text().toStdString());
		equl_ratioGroup.setSetting("equal_ratiosval", ui->equal_ratio_sval->text().toStdString());
		equl_ratioGroup.setSetting(QString("equal_ratiolevel_0").toStdString(), QString("%1").arg(ui->equal_ratio_sval->text().toFloat()).toStdString());
		for (auto index = 1; index < ui->levelnumber->itemText(ui->levelnumber->currentIndex()).toInt()+1;index++)
		{
			equl_ratioGroup.setSetting(QString("equal_ratiolevel_%1").arg(index).toStdString(), QString("%1").
				arg(ui->equal_ratio_sval->text().toFloat()*index*ui->equal_ratioval->text().toFloat()).toStdString());
		}
		//等值
		auto epuivalenceGroup = contourGroup.getGroup("epuivalence");
		epuivalenceGroup.setSetting("epuivalenceval", ui->epuivalenceval->text().toStdString());
		epuivalenceGroup.setSetting("epuivalencesval", ui->epuivalence_sval->text().toStdString());
		for (auto index = 0; index < ui->levelnumber->itemText(ui->levelnumber->currentIndex()).toInt() + 1; index++)
		{
			epuivalenceGroup.setSetting(QString("epuivalenceslevel_%1").arg(index).toStdString(), QString("%1").
				arg(ui->epuivalence_sval->text().toFloat() + index*ui->epuivalenceval->text().toFloat()).toStdString());
		}
		//自定义
		auto user_definedGroup = contourGroup.getGroup("user_defined");
		for (auto index = 0; index < ui->user_definedtableWidget->rowCount();index++)
		{
			QTableWidgetItem* item = ui->user_definedtableWidget->item(index, 0);
			user_definedGroup.setSetting(QString("user_defined_%1").arg(index).toStdString(),item->text().toStdString());
		}
	}
	Config::GetInstance()->saveFile();
	ui->applicButtom->setEnabled(true);
#ifdef MY_DEBUG
	printf("saveclicked\n");
#endif
}
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
*/
void ConfigWidget::SetAllreRender(QPushButton* buttom)
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
	auto toComboxIndex = [&](QComboBox* combox,QString& str){
		for (int i = 0; i < combox->count(); i++)
		{
			if (combox->itemText(i) == str)
			{
				combox->setCurrentIndex(i);
				break;
			}
		}
	};
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
		ui->structcheckBox->setCheckState((QString::fromStdString(StructGroup.getValue("isAlis")).toInt() == 1) ? Qt::Checked:Qt::Unchecked);
	}
	//2维结构图
	{
#define loadStruct2D(x,y,z,w)\
	fileeButtom(y,StructGroup.getValue(#x+5));\
	struct2dinfo[x] = QString::fromStdString(StructGroup.getValue(#x+5));\
	toComboxIndex(z,QString::fromStdString(StructGroup.getValue(#x "type"+5)));\
	toComboxIndex(w,QString::fromStdString(StructGroup.getValue(#x "width"+5)));

		auto StructGroup = Group.getGroup("struct2D");
		loadStruct2D(Mas::Diolectric,ui->diolectricColor_2,ui->diolectrictype,ui->diolectricWidth);
		loadStruct2D(Mas::Vacuo,ui->vacuoColor_2,ui->vacuotype,ui->vacuoWidth);
		loadStruct2D(Mas::Permeability,ui->permeabilityColor_2,ui->permeabilitytype,ui->permeabilityWidth);
		loadStruct2D(Mas::Perfect_Conductor,ui->perfectconductorColor_2,ui->perfectconducttype,ui->perfectconductorWidth);
		loadStruct2D(Mas::Conductor_New,ui->conductorNewColor_2,ui->conductorNewtype,ui->conductorNewWidth);
#undef loadStruct2D(x,y,z,w)
	}
	//时间图
	{
		auto timeGroup = Group.getGroup("observe");
		fileeButtom(ui->lineColor, timeGroup.getValue("lineColor"));
		timeConfig._2nd = QString::fromStdString(timeGroup.getValue("lineColor"));
		QString linesize = QString::fromStdString(timeGroup.getValue("lineSize"));
		toComboxIndex(ui->linesSizeEdit,linesize);
		ui->linescheckBox->setCheckState((QString::fromStdString(timeGroup.getValue("isAlis")).toInt() == 1) ? Qt::Checked : Qt::Unchecked);
	}
	//矢量图
	{
		auto vectorGroup = Group.getGroup("vector");
		fileeButtom(ui->vecColor, vectorGroup.getValue("vectorColor"));
		vecconfig._2nd = QString::fromStdString(vectorGroup.getValue("vectorColor"));
		QString vectorsize = QString::fromStdString(vectorGroup.getValue("vectorsize"));
		toComboxIndex(ui->vectorSize, vectorsize);
		ui->veccheckBox->setCheckState((QString::fromStdString(vectorGroup.getValue("isAlis")).toInt())?Qt::Checked:Qt::Unchecked);
	}
	//刻度
	{
		auto Axisgroup = Group.getGroup("axis");
		fileeButtom(ui->axisColor, Axisgroup.getValue("axisColor"));
		axisinfo._3th = QString::fromStdString(Axisgroup.getValue("axisColor"));
		fileeButtom(ui->axisvalColor, Axisgroup.getValue("axisvalColor"));
		axisinfo._4th = QString::fromStdString(Axisgroup.getValue("axisvalColor"));
		QString axisSize = QString::fromStdString(Axisgroup.getValue("axisSize"));
		toComboxIndex(ui->fontSize,axisSize);
		toComboxIndex(ui->axisvalSize,QString::fromStdString(Axisgroup.getValue("axisvalSize")));
	}
	//粒子图
	{
		auto particlegroup = Group.getGroup("particle");
		fileeButtom(ui->partcleColor, particlegroup.getValue("color"));
		partcleConfig._2nd = QString::fromStdString(particlegroup.getValue("color"));
		auto size = atoi(particlegroup.getValue("size").c_str());
		if (0 == size)size = 1;
		ui->partcleEdit->setText(QString::number(size));
		ui->partclecheckBox->setCheckState((QString::fromStdString(particlegroup.getValue("isAlis")).toInt())?Qt::Checked:Qt::Unchecked);
	}
	//等位图
	{
		auto cleartableWidget = [&](QTableWidget* qtablewidget){
			int row = qtablewidget->rowCount();
			for (auto index = row - 1; index >= 0; index--)
				qtablewidget->removeRow(index);
		};
		auto contourGroup = Group.getGroup("Contour");
		ui->concheckBox->setCheckState(((QString::fromStdString(contourGroup.getValue("isAlis")).toInt() )==1) ?Qt::Checked:Qt::Unchecked);
		toComboxIndex(ui->contourvalType, QString::fromStdString(contourGroup.getValue("valtype")));
		toComboxIndex(ui->levelnumber, QString::fromStdString(contourGroup.getValue("vallevel")));
		{
			auto user_definedGroup = contourGroup.getGroup("user_defined");
			cleartableWidget(ui->user_definedtableWidget);
			for (auto index = 0; index < atoi(contourGroup.getValue("vallevel").c_str())+1;index++)
			{
				ui->user_definedtableWidget->insertRow(index);
				//user_defined_0;
				QString levelval = QString("user_defined_%1").arg(index);
				ui->user_definedtableWidget->setItem(index, 0, new QTableWidgetItem( QString::fromStdString( user_definedGroup.getValue(levelval.toStdString()) ) ));
			}
		}
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
* @brief  ConfigWidget::perfectconductorClicked_2
* @return void  
*/
void ConfigWidget::perfectconductorClicked_2(){ struct_2D_clicked(Mas::Perfect_Conductor, ui->perfectconductorColor_2); }
/**
* @brief  ConfigWidget::conductornewClicked_2
* @return void  
*/
void ConfigWidget::conductornewClicked_2(){ struct_2D_clicked(Mas::Conductor_New, ui->conductorNewColor_2); }
/**
* @brief  ConfigWidget::diolectricClicked_2
* @return void  
*/
void ConfigWidget::diolectricClicked_2(){ struct_2D_clicked(Mas::Diolectric, ui->diolectricColor_2); }
/**
* @brief  ConfigWidget::permeabilityClicked_2
* @return void  
*/
void ConfigWidget::permeabilityClicked_2(){ struct_2D_clicked(Mas::Permeability, ui->permeabilityColor_2); }
/**
* @brief  ConfigWidget::vacuoClicked_2
* @return void  
*/
void ConfigWidget::vacuoClicked_2(){ struct_2D_clicked(Mas::Vacuo, ui->vacuoColor_2);}

/**
* @brief  ConfigWidget::struct_2D_clicked 
* @param  int _property  
* @param  QPushButton *  
* @return void  
*/
void ConfigWidget::struct_2D_clicked(int _property, QPushButton* button){
	QColor color = QColorDialog::getColor(Qt::white, this, "pick Color", QColorDialog::ShowAlphaChannel);
	QPalette qpalette = button->palette();
	qpalette.setColor(QPalette::Button, color);
	button->setPalette(qpalette);
	button->setText(QString("#%1").arg(QColorToQstring(color)));
	struct2dinfo[_property] = QColorToQstring(color);
}

/**
* @brief  ConfigWidget::changeUser_defined 自定义列表修改
* @param  int index  
* @return void  
*/
void ConfigWidget::changeUser_defined(int index)
{
	int rowold=ui->user_definedtableWidget->rowCount();
	int rownew=ui->levelnumber->itemText(index).toInt()+1;
	if (rownew>rowold)
	{
		for (auto i = 0; i < rownew - rowold;i++)
		{
			int row = ui->user_definedtableWidget->rowCount();
			ui->user_definedtableWidget->insertRow(row);
			QTableWidgetItem* item = new QTableWidgetItem(QString("123456"));
			ui->user_definedtableWidget->setItem(row, 0, item);
		}
		ui->user_definedtableWidget->resizeRowsToContents();
	}
	else if (rowold>rownew)
	{
		for (auto  i = rowold; i >=0; i--)
		{
			int row = ui->user_definedtableWidget->rowCount();
			if (row==rownew) break;
			ui->user_definedtableWidget->removeRow(row-1);
		}
	}
}
/**
* @brief  Mas::Setconfig::Setconfig
* @return   
*/
Mas::Setconfig::Setconfig()
	:_1st("1"), _2nd("1"), _3th("1"), _4th("1")
{}
#include "moc_ConfigWidget.cpp"

