#pragma once
#include <QtGui/QDialog>
#include <QCloseEvent>
#include "ContorlConfig.hpp"
namespace Ui{
	class Dialog;
}
class CONTROL_EXPORT HintDailog : public QDialog
{

	Q_OBJECT
public:
	enum ClinkeType
	{
		MODE1_EXIT = 1, //退出
		MODE1_LOSE = 2,		//忽略
		MODE1_LOSE_ALL = 3,	
		MODE1_CONTINUE = 4,	//继续
		MODE1_CONTINUE_ALL = 5,
		MODE2_EXIT = 6,
		MODE2_CONTINUE = 9,
		MODE2_CONTINUE_ALL = 10,
		MODE3_EXIT = 11,

		NULL_TYPE
	};
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

public:
	int mode = 1;

private:
	Ui::Dialog *ui;
public slots:
	void buttonLoseClicked();
	void buttonContinueClicked();
	void buttonExitClincked();
Q_SIGNALS:
	void buttonClicked(int);
protected:
	void closeEvent(QCloseEvent *e) override;
};
