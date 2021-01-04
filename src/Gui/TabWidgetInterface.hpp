#pragma once
#include <QString>
#include <QAction>
#include <QTableWidget>
#include <QList>
#include <iostream>
#include <map>
class TabWidgetInterFace:public QTableWidget{
public:
	TabWidgetInterFace() = default;
	~TabWidgetInterFace() = default;
public:
	virtual void addAction(const QString& tabName,const QString& groupName,QAction* action) = 0;
	virtual void clearAllAction() = 0;
	virtual void clearTab(const QString& tabName) = 0;
	virtual void clearGoup(const QString& groupName) = 0;
	virtual QList<QString> tabs() = 0;
	virtual QList<QString> groups() =0;
	virtual QList<QAction*> getActions() = 0;
	virtual QList<QAction*> getTabActions(const QString& tabName) = 0;
	virtual QList<QAction*> getGroupActions(const QString& groupName) = 0;

};
class TabTest:public TabWidgetInterFace{
public:
	TabTest() = default;
	~TabTest() = default;
public:
	virtual void addAction(const QString& tabName, const QString& groupName, QAction* action){
		std::cerr << "tabName:" << tabName.toStdString() << "groupName:" << groupName.toStdString()
			<< "actionName:" << action->text().toStdString() << std::endl;
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
};