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

/**
* @brief ContorlInterface::hasManualChipicRuning 这个函数主要用与判断是否是有已正常模式启动的chipic在运行，与自动模式区分开来
* @return bool
*/
bool ContorlInterface::hasManualChipicRuning()
{
	return hasChipicRuning() && (getChipicManager()->getRunType() == ChipicManager::MANUAL);
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

void ContorlInterface::showTreeWidget()
{
	contorl->showTreeWidget();
}

/**
* @brief ContorlInterface::clearChipicManager 这个函数主要是在需要清空chipic数据 但是不想关闭内核程序的时候调用
* @return void
*/
void ContorlInterface::clearChipicManager()
{
	auto manager = getChipicManager();
	manager->clearChipicData();
}

/**
* @brief ContorlInterface::getM3dPathForThreadID 根据threadID获取运行路径
* @param unsigned long threadID
* @return QString
*/
QString ContorlInterface::getM3dPathForThreadID(unsigned long threadID)
{
	auto manager = getChipicManager();
	return manager->getM3dpathForThreadID(threadID);
}

/**
* @brief ContorlInterface::getChipicThreadCount 根据线程id获取是否使用并行模式
* @param unsigned long threadID
* @return unsigned int -1 代表没有这个chipic对象
*/
unsigned int ContorlInterface::getChipicThreadCount(unsigned long threadID)
{
	auto manager = getChipicManager();
	return manager->getChipicThreadCount(threadID);
}

bool ContorlInterface::chipicRunModIsAuto()
{
	auto manager = getChipicManager();
	return	(manager->getRunType() == ChipicManager::AUTO);
}

/**
* @brief ContorlInterface::getChipicManager 返回chipic管理器指针  这个指针由contorl对象管理 
* @return ChipicManager*
*/
ChipicManager* ContorlInterface::getChipicManager()
{
	return &(contorl->chipicManager);
}

