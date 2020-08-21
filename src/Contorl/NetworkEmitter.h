#pragma once
#include "EmitterInterface.h"

class NetworkEmitter:public EmitterInterface
{
public:
	NetworkEmitter();
	~NetworkEmitter();

public:
	virtual void sendMessage(const std::string& json) override;
	virtual int getEmitterId() override;
};