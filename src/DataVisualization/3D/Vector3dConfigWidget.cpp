#include "Vector3dConfigWidget.h"
#include "ui_Vector3dConfigWidget.h"
#include "../CustomConfig.h"
#include "../C_encoding.h"
#include "../Arrowctrl.h"
#include "../ColorTab.h"
#include "QPushButton"
DV3D::Vector3dConfigWidget::Vector3dConfigWidget(QWidget* parent/*=nullptr*/)
	:QWidget(parent),ui(new Ui::Vector3dConfigWidget)
{
	ui->setupUi(this);
	initUi();
}

DV3D::Vector3dConfigWidget::~Vector3dConfigWidget()
{

}


/**
* @time	2022/01/10
* @brief DV3D::Vector3dConfigWidget::loadConfig 读取配置
* @return void
*/
void DV3D::Vector3dConfigWidget::loadConfig()
{
	DV::Config::GetInstance()->loadConfig();
	auto Group = DV::Config::GetInstance()->getRootGroup();
	auto vector3dGroup = Group.getGroup("vector3d");
	std::string xGridIncStr = vector3dGroup.getGroup("XorRGridInc").getValue("valMax");
	std::string yGridIncStr = vector3dGroup.getGroup("YorThetaGridInc").getValue("valMax");
	std::string zGridIncStr = vector3dGroup.getGroup("ZGridInc").getValue("valMax");
	ui->xGridInc->setText(QString::fromStdString(xGridIncStr));
	ui->yGridInc->setText(QString::fromStdString(yGridIncStr));
	ui->zGridInc->setText(QString::fromStdString(zGridIncStr));
	auto valNumberGroup = vector3dGroup.getGroup("valueNumber");
	unsigned int valNumber = atoi(valNumberGroup.getValue("value").c_str());
	std::vector<float> vals;
	std::vector<QColor> colors;
	for (auto index=0;index<valNumber;++index)
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
		setButtonColor(ui->endColorBtn,*(colors.end() - 1));
	}
}


/**
* @time	2022/01/10
* @brief DV3D::Vector3dConfigWidget::saveConfig 保存配置
* @return void
*/
void DV3D::Vector3dConfigWidget::saveConfig()
{
	DV::Config::GetInstance()->loadConfig();
	auto Group = DV::Config::GetInstance()->getRootGroup();
	auto vector3dGroup = Group.getGroup("vector3d");
	/*
		3维矢量图
	*/
	vector3dGroup.getGroup("XorRGridInc").setSetting("valMax",ui->xGridInc->text().toStdString());
	vector3dGroup.getGroup("YorThetaGridInc").setSetting("valMax", ui->yGridInc->text().toStdString());
	vector3dGroup.getGroup("ZGridInc").setSetting("valMax", ui->zGridInc->text().toStdString());
	std::vector<float> values = arrowCtrl->getValue();
	std::vector<QColor> colors = mColorTab->GetColors(values);
	auto valueNumber = vector3dGroup.getGroup("valueNumber");
	valueNumber.setSetting("value",std::to_string(values.size()));
	for (auto index = 0; index < values.size(); ++index)
	{
		valueNumber
			.getGroup(QString("level_%1").arg(index).toStdString())
			.setSetting("value", QString("%1").arg(values[index]).toStdString());
		valueNumber
			.getGroup(QString("level_%1").arg(index).toStdString())
			.setSetting("color", DV::QColorToQstring(colors[index]).toStdString());
	}
}

/**
* @time	2022/01/10
* @brief DV3D::Vector3dConfigWidget::initUi 初始话UI
* @return void
*/
void DV3D::Vector3dConfigWidget::initUi()
{
	/*
		初始化相关参数
	*/
	this->setWindowTitle(DV::GetEncodingstr("3维矢量图", ENCODING_GB2312));
	SetAllreRenderer(ui->firstColorBtn);
	SetAllreRenderer(ui->endColorBtn);
	connect(ui->firstColorBtn, SIGNAL(clicked()), this, SLOT(btnClicked()));
	connect(ui->endColorBtn, SIGNAL(clicked()), this, SLOT(btnClicked()));
	//mColorBarWidget = new DV::ColorBarWidget(ui->colorBar);
	//mColorBarWidget->show();
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

void DV3D::Vector3dConfigWidget::btnClicked()
{
	auto button = dynamic_cast<QPushButton*>(sender());
	auto color=setButtonColor(button);
	if (button == ui->firstColorBtn)
		arrowCtrl->SetFirstColor(color);
	else if (button == ui->endColorBtn)
		arrowCtrl->SetEndColor(color);
}

