#include "Contour3dConfigWidget.h"
#include "ui_Contour3dConfigWidget.h"
#include "../CustomConfig.h"
#include "../C_encoding.h"
#include "../Arrowctrl.h"
#include "../ColorTab.h"
#include "QPushButton"
DV3D::Contour3dConfigWidget::Contour3dConfigWidget(QWidget* parent/*=nullptr*/)
	:QWidget(parent), ui(new Ui::Contour3dConfigWidget)
{
	ui->setupUi(this);
	initUi();
}
DV3D::Contour3dConfigWidget::~Contour3dConfigWidget()
{

}
void DV3D::Contour3dConfigWidget::loadConfig()
{
	DV::Config::GetInstance()->loadConfig();
	auto Group = DV::Config::GetInstance()->getRootGroup();
	auto contourGroup = Group.getGroup("contour3d");
	auto valNumberGroup = contourGroup.getGroup("valueNumber");
	unsigned int valNumber = atoi(valNumberGroup.getValue("value").c_str());
	std::vector<float> vals;
	std::vector<QColor> colors;
	for (auto index = 0; index < valNumber; ++index)
	{
		vals.push_back(atof(valNumberGroup.getGroup(QString("level_%1").arg(index).toStdString()).getValue("value").c_str()));
		colors.push_back(DV::QStringToQColor(QString::fromStdString(valNumberGroup.getGroup(QString("level_%1").arg(index).toStdString()).getValue("color"))));
	}
	if (!vals.empty())
	{
		arrowCtrl->setvals(vals, colors);
		mColorTab->setColors(vals, colors);
		arrowCtrl->SetEndColor(*(colors.end() - 1));
		arrowCtrl->SetFirstColor(*colors.begin());
		setButtonColor(ui->firstColorBtn, *colors.begin());
		setButtonColor(ui->endColorBtn, *(colors.end() - 1));
	}
}
void DV3D::Contour3dConfigWidget::saveConfig()
{
	DV::Config::GetInstance()->loadConfig();
	auto Group = DV::Config::GetInstance()->getRootGroup();
	auto contourGroup = Group.getGroup("contour3d");
	/*
		3维等位图
	*/
	std::vector<float> values = arrowCtrl->getValue();
	std::vector<QColor> colors = mColorTab->GetColors(values);
	auto valueNumberGroup = contourGroup.getGroup("valueNumber");
	valueNumberGroup.
		setSetting("value"
			, QString("%1")
			.arg(values.size())
			.toStdString());
	for (auto index = 0; index < values.size(); index++)
	{
		valueNumberGroup
			.getGroup(QString("level_%1").arg(index).toStdString())
			.setSetting("value", QString("%1").arg(values[index]).toStdString());
		valueNumberGroup
			.getGroup(QString("level_%1").arg(index).toStdString())
			.setSetting("color", DV::QColorToQstring(colors[index]).toStdString());
	}
}
void DV3D::Contour3dConfigWidget::initUi()
{
	this->setWindowTitle(DV::GetEncodingstr("3维等位图", ENCODING_GB2312));
	SetAllreRenderer(ui->firstColorBtn);
	SetAllreRenderer(ui->endColorBtn);
	connect(ui->firstColorBtn, SIGNAL(clicked()), this, SLOT(btnClicked()));
	connect(ui->endColorBtn, SIGNAL(clicked()), this, SLOT(btnClicked()));
	boxLayout = new QBoxLayout(QBoxLayout::Direction::BottomToTop, ui->colorBar);
	mColorTab = new DV::ColorTab(ui->colorBar);
	mColorTab->setColorStyle(1);
	ui->colorBar->setLayout(boxLayout);
	boxLayout->addWidget(mColorTab);
	arrowCtrl = new DV::ArrowCtrl(DV::ArrowCtrl::Direction::TopToBottom, ui->colorBar);
	boxLayout->addWidget(arrowCtrl);
	connect(arrowCtrl,
		SIGNAL(changMoveColor(std::vector<float>&, std::vector<QColor>&, const QColor&, const QColor&)),
		mColorTab,
		SLOT(changmoveColor(std::vector<float>&, std::vector<QColor>&, const QColor&, const QColor&)));

}

void DV3D::Contour3dConfigWidget::btnClicked()
{
	auto button = dynamic_cast<QPushButton*>(sender());
	auto color = setButtonColor(button);
	if (button == ui->firstColorBtn)
		arrowCtrl->SetFirstColor(color);
	else if (button == ui->endColorBtn)
		arrowCtrl->SetEndColor(color);
}
