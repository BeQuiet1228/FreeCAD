#pragma once

#include <QMainWindow>
#include "ui_Contorl.h"

class Contorl : public QMainWindow
{
	Q_OBJECT

public:
	Contorl(QWidget *parent = 0);

private:
	Ui::ContorlClass ui;
public slots:
	void on_pushButton_clicked();

};
