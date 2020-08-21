#pragma once
#include <string>
class  EmitterInterface
{
public:
	EmitterInterface(){};
	virtual ~EmitterInterface(){};

public:
	virtual void sendMessage(const std::string& json) = 0;
	virtual int getEmitterId() = 0;

};