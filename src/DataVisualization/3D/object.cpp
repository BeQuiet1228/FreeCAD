#include "object.h"
DV3D::Object::Object()
	:name("Object")
{

}

DV3D::Object::~Object()
{

}

std::string DV3D::Object::getObjectName()
{
	return name;
}

void DV3D::Object::setObjectName(const std::string& name)
{
	this->name = name;
}

