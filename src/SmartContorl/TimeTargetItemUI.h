#pragma once
#include <QWidget>
#include "Target.h"
#include "xml/pugixml.hpp"
#include "TargetItem.h"
namespace Ui {
	class TimeTargetItemUI;
}

class TimeTargetItemUI :public QWidget ,public TargetItem{
	Q_OBJECT
public:
	TimeTargetItemUI(QWidget* parent = 0);
	~TimeTargetItemUI();
public:
	void loadTarget(TargetTime* target);
	TargetTime* GenerateTimeTarget();
	void loadTarget(Target* target) override;
	Target* GenerateTarget() override;

	//‘ÿ»Î∫Õ±£¥Ê
	void saveXml(pugi::xml_node node) override;
	void loadXml(pugi::xml_node node) override;
public Q_SLOTS:
	void currentIndexChange(int index);
private:
	Ui::TimeTargetItemUI* ui;
};