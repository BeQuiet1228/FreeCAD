#include "ContorlDataBar.h"
#include <QString>
#include "ui_ContorlDataBar.h"
#include "MessageTransition.h"
ContorlDataBar::ContorlDataBar(QWidget *parent /*= 0*/)
	:QWidget(parent), ui(new Ui::Form)
{
	ui->setupUi(this);
}

ContorlDataBar::~ContorlDataBar()
{
	//由于加入到了mainwindow中，会先析，这个析构会有问题，暂时先注释
	//delete ui;
}
/**
* @brief ContorlDataBar::setChipicData 设置显示数据
* @param std::shared_ptr<Chipic> chipic
* @return void
*/
void ContorlDataBar::setChipicData(std::shared_ptr<Chipic> chipic)
{
	//设置提示信息、提示信息中有分割符  需要替换
	auto title = MessageTransition::gbkStdstringToQstring(chipic->title);
	title = title.replace("@#$", "\n");
	ui->labelHint->setText(title);
	//设置粒子数目
	ui->labelParticle->setText(QString::number(chipic->particleCount));
	//设置迭代时间
	ui->labelIterationTimer->setText(QString::fromLocal8Bit(chipic->iterationTimeInt.c_str())
		+ "." + QString::fromLocal8Bit(chipic->iterationTimeFloat.c_str()));
	//设置预估时间
	ui->labelUsedTime->setText(QString::fromLocal8Bit(chipic->currentUsedTime.toString().c_str())
		+ "/" + QString::fromLocal8Bit(chipic->UsedTime.toString().c_str()));
	//设置迭代次数
	float iterationValue = ((float)chipic->currentIteration / chipic->iterationCount) * 100;
	ui->progressBarIterationCount->setValue(iterationValue);

	std::string iteration = std::to_string(chipic->currentIteration) + "/" + std::to_string(chipic->iterationCount);
	ui->progressBarIterationCount->setFormat(QString::fromLocal8Bit(iteration.c_str()));
	
}

#include "moc_ContorlDataBar.cpp"