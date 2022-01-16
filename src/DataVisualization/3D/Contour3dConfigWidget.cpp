#include "Contour3dConfigWidget.h"
#include "ui_Contour3dConfigWidget.h"
#include "../CustomConfig.h"
#include "../C_encoding.h"
#include "../Arrowctrl.h"
#include "../ColorTab.h"
#include "QPushButton"
#include "XmlGroup3D.h"
#include "ControlerConfigWidget.h"
#include "QFormLayout"
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
	XmlData::Contour3dXml xmlinf;
	xmlinf.loadXml();
	ui->rotationEdit->setText(QString::number(xmlinf.Rotation.value));
	std::vector<float> values = xmlinf.colorbar.values.toVector();
	std::vector<QColor> colors = xmlinf.colorbar.colors.toVector();
	if (!values.empty())
	{
		arrowCtrl->setvals(values,colors);
		mColorTab->setColors(values, colors);
		arrowCtrl->SetEndColor(*(colors.end() - 1));
		arrowCtrl->SetFirstColor(*colors.begin());
		setButtonColor(ui->firstColorBtn, *colors.begin());
		setButtonColor(ui->endColorBtn, *(colors.end() - 1));
	}
	controlerConfigWidget->loadConfig(xmlinf.controlerXml);
}
void DV3D::Contour3dConfigWidget::saveConfig()
{
	XmlData::Contour3dXml xmlinfo;
	xmlinfo.colorbar.values = arrowCtrl->getValue();
	xmlinfo.colorbar.colors = mColorTab->GetColors(xmlinfo.colorbar.values.toVector());
	xmlinfo.Rotation = ui->rotationEdit->text().toInt();
	xmlinfo.saveXml();
	controlerConfigWidget->saveConfig(xmlinfo.controlerXml);
}
void DV3D::Contour3dConfigWidget::initUi()
{
	this->setWindowTitle(DV::GetEncodingstr("3维等位图", ENCODING_GB2312));
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
	/*
	* 添加窗口
	*/
	QFormLayout* layout = new QFormLayout;
	ui->topWidget->setLayout(layout);
	controlerConfigWidget = new ControlerConfigWidget(ui->topWidget);
	controlerConfigWidget->setParentGroup("contour3d");
	layout->addWidget(controlerConfigWidget);
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
