#pragma once
#include <QObject>
#include <map>
#include <Windows.h>
#include <memory>
#include "ContorlDataBar.h"
#include "ContorlConfig.hpp"
class Chipic;
class CONTROL_EXPORT ChipicManager:public QObject
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
	//新建计算程序，用于启动时未获取线程id时暂存
	std::shared_ptr<Chipic> newChipic;
Q_SIGNALS:
	//当前计算程序有信息更新
	void currentChipicStateUpdate();
public Q_SLOTS:
	void hasNewMessage();
	//更新ui状态
	void chipicStateUpdate(DWORD threadId);
	//运行按钮被点击
	void runButtonClicked(const std::string& m3dPath = "");
	//关闭当前运行的chipic
	void closeCurrentChipic();

public:
	//并行按钮被点击
	void ButtonParalleRunClicked(const std::string& m3dPath);
};