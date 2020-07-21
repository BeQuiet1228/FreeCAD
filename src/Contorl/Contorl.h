#pragma once

#include <QMainWindow>
#include <QTimer>
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
	//chipic管理器
	ChipicManager chipicManager;
	//按钮条
	ContorlButtonBar *contorlButtonBar;
	//信息条
	ContorlDataBar *contorlDataBar;
	//m3d路径
	std::string m3dPath = "";
private:
	Ui::ContorlClass ui;
	
	/*
		计算程序解析m3d文本时，短时间内会有数以万计的消息更新界面信息，
		这样会消耗许多的性能，且意义不大。
		解决方案是使用定时器定时刷新界面。
		每次刷新界面信号来的时候只改变flag的值，定时器触发的时候判断flag的值，来决定界面是否需要刷新
	*/
	bool uiUpdateFlag = false;
	//ui刷新定时器
	QTimer *uiTimer;
private:
	//运行脚本获取m3d路径
	void getM3dPathForRunPython();
public Q_SLOTS:
	void on_pushButton_clicked();

	//chipic状态更新
	void chipicStateUpdate();

	void buttonClinked(int buttonType);

	//定时刷新ui
	void uiUpdateTimerout();

};
