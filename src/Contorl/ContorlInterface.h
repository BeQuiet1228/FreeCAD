#pragma once

#include <memory>
#include <mutex>
#include "ContorlConfig.hpp"
#include "ContorlButtonBar.h"
#include "ContorlDataBar.h"
#include "ChipicManager.h"
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
	//获取按钮widget
	ContorlButtonBar * getContorlButtonBar();
	//获取展示信息widget
	ContorlDataBar * getContorlDataBar();
	//设置运行m3d路径
	void setM3dPath(const std::string& path);
	//发送消息win
	void senWinMessage(const int& type, const int& wParam, const int& lParam);
	//获取chipicManager
	ChipicManager* getChipicManager();
	//获取freecad中的工程路径
	std::string getDocumentPath();
};
