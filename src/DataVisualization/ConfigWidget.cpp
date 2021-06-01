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
#include "ColorTab.h"
#include <sstream>
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
		boxLayout = new QBoxLayout(QBoxLayout::Direction::BottomToTop,ui->colorscale);
		ui->colorscale->setLayout(boxLayout);
		mColorTab = new ColorTab(ui->colorscale);
		boxLayout->addWidget(mColorTab);
		arrowCtrl = new ArrowCtrl( ArrowCtrl::Direction::TopToBottom,ui->colorscale);
		boxLayout->addWidget(arrowCtrl);
		connect(arrowCtrl, 
			SIGNAL(changMoveColor(std::vector<float>&, std::vector<QColor>&,const QColor&,const QColor&)),
			mColorTab, 
			SLOT(changmoveColor(std::vector<float>&, std::vector<QColor>&,const QColor&,const QColor&)));

		connect(ui->FixedColors, SIGNAL(toggled(bool)), this, SLOT(radioButton1(bool)));
		connect(ui->ScaledColors, SIGNAL(toggled(bool)), this, SLOT(radioButton2(bool)));
		SETPERPORE(ui->firstColorBtn,setfirstColor());
		SETPERPORE(ui->endColorBtn,setendColor());
	}
#undef  SETPERPORE(a,b)
	//保存
	connect(ui->applicButtom, SIGNAL(clicked()), this, SLOT(saveclicked()));
	//取消
	connect(ui->cancleButtom,SIGNAL(clicked()), this, SLOT(canclelicked()));
}

