#include "openLog.h"
#include <QProcess>
#include <QFileInfo>
#include <QFileInfo>
#include <QFile>
#include <QDir>
#include <iostream>
#include <QTextIStream>
#include <QTextCodec>
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

QString OpenLog::getLogContent()
{
	QFile file(this->m3dPath);
	if (!file.exists())
		return "";
	if (!file.open(QIODevice::ReadOnly))
		return "";
	auto byte = file.readAll();
	QTextStream stream(&file);
	QString str = file.readAll();
	file.close();
	QTextCodec* pCodec = QTextCodec::codecForName("gb2312");
	if (!pCodec)
		return str;
	str = pCodec->toUnicode(byte.data(), byte.length());

	return str;
}

