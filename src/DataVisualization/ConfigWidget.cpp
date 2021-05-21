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
#include "Arrowctrl.h"
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
#define SETPERPORE(a,b)\
	connect((a),SIGNAL(clicked()),this,SLOT(b));\
	this->SetAllreRender(a);
	//结构图
	{
		SETPERPORE(ui->PerfectConductorColor, PerfectConductorClicked());
		SETPERPORE(ui->ConductorNewColor,ConductorNewClicked());
		SETPERPORE(ui->DiolectricColor,DiolectricClicked());
		SETPERPORE(ui->PermeabilityColor,PermeabilityClicked());
		SETPERPORE(ui->PerfectConductorlineColor, PerfectConductorlineClicked());
		SETPERPORE(ui->ConductorNewlineColor,ConductorNewlineClicked());
		SETPERPORE(ui->DiolectriclineColor,DiolectriclineClicked());
		SETPERPORE(ui->PermeabilitylineColor,PermeabilitylineClicked());
		//新增加属性2021-5-21
		SETPERPORE(ui->dielectirAndconductanceColor, dielectirAndconductanceClicked());
		SETPERPORE(ui->dielectirAndconductancelineColor,dielectirAndconductancelineClicked());
		SETPERPORE(ui->FreespaceColor, FreespaceClicked());
		SETPERPORE(ui->FreespacelineColor, Freespacelineclicked());
		SETPERPORE(ui->FOILColor, FOILclicked());
		SETPERPORE(ui->FOILlineColor, FOILlineclicked());
	}
	//2维结构图
	{
		SETPERPORE(ui->PerfectConductorColor2, PerfectConductorClicked2());
		SETPERPORE(ui->ConductorNewColor2,ConductorNewClicked2());
		SETPERPORE(ui->DiolectricColor2,DiolectricClicked2());
		SETPERPORE(ui->PermeabilityColor2,PermeabilityClicked2());
		SETPERPORE(ui->dielectirAndconductanceColor2,dielectirAndconductanceClicked2());
	}
	//时间图
	SETPERPORE(ui->lineColor,linecolorClicked());
	//矢量图
	SETPERPORE(ui->vecColor,veccolorClicked());
	//保存
	SETPERPORE(ui->applicButtom,saveclicked());
	//取消
	SETPERPORE(ui->cancleButtom,canclelicked());
	//刻度
	SETPERPORE(ui->axisColor,axisColorclicked());
	SETPERPORE(ui->axisvalColor,axisValColorclicked());
	//粒子图
	SETPERPORE(ui->partcleColor,partcleColorclicked());
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
		arrowCtrl = new ArrowCtrl( ArrowCtrl::Direction::TopToBottom,ui->colorscale);
		boxLayout->addWidget(arrowCtrl);
	}
#undef  SETPERPORE(a,b)
}

