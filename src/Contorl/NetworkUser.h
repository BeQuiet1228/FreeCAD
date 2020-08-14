#pragma once
#include "string"
#include "QSettings"
#include <map>
#include <list>
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
	struct ChipicData{
		//包含后缀的文件名
		std::string m3dFileName;
		//不包含后缀的文件名
		std::string fileName;
		//不包含文件名的客户端路径
		std::string clientPath;
		//不包含文件名的服务端路径
		std::string servicePath;
		//线程数
		int threadCount;
	};

public:
	//用户名与密码
	std::string userName, password;
	/*
		chipic信息容器.
		因为考虑到可能多个chipic同时运行时,会产生多个chipic信息.
		所以将信息暂存到容器中.在设置threadId时,根据服务端的路径匹配对应的chipic信息对象.
	*/
	std::list<ChipicData> chipicDataList;
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
	bool addThreadId(const unsigned long &threadId,const std::string& servicePath);
	//移除一个trheadid
	bool removeThreadId(const unsigned long& threadId);
private:
	std::map<unsigned long,ChipicData> threadIdMap;
};