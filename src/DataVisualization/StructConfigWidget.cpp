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
	/*
		读取属性
	*/
	XmlData::StructXml xmlInfo;
	XmlData::getXmlInfo(xmlInfo);
#define LOADCONFIGCOLOR(a,c)\
	{\
setButtonColor(c##Color, xmlInfo.proPerty[#a]);\
setButtonColor(c##lineColor, xmlInfo.proPerty[#a "LINE"]);\
	}
	LOADCONFIGCOLOR(DIOLECTRIC,ui->Diolectric);
	LOADCONFIGCOLOR(DIELECTIRANDCONDUCTANCE,ui->dielectirAndconductance);
	LOADCONFIGCOLOR(PERMEABILITY,ui->Permeability);
	LOADCONFIGCOLOR(PERFECTCONDUCTOR, ui->PerfectConductor);
	LOADCONFIGCOLOR(CONDUCTORNEW, ui->ConductorNew);
	//新增属性-20210521
	LOADCONFIGCOLOR(FREESPACE, ui->Freespace);
	LOADCONFIGCOLOR(FOIL, ui->FOIL);
	LOADCONFIGCOLOR(VACUO,ui->Vacuo);
#undef LOADCONFIGCOLOR(a,c)
#define ADDLINECONFIGCOLOR(a,b)\
	setButtonColor(b,xmlInfo.proPerty[#a]);
	ADDLINECONFIGCOLOR(PORT, ui->Port);
	ADDLINECONFIGCOLOR(DRIVER, ui->Driver);
	ADDLINECONFIGCOLOR(INDUCTOR, ui->Inductor);
#undef ADDLINECONFIGCOLOR(a,b)

	//抗锯齿

	ui->structcheckBox->setCheckState((xmlInfo.AlisAttitude) ? Qt::Checked : Qt::Unchecked);


}

void DV::StructConfigWidget::saveConfig()
{
	/*
	* 
	*/
	XmlData::StructXml xmlInfo;
	xmlInfo.proPerty.clear();
	for (auto iter = btnList.begin(); iter != btnList.end(); iter++)
		saveData(xmlInfo.proPerty, *iter);
	xmlInfo.AlisAttitude=((ui->structcheckBox->checkState() == Qt::Checked) ? 1 : 0);
	XmlData::saveXmlInfo(xmlInfo);
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

void DV::StructConfigWidget::saveData(std::map<std::string, QColor>& group, StructButton* btn)
{
	bool isLine = false;
	if (btn->GetStructType() == StructButton::LINE)
		isLine = true;
	//std::string colorStr = getButtonColorstr(btn);
	auto color = getButtonColor(btn);
#define XX(a)\
case (a):\
	{\
		if (!isLine)\
			group.insert(std::pair<std::string,QColor>((#a+14),color));\
		else\
			group.insert(std::pair<std::string,QColor>((#a "LINE" + 14),color));\
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