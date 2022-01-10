#include "ColorBarWidget.h"
#include "QBoxLayout"
#include "ColorTab.h"
#include "Arrowctrl.h"
DV::ColorBarWidget::ColorBarWidget(QWidget* parent/*=nullptr*/)
{
	initUi();
}
DV::ColorBarWidget::~ColorBarWidget()
{

}

std::vector<float> DV::ColorBarWidget::getValue()
{
	return arrowCtrl->getValue();
}
/**
* @time	2022/01/10
* @brief DV::ColorBarWidget::getColors 获取颜色
* @param std::vector<float> & datas
* @return std::vector<QT_NAMESPACE::QColor>
*/
std::vector<QColor> DV::ColorBarWidget::getColors(std::vector<float>& datas)
{
	return mColorTab->GetColors(datas);
}

void DV::ColorBarWidget::setvals(std::vector<float>& vals, std::vector<QColor>& colors)
{
	arrowCtrl->setvals(vals,colors);
	mColorTab->setColors(vals, colors);
	arrowCtrl->SetFirstColor(*colors.begin());
	arrowCtrl->SetEndColor(*(colors.end() - 1));
}

void DV::ColorBarWidget::initUi()
{
	//初始化颜色条
	boxLayout = new QBoxLayout(QBoxLayout::Direction::BottomToTop,this);
	this->setLayout(boxLayout);
	mColorTab = new ColorTab(this);
	boxLayout->addWidget(mColorTab);
	arrowCtrl = new ArrowCtrl(ArrowCtrl::Direction::TopToBottom,this);
	boxLayout->addWidget(arrowCtrl);
	connect(arrowCtrl,
		SIGNAL(changMoveColor(std::vector<float>&, std::vector<QColor>&, const QColor&, const QColor&)),
		mColorTab,
		SLOT(changmoveColor(std::vector<float>&, std::vector<QColor>&, const QColor&, const QColor&)));
}
#include "moc_ColorBarWidget.cpp"