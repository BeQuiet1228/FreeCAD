#pragma once
#include "ui_HintDailog.h"
#include <QtGui/QDialog>
class HintDailog : public QDialog
{
	enum ClinkeType
	{
		EXIT = 0,	//退出
		LOSE = 1,	//忽略
		CONTINUE =2 //继续
	};
	Q_OBJECT
public:
	HintDailog(QWidget *parent = 0);

	//显示继续、退出、忽略
	void showForMode1();
	//显示退出、继续
	void showForMode2();
	//显示退出
	void showForMode3();
	//设置显示文本
	void setText(const std::string& text);
private:
	Ui::Dialog ui;
public slots:
	void buttonLoseClicked();
	void buttonContinueClicked();
	void buttonExitClincked();
signals:
	void buttonClicked(int);
};
