#include "HintDailog.h"
#include <QPushButton>
HintDailog::HintDailog(QWidget *parent /*= 0*/)
	:QDialog(parent)
{
	ui.setupUi(this);

	connect(ui.pushButtonContinue, SIGNAL(clicked()), this, SLOT(buttonContinueClicked()));
	connect(ui.pushButtonExit, SIGNAL(clicked()), this, SLOT(buttonExitClincked()));
	connect(ui.pushButtonLose, SIGNAL(clicked()), this, SLOT(buttonLoseClicked()));
}

/**
* @brief HintDailog::showForMode1 显示继续、忽略、退出 按钮
* @return void
*/
void HintDailog::showForMode1()
{
	ui.pushButtonContinue->setEnabled(true);
	ui.pushButtonExit->setEnabled(true);
	ui.pushButtonLose->setEnabled(true);
	this->show();
	
}

/**
* @brief HintDailog::showForMode2 显示继续、退出按钮
* @return void
*/
void HintDailog::showForMode2()
{
	ui.pushButtonContinue->setEnabled(true);
	ui.pushButtonExit->setEnabled(true);
	ui.pushButtonLose->setEnabled(false);
	this->show();
}

/**
* @brief HintDailog::showForMode3 显示退出按钮
* @return void
*/
void HintDailog::showForMode3()
{
	ui.pushButtonContinue->setEnabled(false);
	ui.pushButtonExit->setEnabled(true);
	ui.pushButtonLose->setEnabled(false);
	this->show();
}

/**
* @brief HintDailog::setText 设置显示文本
* @param const std::string & text
* @return void
*/
void HintDailog::setText(const std::string& text)
{
	ui.labelContent->setText(QString::fromLocal8Bit(text.c_str()));
}

void HintDailog::buttonLoseClicked()
{
	ClinkeType t;
	t = LOSE;
	emit buttonClicked(t);
}

void HintDailog::buttonContinueClicked()
{
	ClinkeType t;
	t = CONTINUE;
	emit buttonClicked(t);
}

void HintDailog::buttonExitClincked()
{
	ClinkeType t;
	t = EXIT;
	emit buttonClicked(t);
}

#include "moc_HintDailog.cpp"
