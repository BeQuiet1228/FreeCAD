#pragma once
#include <QString>
#include <deque>
#include <vector>
#include "ChipicRunData.h"
class FileMaker{
public:
	struct M3dData{
		QString m3dPath,variates;
	};
public:
	FileMaker();
	~FileMaker();

	//设置原始m3d路径
	void setM3dPath(const QString& m3dPath);
	//生成文件
	ChipicRunDatas makeFile(std::vector<QString>& variates);
	//剪切文件至指定目录
	bool cutFile(const QString& fileName,const QString& path);

	// 文件路径 文件名称 生成的文件路径 原始m3d路径
	QString filePath, fileName, newFilePath, m3dPath;
private:

};