#pragma once
#include "string"
#include "QSettings"
#include <map>
class NetworkUser
{
public: 
	NetworkUser();
	~NetworkUser();

	enum ErrorCode{
		NOT_ERROR = 0,
		DEFAULT_PASSWORD,
		NAME_EXIST
	};

public:
	//用户名与密码
	std::string userName, password;
public:
	//验证用户合法性
	bool verification();
	//设置用户名和密码
	void setNameAndPassword(const std::string& userName, const std::string& password);
	//注册新账户
	ErrorCode registerUser();
	//寻找该用户是否拥有当前这个threadId
	bool findThreadId(const unsigned long& threadId);
	//添加一个threadid到这个账户
	bool addThreadId(const unsigned long &threadId);
	//移除一个trheadid
	bool removeThreadId(const unsigned long& threadId);
private:
	std::map<unsigned long,int> threadIdMap;
};