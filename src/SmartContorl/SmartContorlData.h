#pragma once
#include <mutex>
#include <memory>
#include <map>
class SmartContorl;
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
	SmartContorl *smartContorl;

};