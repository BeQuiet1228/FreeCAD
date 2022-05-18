#pragma once
#include <QWidget>
#include "Target.h"
#include "xml/pugixml.hpp"
namespace Ui {
	class TargetItem;
}

class TargetItem :public QWidget {
	Q_OBJECT
public:
	TargetItem(QWidget* parent = 0);
	~TargetItem();
public:
	void loadTarget(TargetTime* target);
	TargetTime* GenerateTarget();

	//‘ÿ»Î∫Õ±£¥Ê
	void saveXml(pugi::xml_node node);
	void loadXml(pugi::xml_node node);
public Q_SLOTS:
	void currentIndexChange(int index);
private:
	Ui::TargetItem *ui;
};