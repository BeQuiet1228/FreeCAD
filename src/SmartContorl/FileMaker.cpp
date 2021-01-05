#include "FileMaker.h"
#include <qdir>
#include <QMessageBox>
#include <QFileInfo>
#include <QFile>
#include <iostream>
#include <QTextStream>
#include <QProcess>
#include <QDebug>
#include <qregexp.h>
FileMaker::FileMaker()
{

}

FileMaker::~FileMaker()
{

}

/**
* @brief FileMaker::setM3dPath
* @param const std::string & m3dPath
* @return void
*/
void FileMaker::setM3dPath(const QString& m3dPath)
{
	QDir dir;
	if (!dir.exists(m3dPath))
	{
		QMessageBox box;
		box.setText("FileMaker::setM3dPath path not exists， path:" + m3dPath);
		box.exec();
		return;
	}
	QFileInfo fileinfo(m3dPath);
	
	auto fileName = fileinfo.baseName();
	auto filePath = QString(m3dPath).remove(fileinfo.fileName());
	QString newPath = filePath + fileName;
	if (!dir.exists(newPath))
		dir.mkdir(newPath);

	this->newFilePath = newPath;
	this->filePath = filePath;
	this->fileName = fileName;
	this->m3dPath = m3dPath;
}

/**
* @brief FileMaker::makeFile 生成运行所需文件
* @param std::vector<QString> & variates
* @return std::deque<FileMaker::M3dData>
*/
ChipicRunDatas FileMaker::makeFile(std::vector<QString>& variates)
{
	int count = 0;

	QFile file(this->m3dPath);
	if (!file.open(QIODevice::ReadOnly))
	{
		std::cerr << "FileMaker::makeFile file is not open! path:" << this->m3dPath.toStdString() << std::endl;
	}
	QString m3d = file.readAll();
	file.close();

	ChipicRunDatas datas;
	QDir dir;
	for (auto i = variates.begin(); i != variates.end(); i++)
	{
		ChipicRunDataPtr data;
		data.reset(new ChipicRunData);
		auto path = this->newFilePath + "/" + QString::number(count) + "/";
		if (!dir.exists(path))
			dir.mkdir(path);
		auto name =this->fileName + "_" + QString::number(count) + ".m3d";
		data->m3dPath = path + name;
		auto h5file = this->fileName + "_" + QString::number(count) + ".h5";
		data->h5FilePath = path + h5file;
		data->rank = count;
		data->variate = *i;
		//生成m3d文件
		auto newM3d = this->replaceVariate(*i,m3d);
		QString fileName = path + name;
		QFile newFile(path + name);
		if (!newFile.open(QIODevice::ReadWrite))
		{
#ifdef MY_LOG
			std::cerr << "FileMaker::makeFile file is not open! path:" << fileName.toStdString() << std::endl;
#endif // MY_LOG
			continue;
		}
		newFile.remove();
		newFile.close();
		if (!newFile.open(QIODevice::ReadWrite))
		{
#ifdef MY_LOG
			std::cerr << "FileMaker::makeFile file is not open! path:" << fileName.toStdString() << std::endl;
#endif // MY_LOG
			continue;
		}
		QTextStream stream(&newFile);
		stream << newM3d;
		newFile.close();
		datas.push_back(data);

		count++;
	}

	return datas;
}

/**
* @brief FileMaker::cutFile 剪切数据
* @param const QString & fileName
* @param const QString & path
* @return bool
*/
bool FileMaker::cutFile(const QString& fileName, const QString& path)
{
	QFileInfo fileInfo(fileName);

	auto newFileName = path +"/"+ fileInfo.fileName();

	std::cerr << newFileName.toStdString() << std::endl;
	std::cerr << fileName.toStdString() << std::endl;

	QFile::remove(newFileName);
	{
		QFile file(fileName);
		if (file.open(QIODevice::ReadWrite))
		{
			if(file.rename(newFileName))
				file.close();
		}

	}

	/*QString cmd = "move " + fileName + " " + path;
	cmd = cmd.replace("/", "\\");

	std::cerr << cmd.toStdString() << std::endl;

	//调用windows命令实现剪切功能
	QProcess *process = new QProcess;
	process->start(cmd);
	process->waitForFinished();
	//当文件已存在时可能出现是否要求替换的选项 直接覆盖
	process->start("ping www.baidu.com");
	process->waitForFinished();

	std::cerr << process->readAll().data() << "23333" <<std::endl;*/
	return true;
}

QString FileMaker::replaceVariate(const QString& variate, const QString& m3d)
{
	auto lines = variate.split("\n");
	auto tempM3d = m3d;
	for (auto i = lines.begin(); i != lines.end(); i++)
	{
		if (i->isNull())
			continue;
		auto name = i->split("=").at(0);
		auto r ="\\b" + name + "\\s*=.*;";
		QRegExp rex(r);
		rex.setMinimal(true);
		int posStart = 0, posEnd = 0;
		posStart = rex.indexIn(tempM3d);
		if (posStart != -1)
		{
			/*std::cerr << rex.cap(0).toStdString() << std::endl;
			posEnd = posStart + rex.matchedLength();
			std::cerr << tempM3d.size() << "||" <<posStart<<"||"<< posEnd <<std::endl;
			tempM3d.remove(posStart, posEnd);
			tempM3d.insert(posStart, *i + "\n");*/
			tempM3d.replace(rex.cap(0), *i);
		}else{
			tempM3d = *i + "\n" + tempM3d;
		}
	}

	return tempM3d;
}