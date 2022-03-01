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
	xmlinfo.loadXml();
	if (xmlinfo.lineMapColors.value == "ScaleColors")
	{
		ui->ScaledColors->setChecked(true);
		ui->FixedColors->setChecked(false);
		mColorTab->setColorStyle(1);
	}
	if (xmlinfo.valueStyle.value == "raidoOfequality")
	{
		ui->raidoOfequality->setChecked(true);
		ui->equivalent->setChecked(false);
	}
	std::vector<float> values = xmlinfo.colorBar.values.toVector();
	std::vector<QColor> colors = xmlinfo.colorBar.colors.toVector();
	if (xmlinfo.colorBar.values.Size() > 0)
	{
		arrowCtrl->setvals(values, colors);
		mColorTab->setColors(values, colors);
		setButtonColor(ui->firstColorBtn, *(colors.begin()));
		setButtonColor(ui->endColorBtn, *(colors.end() - 1));
		arrowCtrl->SetEndColor(*(colors.end() - 1));
		arrowCtrl->SetFirstColor(*colors.begin());
	}

	return;
}

void DV::ContourConfigWidget::saveConfig()
{
	XmlData::ContourXml xmlinfo;
	//等位图
	ui->equivalent;//等值
	ui->raidoOfequality;//等比
	if (ui->ScaledColors->isChecked())
		xmlinfo.lineMapColors = QString("ScaleColors");
	else
		xmlinfo.lineMapColors = QString("FixedColors");
	(ui->concheckBox->checkState() == Qt::Checked) ?
		(xmlinfo.AlisAttitude = 1) : (xmlinfo.AlisAttitude = 0);
	if (ui->equivalent->isChecked())
		xmlinfo.valueStyle = QString("equivalent");
	else
		xmlinfo.valueStyle = QString("raidoOfequality");
	//获取颜色
	std::vector<float> vals;
	vals = arrowCtrl->getValue();
	xmlinfo.colorBar.values = vals;
	xmlinfo.colorBar.colors = mColorTab->GetColors(vals);
	xmlinfo.saveXml();
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
