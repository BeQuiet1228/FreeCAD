#include "Contour3dConfigWidget.h"
#include "ui_Contour3dConfigWidget.h"
#include "../CustomConfig.h"
#include "../C_encoding.h"
#include "../Arrowctrl.h"
#include "../ColorTab.h"
#include "QPushButton"
#include "XmlGroup3D.h"
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
	XmlData::loadXmlInfo(xmlinf);
	if (!xmlinf.values.empty())
	{
		arrowCtrl->setvals(xmlinf.values,xmlinf.colors);
		mColorTab->setColors(xmlinf.values, xmlinf.colors);
		arrowCtrl->SetEndColor(*(xmlinf.colors.end() - 1));
		arrowCtrl->SetFirstColor(*xmlinf.colors.begin());
		setButtonColor(ui->firstColorBtn, *xmlinf.colors.begin());
		setButtonColor(ui->endColorBtn, *(xmlinf.colors.end() - 1));
	}

}
void DV3D::Contour3dConfigWidget::saveConfig()
{
	XmlData::Contour3dXml xmlinfo;
	xmlinfo.values = arrowCtrl->getValue();
	xmlinfo.colors = mColorTab->GetColors(xmlinfo.values);
	XmlData::saveXmlInfo(xmlinfo);
}
void DV3D::Contour3dConfigWidget::initUi()
{
	this->setWindowTitle(DV::GetEncodingstr("3Î¬µÈÎ»Í¼", ENCODING_GB2312));
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
