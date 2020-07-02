#pragma once
#include <QObject>
#include "Chipic.h"
#include <map>
#include <Windows.h>
#include <memory>
class ChipicManager:public QObject
{
	Q_OBJECT
public:
	ChipicManager();
	~ChipicManager();

private:
	//计算程序集合
	std::map<DWORD, std::shared_ptr<Chipic>> chipicMap;

public slots:
	void hasNewMessage();
};