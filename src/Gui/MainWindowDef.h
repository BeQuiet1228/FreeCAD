#pragma once
#include <QWidget>
#include <QMouseEvent>
#include <QPoint>
#include <windows.h>
#include <windowsx.h>
#include <QToolBar>
#include <qwidget.h>
#include <QResizeEvent>
#include <TabWidgetInterface.hpp>
#include "picgui_ribbon/PICRibbon.h"
#include <QMoveEvent>
class TitleBar: public QWidget{
	Q_OBJECT
public:
	TitleBar(QWidget* parent = 0);
	~TitleBar() = default;
protected:
	void mouseMoveEvent(QMouseEvent *event);
	void mousePressEvent(QMouseEvent *event);
	void mouseReleaseEvent(QMouseEvent *event);
private:
	bool mouseIsPress = false;
	QPoint mouseStartPoint;
Q_SIGNALS:
	void toMove(QPoint pos);
};

namespace Ui {
	class WindowDef;
}
class MainWindowDef:public QWidget{
	Q_OBJECT
public:
	enum CursorState{
		NONE = 0,	//正常状态
		RIGHT,
		RIGHT_BOTTOM,
		BOTTOM
	};
public:
	MainWindowDef(QWidget *parent = 0);
	~MainWindowDef();

private:
	Ui::WindowDef* ui;
	//响应鼠标边框悬停的范围
	int boundaryWidth;
	//鼠标左键按下是记录的位置
	QPoint leftButtonPressPos;
	//鼠标左键是否按下
	bool leftButtonIsPress = false;
	//鼠标光标的状态
	CursorState cursorState = NONE;
	//记录最大化之前的size和位置
	QSize oldSize;
	QPoint oldPoint;
	//顶部的快捷栏
	QToolBar* toolbar;
	//记录窗口是否已经最大化
	bool isMax = false;
public:
	//选项卡对象
	TabWidgetInterFace *tabWidgetInterface;

protected:
	void mouseMoveEvent(QMouseEvent *event) override;
	void mousePressEvent(QMouseEvent *event) override;
	void mouseReleaseEvent(QMouseEvent *event) override;
	void resizeEvent(QResizeEvent *event) override;
	void moveEvent(QMoveEvent *event);
public Q_SLOTS:
	void titleBarMove(QPoint pos);
	void toolButtonClicked(bool b);

private:
	//改变光标样式
	void changeCursor(const QPoint& pos);
	//相应拖拽的放大缩小
	void changeSize(const QPoint& pos);

public:
	//添加中心区域的窗口
	void addCenterWidget(QWidget *widget);
	//添加顶部快捷键
	void addTitleShortcutAction(QAction* action);
	//最大化显示窗口
	void showMax();
	//返回最大化之前的状态
	void showOld();
	//是否最大化
	bool windowIsMax(){
		return isMax;
	}
};