#include "Chipic.h"


Chipic::Chipic(DWORD threadID)
{
	this->threadID = threadID;
}

Chipic::~Chipic()
{

}

void Chipic::disposJsonMessage(const std::string& json)
{

}

#ifndef MY_QTC_DEBUG
#include "moc_Chipic.cpp"
#endif