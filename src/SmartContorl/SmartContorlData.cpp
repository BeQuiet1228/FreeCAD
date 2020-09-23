#include "SmartContorlData.h"
#include "smartcontorl.h"
std::shared_ptr<SmartContorlData> SmartContorlData::_instance;

SmartContorlData::SmartContorlData()
{
	smartContorl = new SmartContorl;
}

SmartContorlData::~SmartContorlData()
{

}


