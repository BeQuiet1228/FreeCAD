#include "TimeTargetItemUI.h"
#include "ui_TimeTargetItemUI.h"
TimeTargetItemUI::TimeTargetItemUI(QWidget* parent /*= 0*/)
	:ui(new Ui::TimeTargetItemUI())
{
	ui->setupUi(this);
	connect(ui->comboBoxExcpcet, SIGNAL(currentIndexChanged(int)), this, SLOT(currentIndexChange(int)));
}

TimeTargetItemUI::~TimeTargetItemUI()
{
	delete ui;
}

void TimeTargetItemUI::loadTarget(TargetTime* target)
{
	ui->lineEditName->setText(QString::fromStdString(target->Name));
	ui->lineEditMaxTime->setText(QString::number(target->getMaxTime()));
	ui->lineEditMiniTime->setText(QString::number(target->getMinTime()));
	ui->lineEditMaxF->setText(QString::number(target->value));

	//判断目标类型
	if (dynamic_cast<TargetTimeMin*>(target))
	{
		ui->comboBoxF->setCurrentIndex(1);
	}
	else if (dynamic_cast<TargetTimeMax*>(target)) {
		ui->comboBoxF->setCurrentIndex(0);
	}
	else if (dynamic_cast<TargetTimeMean*>(target)) {
		ui->comboBoxF->setCurrentIndex(2);
	}

	//判断目标对比方式
	TargetComprison* comprison = target->getTargetComprison();
	if (dynamic_cast<TargetComprisonGreaterThan*>(target))
	{
		ui->comboBoxExcpcet->setCurrentIndex(1);
	}
	else {
		ui->comboBoxExcpcet->setCurrentIndex(0);
		TargetComprisonApproach* approach = dynamic_cast<TargetComprisonApproach*>(comprison);
		ui->lineEditAccuracy->setText(QString::number(approach->errorRange));
	}
}


void TimeTargetItemUI::loadTarget(Target* target)
{
	auto t = dynamic_cast<TargetTime*>(target);
	if (!t)
		return;
	TimeTargetItemUI::loadTarget(t);
}

Target* TimeTargetItemUI::GenerateTarget()
{
	return GenerateTimeTarget();
}

TargetTime* TimeTargetItemUI::GenerateTimeTarget()
{
	TargetTime* target;

	//判断目标类型
	if (ui->comboBoxF->currentIndex() == 1)
	{
		target = new TargetTimeMin();
	}
	else if (ui->comboBoxF->currentIndex() == 0) {
		target = new TargetTimeMax();
	}
	else if (ui->comboBoxF->currentIndex() == 2) {
		target = new TargetTimeMean();
	}


	target->Name = ui->lineEditName->text().toStdString();
	double maxTime = ui->lineEditMaxTime->text().toDouble();
	double minTime = ui->lineEditMiniTime->text().toDouble();
	double value = ui->lineEditMaxF->text().toDouble();

	target->setTimesRange(minTime, maxTime);
	target->value = value;

	//判断目标对比方式
	if (ui->comboBoxExcpcet->currentIndex() == 1)
	{
		target->setTargetComprison(new TargetComprisonGreaterThan());
	}
	else {
		TargetComprisonApproach* approach = new TargetComprisonApproach();
		approach->errorRange = ui->lineEditAccuracy->text().toInt();
		approach->expect = value;
		target->setTargetComprison(approach);
	}

	return target;
}

void TimeTargetItemUI::saveXml(pugi::xml_node node)
{
	node.append_attribute("ID") = "TimeTarget";
	node.append_attribute("ObserveName") = ui->lineEditName->text().toStdString().c_str();
	node.append_attribute("MaxTime") = ui->lineEditMaxTime->text().toDouble();
	node.append_attribute("MiniTime") = ui->lineEditMiniTime->text().toDouble();
	node.append_attribute("FModIndex") = ui->comboBoxF->currentIndex();
	node.append_attribute("F") = ui->lineEditMaxF->text().toLongLong();
	node.append_attribute("ExcpectMod") = ui->comboBoxExcpcet->currentIndex();
	node.append_attribute("Accuracy") = ui->lineEditAccuracy->text().toStdString().c_str();
}

void TimeTargetItemUI::loadXml(pugi::xml_node node)
{
	ui->lineEditName->setText(QString::fromStdString(node.attribute("ObserveName").as_string()));
	ui->lineEditMaxTime->setText(QString::number(node.attribute("MaxTime").as_double()));
	ui->lineEditMiniTime->setText(QString::number(node.attribute("MiniTime").as_double()));
	ui->comboBoxF->setCurrentIndex(node.attribute("FModIndex").as_int());
	ui->lineEditMaxF->setText(QString::number(node.attribute("F").as_llong()));
	ui->comboBoxExcpcet->setCurrentIndex(node.attribute("ExcpectMod").as_int());
	ui->lineEditAccuracy->setText(QString::number(node.attribute("Accuracy").as_double()));
}

void TimeTargetItemUI::currentIndexChange(int index)
{
	if (index == 0)
	{
		ui->widgetAccuracy->show();
	}
	else {
		ui->widgetAccuracy->hide();
	}
}

#include "moc_TimeTargetItemUI.cpp"
