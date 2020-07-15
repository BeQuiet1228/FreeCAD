#pragma once

#include <memory>
#include <mutex>
#include "ContorlConfig.hpp"
#include "ContorlButtonBar.h"
#include "ContorlDataBar.h"
class Contorl;
class CONTROL_EXPORT ContorlInterface
{
public:
	static std::shared_ptr<ContorlInterface> GetInstance(){
		static std::once_flag flag;
		std::call_once(flag, [&](){
			_instance.reset(new ContorlInterface);
		});

		return _instance;
	}
	~ContorlInterface();
private:
	ContorlInterface();
	ContorlInterface(const ContorlInterface&) = delete;
	ContorlInterface operator =(const ContorlInterface&) = delete;
public:
	Contorl *contorl;
	static std::shared_ptr<ContorlInterface> _instance;

public:
	ContorlButtonBar * getContorlButtonBar();
	ContorlDataBar * getContorlDataBar();
	void setM3dPath(const std::string& path);
};
