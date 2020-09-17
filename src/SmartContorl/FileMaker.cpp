#include "FileMaker.h"
#include <qdir>
#include <QMessageBox>
#include <QFileInfo>
#include <QFile>
#include <iostream>
#include <QTextStream>

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
void FileMaker::setM3dPath(const std::string& m3dPath)
{
	QString temp = QString::fromStdString(m3dPath);
	QDir dir;
	if (!dir.exists(temp))
	{
		QMessageBox box;
		box.setText("FileMaker::setM3dPath path not exists， path:" + temp);
		box.exec();
		return;
	}
	QFileInfo fileinfo(temp);
	
	auto fileName = fileinfo.baseName();
	auto filePath = QString(temp).remove(fileinfo.fileName());
	QString newPath = filePath + fileName;

	if (!dir.exists(newPath))
		dir.mkdir(newPath);

	this->newFilePath = newPath;
	this->filePath = filePath;
	this->fileName = fileName;
	this->m3dPath = temp;
}

/**
* @brief FileMaker::makeFile 生成运行所需文件
* @param std::vector<QString> & variates
* @return std::deque<FileMaker::M3dData>
*/
std::deque<FileMaker::M3dData> FileMaker::makeFile(std::vector<QString>& variates)
{
	int count = 0;

	QFile file(this->m3dPath);
	if (!file.open(QIODevice::ReadOnly))
	{
		std::cerr << "FileMaker::makeFile file is not open! path:" << this->m3dPath.toStdString() << std::endl;
	}
	QString m3d = file.readAll();

	std::deque<M3dData> datas;
	QDir dir;

	for (auto i = variates.begin(); i != variates.end(); i++)
	{
		M3dData data;
		auto path = this->filePath + QString::number(count) + "/";
		if (!dir.exists(path))
			dir.mkdir(path);
		auto name =this->fileName + ".m3d";
		data.m3dPath = path + name;
		data.variates = *i;
		//生成m3d文件
		auto newM3d = *i + m3d;
		QFile newFile(path + name);
		if (!newFile.open(QIODevice::ReadWrite))
		{
			std::cerr << "FileMaker::makeFile file is not open! path:" << path.toStdString() << std::endl;
			continue;
		}

		QTextStream stream(&newFile);
		stream << newM3d;
		newFile.close();
		datas.push_back(data);

		count++;
	}

	file.close();

	return datas;
}
