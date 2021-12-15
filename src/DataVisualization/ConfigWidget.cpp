#include "ConfigWidget.h"
#include "ui_ConfigWidget.h"
#include "C_encoding.h"
#include <QDebug>
#include <QColorDialog>
#include <QPalette>
#include "C_encoding.h"
#include "CustomConfig.h"
#include<QPushButton>
#include "qwt/qwt_scale_widget.h"
#include"qwt/qwt_scale_engine.h";
#include "qwt/qwt_color_map.h"
#include "Arrowctrl.h"
#include "ColorTab.h"
#include <sstream>
#include "Plot.h"
#include "SysInfo.h"
namespace DV {
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
	ConfigWidget::~ConfigWidget() {

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
		SETPERPORE(ui->ConductorNewColor, ConductorNewClicked());
		SETPERPORE(ui->DiolectricColor, DiolectricClicked());
		SETPERPORE(ui->PermeabilityColor, PermeabilityClicked());
		SETPERPORE(ui->PerfectConductorlineColor, PerfectConductorlineClicked());
		SETPERPORE(ui->ConductorNewlineColor, ConductorNewlineClicked());
		SETPERPORE(ui->DiolectriclineColor, DiolectriclineClicked());
		SETPERPORE(ui->PermeabilitylineColor, PermeabilitylineClicked());
		//新增加属性2021-5-21
		SETPERPORE(ui->dielectirAndconductanceColor, dielectirAndconductanceClicked());
		SETPERPORE(ui->dielectirAndconductancelineColor, dielectirAndconductancelineClicked());
		SETPERPORE(ui->FreespaceColor, FreespaceClicked());
		SETPERPORE(ui->FreespacelineColor, Freespacelineclicked());
		SETPERPORE(ui->FOILColor, FOILclicked());
		SETPERPORE(ui->FOILlineColor, FOILlineclicked());
		//新增加属性真空2021-11-23
		SETPERPORE(ui->VacuoColor, Vacuoclicked());
		SETPERPORE(ui->VacuolineColor, Vacuolineclicked());
		//线段
		SETPERPORE(ui->Port, PortClicked());
		SETPERPORE(ui->Inductor, InductorClicked());
		SETPERPORE(ui->Driver, DriverClicked());
	}
	//时间图
	SETPERPORE(ui->lineColor, linecolorClicked());
	//矢量图
	SETPERPORE(ui->vecColor, veccolorClicked());
	//刻度
	SETPERPORE(ui->axisColor, axisColorclicked());
	SETPERPORE(ui->axisvalColor, axisValColorclicked());
	//粒子图
	SETPERPORE(ui->partcleColor, partcleColorclicked());
	//限制只能输入整数
	QRegExp rx("^(\\d{0,2})$");
	QValidator* validator = new QRegExpValidator(rx, this);
	ui->partcleEdit->setValidator(validator);
	{
		//等位图
		boxLayout = new QBoxLayout(QBoxLayout::Direction::BottomToTop, ui->colorscale);
		ui->colorscale->setLayout(boxLayout);
		mColorTab = new ColorTab(ui->colorscale);
		boxLayout->addWidget(mColorTab);
		arrowCtrl = new ArrowCtrl(ArrowCtrl::Direction::TopToBottom, ui->colorscale);
		boxLayout->addWidget(arrowCtrl);
		connect(arrowCtrl,
			SIGNAL(changMoveColor(std::vector<float>&, std::vector<QColor>&, const QColor&, const QColor&)),
			mColorTab,
			SLOT(changmoveColor(std::vector<float>&, std::vector<QColor>&, const QColor&, const QColor&)));

		connect(ui->FixedColors, SIGNAL(toggled(bool)), this, SLOT(radioButton1(bool)));
		connect(ui->ScaledColors, SIGNAL(toggled(bool)), this, SLOT(radioButton2(bool)));
		SETPERPORE(ui->firstColorBtn, setfirstColor());
		SETPERPORE(ui->endColorBtn, setendColor());
	}
#undef  SETPERPORE(a,b)
	//保存
	connect(ui->applicButtom, SIGNAL(clicked()), this, SLOT(saveclicked()));
	//取消
	connect(ui->cancleButtom, SIGNAL(clicked()), this, SLOT(canclelicked()));

