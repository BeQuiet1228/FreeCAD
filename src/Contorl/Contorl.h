#pragma once

#include <QMainWindow>
#include "ui_Contorl.h"
#include "ChipicManager.h"
#include "ContorlButtonBar.h"
#include "ContorlDataBar.h"
#include "ContorlConfig.hpp"
class  Contorl : public QMainWindow
{
	Q_OBJECT
public:
	Contorl(QWidget *parent = 0);
	

public:
	ChipicManager chipicManager;
	ContorlButtonBar *contorlButtonBar;
	ContorlDataBar *contorlDataBar;

	std::string m3dPath = "";
private:
	Ui::ContorlClass ui;
private:
	//运行脚本获取m3d路径
	void getM3dPathForRunPython();
public Q_SLOTS:
	void on_pushButton_clicked();

	//chipic状态更新
	void chipicStateUpdate();

	void buttonClinked(int buttonType);

};
