#include "ContorlInterface.h"
#include "Contorl.h"
#include "ContorlDataBar.h"
#include "ContorlButtonBar.h"
#include <QString>
#include "MessageTransition.h"
#include "Chipic.h"
std::shared_ptr<ContorlInterface> ContorlInterface::_instance;
ContorlInterface::ContorlInterface()
{
	contorl = new Contorl;
}

ContorlInterface::~ContorlInterface()
{
 	delete contorl;
}

ContorlButtonBar * ContorlInterface::getContorlButtonBar()
{
	return (contorl->contorlButtonBar);
}

ContorlDataBar * ContorlInterface::getContorlDataBar()
{
	return (contorl->contorlDataBar);
}

/**
* @brief ContorlInterface::setButtonBar 设置按钮ui对象
* @param ContorlButtonBar * bar
* @return void
*/
void ContorlInterface::setButtonBar(ContorlButtonBar* bar)
{
	if (contorl->contorlButtonBar == bar)
		return;
	delete contorl->contorlButtonBar;
	contorl->contorlButtonBar = bar;
}

/**
* @brief ContorlInterface::setDataBar 设置信息展示的ui对象
* @param ContorlDataBar * bar
* @return void
*/
void ContorlInterface::setDataBar(ContorlDataBar* bar)
{
	if (contorl->contorlDataBar == bar)
		return;
	delete contorl->contorlDataBar;
	contorl->contorlDataBar = bar;
	contorl->connectButtonBar();
}

void ContorlInterface::setM3dPath(const std::string& path)
{
	contorl->m3dPath = path;
}

void ContorlInterface::senWinMessage(const int& type, const int& wParam, const int& lParam)
{
	if (contorl->chipicManager.CurrentChipic)
	{
		contorl->chipicManager.CurrentChipic->sendMessage(type, wParam, lParam);
	}
}

std::string ContorlInterface::getDocumentPath()
{
	contorl->getM3dPathForRunPython();
	return contorl->m3dPath;
}

/**
* @brief ContorlInterface::closeAllChipic 关闭所有的chipic程序
* @return void
*/
void ContorlInterface::closeAllChipic()
{
	contorl->chipicManager.closeAllChipic();
}

/**
* @brief ContorlInterface::hasChipicRuning
* @return bool
*/
bool ContorlInterface::hasChipicRuning()
{
	if (contorl->chipicManager.chipicMap.size() != 0)
		return true;
	return false;
}

void ContorlInterface::buttonClicked(const int& buttonID)
{
	contorl->buttonClinked(buttonID);
}

/**
* @brief ContorlInterface::getConnectWay 获取控制模块的连接方式
* @return int 1=本地连接 2=网络连接
*/
int ContorlInterface::getConnectWay()
{
	return contorl->getConnectWay();
}

/**
* @brief ContorlInterface::getChipicManager 返回chipic管理器指针  这个指针由contorl对象管理 
* @return ChipicManager*
*/
ChipicManager* ContorlInterface::getChipicManager()
{
	return &(contorl->chipicManager);
}

