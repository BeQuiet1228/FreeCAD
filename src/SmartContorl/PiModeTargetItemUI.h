#pragma once
#include "TargetItem.h" 
#include <QWidget>
#include "Target.h"
namespace Ui {
	class PiModeTargetItemUI;
}

class PiModeTargetItemUI : public QWidget, public TargetItem {
	Q_OBJECT 

public:
	// 构造函数
	PiModeTargetItemUI(QWidget* parent = 0);
	// 析构函数
	~PiModeTargetItemUI();

	void showG();

public:
	virtual void loadTarget(Target* target) override;
	virtual Target* GenerateTarget() override;
	virtual void saveXml(pugi::xml_node node) override;
	virtual void loadXml(pugi::xml_node node) override;

private:
	Ui::PiModeTargetItemUI* ui;
};