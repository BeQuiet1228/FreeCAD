#pragma once
#include "LonelinessMode.h"
#include "CJsonObject.hpp"
class MessageTransition
{
public:
	MessageTransition();
	~MessageTransition();

public:
	static Message jsonToWinMessage(const std::string &json);
	static std::string winMessageTojson(const Message &msg);
	static void jsonGetStringValue(neb::CJsonObject& jsonObject,const std::string& key,std::string& value);
	static std::string creatRunChipicJsonMessage(const std::string& m3dPath,const int& threadCount);
};
