#include "StructConfigWidget.h"
#include "structbutton.h"
#include "ui_StructConfigWidget.h"
#include "C_encoding.h"
#include "XmlGroup.h"
DV::StructConfigWidget::StructConfigWidget(QWidget* parent /*= nullptr*/)
	:QWidget(parent), ui(new Ui::StructConfigWidget)
{
	ui->setupUi(this);
	initUi();
}

DV::StructConfigWidget::~StructConfigWidget()
{
	btnList.clear();
}

void DV::StructConfigWidget::loadConfig()
{
	Config::GetInstance()->loadConfig();
	auto Group = Config::GetInstance()->getRootGroup();
	auto StructGroup = Group.getGroup("struct");
	/*
		读取属性
	*/
#define LOADCONFIGCOLOR(a,b,c)\
	{\
	setButtonColor(c##Color, (b).getGroup(#a).getValue("value")); \
	setButtonColor(c##lineColor, (b).getGroup(#a "LINE").getValue("value"));\
	}
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
#define ADDLINECONFIGCOLOR(a,b)\
	setButtonColor(b,StructGroup.getGroup(#a).getValue("value"));
	ADDLINECONFIGCOLOR(PORT, ui->Port);
	ADDLINECONFIGCOLOR(DRIVER, ui->Driver);
	ADDLINECONFIGCOLOR(INDUCTOR, ui->Inductor);
#undef ADDLINECONFIGCOLOR(a,b)
	StructXmlGroup structXmlGroup;
	auto xmlInfo = structXmlGroup.getXmlInfo();
	//抗锯齿

	ui->structcheckBox->setCheckState((xmlInfo.AlisAttitude) ? Qt::Checked : Qt::Unchecked);


}

void DV::StructConfigWidget::saveConfig()
{
	Config::GetInstance()->loadConfig();
	auto Group = Config::GetInstance()->getRootGroup();
	auto StructGroup = Group.getGroup("struct");
	for (auto iter = btnList.begin(); iter != btnList.end(); iter++)
		saveData(StructGroup, *iter);
	Config::GetInstance()->saveFile();
}

void DV::StructConfigWidget::initUi()
{
	this->setWindowTitle(GetEncodingstr("结构图", ENCODING_GB2312));
	/*
	设置属性
	*/
#define SETSTRUCTPERPORE(a,b,c)\
	(a)->setStructType((b), (c)); \
	SETPERPORE((a), btnClicked())\
	btnList.push_back(a);

	SETSTRUCTPERPORE(ui->PerfectConductorColor, StructButton::BLACK, StructButton::PERFECTCONDUCTOR);
	SETSTRUCTPERPORE(ui->ConductorNewColor, StructButton::BLACK, StructButton::CONDUCTORNEW);
	SETSTRUCTPERPORE(ui->DiolectricColor, StructButton::BLACK, StructButton::DIOLECTRIC);
	SETSTRUCTPERPORE(ui->PermeabilityColor, StructButton::BLACK, StructButton::PERMEABILITY);
	//
	SETSTRUCTPERPORE(ui->PerfectConductorlineColor, StructButton::LINE, StructButton::PERFECTCONDUCTOR);
	SETSTRUCTPERPORE(ui->ConductorNewlineColor, StructButton::LINE, StructButton::CONDUCTORNEW);
	SETSTRUCTPERPORE(ui->DiolectriclineColor, StructButton::LINE, StructButton::DIOLECTRIC);
	SETSTRUCTPERPORE(ui->PermeabilitylineColor, StructButton::LINE, StructButton::PERMEABILITY);

	//新增加属性2021-5-21
	SETSTRUCTPERPORE(ui->dielectirAndconductanceColor, StructButton::BLACK, StructButton::DIELECTIRANDCONDUCTANCE);
	SETSTRUCTPERPORE(ui->dielectirAndconductancelineColor, StructButton::LINE, StructButton::DIELECTIRANDCONDUCTANCE);
	SETSTRUCTPERPORE(ui->FreespaceColor, StructButton::BLACK, StructButton::FREESPACE);
	SETSTRUCTPERPORE(ui->FreespacelineColor, StructButton::LINE, StructButton::FREESPACE);
	SETSTRUCTPERPORE(ui->FOILColor, StructButton::BLACK, StructButton::FOIL);
	SETSTRUCTPERPORE(ui->FOILlineColor, StructButton::LINE, StructButton::FOIL);
	//新增加属性真空2021-11-23			
	SETSTRUCTPERPORE(ui->VacuoColor, StructButton::BLACK, StructButton::VACUO);
	SETSTRUCTPERPORE(ui->VacuolineColor, StructButton::LINE, StructButton::VACUO);
	//线段							  
	SETSTRUCTPERPORE(ui->Port, StructButton::BLACK, StructButton::PORT);
	SETSTRUCTPERPORE(ui->Inductor, StructButton::BLACK, StructButton::INDUCTOR);
	SETSTRUCTPERPORE(ui->Driver, StructButton::BLACK, StructButton::DRIVER);
#undef SETSTRUCTPERPORE(a,b,c) 
}

void DV::StructConfigWidget::saveData(ConfigGroup& group, StructButton* btn)
{
	bool isLine = false;
	if (btn->GetStructType() == StructButton::LINE)
		isLine = true;
	std::string colorStr = getButtonColorstr(btn);

#define XX(a)\
case (a):\
	{\
		if (!isLine)\
			group.getGroup((#a + 14)).setSetting("value", colorStr); \
		else\
			group.getGroup((#a "LINE" + 14)).setSetting("value", colorStr);\
	}\
	break;
	switch (btn->GetStructTexture())
	{
		XX(StructButton::VACUO);
		XX(StructButton::PERFECTCONDUCTOR);
		XX(StructButton::CONDUCTORNEW);
		XX(StructButton::DIOLECTRIC);
		XX(StructButton::DIELECTIRANDCONDUCTANCE);
		XX(StructButton::PERMEABILITY);
		XX(StructButton::FREESPACE);
		XX(StructButton::FOIL);
		//线段
		XX(StructButton::PORT);
		XX(StructButton::DRIVER);
		XX(StructButton::INDUCTOR);
	}
#undef XX(a)
}

void DV::StructConfigWidget::btnClicked()
{
	auto button = dynamic_cast<QPushButton*>(sender());
	auto color = setButtonColor(button);
}
#include "moc_StructConfigWidget.cpp"