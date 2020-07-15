#pragma once

#include <QMainWindow>
#include "ui_Contorl.h"
#include "ChipicManager.h"
#include "ContorlButtonBar.h"
#include "ContorlDataBar.h"
#include "ContorlConfig.hpp"
class  CONTROL_EXPORT Contorl : public QMainWindow
{
	Q_OBJECT
public:
	Contorl(QWidget *parent = 0);
	

public:
	ChipicManager chipicManager;
	ContorlButtonBar contorlButtonBar;
	ContorlDataBar contorlDataBar;

	std::string m3dPath = "E:\\lingshiwenjianjia\\MILO_D\\MILO_D.m3d";
private:
	Ui::ContorlClass ui;
private:
public Q_SLOTS:
	void on_pushButton_clicked();

	//chipic×´Ì¬¸üÐÂ
	void chipicStateUpdate();

	void buttonClinked(int buttonType);

};
