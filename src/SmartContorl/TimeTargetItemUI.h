#pragma once
#include <QWidget>
#include "Target.h"
#include "xml/pugixml.hpp"
#include "TargetItem.h"
#include <QHBoxLayout>
#include <QLabel>
#include <QLineEdit>
namespace Ui {
	class TimeTargetItemUI;
	class TimeDoubleTargetItemUI;
}

class TimeTargetItemUI :public QWidget ,public TargetItem{
	Q_OBJECT
public:
	TimeTargetItemUI(QWidget* parent = 0);
	~TimeTargetItemUI();

	void showG();
public:
	void loadTarget(TargetTime* target);
	TargetTime* GenerateTimeTarget();
	void loadTarget(Target* target) override;
	Target* GenerateTarget() override;

	//载入和保存
	void saveXml(pugi::xml_node node) override;
	void loadXml(pugi::xml_node node) override;
public Q_SLOTS:
	void currentIndexChange(int index);
private:
	Ui::TimeTargetItemUI* ui;
};

class TimeDoubleTargetItemUI :public QWidget, public TargetItem {
	Q_OBJECT
public:
	TimeDoubleTargetItemUI(QWidget* parent = 0);
	~TimeDoubleTargetItemUI();

	void showG();
public:
	void loadTarget(TargetTime* target);
	TargetTime* GenerateTimeTarget();
	void loadTarget(Target* target) override;
	Target* GenerateTarget() override;

	//载入和保存
	void saveXml(pugi::xml_node node) override;
	void loadXml(pugi::xml_node node) override;
public Q_SLOTS:
	void currentIndexChange(int index);
private:
	Ui::TimeDoubleTargetItemUI* ui;
};
