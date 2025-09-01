#include "TimeTargetItemUI.h"
#include "ui_TimeTargetItemUI.h"
#include "ui_TimeDoubleTargetItemUI.h"
TimeTargetItemUI::TimeTargetItemUI(QWidget* parent /*= 0*/)
	:ui(new Ui::TimeTargetItemUI())
{
	ui->setupUi(this);
	connect(ui->comboBoxExcpcet, SIGNAL(currentIndexChanged(int)), this, SLOT(currentIndexChange(int)));
	ui->widgetAccuracy->hide();
	ui->widgetG->hide();
}

TimeTargetItemUI::~TimeTargetItemUI()
{
	delete ui;
}

void TimeTargetItemUI::showG()
{
	ui->widgetG->show();
}

void TimeTargetItemUI::loadTarget(TargetTime* target)
{
	ui->lineEditName->setText(QString::fromStdString(target->Name));
	ui->lineEditMaxTime->setText(QString::number(target->getMaxTime()));
	ui->lineEditMiniTime->setText(QString::number(target->getMinTime()));
	ui->lineEditMaxF->setText(QString::number(target->value));
	ui->lineEditG->setText(QString::number(target->getG()));
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
	target->setG(ui->lineEditG->text().toDouble());
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
	node.append_attribute("GValue") = ui->lineEditG->text().toStdString().c_str();
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
	ui->lineEditG->setText(QString::number(node.attribute("GValue").as_double()));
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

TimeDoubleTargetItemUI::TimeDoubleTargetItemUI(QWidget* parent /*= 0*/)
	:ui(new Ui::TimeDoubleTargetItemUI())
{
	ui->setupUi(this);
	connect(ui->comboBoxExcpcet, SIGNAL(currentIndexChanged(int)), this, SLOT(currentIndexChange(int)));
	ui->widgetAccuracy->hide();
	ui->widgetG->hide();
}

TimeDoubleTargetItemUI::~TimeDoubleTargetItemUI()
{
	delete ui;
}

void TimeDoubleTargetItemUI::showG()
{
	ui->widgetG->show();
}

void TimeDoubleTargetItemUI::loadTarget(TargetTime* target)
{
	ui->lineEditName->setText(QString::fromStdString(target->Name));
	ui->lineEditMaxTime->setText(QString::number(target->getMaxTime()));
	ui->lineEditMiniTime->setText(QString::number(target->getMinTime()));
	ui->lineEditMaxF->setText(QString::number(target->value));
	ui->lineEditG->setText(QString::number(target->getG()));
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


void TimeDoubleTargetItemUI::loadTarget(Target* target)
{
	auto t = dynamic_cast<TargetTime*>(target);
	if (!t)
		return;
	TimeDoubleTargetItemUI::loadTarget(t);
}

Target* TimeDoubleTargetItemUI::GenerateTarget()
{
	return GenerateTimeTarget();
}

TargetTime* TimeDoubleTargetItemUI::GenerateTimeTarget()
{
	TargetTimeDouble* target = new TargetTimeDouble();
	TargetTimeDouble::TargetType targetType;
	//判断目标类型
	if (ui->comboBoxF->currentIndex() == 1)
	{
		targetType = TargetTimeDouble::Mini;
	}
	else if (ui->comboBoxF->currentIndex() == 0) {
		targetType = TargetTimeDouble::MAX;
	}
	else if (ui->comboBoxF->currentIndex() == 2) {
		targetType = TargetTimeDouble::Mean;
	}

	target->setType(targetType);
	target->Name = ui->lineEditName->text().toStdString();
	target->name1 = ui->lineEditName->text().toStdString();
	target->name2 = ui->lineEditName_2->text().toStdString();
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
	target->setG(ui->lineEditG->text().toDouble());
	return target;
}

void TimeDoubleTargetItemUI::saveXml(pugi::xml_node node)
{
	node.append_attribute("ID") = "TimeTargetDouble";
	node.append_attribute("ObserveName") = ui->lineEditName->text().toStdString().c_str();
	node.append_attribute("ObserveName2") = ui->lineEditName_2->text().toStdString().c_str();
	node.append_attribute("MaxTime") = ui->lineEditMaxTime->text().toDouble();
	node.append_attribute("MiniTime") = ui->lineEditMiniTime->text().toDouble();
	node.append_attribute("FModIndex") = ui->comboBoxF->currentIndex();
	node.append_attribute("F") = ui->lineEditMaxF->text().toLongLong();
	node.append_attribute("ExcpectMod") = ui->comboBoxExcpcet->currentIndex();
	node.append_attribute("Accuracy") = ui->lineEditAccuracy->text().toStdString().c_str();
	node.append_attribute("GValue") = ui->lineEditG->text().toStdString().c_str();
}

void TimeDoubleTargetItemUI::loadXml(pugi::xml_node node)
{
	ui->lineEditName->setText(QString::fromStdString(node.attribute("ObserveName").as_string()));
	ui->lineEditName_2->setText(QString::fromStdString(node.attribute("ObserveName2").as_string()));
	ui->lineEditMaxTime->setText(QString::number(node.attribute("MaxTime").as_double()));
	ui->lineEditMiniTime->setText(QString::number(node.attribute("MiniTime").as_double()));
	ui->comboBoxF->setCurrentIndex(node.attribute("FModIndex").as_int());
	ui->lineEditMaxF->setText(QString::number(node.attribute("F").as_llong()));
	ui->comboBoxExcpcet->setCurrentIndex(node.attribute("ExcpectMod").as_int());
	ui->lineEditAccuracy->setText(QString::number(node.attribute("Accuracy").as_double()));
	ui->lineEditG->setText(QString::number(node.attribute("GValue").as_double()));
}

void TimeDoubleTargetItemUI::currentIndexChange(int index)
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
