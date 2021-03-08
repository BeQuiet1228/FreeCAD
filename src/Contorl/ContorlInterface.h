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
private:
	Contorl *contorl;
	static std::shared_ptr<ContorlInterface> _instance;

public:
	//获取按钮widget
	ContorlButtonBar * getContorlButtonBar();
	//获取展示信息widget
	ContorlDataBar * getContorlDataBar();
	//设置按钮显示  以及信息显示窗口
	void setButtonBar(ContorlButtonBar* bar);
	void setDataBar(ContorlDataBar* bar);
	//设置运行m3d路径
	void setM3dPath(const std::string& path);
	//发送消息win
	void senWinMessage(const int& type, const int& wParam, const int& lParam);
	//获取chipicManager
	ChipicManager* getChipicManager();
	//获取freecad中的工程路径
	std::string getDocumentPath();
	//关闭所有正在运行的程序
	void closeAllChipic();
	//判断是否有chipic正在运行
	bool hasChipicRuning();
	//判断是否有已标准模式运行的chipic
	bool hasManualChipicRuning();
	//按钮点击时调用函数
	void buttonClicked(const int& buttonID);
	//获取控制模块的连接方式
	int getConnectWay();
	//显示树控件
	void showTreeWidget();
	//清理chipicmanager的数据对象
	void clearChipicManager();

};
