#include "TargetItem.h"

TargetItem::TargetItem()
{
	type = "target";
}

TargetItem::~TargetItem()
{

}

void TargetItem::setType(const std::string& t)
{
	type = t;
}

std::string TargetItem::getType()
{
	return type;
}

