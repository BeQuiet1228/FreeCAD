#pragma  once
#include "HDF5Reader/hdf5io.h"
#include <vector>
#include <list>
#include <mutex>
#include <memory>
#include <QPoint>

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
public:
	//获取类名
	virtual	std::string getClassName(){
		return "Data";
	}
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
};