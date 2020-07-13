#pragma once
#include <QObject>
#include "Chipic.h"
#include <map>
#include <Windows.h>
#include <memory>
#include "ContorlDataBar.h"
class ChipicManager:public QObject
{
	Q_OBJECT
public:
	ChipicManager();
	~ChipicManager();
private:
	//计算程序集合
	std::map<DWORD, std::shared_ptr<Chipic>> chipicMap;
public:
	//当前管理的计算程序
	std::shared_ptr<Chipic> CurrentChipic;
signals:
	//当前计算程序有信息更新
	void currentChipicStateUpdate();
public slots:
	void hasNewMessage();
	//更新ui状态
	void chipicStateUpdate(DWORD threadId);
	//运行按钮被点击
	void runButtonClicked(const std::string& m3dPtah = "");
	//关闭当前运行的chipic
	void closeCurrentChipic();
};