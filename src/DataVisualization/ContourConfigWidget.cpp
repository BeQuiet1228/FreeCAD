#include "ContourConfigWidget.h"
#include "ui_ContourConfigWidget.h"
#include "QBoxLayout"
#include "ColorTab.h"
#include "Arrowctrl.h"
#include "QPushButton"
#include "CustomConfig.h"
#include "C_encoding.h"
#include "XmlGroup.h"
DV::ContourConfigWidget::ContourConfigWidget(QWidget* parent /*= nullptr*/)
	:QWidget(parent), ui(new Ui::ContourConfigWidget)
{
	ui->setupUi(this);
	initUi();
}

DV::ContourConfigWidget::~ContourConfigWidget()
{

}

void DV::ContourConfigWidget::loadConfig()
{
	/*
		
	*/
	XmlData::ContourXml xmlinfo;
	XmlData::getXmlInfo(xmlinfo);
	if(xmlinfo.lineMapColors=="ScaleColors")
	{
		ui->ScaledColors->setChecked(true);
		ui->FixedColors->setChecked(false);
		mColorTab->setColorStyle(1);
	}
	if(xmlinfo.valueStyle=="raidoOfequality")
	{
		ui->raidoOfequality->setChecked(true);
		ui->equivalent->setChecked(false);
	}
	if (!xmlinfo.values.empty())
	{
		arrowCtrl->setvals(xmlinfo.values, xmlinfo.colors);
		mColorTab->setColors(xmlinfo.values, xmlinfo.colors);
		setButtonColor(ui->firstColorBtn,*(xmlinfo.colors.begin()));
		setButtonColor(ui->endColorBtn,*(xmlinfo.colors.end()-1));
		arrowCtrl->SetEndColor(*(xmlinfo.colors.end() - 1));
		arrowCtrl->SetFirstColor(*xmlinfo.colors.begin());
	}
}

void DV::ContourConfigWidget::saveConfig()
{
	Config::GetInstance()->loadConfig();
	ConfigGroup Group = Config::GetInstance()->getRootGroup();
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
	Config::GetInstance()->saveFile();
}

void DV::ContourConfigWidget::initUi()
{
	this->setWindowTitle(GetEncodingstr("等位图", ENCODING_GB2312));
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
	SETPERPORE(ui->firstColorBtn, btnClicked());
	SETPERPORE(ui->endColorBtn, btnClicked());

	ui->FixedColors->setChecked(true);
	ui->ScaledColors->setChecked(false);
	mColorTab->setColorStyle(0);

	ui->equivalent->setChecked(true);
	ui->raidoOfequality->setChecked(false);
}

void DV::ContourConfigWidget::btnClicked()
{
	auto button = dynamic_cast<QPushButton*>(sender());
	auto color = setButtonColor(button);
	if (button == ui->firstColorBtn)
		arrowCtrl->SetFirstColor(color);
	else if (button == ui->endColorBtn)
		arrowCtrl->SetEndColor(color);
}

void DV::ContourConfigWidget::radioButton1(bool flag)
{
	if (flag == true)
	{
		mColorTab->setColorStyle(0);
	}
}

void DV::ContourConfigWidget::radioButton2(bool flag)
{
	if (flag == true)
	{
		mColorTab->setColorStyle(1);
	}
}

#include "moc_ContourConfigWidget.cpp"
