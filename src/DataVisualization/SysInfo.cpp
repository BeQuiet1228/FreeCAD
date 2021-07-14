#include "SysInfo.h"
#include <QFontDatabase>
#include <QDebug>
#include <QStringList>
SysInfo* SysInfo::GetInstance()
{
	static SysInfo instance;
	return &instance;
}
SysInfo::SysInfo():isinit(false)
{
	init();
}
SysInfo::~SysInfo()
{

}
/**
* @brief SysInfo::init 初始化相关信息
* @return void
* @Time 2021/7/13
*/
void SysInfo::init()
{
	//获取字体
	{
		fonts.clear();
		QFontDatabase database;
		foreach (const QString &family , database.families(QFontDatabase::SimplifiedChinese))
			fonts.push_back(QString("%1").arg(family));
		foreach (const QString &family ,database.families())
			fonts.push_back(QString("%1").arg(family));
	}
}
std::vector<QString> SysInfo::getfonts()
{
	return fonts;
}