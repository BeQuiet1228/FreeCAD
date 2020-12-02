#pragma once

#include <QMainWindow>
#include <QTimer>
#include "ui_Contorl.h"
#include "ChipicManager.h"
#include "ContorlButtonBar.h"
#include "ContorlDataBar.h"
#include "ContorlConfig.hpp"
#include "EmitterInterface.h"
class  Contorl : public QMainWindow
{
	Q_OBJECT
public:
	Contorl(QWidget *parent = 0);
	~Contorl();

public:
	//chipic管理器
	ChipicManager chipicManager;
	//按钮条
	ContorlButtonBar *contorlButtonBar;
	//信息条
	ContorlDataBar *contorlDataBar;
	//运行脚本获取m3d路径
	void getM3dPathForRunPython();
	//m3d路径
	std::string m3dPath = "E:/lingshiwenjianjia/MILO_D/MILO_D.m3d";
private:
	Ui::ContorlClass ui;
private:
	//切换连接方式
	void changeConnectionWay();
	//打开log文件
	void openLog();
public Q_SLOTS:
	void on_pushButton_clicked();

	//chipic状态更新
	void chipicStateUpdate();

	void buttonClinked(int buttonType);

public: 
	//连接按钮条的信号
	void connectButtonBar();
	//获取连接方式
	int getConnectWay();

};
