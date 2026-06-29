#include "PiModeTargetItemUI.h"
#include "ui_PiModeTargetItemUI.h" 

PiModeTargetItemUI::PiModeTargetItemUI(QWidget* parent /*= 0*/)
: ui(new Ui::PiModeTargetItemUI())
{
	ui->setupUi(this);
	// 默认隐藏 G 值相关控件
	ui->labelG->hide();
	ui->lineEditG->hide();
}

PiModeTargetItemUI::~PiModeTargetItemUI()
{
	delete ui;
}

void PiModeTargetItemUI::showG()
{
	ui->labelG->show();
	ui->lineEditG->show();
}

void PiModeTargetItemUI::loadTarget(Target* target)
{
	auto piTarget = dynamic_cast<TargetPiMode*>(target);
	if (!piTarget)
		return;
	// 加载轮辐个数
	ui->lineEditWheelCount->setText(QString::number(piTarget->getTargetWheelCount()));
	// 加载 G 值
	ui->lineEditG->setText(QString::number(piTarget->getG()));
}

Target* PiModeTargetItemUI::GenerateTarget()
{
	TargetPiMode* target = new TargetPiMode();

	// 1. 设置基础数据
	int wantCount = ui->lineEditWheelCount->text().toInt();
	target->setTargetWheelCount(wantCount);
	target->setG(ui->lineEditG->text().toDouble());

	// 2. 【关键】设置比较策略：越接近目标值越好 (TargetComprisonApproach)
	// 实例化一个“逼近比较器”
	TargetComparisonProminence* approach = new TargetComparisonProminence();

	// 告诉它：我的满分目标是 8 (wantCount)
	approach->expect = (double)wantCount;
	// 把这个比较器安装给 target 对象
	target->setTargetComprison(approach);

	return target;
}

void PiModeTargetItemUI::saveXml(pugi::xml_node node)
{
	// ID 用于在读取时区分是哪种 Target
	node.append_attribute("ID") = "PiModeTarget";
	node.append_attribute("WheelCount") = ui->lineEditWheelCount->text().toInt();
	node.append_attribute("GValue") = ui->lineEditG->text().toDouble();
}

void PiModeTargetItemUI::loadXml(pugi::xml_node node)
{
	ui->lineEditWheelCount->setText(QString::number(node.attribute("WheelCount").as_int()));
	ui->lineEditG->setText(QString::number(node.attribute("GValue").as_double()));
}
#include "moc_PiModeTargetItemUI.cpp"