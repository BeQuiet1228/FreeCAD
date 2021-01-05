#include "NetworkUser.h"
#include <iostream>
NetworkUser::NetworkUser()
{

}

NetworkUser::~NetworkUser()
{

}

/**
* @brief NetworkUser::verification 验证用户名密码是否正确
* @return bool true 正确
*/
bool NetworkUser::verification()
{
	QSettings setting("PICGUI", "NetworkUser");
	std::string password = setting.value(QString::fromStdString(userName), "defaultPasswprd").toString().toStdString();

	if (password == "defaultPasswprd")
		return false;
	if (password == this->password)
		return true;
	return false;
}

/**
* @brief NetworkUser::setNameAndPassword 设置用户名与密码
* @param const std::string & userName
* @param const std::string & password
* @return void
*/
void NetworkUser::setNameAndPassword(const std::string& userName, const std::string& password)
{
	this->userName = userName;
	this->password = password;
}

/**
* @brief NetworkUser::registerUser 注册一个新的账户
* @return NetworkUser::ErrorCode
*/
NetworkUser::ErrorCode NetworkUser::registerUser()
{
	QSettings setting("PICGUI", "NetworkUser");
	std::string password = setting.value(QString::fromStdString(userName), "defaultPasswprd").toString().toStdString();

	if (password != "defaultPasswprd")
		return NAME_EXIST;
	if (this->password == password)
		return DEFAULT_PASSWORD;

	setting.setValue(QString::fromStdString(userName), QString::fromStdString(this->password));
	return NOT_ERROR;
}

/**
* @brief NetworkUser::findThreadId 寻找这个thraedid是否属于该账户
* @param const unsigned long & threadId
* @return bool true表示属于
*/
bool NetworkUser::findThreadId(const unsigned long& threadId)
{
	auto iter = threadIdMap.find(threadId);

	if (iter == threadIdMap.end())
		return false;
	return true;
}

/**
* @brief NetworkUser::addThreadId 添加一个threadid到该账户 并记录chipic的路径信息
* @param const unsigned long & threadId
* @param const std::string & servicePath 服务端路径,这个路径含有文件名 根据这个路径匹配账户下已有的chipic信息 如果没有匹配到 则键入一个空的对象
* @return bool
*/
bool NetworkUser::addThreadId(const unsigned long &threadId, const std::string& servicePath)
{
	auto i = chipicDataList.begin();
	for (; i != chipicDataList.end(); i++)
	{
		if ((i->servicePath +"/"+ i->m3dFileName) == servicePath)
			break;
	}

	ChipicData chipicData;
	if (i == chipicDataList.end())
	{
#ifdef MY_LOG
		std::cerr << "NetworkUser::addThreadId not find chipicData! servic path :"
			<< servicePath << std::endl;
#endif // MY_LOG
	}else{
		chipicData = (*i);
		chipicData.threadID = threadId;
		//移除已取到的chipic信息
		chipicDataList.erase(i);
	}
	threadIdMap.insert(std::map<unsigned long, ChipicData>::value_type(threadId, chipicData));
	return true;
}

/**
* @brief NetworkUser::removeThreadId 移除一个threadid
* @param const unsigned long & threadId
* @return bool
*/
bool NetworkUser::removeThreadId(const unsigned long& threadId)
{
	auto iter = threadIdMap.find(threadId);
	
	if (iter == threadIdMap.end())
		return false;
	threadIdMap.erase(iter);
	return true;
}

/**
* @brief NetworkUser::getChipicDataForThreadID 根据threadID寻找对应的chipic信息对象
* @param const unsigned long & threadId 
* @param ChipicData & data
* @return bool false 表示不存在这个信息
*/
bool NetworkUser::getChipicDataForThreadID(const unsigned long& threadId, ChipicData& data)
{
	auto iter = threadIdMap.find(threadId);
	if (iter == threadIdMap.end())
		return false;
	data = iter->second;
	return true;
}

