#pragma once
#ifndef SYSINFO_H_
#define SYSINFO_H_
#include <QObject>
#include <vector>
#include <QString>
namespace DV {
	//系统相关
	class SysInfo
	{
	public:
		static SysInfo* GetInstance();
		std::vector<QString> getfonts();
	private:
		void init();
		SysInfo();
		~SysInfo();
	private:
		bool isinit;
		std::vector<QString> fonts;
	};
};


#endif