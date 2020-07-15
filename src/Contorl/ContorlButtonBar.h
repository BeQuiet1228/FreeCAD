#pragma once

#include <QWidget>
#include <memory>
#include "Chipic.h"
#include "ContorlConfig.hpp"

namespace Ui {
	class ContorlButtonBar;
}
class CONTROL_EXPORT ContorlButtonBar : public QWidget
{
	Q_OBJECT
public:
	enum ButtonType
	{
		RUN = 0,	//运行按钮
		PARALLE_RUN,//并行运行
		REFREASH,	//刷新按钮
		PAUSE,		//暂停开始
		TIMER,		//定时器按钮
		LOG			//LOG按钮
	};
public:
	ContorlButtonBar (QWidget *parent = 0);
	~ContorlButtonBar();
private:
	Ui::ContorlButtonBar *ui;
public:
	//设置计算程序数据
	void setChipicData(std::shared_ptr<Chipic> Chipic);
public slots:
	//运行按钮被点击
	void on_toolButtonRun_clicked();
	//并行运行按钮被点击
	void on_toolButtonParalleRun_clicked();
	//刷新按钮被点击
	void on_toolButtonRefreash_clicked();
	//log按钮被点击
	void on_toolButtonLOG_clicked();
	//暂停按钮被点击
	void on_toolButtonPause_clicked();
	//定时器按钮被点击
	void on_toolButtonTimer_clicked();
	//批处理按钮被点击
	void on_toolButton_clicked();
Q_SIGNALS:
	void buttonClicked(int);
};
