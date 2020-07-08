#include "ContorlDataBar.h"
#include <QString>
ContorlDataBar::ContorlDataBar(QWidget *parent /*= 0*/)
	:QWidget(parent)
{
	ui.setupUi(this);
}

ContorlDataBar::~ContorlDataBar()
{

}

/**
* @brief ContorlDataBar::setChipicData 设置显示数据
* @param std::shared_ptr<Chipic> chipic
* @return void
*/
void ContorlDataBar::setChipicData(std::shared_ptr<Chipic> chipic)
{
	ui.labelHint->setText(QString::fromLocal8Bit(chipic->titile.c_str()));
	ui.labelParticle->setText(QString::number(chipic->particleCount));
}

#include "moc_ContorlDataBar.cpp"