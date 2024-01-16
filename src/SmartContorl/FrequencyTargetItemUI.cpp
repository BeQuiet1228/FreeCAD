#include "FrequencyTargetItemUI.h"
#include "ui_FrequencyTargetItemUI.h"
FrequencyTargetItemUI::FrequencyTargetItemUI(QWidget* parent /*= 0*/)
	:ui(new Ui::FrequencyTargetItemUI())
{
	ui->setupUi(this);
	ui->labelG->hide();
	ui->lineEditG->hide();
}

FrequencyTargetItemUI::~FrequencyTargetItemUI()
{
	delete ui;
}

void FrequencyTargetItemUI::showG()
{
	ui->labelG->show();
	ui->lineEditG->show();
}

void FrequencyTargetItemUI::loadTarget(Target* target)
{
	auto frequencyTarget = dynamic_cast<TargetFrequency*>(target);
	if (!frequencyTarget)
		return;

	ui->lineEditName->setText(QString::fromStdString(frequencyTarget->Name));
	ui->lineEditMaxFrequency->setText(QString::number(frequencyTarget->getMaxFrequency()));
	ui->lineEditMiniFrequency->setText(QString::number(frequencyTarget->getMinFrequency()));
	ui->lineEditG->setText(QString::number(frequencyTarget->getG()));
}

Target* FrequencyTargetItemUI::GenerateTarget()
{
	TargetFrequency* target = new TargetFrequency();
	double max, min;
	max = ui->lineEditMaxFrequency->text().toDouble();
	min = ui->lineEditMiniFrequency->text().toDouble();
	target->setFrequencyRange(max, min);

	target->Name = ui->lineEditName->text().toStdString();
	target->setG(ui->lineEditG->text().toDouble());

	return target;
}

void FrequencyTargetItemUI::saveXml(pugi::xml_node node)
{
	node.append_attribute("ID") = "FrequencyTarget";
	node.append_attribute("ObserveName") = ui->lineEditName->text().toStdString().c_str();
	node.append_attribute("MaxFrequency") = ui->lineEditMaxFrequency->text().toDouble();
	node.append_attribute("MinFrequency") = ui->lineEditMiniFrequency->text().toDouble();
	node.append_attribute("GValue") = ui->lineEditG->text().toDouble();
}

void FrequencyTargetItemUI::loadXml(pugi::xml_node node)
{
	ui->lineEditName->setText(QString::fromStdString(node.attribute("ObserveName").as_string()));
	ui->lineEditMaxFrequency->setText(QString::number(node.attribute("MaxFrequency").as_double()));
	ui->lineEditMiniFrequency->setText(QString::number(node.attribute("MinFrequency").as_double()));
	ui->lineEditG->setText(QString::number(node.attribute("GValue").as_double()));
}