	//字体
	std::vector<QString> fonts = SysInfo::GetInstance()->getfonts();
	for (auto iter = fonts.begin(); iter != fonts.end(); iter++)
	{
		ui->fontStyle->addItem(*iter);
	}
	}

	/**
	* @brief  ConfigWidget::structInfoClicked
	* @param  int _property
	* @param  QPushButton * button
	* @return void
	*/
	void ConfigWidget::structInfoClicked(int _property, QPushButton* button)
	{

		QColor color = button->palette().button().color();
		QColorDialog dlg(this);
		dlg.setOption(QColorDialog::ShowAlphaChannel);
		dlg.setCurrentColor(color);
		if (dlg.exec() == QColorDialog::Accepted)
		{
			color = dlg.currentColor();
		}
		QPalette qpalette = button->palette();
		qpalette.setColor(QPalette::Button, color);
		button->setPalette(qpalette);
		button->setText(QString("#%1").arg(QColorToQstring(color)));
#define XX(a)\
	a:\
	structColor[#a+5]=QColorToQstring(color);break;
		switch (_property)
		{
			case XX(Mas::CONDUCTORNEW)
				case XX(Mas::DIOLECTRIC)
				case XX(Mas::PERFECTCONDUCTOR)
				case XX(Mas::PERMEABILITY)
				case XX(Mas::DIELECTIRANDCONDUCTANCE)
				case XX(Mas::FREESPACE)
				case XX(Mas::FOIL)
				case XX(Mas::PORT)
				case XX(Mas::DRIVER)
				case XX(Mas::INDUCTOR)
				case XX(Mas::VACUO)
		}
#undef  XX(a)
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
			for (auto iter = structlineColor.begin(); iter != structlineColor.end(); iter++)
				StructGroup.getGroup(iter->first.toStdString()).setSetting("value", iter->second.toStdString());

			//抗锯齿
			ConfigGroup AlisAttitude = StructGroup.getGroup("AlisAttitude");
			(ui->structcheckBox->checkState() == Qt::Checked) ? AlisAttitude.setSetting("isAlis", "1") : AlisAttitude.setSetting("isAlis", "0");
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

			(ui->veccheckBox->checkState() == Qt::Checked) ? vectorGroup.getGroup("AlisAttitude").setSetting("isAlis", "1") :
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
			Axisgroup.getGroup("axisvalColor").setSetting("value", axisinfo._4th.toStdString());
			auto axisvalSize = (ui->axisvalSize->itemText(ui->axisvalSize->currentIndex())).toStdString();
			Axisgroup.getGroup("axisvalSize").setSetting("value", axisvalSize);
			if (ui->infoshow->isChecked())Axisgroup.getGroup("infoShow").setSetting("value", "1");
			else
				Axisgroup.getGroup("infoShow").setSetting("value", "0");
			//存储字体
			std::string mfont = ui->fontStyle->itemText(ui->fontStyle->currentIndex()).toStdString();
			Axisgroup.getGroup("font").setSetting("value", mfont);
			//Axisgroup.getGroup("font").setSetting("value");
		}
		//相空间图
		{
			auto particlegroup = Group.getGroup("particle");
			auto particleSize = ui->partcleEdit->text().toStdString();
			particlegroup.getGroup("size").setSetting("value", particleSize);
			particlegroup.getGroup("color").setSetting("value", partcleConfig._2nd.toStdString());
			(ui->partclecheckBox->checkState() == Qt::Checked) ? particlegroup.getGroup("AlisAttitude").setSetting("isAlis", "1") : particlegroup.getGroup("AlisAttitude").setSetting("isAlis", "0");
		}
		{
			//等位图
			auto contourGroup = Group.getGroup("contour");
			ui->equivalent;//等值
			ui->raidoOfequality;//等比
			if (ui->ScaledColors->isChecked()) contourGroup.getGroup("lineMapColors").setSetting("value", "ScaleColors");
			else contourGroup.getGroup("lineMapColors").setSetting("value", "FixedColors");
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
				for (auto index = 0; index < vals.size(); index++)
				{
					levelGroup.getGroup(QString("level_%1").arg(index).toStdString()).setSetting("value", QString("%1").arg(vals[index]).toStdString());
					levelGroup.getGroup(QString("level_%1").arg(index).toStdString()).setSetting("color", QColorToQstring(colors[index]).toStdString());
				}
			}
		}
		Config::GetInstance()->saveFile();
		ui->applicButtom->setEnabled(true);
