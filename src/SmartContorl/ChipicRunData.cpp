#include "ChipicRunData.h"
#include "Contorl/ContorlDataBar.h"
#include "Contorl/Chipic.h"
ChipicRunData::ChipicRunData()
{
	this->widgetItem = nullptr;
	this->dataBar = nullptr;
	resultData.reset(new ResultData);
}

ChipicRunData::~ChipicRunData()
{

}

/**
* @brief ChipicRunData::setCreatDataBar 用chipic对象创建一个databar
* @param std::shared_ptr<Chipic> chipic
* @return void
*/
void ChipicRunData::setCreatDataBar(std::shared_ptr<Chipic> chipic)
{
	this->deleteItemAndBarPtr();

	this->widgetItem = new QListWidgetItem;
	this->dataBar = new ContorlDataBar;
	this->widgetItem->setSizeHint(this->dataBar->size());
	this->dataBar->setChipicData(chipic);
}

/**
* @brief ChipicRunData::deleteItemAndBarPtr 释放调ui对象
* @return void
*/
void ChipicRunData::deleteItemAndBarPtr()
{
	if (this->widgetItem != nullptr)
		delete this->widgetItem;
	if (this->dataBar != nullptr)
		delete this->dataBar;
}


