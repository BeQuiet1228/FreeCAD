#include "HintDailog.h"
#include <QPushButton>
#include "ui_HintDailog.h"
#include "MessageTransition.h"
HintDailog::HintDailog(QWidget *parent /*= 0*/)
	:QDialog(parent), ui(new Ui::Dialog)
{
	ui->setupUi(this);

	connect(ui->pushButtonContinue, SIGNAL(clicked()), this, SLOT(buttonContinueClicked()));
	connect(ui->pushButtonExit, SIGNAL(clicked()), this, SLOT(buttonExitClincked()));
	connect(ui->pushButtonLose, SIGNAL(clicked()), this, SLOT(buttonLoseClicked()));

	this->setModal(true);
}

HintDailog::~HintDailog()
{

}

/**
* @brief HintDailog::showForMode1 显示继续、忽略、退出 按钮
* @return void
*/
void HintDailog::showForMode1()
{
	mode = 1;
	ui->pushButtonContinue->setEnabled(true);
	ui->pushButtonExit->setEnabled(true);
	ui->pushButtonLose->setEnabled(true);
	this->show();
	
}

/**
* @brief HintDailog::showForMode2 显示继续、退出按钮
* @return void
*/
void HintDailog::showForMode2()
{
	mode = 2;
	ui->pushButtonContinue->setEnabled(true);
	ui->pushButtonExit->setEnabled(true);
	ui->pushButtonLose->setEnabled(false);
	this->show();
}

/**
* @brief HintDailog::showForMode3 显示退出按钮
* @return void
*/
void HintDailog::showForMode3()
{
	mode = 3;
	ui->pushButtonContinue->setEnabled(false);
	ui->pushButtonExit->setEnabled(true);
	ui->pushButtonLose->setEnabled(false);
	this->show();
}

/**
* @brief HintDailog::setText 设置显示文本
* @param const std::string & text
* @return void
*/
void HintDailog::setText(const std::string& text)
{
	QString temp = MessageTransition::gbkStdstringToQstring(text);
	temp = temp.replace("@#$", "\n");
	ui->labelContent->setText(temp);
}

void HintDailog::buttonLoseClicked()
{
	int temp = MODE1_LOSE;
	temp += (mode - 1) * 5;
	if (ui->checkBox->isChecked())
		temp++;
	auto  t = ClinkeType(temp);
	this->close();
	emit buttonClicked(t);

}

void HintDailog::buttonContinueClicked()
{
	int temp = MODE1_CONTINUE;
	temp += (mode - 1) * 5;
	if (ui->checkBox->isChecked())
		temp++;
	auto  t = ClinkeType(temp);
	this->close();
	emit buttonClicked(t);

}

void HintDailog::buttonExitClincked()
{
	int temp = MODE1_EXIT;
	temp += (mode - 1) * 5;
	if (ui->checkBox->isChecked())
		temp++;
	auto  t = ClinkeType(temp);
	this->close();
	emit buttonClicked(t);

}


#include "moc_HintDailog.cpp"