/**
* @brief  ConfigWidget::PerfectConductorClicked
* @return void  
*/
void ConfigWidget::PerfectConductorClicked(){ structInfoClicked(Mas::PERFECTCONDUCTOR, ui->PerfectConductorColor); }
/**
* @brief  ConfigWidget::ConductorNewClicked
* @return void  
*/
void ConfigWidget::ConductorNewClicked(){ structInfoClicked(Mas::CONDUCTORNEW, ui->ConductorNewColor); }
/**
* @brief  ConfigWidget::DiolectricClicked
* @return void  
*/
void ConfigWidget::DiolectricClicked(){	structInfoClicked(Mas::DIOLECTRIC, ui->DiolectricColor);}
/**
* @brief  ConfigWidget::PermeabilityClicked
* @return void  
*/
void ConfigWidget::PermeabilityClicked(){structInfoClicked(Mas::PERMEABILITY, ui->PermeabilityColor);}
/**
* @brief  ConfigWidget::dielectirAndconductanceClicked
* @return void  
*/
void ConfigWidget::dielectirAndconductanceClicked(){ structInfoClicked(Mas::DIELECTIRANDCONDUCTANCE, ui->dielectirAndconductanceColor); }
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
	case Mas::CONDUCTORNEW:
		structColor["CONDUCTORNEW"] = QColorToQstring(color); break;
	case Mas::DIOLECTRIC:
		structColor["DIOLECTRIC"] = QColorToQstring(color); break;
	case Mas::PERFECTCONDUCTOR:
		structColor["PERFECTCONDUCTOR"] = QColorToQstring(color); break;
	case Mas::PERMEABILITY:
		structColor["PERMEABILITY"] = QColorToQstring(color); break;
	case Mas::DIELECTIRANDCONDUCTANCE:
		structColor["DIELECTIRANDCONDUCTANCE"] = QColorToQstring(color); break;
	case Mas::FREESPACE:
		structColor["FREESPACE"] = QColorToQstring(color); break;
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
			StructGroup.getGroup(iter->first.toStdString()).setSetting("value", iter->second.toStdString());
		for (auto iter = structlineColor.begin(); iter != structlineColor.end();iter++)
			StructGroup.getGroup(iter->first.toStdString()).setSetting("value", iter->second.toStdString());
		
		//抗锯齿
		ConfigGroup AlisAttitude = StructGroup.getGroup("AlisAttitude");
		(ui->structcheckBox->checkState() == Qt::Checked) ? AlisAttitude.setSetting("isAlis", "1") : AlisAttitude.setSetting("isAlis", "0");
	}
	//2维结构图参数
	{
		auto Struct2DGroup = Group.getGroup("struct2D");
#define SetSeting(x,y,z,w) (x):\
										{\
			Struct2DGroup.getGroup((#x+5)).setSetting("value",(y));\
		Struct2DGroup.getGroup(#x "TYPE" + 5).setSetting("value", (z->itemText(z->currentIndex())).toStdString());\
		Struct2DGroup.getGroup(#x "WIDTH" + 5).setSetting("value", (w->itemText(w->currentIndex())).toStdString());\
				}\
		break
		for (auto iter = struct2dinfo.begin(); iter != struct2dinfo.end(); iter++)
		{
			switch (iter->first)
			{
				case SetSeting(Mas::CONDUCTORNEW, iter->second.toStdString(), ui->ConductorNewtype, ui->ConductorNewWidth);
				case SetSeting(Mas::DIOLECTRIC, iter->second.toStdString(), ui->Diolectrictype, ui->DiolectricWidth);
				case SetSeting(Mas::PERFECTCONDUCTOR, iter->second.toStdString(), ui->PerfectConductortype, ui->PerfectConductorWidth);
				case SetSeting(Mas::DIELECTIRANDCONDUCTANCE, iter->second.toStdString(), ui->dielectirAndconductancetype, ui->dielectirAndconductanceWidth);
				case SetSeting(Mas::PERMEABILITY, iter->second.toStdString(), ui->Permeabilitytype, ui->PermeabilityWidth);
			}
#undef SetSeting(x,y)
		}
	}
	//时间图
	{
		auto timeGroup = Group.getGroup("observe");
		QString pensize = ui->linesSizeEdit->itemText(ui->linesSizeEdit->currentIndex());
		timeGroup.getGroup("lineSize").setSetting("value", pensize.toStdString());
		//timeGroup.setSetting("lineSize", pensize.toStdString());
		timeGroup.getGroup("lineColor").setSetting("value", timeConfig._2nd.toStdString());
		//timeGroup.setSetting("lineColor", timeConfig._2nd.toStdString());
		//抗锯齿
		auto AlisAttitude = timeGroup.getGroup("AlisAttitude");
		(ui->linescheckBox->checkState() == Qt::Checked) ? AlisAttitude.setSetting("isAlis", "1") : AlisAttitude.setSetting("isAlis", "0");
	}
	//矢量图
	{
		auto vectorGroup = Group.getGroup("vector");
		auto vecsizestr = (ui->vectorSize->itemText(ui->vectorSize->currentIndex())).toStdString();
		vectorGroup.getGroup("vectorsize").setSetting("value", vecsizestr);
		//vectorGroup.setSetting("vectorsize", vecsizestr);
		vectorGroup.getGroup("vectorColor").setSetting("value", vecconfig._2nd.toStdString());
		//vectorGroup.setSetting("vectorColor", vecconfig._2nd.toStdString());

		(ui->veccheckBox->checkState() == Qt::Checked)?vectorGroup.getGroup("AlisAttitude").setSetting("isAlis", "1"):
			vectorGroup.getGroup("AlisAttitude").setSetting("isAlis", "0");

		(ui->disMode->checkState() == Qt::Checked) ? vectorGroup.getGroup("disMode").setSetting("value", "1") : 
			vectorGroup.getGroup("disMode").setSetting("value", "0");
	}
	//刻度
	{
		auto Axisgroup = Group.getGroup("axis");
		auto AxisUnitSize = (ui->fontSize->itemText(ui->fontSize->currentIndex())).toStdString();
		Axisgroup.getGroup("axisSize").setSetting("value", AxisUnitSize);
		Axisgroup.getGroup("axisColor").setSetting("value", axisinfo._3th.toStdString());
		Axisgroup.getGroup("axisvalColor").setSetting("value",axisinfo._4th.toStdString());
		auto axisvalSize = (ui->axisvalSize->itemText(ui->axisvalSize->currentIndex())).toStdString();
		Axisgroup.getGroup("axisvalSize").setSetting("value",axisvalSize);
	}
	//相空间图
	{
		auto particlegroup = Group.getGroup("particle");
		auto particleSize = ui->partcleEdit->text().toStdString();
		particlegroup.getGroup("size").setSetting("value",particleSize);
		particlegroup.getGroup("color").setSetting("value", partcleConfig._2nd.toStdString());
		(ui->partclecheckBox->checkState() == Qt::Checked)?particlegroup.getGroup("AlisAttitude").setSetting("isAlis", "1"):particlegroup.getGroup("AlisAttitude").setSetting("isAlis", "0");
	}
	{
		//等位图
		auto contourGroup = Group.getGroup("contour");
		ui->equivalent;//等值
		ui->raidoOfequality;//等比
		if (ui->ScaledColors->isChecked()) contourGroup.getGroup("lineMapColors").setSetting("value", "ScaleColors");
		else contourGroup.getGroup("lineMapColors").setSetting("value","FixedColors");
		(ui->concheckBox->checkState() == Qt::Checked) ? (contourGroup.getGroup("AlisAttitude").setSetting("isAlis", "1")) : (contourGroup.getGroup("AlisAttitude").setSetting("isAlis", "0"));
		if (ui->equivalent->isChecked()) contourGroup.getGroup("valueStyle").setSetting("value", "equivalent");
		else contourGroup.getGroup("valueStyle").setSetting("value", "raidoOfequality");
		//lineMapValue
		//获取颜色
		{
			std::vector<float> vals;
			vals = arrowCtrl->getValue();
			auto levelGroup = contourGroup.getGroup("lineMapColorval");
			levelGroup.setSetting("valueNumber", QString("%1").arg(vals.size()).toStdString());
			std::vector<QColor> colors = mColorTab->GetColors(vals);
			for (auto index = 0; index < vals.size();index++)
			{
				levelGroup.getGroup(QString("level_%1").arg(index).toStdString()).setSetting("value",QString("%1").arg(vals[index]).toStdString());
				levelGroup.getGroup(QString("level_%1").arg(index).toStdString()).setSetting("color",QColorToQstring(colors[index]).toStdString());
			}
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
*/void ConfigWidget::PerfectConductorlineClicked(){ structinfolineClicked(Mas::PERFECTCONDUCTOR, ui->PerfectConductorlineColor); }

/**
* @brief  ConfigWidget::ConductorNewlineClicked
* @return void  
*/void ConfigWidget::ConductorNewlineClicked(){ structinfolineClicked(Mas::CONDUCTORNEW, ui->ConductorNewlineColor); }

/**
* @brief  ConfigWidget::DiolectriclineClicked
* @return void  
*/void ConfigWidget::DiolectriclineClicked(){ structinfolineClicked(Mas::DIOLECTRIC, ui->DiolectriclineColor); }
/**
* @brief  ConfigWidget::PermeabilitylineClicked
* @return void  
*/
void ConfigWidget::PermeabilitylineClicked(){ structinfolineClicked(Mas::PERMEABILITY, ui->PermeabilitylineColor); }
/**
* @brief  ConfigWidget::dielectirAndconductancelineClicked
* @return void  
*/
void ConfigWidget::dielectirAndconductancelineClicked(){ structinfolineClicked(Mas::DIELECTIRANDCONDUCTANCE, ui->dielectirAndconductancelineColor); }
void ConfigWidget::FreespaceClicked(){ structInfoClicked(Mas::FREESPACE, ui->FreespaceColor); }
void ConfigWidget::Freespacelineclicked(){ structinfolineClicked(Mas::FREESPACE, ui->FreespacelineColor);}
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
	case Mas::CONDUCTORNEW:
		structlineColor["CONDUCTORNEWLINE"] = QColorToQstring(color); break;
	case Mas::DIOLECTRIC:
		structlineColor["DIOLECTRICLINE"] = QColorToQstring(color); break;
	case Mas::PERFECTCONDUCTOR:
		structlineColor["PERFECTCONDUCTORLINE"] = QColorToQstring(color); break;
	case Mas::PERMEABILITY:
		structlineColor["PERMEABILITYLINE"] = QColorToQstring(color); break;
	case Mas::DIELECTIRANDCONDUCTANCE:
		structlineColor["DIELECTIRANDCONDUCTANCELINE"] = QColorToQstring(color); break;
	case Mas::FREESPACE:
		structlineColor["FREESPACELINE"] = QColorToQstring(color); break;
	case Mas::FOIL:
		structlineColor["FOILLINE"] = QColorToQstring(color); break;

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
#define LOADCONFIGCOLOR(a,b,c)\
	fileeButtom(c##Color,(b).getGroup(#a).getValue("value"));\
	structColor[#a] = QString::fromStdString(StructGroup.getGroup(#a).getValue("value"));\
	fileeButtom(c##lineColor,(b).getGroup(#a "LINE").getValue("value"));\
	structlineColor[#a "LINE"] = QString::fromStdString((b).getGroup(#a "LINE").getValue("value"));
	{
		auto StructGroup = Group.getGroup("struct");
		LOADCONFIGCOLOR(DIOLECTRIC, StructGroup, ui->Diolectric);
		LOADCONFIGCOLOR(DIELECTIRANDCONDUCTANCE, StructGroup, ui->dielectirAndconductance);
		LOADCONFIGCOLOR(PERMEABILITY, StructGroup, ui->Permeability);
		LOADCONFIGCOLOR(PERFECTCONDUCTOR, StructGroup, ui->PerfectConductor);
		LOADCONFIGCOLOR(CONDUCTORNEW, StructGroup, ui->ConductorNew);
		//新增属性-20210521
		LOADCONFIGCOLOR(FREESPACE, StructGroup, ui->Freespace);
		LOADCONFIGCOLOR(FOIL, StructGroup, ui->FOIL);
		//抗锯齿
		ui->structcheckBox->setCheckState((QString::fromStdString(StructGroup.getGroup("AlisAttitude").getValue("isAlis")).toInt() == 1) ? Qt::Checked:Qt::Unchecked);
	}
#undef LOADCONFIGCOLOR(a,b,c)
	//2维结构图
	{
#define LOADSTRUCT2D(x,y)\
	fileeButtom(y##Color2,StructGroup.getGroup(#x).getValue("value"));\
	struct2dinfo[Mas::##x] = QString::fromStdString(StructGroup.getGroup(#x).getValue("value"));\
	toComboxIndex(y##type,QString::fromStdString(StructGroup.getGroup(#x "TYPE").getValue("value")));\
	toComboxIndex(y##Width,QString::fromStdString(StructGroup.getGroup(#x "WIDTH").getValue("value")));
		auto StructGroup = Group.getGroup("struct2D");
		LOADSTRUCT2D(DIOLECTRIC,ui->Diolectric);
		LOADSTRUCT2D(DIELECTIRANDCONDUCTANCE, ui->dielectirAndconductance);
		LOADSTRUCT2D(PERMEABILITY, ui->Permeability);
		LOADSTRUCT2D(PERFECTCONDUCTOR, ui->PerfectConductor);
		LOADSTRUCT2D(CONDUCTORNEW, ui->ConductorNew);
#undef LOADSTRUCT2D(x,y)
	}
	//时间图
	{
		auto timeGroup = Group.getGroup("observe");
		fileeButtom(ui->lineColor, timeGroup.getGroup("lineColor").getValue("value"));
		timeConfig._2nd = QString::fromStdString(timeGroup.getGroup("lineColor").getValue("value"));
		QString linesize = QString::fromStdString(timeGroup.getGroup("lineSize").getValue("value"));
		toComboxIndex(ui->linesSizeEdit,linesize);
		ui->linescheckBox->setCheckState((QString::fromStdString(timeGroup.getGroup("AlisAttitude").getValue("isAlis")).toInt() == 1) ? Qt::Checked : Qt::Unchecked);
	}
	//矢量图
	{
		auto vectorGroup = Group.getGroup("vector");
		fileeButtom(ui->vecColor, vectorGroup.getGroup("vectorColor").getValue("value"));
		vecconfig._2nd = QString::fromStdString(vectorGroup.getGroup("vectorColor").getValue("value"));
		QString vectorsize = QString::fromStdString(vectorGroup.getGroup("vectorsize").getValue("value"));
		toComboxIndex(ui->vectorSize, vectorsize);
		ui->veccheckBox->setCheckState((QString::fromStdString(vectorGroup.getGroup("AlisAttitude").getValue("isAlis")).toInt())?Qt::Checked:Qt::Unchecked);
		ui->disMode->setCheckState((QString::fromStdString(vectorGroup.getGroup("disMode").getValue("value")).toInt()) ? Qt::Checked : Qt::Unchecked);
	}
	//刻度
	{
		auto Axisgroup = Group.getGroup("axis");
		fileeButtom(ui->axisColor, Axisgroup.getGroup("axisColor").getValue("value"));
		axisinfo._3th = QString::fromStdString(Axisgroup.getGroup("axisColor").getValue("value"));
		fileeButtom(ui->axisvalColor, Axisgroup.getGroup("axisvalColor").getValue("value"));
		axisinfo._4th = QString::fromStdString(Axisgroup.getGroup("axisvalColor").getValue("value"));
		QString axisSize = QString::fromStdString(Axisgroup.getGroup("axisSize").getValue("value"));
		toComboxIndex(ui->fontSize,axisSize);
		toComboxIndex(ui->axisvalSize,QString::fromStdString(Axisgroup.getGroup("axisvalSize").getValue("value")));
	}
	//粒子图
	{
		auto particlegroup = Group.getGroup("particle");
		fileeButtom(ui->partcleColor, particlegroup.getGroup("color").getValue("value"));
		partcleConfig._2nd = QString::fromStdString(particlegroup.getGroup("color").getValue("value"));
		auto size = atoi(particlegroup.getGroup("size").getValue("value").c_str());
		if (0 == size)size = 1;
		ui->partcleEdit->setText(QString::number(size));
		ui->partclecheckBox->setCheckState((QString::fromStdString(particlegroup.getGroup("AlisAttitude").getValue("isAlis")).toInt())?Qt::Checked:Qt::Unchecked);
	}
	//等位图
	{
		auto contourGroup = Group.getGroup("contour");
		//lineMapColors
		if (contourGroup.getGroup("lineMapColors").getValue("value").find("ScaleColors") != std::string::npos)
		{
			ui->ScaledColors->setChecked(true);
			ui->FixedColors->setChecked(false);
			mColorTab->setColorStyle(1);
		}
		else
		{
			ui->FixedColors->setChecked(true);
			ui->ScaledColors->setChecked(false);
			mColorTab->setColorStyle(0);
		}
		//valueStyle
		if (contourGroup.getGroup("valueStyle").getValue("value").find("raidoOfequality")!=std::string::npos)
		{
			ui->raidoOfequality->setChecked(true);
			ui->equivalent->setChecked(false);
		}
		else
		{
			ui->equivalent->setChecked(true);
			ui->raidoOfequality->setChecked(false);
		}
		auto levelGroup = contourGroup.getGroup("lineMapColorval");
		unsigned int levelSize = atoi(levelGroup.getValue("valueNumber").c_str());
		std::vector<float> vals;
		std::vector<QColor> colors;
		for (auto index = 0; index < levelSize;index++)
		{
			vals.push_back(atof( levelGroup.getGroup(QString("level_%1").arg(index).toStdString()).getValue("value").c_str()));
			colors.push_back(QStringToQColor(QString::fromStdString(levelGroup.getGroup(QString("level_%1").arg(index).toStdString()).getValue("color"))));
		}
		if (!vals.empty())
		{
			arrowCtrl->setvals(vals, colors);
			mColorTab->setColors(vals, colors);
			QPalette qpalette1 = ui->firstColorBtn->palette();
			qpalette1.setColor(QPalette::Button, *colors.begin());
			ui->firstColorBtn->setPalette(qpalette1);
			QPalette qpalette2 = ui->endColorBtn->palette();
			qpalette2.setColor(QPalette::Button, *(colors.end() - 1));
			ui->endColorBtn->setPalette(qpalette2);
			arrowCtrl->SetFirstColor(*colors.begin());
			arrowCtrl->SetEndColor(*(colors.end() - 1));
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
* @brief  ConfigWidget::PerfectConductorClicked_2
* @return void  
*/
void ConfigWidget::PerfectConductorClicked2(){ struct_2D_clicked(Mas::PERFECTCONDUCTOR, ui->PerfectConductorColor2); }
/**
* @brief  ConfigWidget::ConductorNewClicked_2
* @return void  
*/
void ConfigWidget::ConductorNewClicked2(){ struct_2D_clicked(Mas::CONDUCTORNEW, ui->ConductorNewColor2); }
/**
* @brief  ConfigWidget::DiolectricClicked_2
* @return void  
*/
void ConfigWidget::DiolectricClicked2(){ struct_2D_clicked(Mas::DIOLECTRIC, ui->DiolectricColor2); }
/**
* @brief  ConfigWidget::PermeabilityClicked_2
* @return void  
*/
void ConfigWidget::PermeabilityClicked2(){ struct_2D_clicked(Mas::PERMEABILITY, ui->PermeabilityColor2); }
/**
* @brief  ConfigWidget::dielectirAndconductanceClicked_2
* @return void  
*/
void ConfigWidget::dielectirAndconductanceClicked2(){ struct_2D_clicked(Mas::DIELECTIRANDCONDUCTANCE, ui->dielectirAndconductanceColor2); }

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
void ConfigWidget::canclelicked()
{
	this->close();
}
void ConfigWidget::radioButton1(bool flag){
	if (flag==true)
	{
		mColorTab->setColorStyle(0);
	}
}
void ConfigWidget::radioButton2(bool flag){
	if (flag==true)
	{
		mColorTab->setColorStyle(1);
	}
}
/**
* @brief  ConfigWidget::setfirstColor 设置起始颜色
* @return void  
*/
void ConfigWidget::setfirstColor(){
	QColor color = QColorDialog::getColor(Qt::white, this, "pick Color", QColorDialog::ShowAlphaChannel);
	QPalette qpalette = ui->firstColorBtn->palette();
	qpalette.setColor(QPalette::Button, color);
	ui->firstColorBtn->setPalette(qpalette);
	arrowCtrl->SetFirstColor(color);

}
/**
* @brief  ConfigWidget::setendColor 设置终止颜色
* @return void  
*/
void ConfigWidget::setendColor(){
	QColor color = QColorDialog::getColor(Qt::black, this, "pick Color", QColorDialog::ShowAlphaChannel);
	QPalette qpalette = ui->endColorBtn->palette();
	qpalette.setColor(QPalette::Button, color);
	ui->endColorBtn->setPalette(qpalette);
	arrowCtrl->SetEndColor(color);
}
/**
* @brief  Mas::Setconfig::Setconfig
* @return   
*/
Mas::Setconfig::Setconfig()
	:_1st("1"), _2nd("1"), _3th("1"), _4th("1")
{}
#include "moc_ConfigWidget.cpp"