/**
* @brief  ConfigWidget::PerfectConductorClicked
* @return void  
*/
void ConfigWidget::PerfectConductorClicked(){ structInfoClicked(Mas::PerfectConductor, ui->PerfectConductorColor); }
/**
* @brief  ConfigWidget::ConductorNewClicked
* @return void  
*/
void ConfigWidget::ConductorNewClicked(){ structInfoClicked(Mas::ConductorNew, ui->ConductorNewColor); }
/**
* @brief  ConfigWidget::DiolectricClicked
* @return void  
*/
void ConfigWidget::DiolectricClicked(){	structInfoClicked(Mas::Diolectric, ui->DiolectricColor);}
/**
* @brief  ConfigWidget::PermeabilityClicked
* @return void  
*/
void ConfigWidget::PermeabilityClicked(){structInfoClicked(Mas::Permeability, ui->PermeabilityColor);}
/**
* @brief  ConfigWidget::dielectirAndconductanceClicked
* @return void  
*/
void ConfigWidget::dielectirAndconductanceClicked(){ structInfoClicked(Mas::dielectirAndconductance, ui->dielectirAndconductanceColor); }
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
	case Mas::ConductorNew:
		structColor["ConductorNew"] = QColorToQstring(color); break;
	case Mas::Diolectric:
		structColor["Diolectric"] = QColorToQstring(color); break;
	case Mas::PerfectConductor:
		structColor["PerfectConductor"] = QColorToQstring(color); break;
	case Mas::Permeability:
		structColor["Permeability"] = QColorToQstring(color); break;
	case Mas::dielectirAndconductance:
		structColor["dielectirAndconductance"] = QColorToQstring(color); break;
	case Mas::Freespace:
		structColor["Freespace"] = QColorToQstring(color); break;
	case Mas::FOIL:
		structColor["FOIL"] = QColorToQstring(color); break;
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
				case SetSeting(Mas::ConductorNew, iter->second.toStdString(), ui->ConductorNewtype, ui->ConductorNewWidth);
				case SetSeting(Mas::Diolectric, iter->second.toStdString(), ui->Diolectrictype, ui->DiolectricWidth);
				case SetSeting(Mas::PerfectConductor, iter->second.toStdString(), ui->PerfectConductortype, ui->PerfectConductorWidth);
				case SetSeting(Mas::dielectirAndconductance, iter->second.toStdString(), ui->dielectirAndconductancetype, ui->dielectirAndconductanceWidth);
				case SetSeting(Mas::Permeability, iter->second.toStdString(), ui->Permeabilitytype, ui->PermeabilityWidth);
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
		(ui->disMode->checkState() == Qt::Checked) ? vectorGroup.setSetting("disMode", "1") : vectorGroup.setSetting("disMode", "0");
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
		equl_ratioGroup.setSetting(QString("level_0").toStdString(), QString("%1").arg(ui->equal_ratio_sval->text().toFloat()).toStdString());
		for (auto index = 1; index < ui->levelnumber->itemText(ui->levelnumber->currentIndex()).toInt()+1;index++)
		{
			equl_ratioGroup.setSetting(QString("level_%1").arg(index).toStdString(), QString("%1").
				arg(ui->equal_ratio_sval->text().toFloat()*index*ui->equal_ratioval->text().toFloat()).toStdString());
		}
		//等值
		auto epuivalenceGroup = contourGroup.getGroup("epuivalence");
		epuivalenceGroup.setSetting("epuivalenceval", ui->epuivalenceval->text().toStdString());
		epuivalenceGroup.setSetting("epuivalencesval", ui->epuivalence_sval->text().toStdString());
		for (auto index = 0; index < ui->levelnumber->itemText(ui->levelnumber->currentIndex()).toInt() + 1; index++)
		{
			epuivalenceGroup.setSetting(QString("level_%1").arg(index).toStdString(), QString("%1").
				arg(ui->epuivalence_sval->text().toFloat() + index*ui->epuivalenceval->text().toFloat()).toStdString());
		}
		//自定义
		auto user_definedGroup = contourGroup.getGroup("user_defined");
		for (auto index = 0; index < ui->user_definedtableWidget->rowCount();index++)
		{
			QTableWidgetItem* item = ui->user_definedtableWidget->item(index, 0);
			user_definedGroup.setSetting(QString("level_%1").arg(index).toStdString(),item->text().toStdString());
		}
		auto levelColorVal = contourGroup.getGroup("levelColorVal");
		auto levelColor = contourGroup.getGroup("levelColor");
		std::vector<float> val = arrowCtrl->getVal();
		const QwtColorMap* xmap = scaleWIdget->colorMap();
		for (auto index = 0; index < val.size();index++)
		{
			levelColorVal.setSetting(QString("level_%1").arg(index).toStdString(),QString("%1").arg(val[index]).toStdString());
			QColor color = xmap->color(QwtInterval(0.0,1.0),val[index]);
			levelColor.setSetting(QString("level_%1").arg(index).toStdString(),QColorToQstring(color).toStdString());
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
* @brief  ConfigWidget::PerfectConductorlineClicked 
* @return void  
*/void ConfigWidget::PerfectConductorlineClicked(){ structinfolineClicked(Mas::PerfectConductor, ui->PerfectConductorlineColor); }

/**
* @brief  ConfigWidget::ConductorNewlineClicked
* @return void  
*/void ConfigWidget::ConductorNewlineClicked(){ structinfolineClicked(Mas::ConductorNew, ui->ConductorNewlineColor); }

/**
* @brief  ConfigWidget::DiolectriclineClicked
* @return void  
*/void ConfigWidget::DiolectriclineClicked(){ structinfolineClicked(Mas::Diolectric, ui->DiolectriclineColor); }
/**
* @brief  ConfigWidget::PermeabilitylineClicked
* @return void  
*/
void ConfigWidget::PermeabilitylineClicked(){ structinfolineClicked(Mas::Permeability, ui->PermeabilitylineColor); }
/**
* @brief  ConfigWidget::dielectirAndconductancelineClicked
* @return void  
*/
void ConfigWidget::dielectirAndconductancelineClicked(){ structinfolineClicked(Mas::dielectirAndconductance, ui->dielectirAndconductancelineColor); }
void ConfigWidget::FreespaceClicked(){ structInfoClicked(Mas::Freespace, ui->FreespaceColor); }
void ConfigWidget::Freespacelineclicked(){ structinfolineClicked(Mas::Freespace, ui->FreespacelineColor);}
void ConfigWidget::FOILclicked(){ structInfoClicked(Mas::FOIL,ui->FOILColor);}
void ConfigWidget::FOILlineclicked(){ structinfolineClicked(Mas::FOIL, ui->FOILlineColor); }
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
	case Mas::ConductorNew:
		structlineColor["ConductorNewline"] = QColorToQstring(color); break;
	case Mas::Diolectric:
		structlineColor["Diolectricline"] = QColorToQstring(color); break;
	case Mas::PerfectConductor:
		structlineColor["PerfectConductorline"] = QColorToQstring(color); break;
	case Mas::Permeability:
		structlineColor["Permeabilityline"] = QColorToQstring(color); break;
	case Mas::dielectirAndconductance:
		structlineColor["dielectirAndconductanceline"] = QColorToQstring(color); break;
	case Mas::Freespace:
		structlineColor["Freespaceline"] = QColorToQstring(color); break;
	case Mas::FOIL:
		structlineColor["FOILline"] = QColorToQstring(color); break;

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
				return;
			}
		}
		combox->setCurrentIndex(0);
	};
	//结构图
	//此处写成宏是因为后续如果有新增加得属性，只需在域内使用该宏即可，减少重复书写
