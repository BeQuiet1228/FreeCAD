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
		QIcon icon5;
		icon5.addFile(QString::fromUtf8(":/icon/continue.svg"), QSize(), QIcon::Normal, QIcon::Off);
		ui.toolButtonPause->setIcon(icon5);
	}
	else
	{
		QIcon icon5;
		icon5.addFile(QString::fromUtf8(":/icon/pause.svg"), QSize(), QIcon::Normal, QIcon::Off);
		ui.toolButtonPause->setIcon(icon5);
	}

	if (Chipic->timerSate)
	{
		QIcon icon5;
		icon5.addFile(QString::fromUtf8(":/icon/on.svg"), QSize(), QIcon::Normal, QIcon::Off);
		ui.toolButtonTimer->setIcon(icon5);
	}
	else
	{
		QIcon icon5;
		icon5.addFile(QString::fromUtf8(":/icon/off.svg"), QSize(), QIcon::Normal, QIcon::Off);
		ui.toolButtonTimer->setIcon(icon5);
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