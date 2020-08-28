#include "openLog.h"
#include <QProcess>
std::shared_ptr<OpenLog> OpenLog::_instance;

OpenLog::~OpenLog()
{

}
OpenLog::OpenLog()
{

}

/**
* @brief OpenLog::setCurrentChipicM3dPath 设置当前运算中的工程路径
* @param const std::string & path
* @return void
*/
void OpenLog::setCurrentChipicM3dPath(const std::string& path)
{
	QString temp = QString::fromStdString(path);
	this->m3dPath =  temp.left(temp.size() - 4) + ".LOG";
}

/**
* @brief OpenLog::openLog 打开log文件
* @return void
*/
void OpenLog::openLog()
{
	QString cmd = "notepad.exe " + this->m3dPath;
	QProcess process;

	process.start(cmd);
	process.waitForFinished();
}

