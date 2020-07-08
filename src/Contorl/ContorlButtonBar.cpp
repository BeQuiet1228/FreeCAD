#include "ContorlButtonBar.h"
#include <iostream>
#include <QMetaType>
ContorlButtonBar::ContorlButtonBar(QWidget *parent /*= 0*/)
{
	ui.setupUi(this);
}

ContorlButtonBar::~ContorlButtonBar()
{

}

void ContorlButtonBar::setChipicData(std::shared_ptr<Chipic> Chipic)
{
	if (Chipic->pausState)
	{
		ui.toolButtonPause->setText(QString::fromLocal8Bit("开始"));
	}
	else
	{
		ui.toolButtonPause->setText(QString::fromLocal8Bit("暂停"));
	}

	if (Chipic->timerSate)
	{
		ui.toolButtonTimer->setText(QString::fromLocal8Bit("定时器(开)"));
	}
	else
	{
		ui.toolButtonTimer->setText(QString::fromLocal8Bit("定时器(关)"));
	}
}

void ContorlButtonBar::on_toolButtonRun_clicked()
{
	emit buttonClicked(RUN);
}

void ContorlButtonBar::on_toolButtonParalleRun_clicked()
{
	emit buttonClicked(PARALLE_RUN);
}

void ContorlButtonBar::on_toolButtonRefreash_clicked()
{
	emit buttonClicked(REFREASH);
}

void ContorlButtonBar::on_toolButtonLOG_clicked()
{
	emit buttonClicked(LOG);
}

void ContorlButtonBar::on_toolButtonPause_clicked()
{
	emit buttonClicked(PAUSE);
}

void ContorlButtonBar::on_toolButtonTimer_clicked()
{
	emit buttonClicked(TIMER);
}

void ContorlButtonBar::on_toolButton_clicked()
{
	std::cerr << "mm" << std::endl;
}

#include "moc_ContorlButtonBar.cpp"