#ifdef MY_DEBUG
		printf("saveclicked\n");
#endif
		emit plotLoadconfig();
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
		QColor color = setbuttomColor(ui->vecColor);
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
	void ConfigWidget::axisColorclicked() {
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
		QColor lastColor = button->palette().button().color();
		{
			QColorDialog dlg(this);
			dlg.setOptions(QColorDialog::ShowAlphaChannel);
			dlg.setCurrentColor(lastColor);
			if (dlg.exec() == QColorDialog::Accepted)
			{
				QColor color = dlg.currentColor();
				QPalette qpalette = button->palette();
				qpalette.setColor(QPalette::Button, color);
				button->setPalette(qpalette);
				button->setText(QString("#%1").arg(QColorToQstring(color)));
				return color;
			}
		}
		return lastColor;
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
	void ConfigWidget::PerfectConductorClicked() { structInfoClicked(Mas::PERFECTCONDUCTOR, ui->PerfectConductorColor); }
	void ConfigWidget::ConductorNewClicked() { structInfoClicked(Mas::CONDUCTORNEW, ui->ConductorNewColor); }
	void ConfigWidget::DiolectricClicked() { structInfoClicked(Mas::DIOLECTRIC, ui->DiolectricColor); }
	void ConfigWidget::PermeabilityClicked() { structInfoClicked(Mas::PERMEABILITY, ui->PermeabilityColor); }
	void ConfigWidget::dielectirAndconductanceClicked() { structInfoClicked(Mas::DIELECTIRANDCONDUCTANCE, ui->dielectirAndconductanceColor); }
	void ConfigWidget::PerfectConductorlineClicked() { structinfolineClicked(Mas::PERFECTCONDUCTOR, ui->PerfectConductorlineColor); }
	void ConfigWidget::ConductorNewlineClicked() { structinfolineClicked(Mas::CONDUCTORNEW, ui->ConductorNewlineColor); }
	void ConfigWidget::DiolectriclineClicked() { structinfolineClicked(Mas::DIOLECTRIC, ui->DiolectriclineColor); }
	void ConfigWidget::PermeabilitylineClicked() { structinfolineClicked(Mas::PERMEABILITY, ui->PermeabilitylineColor); }
	void ConfigWidget::dielectirAndconductancelineClicked() { structinfolineClicked(Mas::DIELECTIRANDCONDUCTANCE, ui->dielectirAndconductancelineColor); }
	void ConfigWidget::FreespaceClicked() { structInfoClicked(Mas::FREESPACE, ui->FreespaceColor); }
	void ConfigWidget::Freespacelineclicked() { structinfolineClicked(Mas::FREESPACE, ui->FreespacelineColor); }
	void ConfigWidget::FOILclicked() { structInfoClicked(Mas::FOIL, ui->FOILColor); }
	void ConfigWidget::FOILlineclicked() { structinfolineClicked(Mas::FOIL, ui->FOILlineColor); }
	void ConfigWidget::PortClicked() { structInfoClicked(Mas::PORT, ui->Port); }
	void ConfigWidget::InductorClicked() { structInfoClicked(Mas::INDUCTOR, ui->Inductor); }
	void ConfigWidget::DriverClicked() { structInfoClicked(Mas::DRIVER, ui->Driver); }
	//新增属性
	void ConfigWidget::Vacuoclicked() { structInfoClicked(Mas::VACUO, ui->VacuoColor); }
	void ConfigWidget::Vacuolineclicked() { structinfolineClicked(Mas::VACUO, ui->VacuolineColor); }
	/**
	* @brief  ConfigWidget::structinfolineClicked
	* @param  int _property
	* @param  QPushButton * button
	* @return void
	*/
	void ConfigWidget::structinfolineClicked(int _property, QPushButton* button) {
		QColor color = button->palette().button().color();
		QColorDialog dlg(this);
		dlg.setOption(QColorDialog::ShowAlphaChannel);
		dlg.setCurrentColor(color);
		if (dlg.exec() == QColorDialog::Accepted)
			color = dlg.currentColor();
		QPalette qpalette = button->palette();
		qpalette.setColor(QPalette::Button, color);
		button->setPalette(qpalette);
		button->setText(QString("#%1").arg(QColorToQstring(color)));
#define XX(a) \
	case (a):\
	structlineColor[#a "LINE"+5] = QColorToQstring(color); break;
		switch (_property)
		{
			XX(Mas::CONDUCTORNEW)
				XX(Mas::DIOLECTRIC)
				XX(Mas::PERFECTCONDUCTOR)
				XX(Mas::PERMEABILITY)
				XX(Mas::DIELECTIRANDCONDUCTANCE)
				XX(Mas::FREESPACE)
				XX(Mas::FOIL)
				XX(Mas::VACUO)
		}
#undef XX(a)
	}
	/**
	* @brief  ConfigWidget::partcleColorclicked
	* @return void
	*/
	void ConfigWidget::partcleColorclicked() {
		QColor color = setbuttomColor(ui->partcleColor);
		partcleConfig._2nd = QColorToQstring(color);
	}
	/**
	* @brief  ConfigWidget::loadxmlConfig 读取xml配置信息
	* @return void
	*/
	void ConfigWidget::loadxmlConfig() {
		Config::GetInstance()->loadConfig();
		auto Group = Config::GetInstance()->getRootGroup();
		auto toComboxIndex = [&](QComboBox* combox, QString& str) {
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
#define LOADCONFIGCOLOR(a,b,c,d)\
	fileeButtom(c##Color,(b).getGroup(#a).getValue("value"));\
	structColor[#a] = QString::fromStdString(StructGroup.getGroup(#a).getValue("value"));\
	fileeButtom(c##lineColor, (b).getGroup(#a "LINE").getValue("value")); \
	structlineColor[#a "LINE"] = QString::fromStdString((b).getGroup(#a "LINE").getValue("value"));

		{
			auto StructGroup = Group.getGroup("struct");
			LOADCONFIGCOLOR(DIOLECTRIC, StructGroup, ui->Diolectric, true);
			LOADCONFIGCOLOR(DIELECTIRANDCONDUCTANCE, StructGroup, ui->dielectirAndconductance, true);
			LOADCONFIGCOLOR(PERMEABILITY, StructGroup, ui->Permeability, true);
			LOADCONFIGCOLOR(PERFECTCONDUCTOR, StructGroup, ui->PerfectConductor, true);
			LOADCONFIGCOLOR(CONDUCTORNEW, StructGroup, ui->ConductorNew, true);
			//新增属性-20210521
			LOADCONFIGCOLOR(FREESPACE, StructGroup, ui->Freespace, true);
			LOADCONFIGCOLOR(FOIL, StructGroup, ui->FOIL, true);
			LOADCONFIGCOLOR(VACUO, StructGroup, ui->Vacuo, true);
#undef LOADCONFIGCOLOR(a,b,c)
#define ADDLINECOLOR(a,b)\
	{auto color=StructGroup.getGroup(#a).getValue("value");\
	fileeButtom(b,color);\
	structColor[#a]=QString::fromStdString(color);\
	}
			ADDLINECOLOR(PORT, ui->Port);
			ADDLINECOLOR(DRIVER, ui->Driver);
			ADDLINECOLOR(INDUCTOR, ui->Inductor);
#undef ADDLINECOLOR(a,b)
			//抗锯齿
			ui->structcheckBox->setCheckState((QString::fromStdString(StructGroup.getGroup("AlisAttitude").getValue("isAlis")).toInt() == 1) ? Qt::Checked : Qt::Unchecked);
		}

		//时间图
		{
			auto timeGroup = Group.getGroup("observe");
			fileeButtom(ui->lineColor, timeGroup.getGroup("lineColor").getValue("value"));
			timeConfig._2nd = QString::fromStdString(timeGroup.getGroup("lineColor").getValue("value"));
			QString linesize = QString::fromStdString(timeGroup.getGroup("lineSize").getValue("value"));
			toComboxIndex(ui->linesSizeEdit, linesize);
			ui->linescheckBox->setCheckState((QString::fromStdString(timeGroup.getGroup("AlisAttitude").getValue("isAlis")).toInt() == 1) ? Qt::Checked : Qt::Unchecked);
		}
		//矢量图
		{
			auto vectorGroup = Group.getGroup("vector");
			fileeButtom(ui->vecColor, vectorGroup.getGroup("vectorColor").getValue("value"));
			vecconfig._2nd = QString::fromStdString(vectorGroup.getGroup("vectorColor").getValue("value"));
			QString vectorsize = QString::fromStdString(vectorGroup.getGroup("vectorsize").getValue("value"));
			toComboxIndex(ui->vectorSize, vectorsize);
			ui->veccheckBox->setCheckState((QString::fromStdString(vectorGroup.getGroup("AlisAttitude").getValue("isAlis")).toInt()) ? Qt::Checked : Qt::Unchecked);
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
		//粒子图
		{
			auto particlegroup = Group.getGroup("particle");
			fileeButtom(ui->partcleColor, particlegroup.getGroup("color").getValue("value"));
			partcleConfig._2nd = QString::fromStdString(particlegroup.getGroup("color").getValue("value"));
			auto size = atoi(particlegroup.getGroup("size").getValue("value").c_str());
			if (0 == size)size = 1;
			ui->partcleEdit->setText(QString::number(size));
			ui->partclecheckBox->setCheckState((QString::fromStdString(particlegroup.getGroup("AlisAttitude").getValue("isAlis")).toInt()) ? Qt::Checked : Qt::Unchecked);
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
			if (contourGroup.getGroup("valueStyle").getValue("value").find("raidoOfequality") != std::string::npos)
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
			for (auto index = 0; index < levelSize; index++)
			{
				vals.push_back(atof(levelGroup.getGroup(QString("level_%1").arg(index).toStdString()).getValue("value").c_str()));
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
				arrowCtrl->SetEndColor(*(colors.end() - 1));
				arrowCtrl->SetFirstColor(*colors.begin());

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
	* @brief  ConfigWidget::canclelicked 取消按钮
	* @return void
	*/
	void ConfigWidget::canclelicked()
	{
		this->close();
	}
	/**
	* @brief  ConfigWidget::radioButton1
	* @param  bool flag
	* @return void
	*/
	void ConfigWidget::radioButton1(bool flag) {
		if (flag == true)
		{
			mColorTab->setColorStyle(0);
		}
	}
	/**
	* @brief  ConfigWidget::radioButton2
	* @param  bool flag
	* @return void
	*/
	void ConfigWidget::radioButton2(bool flag) {
		if (flag == true)
		{
			mColorTab->setColorStyle(1);
		}
	}
	/**
	* @brief  ConfigWidget::setfirstColor 设置起始颜色
	* @return void
	*/
	void ConfigWidget::setfirstColor() {
		QColor color = ui->firstColorBtn->palette().button().color();
		//QColor color = QColorDialog::getColor(Qt::white, this, "pick Color", QColorDialog::ShowAlphaChannel);
		QColorDialog dlg(this);
		dlg.setOption(QColorDialog::ShowAlphaChannel);
		dlg.setCurrentColor(color);
		if (dlg.exec() == QColorDialog::Accepted)
			color = dlg.currentColor();
		QPalette qpalette = ui->firstColorBtn->palette();
		qpalette.setColor(QPalette::Button, color);
		ui->firstColorBtn->setPalette(qpalette);
		arrowCtrl->SetFirstColor(color);

	}
	/**
	* @brief  ConfigWidget::setendColor 设置终止颜色
	* @return void
	*/
	void ConfigWidget::setendColor() {

		QColor color = ui->endColorBtn->palette().button().color();
		QColorDialog dlg(this);
		dlg.setOption(QColorDialog::ShowAlphaChannel);
		dlg.setCurrentColor(color);
		if (dlg.exec() == QColorDialog::Accepted)
			color = dlg.currentColor();
		QPalette qpalette = ui->endColorBtn->palette();
		qpalette.setColor(QPalette::Button, color);
		ui->endColorBtn->setPalette(qpalette);
		arrowCtrl->SetEndColor(color);
	}
	/**
	* @brief  ConfigWidget::getQwtLinearColorMap 返回颜色
	* @return QwtLinearColorMap*
	*/
	QwtLinearColorMap* ConfigWidget::getQwtLinearColorMap()
	{
		//读取xml文件
		Config::GetInstance()->loadConfig();
		ConfigGroup mGroup = Config::GetInstance()->getRootGroup();
		if (!mGroup.GroupIsempty("contour"))
		{
			ConfigGroup contourGroup = mGroup.getGroup("contour");
			bool isres = contourGroup.empty();
			QwtLinearColorMap::Mode mode;
			if (contourGroup.getGroup("lineMapColors").getValue("value").find("ScaleColors") != std::string::npos)
				mode = QwtLinearColorMap::Mode::ScaledColors;
			else
				mode = QwtLinearColorMap::Mode::FixedColors;
			std::vector<float> vals;
			std::vector<QColor> colors;
			auto lineMapColorGroup = contourGroup.getGroup("lineMapColorval");
			int count = atoi(lineMapColorGroup.getValue("valueNumber").c_str());
			vals.clear(); vals.reserve(count);
			colors.clear(); colors.reserve(count);
			for (auto index = 0; index < count; index++)
			{
				float val;
				QColor color;
				val = atof(
					lineMapColorGroup.getGroup(QString("level_%1").arg(index).toStdString()).getValue("value").c_str());
				color = QStringToQColor(QString::fromStdString(
					lineMapColorGroup.getGroup(QString("level_%1").arg(index).toStdString()).getValue("color")));
				vals.push_back(val);
				colors.push_back(color);
			}
			QwtLinearColorMap* colormap = new QwtLinearColorMap(*(colors.begin()), *(colors.end() - 1));
			for (auto index = 1; index < count - 1; index++)
			{
				colormap->addColorStop(vals[index], colors[index]);
			}
			colormap->setMode(mode);
			return colormap;
		}
		else
		{
			QwtLinearColorMap* map = new QwtLinearColorMap(Qt::darkBlue, Qt::darkRed);
			map->addColorStop(0.2, Qt::blue);
			map->addColorStop(0.4, Qt::cyan);
			map->addColorStop(0.6, Qt::yellow);
			map->addColorStop(0.8, Qt::red);
			return map;
		}

	}
	//std::map<double, QColor> ConfigWidget::getColortab()
	//{
	//	std::map<double, QColor> maptab;
	//	Config::GetInstance()->loadConfig();
	//	ConfigGroup mGroup = Config::GetInstance()->getRootGroup();
	//	if (!mGroup.GroupIsempty("contour"))
	//	{
	//
	//	}
	//	else
	//	{
	//
	//	}
	//}
	void ConfigWidget::bindplot(Plot* lp)
	{
		if (lp)
		{
			connect(this, SIGNAL(plotLoadconfig()), lp, SLOT(setappEvent()));
		}
	}
	/**
	* @brief  Mas::Setconfig::Setconfig
	* @return
	*/

	Mas::Setconfig::Setconfig()
		:_1st("1"), _2nd("1"), _3th("1"), _4th("1")
	{}
};

#include "moc_ConfigWidget.cpp"

