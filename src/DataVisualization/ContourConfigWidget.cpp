#include "ContourConfigWidget.h"
#include "ui_ContourConfigWidget.h"
#include "QBoxLayout"
#include "ColorTab.h"
#include "Arrowctrl.h"
#include "QPushButton"
#include "CustomConfig.h"
#include "C_encoding.h"
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
	Config::GetInstance()->loadConfig();
	auto Group = Config::GetInstance()->getRootGroup();
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
