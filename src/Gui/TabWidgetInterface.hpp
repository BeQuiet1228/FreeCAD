#pragma once
#include <QString>
#include <QAction>
#include <QTabWidget>
#include <QList>
#include <iostream>
#include <map>
class MainWindowDef;
class TabWidgetInterFace : virtual public QTabWidget{
public:
	TabWidgetInterFace() = default;
	~TabWidgetInterFace() = default;
public:
	//添加一个action
	virtual void addAction(const QString& tabName,const QString& groupName,QAction* action) = 0;
	//清理掉所有的action
	virtual void clearAllAction() = 0;
	//清理掉一个tab 包括下面的组、和action-+
	virtual void clearTab(const QString& tabName) = 0;
	//清理掉一个组以及下面的action
	virtual void clearGoup(const QString& groupName) = 0;
	//获取所有tab的名字
	virtual QList<QString> getTabs() = 0;
	//获取所有组的名字
	virtual QList<QString> getGroups() =0;
	//获取特定tab下组的名字
	virtual QList<QString> getGroup(const QString& tabName) = 0;
	//获取所有的action
	virtual QList<QAction*> getActions() = 0;
	//获取某个tab下所有的action
	virtual QList<QAction*> getTabActions(const QString& tabName) = 0;
	//获取某个group下所有的action
	virtual QList<QAction*> getGroupActions(const QString& groupName) = 0;
	/*
		改变tab位置，如果older超出最大范围将tab放置到最后。
		如果tab不存在，不做操作。
	*/
	virtual void  setTabOlder(const QString& tabName, const int older){};
	//判断是否已有该action
	virtual bool hasAction(const QAction* action){ return true; };
	//新增，2021-6-10,用于进行缩放判断
	virtual void setParentWidget(MainWindowDef*){}
};
class TabTest :public TabWidgetInterFace{
public:
	TabTest() = default;
	~TabTest() = default;
public:
	virtual void addAction(const QString& tabName, const QString& groupName, QAction* action){
		std::cerr << "tabName:" << tabName.toStdString() << ",groupName:" << groupName.toStdString()
			<< ",actionName:" << action->text().toStdString() << std::endl;
	};
	virtual void clearAllAction(){
		std::cerr << "clear all Action" << std::endl;
	};
	virtual void clearTab(const QString& tabName){
		std::cerr << "clear Tab " << tabName.toStdString() << std::endl;
	};
	virtual void clearGoup(const QString& groupName){
		std::cerr << "clear group " << groupName.toStdString() << std::endl;
	};
	virtual QList<QAction*> getActions(){
		std::cerr << "getActions()" << std::endl;
		QList<QAction*> a;
		return a;
	};
	virtual QList<QAction*> getTabActions(const QString& tabName){
		std::cerr << "getTabActions" << tabName.toStdString() << std::endl;
		QList<QAction*> a;
		return a;
	};
	virtual QList<QAction*> getGroupActions(const QString& groupName){
		std::cerr << "getTabActions" << groupName.toStdString() << std::endl;
		QList<QAction*> a;
		return a;
	};
	virtual QList<QString> tabs(){
		QList<QString> a;
		return a;
	};
	virtual QList<QString> groups(){
		QList<QString> a;
		return a;
	};
	//获取所有tab的名字
	virtual QList<QString> getTabs(){
		QList<QString> a;
		return a;
	};
	//获取所有组的名字
	virtual QList<QString> getGroups(){
		QList<QString> a;
		return a;
	};
	//获取特定tab下组的名字
	virtual QList<QString> getGroup(const QString& tabName){
		QList<QString> a;
		return a;
	};
};