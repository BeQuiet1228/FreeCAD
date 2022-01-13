#include "Vector3dConfigWidget.h"
#include "ui_Vector3dConfigWidget.h"
#include "../CustomConfig.h"
#include "../C_encoding.h"
#include "../Arrowctrl.h"
#include "../ColorTab.h"
#include "QPushButton"
#include "XmlGroup3D.h"
#include "ControlerConfigWidget.h"
#include "QFormLayout"
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
	XmlData::Vector3dXml xmlinfo;
	XmlData::loadXmlInfo(xmlinfo);
	ui->xGridInc->setText(QString::number(xmlinfo.XorRGridInc));
	ui->yGridInc->setText(QString::number(xmlinfo.YorThetaGridInc));
	ui->zGridInc->setText(QString::number(xmlinfo.ZGridInc));
	if (!xmlinfo.colorBar.values.empty())
	{
		arrowCtrl->setvals(xmlinfo.colorBar.values,xmlinfo.colorBar.colors);
		mColorTab->setColors(xmlinfo.colorBar.values, xmlinfo.colorBar.colors);
		arrowCtrl->SetEndColor(*(xmlinfo.colorBar.colors.end() - 1));
		arrowCtrl->SetFirstColor(*xmlinfo.colorBar.colors.begin());
		setButtonColor(ui->firstColorBtn, *xmlinfo.colorBar.colors.begin());
		setButtonColor(ui->endColorBtn, *(xmlinfo.colorBar.colors.end() - 1));
	}
	controlerConfigWidget->loadConfig();
}


/**
* @time	2022/01/10
* @brief DV3D::Vector3dConfigWidget::saveConfig 保存配置
* @return void
*/
void DV3D::Vector3dConfigWidget::saveConfig()
{
	XmlData::Vector3dXml xmlinf;
	xmlinf.XorRGridInc = ui->xGridInc->text().toInt();
	xmlinf.YorThetaGridInc= ui->yGridInc->text().toInt();
	xmlinf.ZGridInc= ui->zGridInc->text().toInt();
	xmlinf.colorBar.values= arrowCtrl->getValue();
	xmlinf.colorBar.colors= mColorTab->GetColors(xmlinf.colorBar.values);
	XmlData::saveXmlInfo(xmlinf);
	controlerConfigWidget->saveConfig();
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
	SETPERPORE(ui->firstColorBtn, btnClicked());
	SETPERPORE(ui->endColorBtn, btnClicked());
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
	QFormLayout* layout = new QFormLayout;
	ui->topWidget->setLayout(layout);
	controlerConfigWidget = new ControlerConfigWidget(ui->topWidget);
	controlerConfigWidget->setParentGroup("vector3d");
	layout->addWidget(controlerConfigWidget);
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

