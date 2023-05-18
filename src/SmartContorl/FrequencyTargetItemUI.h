#pragma once
#include "TargetItem.h"
#include <QWidget>
namespace Ui {
	class FrequencyTargetItemUI;
}

class FrequencyTargetItemUI :public QWidget,public TargetItem{
public:
	FrequencyTargetItemUI(QWidget* parent = 0);
	~FrequencyTargetItemUI();
	void showG();
public:
	virtual void loadTarget(Target* target) override;
	virtual Target* GenerateTarget() override;

	//‘ÿ»Î∫Õ±£¥Ê
	virtual void saveXml(pugi::xml_node node) override;
	virtual void loadXml(pugi::xml_node node) override;
private:
	Ui::FrequencyTargetItemUI* ui;
};