#define LOADCONFIGCOLOR(a,b)\
	fileeButtom(ui->##a##Color,(b).getValue(#a));\
	structColor[#a] = QString::fromStdString(StructGroup.getValue(#a));\
	fileeButtom(ui->##a##lineColor,(b).getValue(#a "line"));\
	structlineColor[#a "line"] = QString::fromStdString((b).getValue(#a "line"));
	{
		auto StructGroup = Group.getGroup("struct");
		LOADCONFIGCOLOR(Diolectric, StructGroup);
		LOADCONFIGCOLOR(dielectirAndconductance,StructGroup);
		LOADCONFIGCOLOR(Permeability,StructGroup);
		LOADCONFIGCOLOR(PerfectConductor,StructGroup);
		LOADCONFIGCOLOR(ConductorNew,StructGroup);
		//新增属性-20210521
		LOADCONFIGCOLOR(Freespace,StructGroup);
		LOADCONFIGCOLOR(FOIL,StructGroup);
		ui->structcheckBox->setCheckState((QString::fromStdString(StructGroup.getValue("isAlis")).toInt() == 1) ? Qt::Checked:Qt::Unchecked);
	}
#undef LOADCONFIGCOLOR(a,b)
	//2维结构图
	{
#define LOADSTRUCT2D(x)\
	fileeButtom(ui->##x##Color2,StructGroup.getValue(#x));\
	struct2dinfo[Mas::##x] = QString::fromStdString(StructGroup.getValue(#x));\
	toComboxIndex(ui->##x##type,QString::fromStdString(StructGroup.getValue(#x "type")));\
	toComboxIndex(ui->##x##Width,QString::fromStdString(StructGroup.getValue(#x "width")));
		auto StructGroup = Group.getGroup("struct2D");
		LOADSTRUCT2D(Diolectric);
		LOADSTRUCT2D(dielectirAndconductance);
		LOADSTRUCT2D(Permeability);
		LOADSTRUCT2D(PerfectConductor);
		LOADSTRUCT2D(ConductorNew);
#undef LOADSTRUCT2D(x)
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
		ui->disMode->setCheckState((QString::fromStdString(vectorGroup.getValue("disMode")).toInt()) ? Qt::Checked : Qt::Unchecked);
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
		int levelNumber = ui->levelnumber->itemText(ui->levelnumber->currentIndex()).toInt();
		{
			auto user_definedGroup = contourGroup.getGroup("user_defined");
			cleartableWidget(ui->user_definedtableWidget);
			for (auto index = 0; index < levelNumber+1;index++)
			{
				ui->user_definedtableWidget->insertRow(index);
				QString levelval = QString("level_%1").arg(index);
				ui->user_definedtableWidget->setItem(index, 0, new QTableWidgetItem( QString::fromStdString(user_definedGroup.getValue(levelval.toStdString()))));
			}
		}
		{
			//等比
			auto equl_ratioGroup = contourGroup.getGroup("equl_ratio");
			ui->equal_ratioval->setText(QString::fromStdString(equl_ratioGroup.getValue("equal_ratioval")));
			ui->equal_ratio_sval->setText(QString::fromStdString(equl_ratioGroup.getValue("equal_ratiosval")));
		}
		{
			//等值
			auto epuivalenceGroup = contourGroup.getGroup("epuivalence");
			ui->epuivalenceval->setText(QString::fromStdString( epuivalenceGroup.getValue("epuivalenceval") ));
			ui->epuivalence_sval->setText(QString::fromStdString(epuivalenceGroup.getValue("epuivalencesval")));
		}
		auto levelColorval = contourGroup.getGroup("levelColorVal");
		arrowCtrl->setlevel(levelNumber+1);
		std::vector<float> val;
		val.reserve(levelNumber+1);
		for (auto index = 0; index < levelNumber + 1;++index)
		{
			std::string s_val = levelColorval.getValue(QString("level_%1").arg(index).toStdString());
			if (s_val!="")
			{
				val.push_back(atof(s_val.c_str()));
			}
		}
		arrowCtrl->setVal(val);
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
* @brief  ConfigWidget::PerfectConductorClicked_2
* @return void  
*/
void ConfigWidget::PerfectConductorClicked2(){ struct_2D_clicked(Mas::PerfectConductor, ui->PerfectConductorColor2); }
/**
* @brief  ConfigWidget::ConductorNewClicked_2
* @return void  
*/
void ConfigWidget::ConductorNewClicked2(){ struct_2D_clicked(Mas::ConductorNew, ui->ConductorNewColor2); }
/**
* @brief  ConfigWidget::DiolectricClicked_2
* @return void  
*/
void ConfigWidget::DiolectricClicked2(){ struct_2D_clicked(Mas::Diolectric, ui->DiolectricColor2); }
/**
* @brief  ConfigWidget::PermeabilityClicked_2
* @return void  
*/
void ConfigWidget::PermeabilityClicked2(){ struct_2D_clicked(Mas::Permeability, ui->PermeabilityColor2); }
/**
* @brief  ConfigWidget::dielectirAndconductanceClicked_2
* @return void  
*/
void ConfigWidget::dielectirAndconductanceClicked2(){ struct_2D_clicked(Mas::dielectirAndconductance, ui->dielectirAndconductanceColor2); }

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
	arrowCtrl->setlevel(rownew);
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
void ConfigWidget::canclelicked()
{
}
/**
* @brief  Mas::Setconfig::Setconfig
* @return   
*/
Mas::Setconfig::Setconfig()
	:_1st("1"), _2nd("1"), _3th("1"), _4th("1")
{}
#include "moc_ConfigWidget.cpp"

