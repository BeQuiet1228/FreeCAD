#pragma once
#include <string>
#include "VariateAnalysis.h"
#include "ChipicRunData.h"
#include "FileMaker.h"
#include "Contorl/ChipicManager.h"
#include <QObject>
#include <QListWidgetItem>
#include <QWidget>
struct lua_State;
//提供给lua接口获取运算结果
class ChipicResultGetter{

public:
	ChipicResultGetter() = default;
	ChipicResultGetter(const ChipicRunDatas& result){
		setData(result);
	}
	~ChipicResultGetter(){};

	bool next(ChipicRunDataPtr& runData);
	//重新将迭代器指向第一个
	void reset(){
		this->iter = this->result.begin();
	};
	//设置数据
	void setData(const ChipicRunDatas& result){
		this->result = result;
		this->iter = this->result.begin();
	}
private:
	ChipicRunDatas::iterator iter;
	ChipicRunDatas result;
};

class SmartContorl:public QObject{
	Q_OBJECT
public:
	SmartContorl();
	~SmartContorl();
public:
	struct HistoryData{
		//运行结果
		ChipicRunDatas datas;
		//参数设置
		std::vector<Variate> variates;
	};
	enum MakeRunDataType {
		CONBINATION,	//组合
		EXHAUSTIVITY	//穷举
	};
public:
	//调用lua中的初始化函数
	void luaInit();
	//void luaInit(std::string name,double max,double min,int count);
	//调用lua中的结果筛选函数
	bool luaResultDataFilter();
	//调用lua中的结果比对函数
	bool luaResultExpcet();
	//调用lua中参数优化函数
	void luaOptimize();
	//载入lua脚本
	void luaLoadFromString(const std::string& lua);
	void luaLoadFromFile(const std::string& filePath);
	//根据参数组生成新的运行信息
	void makeRunData();
	//运行chipic
	void runChipic();
	//数据优化
	void dataOptimize();
	//获取历史数据中一个组的数据大小
	int getHistoryGroupSize(const int& groupIndex);
	//获取一组数据中的参数个数大小
	int getHistoryGroupParamSize(const int& groupIndex,const int& index);
	//获取一个参数的值
	float getHistoryGroupParam(const int& goupIdex, const int& index, const int& paramIndex);
	//清空已完成的数据，并将数据存到历史数据中
	void clearFinishData();
	//打印出运行信息
	void printLog(const std::string& log);
	//停止运行
	void stop();
	//启动运行
	void run(const QString& lua);
	//初始化
	void initDataFile();
	//存储当前一次的运行数据
	void saveCurrentData();
	//获取历史运行数据大小
	int getHistorySize(){
		return historyDatas.size();
	}
	//添加一个参数组
	void addVariate(const Variate& v){
		this->variates.push_back(v);
	};
	//获取虚拟机指针
	lua_State* getLuaState(){
		return lua_state;
	}
	//设置优化的m3d路径
	void setM3dPath(const QString& s){
		this->m3dPath = s;
		fileMaker.setM3dPath(s);
	}
	QString getM3dPath(){
		return m3dPath;
	}
	void setM3dPath(const std::string s){
		this->m3dPath = QString::fromStdString(s);
		fileMaker.setM3dPath(m3dPath);
	}
	//获取运算结果
	ChipicResultGetter getResult(){
		ChipicResultGetter result(chipicDataFinish);
		return result;
	}
	//获取运行的历史数据
	std::vector<HistoryData> getHistoryDatas(){
		return historyDatas;
	}
	void  setRunDataMakeType(const MakeRunDataType& type) {
		this->makeRunDataType = type;
	}
public:
	//同时运行chipic的个数
	unsigned int chipicCount = 6;
private:
	//lua虚拟机
	lua_State *lua_state;
	//参数组
	std::vector<Variate> variates;
	//待运行的m3d数据
	ChipicRunDatas chipicDataWait;
	//正在运行的m3d数据
	ChipicRunDataMap chipicDataRuning;
	//已经运行完的m3d数据
	ChipicRunDatas chipicDataFinish;
	//已筛选完数据的历史信息
	std::vector<HistoryData> historyDatas;
	//m3d文件路径
	QString m3dPath;
	//参数文件生成器
	FileMaker fileMaker;
	//contorl模块中的chipicManager 这个对象由contorl模块管理  不能在外部释放
	ChipicManager *chipicManager;
	//运行一次的所有信息
	HistoryData runData;
	//运行数据的成成模式
	MakeRunDataType makeRunDataType;
	//优化算法整个模块的运行状态
	bool runing = false;
	//暂时写一个参数来确定是否要响应已经完成的chipic启动新的chipic。这里为了保证优化时每次都一个一个的启动
	bool finishedIsVasible = true;
private:
	//获取错误处理函数再栈中的位置
	int getLuaErrorCallBackFunction();
	//打印lua脚本中的错误
	void printLuaError(const int& error);
	//调用一个lua函数
	void callLuaFunction(const std::string& functionName, const int& paramCount = 0, const int& returnCount = 0);
	//判断优化方法是否可用
	bool controlModIsRuning();
public Q_SLOTS:
	void chipicWorkFinished(unsigned long threadID);
	void chipicStartFinished(unsigned long threadID);
	//chipic解析完成槽
	void chipicAnalysisFinished(unsigned long threadID);
	//chipic异常退出槽
	void chipicErrorClose(unsigned long threadID);

Q_SIGNALS:
	//chipic启动成功之后的ui
	void addDataBar(QListWidgetItem*,QWidget*);
	//运行时的信息
	void smartContorlLog(std::string);
};