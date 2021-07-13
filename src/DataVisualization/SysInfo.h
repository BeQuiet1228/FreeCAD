#pragma once
#ifndef SYSINFO_H_
#define SYSINFO_H_
#include <QObject>
#include <vector>
#include <QString>
//系统相关
class SysInfo
{
public:
	static SysInfo* GetInstance();
private:
	void init();
	SysInfo();
	~SysInfo();
	bool isinit;
};

#endif