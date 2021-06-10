#include "openLog.h"
#include <QProcess>
#include <QFileInfo>
std::shared_ptr<OpenLog> OpenLog::_instance;

OpenLog::OpenLog()
{
	process = new QProcess;
}

OpenLog::~OpenLog()
{
	delete process;
}


/**
* @brief OpenLog::setCurrentChipicM3dPath 设置当前运算中的工程路径
* @param const std::string & path
* @return void
*/
void OpenLog::setCurrentChipicM3dPath(const std::string& path, const int& threadCount)
{
	QString temp = QString::fromStdString(path);
	if (threadCount > 1)
	{
		QFileInfo info(temp);
		auto filename = info.fileName();
		temp = temp.remove(filename);
		temp += "/1/" + filename;
	}
	
	this->m3dPath =  temp.left(temp.size() - 4) + ".LOG";
}

/**
* @brief OpenLog::openLog 打开log文件
* @return void
*/
void OpenLog::openLog()
{
	QString cmd = "notepad.exe " + this->m3dPath;
#if 1
	process->start(cmd);
	//process->waitForFinished();
#else
	QProcess pr;
	pr.start(cmd);
	pr.waitForFinished();
#endif

}

