#pragma once
#include "LonelinessMode.h"
#include "CJsonObject.hpp"
class MessageTransition
{
public:
	MessageTransition();
	~MessageTransition();

public:
	//json消息转换为winmessage
	static Message jsonToWinMessage(const std::string &json);
	//winmessage转换为json消息
	static std::string winMessageTojson(const Message &msg);
	//获取json中的字符串
	static void jsonGetStringValue(neb::CJsonObject& jsonObject,const std::string& key,std::string& value);
	//创建一个启动chipic的json消息
	static std::string creatRunChipicJsonMessage(const std::string& m3dPath,const int& threadCount);
	//创建一个关闭chipic的json消息
	static std::string creatCloseChipicJsonMessage(const DWORD threadId);
	//GBK编码的std::string转换为qstring
	static QString gbkStdstringToQstring(const std::string& str);
};
