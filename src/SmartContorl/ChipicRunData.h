#pragma once
#include <QString>
#include <vector>
#include <map>
#include <memory>
#include <QListWidgetItem>
class ContorlDataBar;
class Chipic;
class ResultData{
public:
	ResultData(){};
	~ResultData(){};
	//添加数据
	void addValue(const float& v){
		data.push_back(v);
	};
	//获取大小
	int size(){
		return data.size();
	}
	//获取数据 如果超出索引范围则返回0
	float getValue(const int& index){
		if (data.size() <= index)
			return 0.0;
		return data.at(index);
	}
	std::vector<float> getData() {
		return data;
	}
private:
	std::vector<float> data;
};
using ResultDataPtr = std::shared_ptr<ResultData>   ;
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
	//数据筛选之后的结果
	ResultDataPtr resultData;
	//变量的顺序
	unsigned int rank = 0;
	//错误退出次数
	unsigned int  errorExitCount = 0;
	/*
		这里记录运行时内核是否解析完成。
		由于有未解析完成但触发异常退出的情况，这个时候将异常退出的数据重新放入等待区。
		但是在这个流程中只有解析完成槽函数会重新调用RunChipic函数，会因为将错误退出的对象拿出导致卡在这个步骤。
	*/
	bool IsAnalysis = false;
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
