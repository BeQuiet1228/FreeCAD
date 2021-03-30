#pragma  once
#include "HDF5Reader/hdf5io.h"
#include <vector>
#include <list>
#include <mutex>
#include <memory>
#include <QPoint>
#include <QString>
#include <QStringList>
class Data{


public:
	using Values = std::vector<float>;
	using ValuesPtr = std::shared_ptr<Values>;
	using ListValues = std::list< ValuesPtr >;
	using ListValuesPtr = std::shared_ptr<ListValues>;
	using MutexPtr = std::shared_ptr<std::mutex>;
	//自动锁
	class AutoMutx{
	public:
		AutoMutx(const MutexPtr& mutex){
			this->mutex = mutex;
			mutex->lock();
		}
		~AutoMutx(){
			this->mutex->unlock();
		}
	private:
		MutexPtr mutex;
	};
	struct Rang{
		Rang() :max(0), min(0){};
		float length(){
			return max - min;
		}
		float max;
		float min;
	};

public:
	enum RunMod{
		SINGLE_THREAD = 0, //单线程
		MULTITHREAD		//多线程
	};
public:
	Data(Hdf5Data& h5Data ,const RunMod& mod = SINGLE_THREAD);
	virtual ~Data();

private:
	//h5文件数据
	Hdf5Data h5Data;
	//原始数据
	ListValuesPtr sourceData;
	//原始数据锁
	MutexPtr sourceDataMutex;
	//运行模式
	RunMod runMod;
	//原数据是否已载入
	bool sourceDataIsLoad;
protected:
	//h5数据头部信息
	std::vector<std::string> headList;
public:
	//载入h5文件中的数据
	bool  loadSourceData();
	//强制载入h5文件 不管是否已经载入都重新载入
	bool loadSourceDataHard();
	//清除原始数据
	void clearSourceData();
	//设置渲染模式
	void setRunMod(const RunMod& mod);
	//数据是否已载入
	bool isLoad(){
		return sourceDataIsLoad;
	}

	//数据获取接口，这里强制通过接口获取是为了之后多线程处理时数据同步。
protected:
	//获取原始数据，获取的时copy对象
	bool getSourceDataCopy(ListValuesPtr& listValuePtr);
	//获取原始数据，获取的是reference
	bool getSourceData(ListValuesPtr& listValuePtr);
	//重新获取数据
	//主要用于线程模式发生变化时，如单线程渲染切换到多线程渲染的时候，如果之前是获取的原数据的引用，那么不重新获取会有问题。
	virtual void restorDeriveData() = 0;
	//根据运行模式自动调整获取数据的方式
	bool autoModGetSourceData(ListValuesPtr& listValues);
	//初始化基本信息
	virtual void initInformation();
};

class XYData :public Data{
public:
	XYData(Hdf5Data& h5Data, const RunMod& mod = SINGLE_THREAD);
	~XYData() = default;
public:
	virtual unsigned int findIndexFromXValueL(const float& x) = 0;
	unsigned int findIndexFromXValueR(const float& x);
	virtual bool loadPoint() = 0;
	//操作size
	unsigned int getPointSize(){
		std::lock_guard<std::mutex> am(pointSizeMutex);
		return pointSize;
	};
	//获取范围
	Rang getXRang(){
		std::lock_guard<std::mutex> am(xRangMutex);
		return xRang;
	};
	void setXRang(const Rang& rg){
		std::lock_guard<std::mutex> am(xRangMutex);
		xRang = rg;
	}
	Rang getYRang(){
		std::lock_guard<std::mutex> am(yRangMutex);
		return yRang;
	};
	void setYRang(const Rang& rg){
		std::lock_guard<std::mutex> am(yRangMutex);
		yRang = rg;
	}
	//操作tag
	void setXTag(const std::string& tag){
		std::lock_guard<std::mutex> am(xTagMute);
		xTag = tag;
	}
	std::string getXTag(){
		std::lock_guard<std::mutex> am(xTagMute);
		return xTag;
	}
	void setYTag(const std::string tag){
		std::lock_guard<std::mutex> am(yTagMutex);
		yTag = tag;
	}
	std::string getYTag(){
		std::lock_guard<std::mutex> am(yTagMutex);
		return yTag;
	}
protected:
	virtual bool initXYRang() = 0;
	//设置size
	void setPointSize(const unsigned int& size){
		std::lock_guard<std::mutex> am(pointSizeMutex);
		pointSize = size;
	}
	void initInformation();
private:
	//点的个数
	unsigned int pointSize;
	std::mutex pointSizeMutex;
	//xy的范围
	Rang xRang, yRang;
	std::mutex xRangMutex, yRangMutex;
	//xy数据的单位
	std::string xTag, yTag;
	std::mutex xTagMute, yTagMutex;
};