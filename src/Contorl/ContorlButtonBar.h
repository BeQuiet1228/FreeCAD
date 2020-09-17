#pragma once

#include <QWidget>
#include <memory>
#include "ContorlConfig.hpp"
#include "ContorlBar.h"
class Chipic;
namespace Ui {
	class ContorlButtonBar;
}
class  ContorlButtonBar : public ContorlBar
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
		LOG,			//LOG按钮
		CONNECTION_WAY  //连接方式被点击
	};
public:
	ContorlButtonBar (QWidget *parent = 0);
	~ContorlButtonBar();
private:
	Ui::ContorlButtonBar *ui;
public:
	//chipic被关闭 重新设置按钮状态
	void chipicClose();
	//设置连接方式图标
	void setConnectionWayIcon(const int& way);
	//刷新ui显示
	void updateUI() override;
public Q_SLOTS:
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
	//切换连接模式按钮被点击
	void on_toolButtonConnectionWay_clicked();
Q_SIGNALS:
	void buttonClicked(int);
};
