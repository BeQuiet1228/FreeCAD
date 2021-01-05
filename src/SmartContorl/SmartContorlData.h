#pragma once
#include <mutex>
#include <memory>
#include <map>
#include <HDF5Reader/hdf5io.h>
class SmartContorl;
class ChipicResultGetter;
class CInterfaceStack;
class SmartContorlData{

public:
	~SmartContorlData();
	SmartContorlData(const SmartContorlData&) = delete;
	SmartContorlData operator=(const SmartContorlData&) = delete;

	static std::shared_ptr<SmartContorlData> GetInstance(){
		static std::once_flag flag;
		std::call_once(flag, [&](){
			_instance.reset(new SmartContorlData);
		});
		return _instance;
	}
private:
	SmartContorlData();
	static std::shared_ptr<SmartContorlData> _instance;

public:
	//控制对象
	SmartContorl *smartContorl;
	//运算结果对象
	ChipicResultGetter *resultGetter;
	//h5文件io
	Hdf5IO hdf5IO;
	//lua接口栈
	CInterfaceStack *cStack;
public:
	//打开当前hdf5文件
	bool openActiveH5File();
	//找到结果数据
	bool findResultData(const std::string& name);
	//打开一个数据库
	bool openDataSet(const int& index = 0);
	//获取数据库中的值的大小
	int getDataSetValueSize();
	//获取一个数据
	float getDataSetValue(const int& index);
	//获取下一个运算结果
	bool nextResult();
	//获取运算结果对象
	void getChipicRunResult();
	//添加一个已优化参数
	void addParam(const float& value);
	//清理数据
	void clear();
};