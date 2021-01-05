#include "ContorlBar.h"
#include "Chipic.h"
std::shared_ptr<QTimer> ContorlBar::timer;

ContorlBar::ContorlBar(QWidget *parent /*= 0*/)
	:QWidget(parent)
{
	//如果定时器还未初始化，则初始化定时器
	if (!timer)
	{
		timer.reset(new QTimer);
		//开始定时
		timer->start(timerTime);
	}

	//链接刷新槽
	connect(timer.get(), SIGNAL(timeout()), this, SLOT(uiTimerOut()));
}

ContorlBar::~ContorlBar()
{

}

/**
* @brief ContorlBar::setChipicData 设置刷新信息的chipic
* @param std::shared_ptr<Chipic> chipic
* @return void
*/
void ContorlBar::setChipicData(std::shared_ptr<Chipic> chipic)
{
	this->chipic = chipic;
}

/**
* @brief ContorlBar::uiTimerOut 定时器界面刷新槽
* @return void
*/
void ContorlBar::uiTimerOut()
{
	//如果chipic存在 且有数据更新 则更新界面信息
	if (!chipic)
		return;
	//如果chipic不为运行状态了  那么将界面初始化为最初的状态
	if (chipic->runState == false)
	{
		chipic.reset();
		this->chipicClose();
		return;
	}	
	if (!chipic->getIsUpdate())
		return;
	updateUI();

}

#include "moc_ContorlBar.cpp"