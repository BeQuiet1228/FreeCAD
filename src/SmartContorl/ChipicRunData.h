#pragma once
#include <QString>
#include <vector>
#include <map>
#include <memory>
class ChipicRunData{
public:
	ChipicRunData(){};
	~ChipicRunData(){};
public:
	//m3d文件路径
	QString m3dPath;
	//h5文件路径
	QString h5FilePath;
	//优化之后的参数
	QString variate;
	
};
using ChipicRunDataPtr = std::shared_ptr<ChipicRunData>;
using ChipicRunDatas = std::vector<ChipicRunDataPtr>;
using ChipicRunDataMap = std::map<QString, ChipicRunDataPtr>;
