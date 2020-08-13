#include "NetworkUser.h"
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
* @brief NetworkUser::addThreadId 添加一个threadid到该账户
* @param const unsigned long & thradId
* @return bool
*/
bool NetworkUser::addThreadId(const unsigned long &threadId)
{
	threadIdMap.insert(std::map<unsigned long,int>::value_type(threadId,0));
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

