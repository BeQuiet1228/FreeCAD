#pragma once
#include <QString>
#include <vector>
#include <map>
#include <memory>
#include <QListWidgetItem>
class ContorlDataBar;
class Chipic;
class ChipicRunData{
public:
	ChipicRunData();
	~ChipicRunData();
public:
	//m3d文件路径
	QString m3dPath;
	//h5文件路径
	QString h5FilePath;
	//优化之后的参数
	QString variate;
	//启动程序之后的线程id
	unsigned long threadID = 0;
public:
	void setCreatDataBar(std::shared_ptr<Chipic> chipic);
	void deleteItemAndBarPtr();
public:
	QListWidgetItem *widgetItem;
	ContorlDataBar *dataBar;
};
using ChipicRunDataPtr = std::shared_ptr<ChipicRunData>;
using ChipicRunDatas = std::vector<ChipicRunDataPtr>;
using ChipicRunDataMap = std::map<QString, ChipicRunDataPtr>;
