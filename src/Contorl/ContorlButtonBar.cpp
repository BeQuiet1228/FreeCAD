#include "ContorlButtonBar.h"
#include <iostream>
#include <QMetaType>
#include "ui_ContorlButtonBar.h"
#include "Chipic.h"
ContorlButtonBar::ContorlButtonBar(QWidget *parent /*= 0*/)
	:ContorlBar(parent), ui(new Ui::ContorlButtonBar)
{
	ui->setupUi(this);
#ifdef _CONTORL_DLL_
	ui->toolButtonConnectionWay->hide();
	ui->toolButton->hide();
	ui->toolButtonLOG->hide();
	ui->toolButtonParalleRun->hide();
	ui->toolButtonRun->hide();
	ui->toolButtonRefreash->hide();
#endif // _CONTORL_DLL_

	
}

ContorlButtonBar::~ContorlButtonBar()
{
	delete ui;
}

void ContorlButtonBar::chipicClose()
{
	this->ui->toolButtonRefreash->setEnabled(false);
	this->ui->toolButtonPause->setEnabled(false);
	this->ui->toolButtonTimer->setEnabled(false);
	this->ui->toolButtonParalleRun->setEnabled(true);
	this->ui->toolButtonConnectionWay->setEnabled(true);
	this->ui->toolButton->setEnabled(true);

	QIcon icon;
	icon.addFile(QString::fromUtf8(":/icon/run.svg"), QSize(), QIcon::Normal, QIcon::Off);
	ui->toolButtonRun->setIcon(icon);
}

/**
* @brief ContorlButtonBar::setConnectionWayIcon 设置连接方式图标
* @param const int & way  1:本地连接图标 2:网络连接图标 其他:不做处理
* @return void
*/
void ContorlButtonBar::setConnectionWayIcon(const int& way)
{
	QIcon icon;
	if (way == 1)
	{
		icon.addFile(QString::fromUtf8(":/icon/local.svg"), QSize(), QIcon::Normal, QIcon::Off);
		ui->toolButtonConnectionWay->setIcon(icon);
	} else if (way == 2){
		icon.addFile(QString::fromUtf8(":/icon/network .svg"), QSize(), QIcon::Normal, QIcon::Off);
		ui->toolButtonConnectionWay->setIcon(icon);
	}
}

void ContorlButtonBar::updateUI()
{
	//有chipic在运行 则改变图标可用状态
	this->ui->toolButtonRefreash->setEnabled(true);
	this->ui->toolButtonPause->setEnabled(true);
	this->ui->toolButtonTimer->setEnabled(true);
	this->ui->toolButtonParalleRun->setEnabled(false);
	this->ui->toolButtonConnectionWay->setShortcutEnabled(false);
	this->ui->toolButton->setEnabled(false);
	if (chipic->pausState)
	{
		QIcon icon5;
		icon5.addFile(QString::fromUtf8(":/icon/continue.svg"), QSize(), QIcon::Normal, QIcon::Off);
		ui->toolButtonPause->setIcon(icon5);
	}
	else
	{
		QIcon icon5;
		icon5.addFile(QString::fromUtf8(":/icon/pause.svg"), QSize(), QIcon::Normal, QIcon::Off);
		ui->toolButtonPause->setIcon(icon5);
	}

	if (chipic->timerSate)
	{
		QIcon icon5;
		icon5.addFile(QString::fromUtf8(":/icon/on.svg"), QSize(), QIcon::Normal, QIcon::Off);
		ui->toolButtonTimer->setIcon(icon5);
	}
	else
	{
		QIcon icon5;
		icon5.addFile(QString::fromUtf8(":/icon/off.svg"), QSize(), QIcon::Normal, QIcon::Off);
		ui->toolButtonTimer->setIcon(icon5);
	}

	QIcon icon;
	icon.addFile(QString::fromUtf8(":/icon/finish.svg"), QSize(), QIcon::Normal, QIcon::Off);
	ui->toolButtonRun->setIcon(icon);

	this->update();
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
	emit buttonClicked(SMART_CONTORL);
}

void ContorlButtonBar::on_toolButtonConnectionWay_clicked()
{
	emit buttonClicked(CONNECTION_WAY);
}

#include "moc_ContorlButtonBar.cpp"