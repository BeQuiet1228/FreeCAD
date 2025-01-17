#pragma once
#include "RunChipic3dListener.h"
#include "runchipic3d.h"
#include "CJsonObject.hpp"
class MessageTransition
{
public:
	MessageTransition();
	~MessageTransition();

public:
	//向json中添加一个cmd
	static bool addCmd(neb::CJsonObject& json, const std::string& cmd);
	//从json中获取一个cmd
	static bool getCmd(const neb::CJsonObject& json, std::string& cmd);
	//向json中添加一个username
	static bool addUserName(neb::CJsonObject& json, const std::string& userName){
		return json.Add("userName", userName);
	};
	//向json中添加一个password
	static bool addPassword(neb::CJsonObject& json, const std::string& password){
		return json.Add("password", password);
	};
	//从json中获取一个用户名
	static bool getUserName(const neb::CJsonObject& json, std::string& userName){
		return json.Get("userName", userName);
	};
	//从json中获取一个密码
	static bool getPassword(const neb::CJsonObject& json, std::string& password){
		return json.Get("password", password);
	};
	//向json中添加一个错误代码
	static bool addErrorCode(neb::CJsonObject& json, const std::string& errorCode){
		return json.Add("errorCode", errorCode);
	};
	//从json中获取一个错误代码
	static bool getErrorCOde(const neb::CJsonObject& json, std::string& errorCode){
		return json.Get("errorCode", errorCode);
	};
	//从json中获取一个threadID
	static bool getThreadID(const neb::CJsonObject& json, std::string& threadId){
		return json.Get("threadID", threadId);
	};
	static bool getThreadID(const neb::CJsonObject& json, unsigned long& id){
		std::string temp;
		bool ok = getThreadID(json, temp);
		id = std::stoul(temp);
		return ok;
	};
	//向json中添加一个threadid
	static bool addThreadID(neb::CJsonObject& json, const std::string& threadId){
		return json.Add("threadID", threadId);
	};
	//向json中添加一个路径
	static bool addPath(neb::CJsonObject& json, const std::string& path){
		return json.Add("path", path);
	}
	//向json中获取一个路径
	static bool getPath(const neb::CJsonObject& json, std::string& path){
		return json.Get("path", path);
	}
	//设置路径 针对json中已有的键 更改其值
	static bool setPath(neb::CJsonObject& json, const std::string& path){
		return json.Replace("path", path);
	}
	//向json中添加一个文件名
	static bool addFileName(neb::CJsonObject& json, const std::string& fileName){
		return json.Add("fileName", fileName);
	}
	//从json中获取一个文件名
	static bool getFileName(const neb::CJsonObject& json, std::string& fileName){
		return json.Get("fileName", fileName);
	}
	//获取一个线程数
	static bool getThreadCount(const neb::CJsonObject& json, std::string& threadCount){
		return json.Get("threadCount", threadCount);
	}
	//添加一个线程数
	static bool addThreadCount(neb::CJsonObject& json, std::string& threadCount){
		return json.Add("threadCount", threadCount);
	}
	//添加一个索引
	static bool addIndex(neb::CJsonObject& json, const int& index)
	{
		return json.Add("index", std::to_string(index));
	}
	//设置一个索引  针对已有元素 进行修改
	static bool setIndex(neb:: CJsonObject& json, const int& index){
		return json.Replace("index", std::to_string(index));
	}
	//获取一个索引
	static bool getIndex(const neb::CJsonObject& json, int& index){
		std::string temp;
		bool ok = json.Get("index", temp);
		index = std::stoi(temp);
		return ok;
	};
	//json消息转换为winmessage
	static Message jsonToWinMessage(const std::string &json);
	//winmessage转换为json消息
	static std::string winMessageTojson(const Message &msg);
	//获取json中的字符串
	static void jsonGetStringValue(neb::CJsonObject& jsonObject,const std::string& key,std::string& value);
	//创建一个启动chipic的json消息
	static std::string creatRunChipicJsonMessage(const std::string& m3dPath,const int& threadCount);
	//创建一个启动chipic的json消息
	static std::string creatRunChipicFixJsonMessage(const std::string& m3dPath, const int& threadCount);
	//创建一个关闭chipic的json消息
	static std::string creatCloseChipicJsonMessage(const DWORD threadId, const int& errorCode = 0);
	//GBK编码的std::string转换为qstring
	static QString gbkStdstringToQstring(const std::string& str);
	//UTF-8编码的std::string 转GBK std::string
	static std::string utf8StdstringToGbkStdstring(const std::string& str);
	//创建一个cmd消息
	static std::string creatCmdMessage(const std::string& Cmd, const DWORD& threadId = 0);
	//创建一个chipic启动完成消息
	static std::string creatChipicStartfinishedJsonMessage(const std::string& m3dPath,const DWORD& threadId,const int& threadCount,const std::string& userName);
	//创建一个申请登录cmd
	static std::string creatLoginCmd(const std::string username,const std::string password);
	//创建一个申请注册的cmd
	static std::string creatRegisterCmd(const std::string username, const std::string password);
};
