#pragma once

#include <QMainWindow>
#include "ui_Contorl.h"
#include "ChipicManager.h"
#include "ContorlButtonBar.h"
#include "ContorlDataBar.h"
class Contorl : public QMainWindow
{
	Q_OBJECT

public:
	Contorl(QWidget *parent = 0);
	

public:
	ChipicManager chipicManager;
	ContorlButtonBar contorlButtonBar;
	ContorlDataBar contorlDataBar;
private:
	Ui::ContorlClass ui;
private:
	std::string m3dPath = "E:\\lingshiwenjianjia\\MILO_D\\MILO_D.m3d";
public slots:
	void on_pushButton_clicked();

	//chipic×´Ì¬¸üÐÂ
	void chipicStateUpdate();

	void buttonClinked(int buttonType);

};
