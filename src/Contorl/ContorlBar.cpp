#include "ContorlBar.h"
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
	if (chipic)
	{
		updateUI();
		chipic.reset();
	}
		
}

#include "moc_ContorlBar.cpp"