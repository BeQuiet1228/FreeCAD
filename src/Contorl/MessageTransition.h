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
	//UTF-8编码的std::string 转GBK std::string
	static std::string utf8StdstringToGbkStdstring(const std::string& str);
	//创建一个cmd消息
	static std::string creatCmdMessage(const std::string& Cmd, const DWORD& threadId = 0);
	//创建一个chipic启动完成消息
	static std::string creatChipicStartfinishedJsonMessage(const std::string& m3dPath,const DWORD& threadId,const int& threadCount);
};
