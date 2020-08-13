#include "MessageTransition.h"
#include <qtextcodec.h>

MessageTransition::MessageTransition()
{

}
MessageTransition::~MessageTransition()
{
}

/**
* @brief MessageTransition::jsonToWinMessage 将json消息转换为winMessage消息
* @param const std::string & json json消息
* @return Message winmessage消息
*/
Message MessageTransition::jsonToWinMessage(const std::string &json)
{
	neb::CJsonObject jsonObject(json);
	std::string temp;
	Message msg;
	//获取线程id
	jsonGetStringValue(jsonObject, "threadID", temp);
	msg.threadId = std::stol(temp);
	
	jsonGetStringValue(jsonObject, "MessageID", temp);
	msg.Msg = std::stol(temp);

	jsonGetStringValue(jsonObject, "WParam", temp);
	msg.wParam = std::stol(temp);

	jsonGetStringValue(jsonObject, "LParam", temp);
	msg.lParam = std::stol(temp);

	jsonGetStringValue(jsonObject, "Text", temp);
	msg.text = temp;

	return msg;
}

/**
* @brief MessageTransition::winMessageTojson 将winMessage消息转换为json消息
* @param const Message & msg 
* @return std::string
*/
std::string MessageTransition::winMessageTojson(const Message &msg)
{
	neb::CJsonObject json;
	bool ok = json.Add("threadID",msg.threadId )&&
		json.Add("MessageID", msg.Msg)&&
		json.Add("WParam", msg.wParam)&&
		json.Add("LParam", msg.lParam)&&
		json.Add("Text", msg.text);
#ifdef MY_DEBUG
	if (!ok)
		std::cerr << "MessageTransition WinMessageTojson add json value failed!" << std::endl;
#endif // DEBUG

	return json.ToString();
}

/**
* @brief MessageTransition::jsonGetStringValue 获取json对象中的字符串值
* @param CJsonObject& jsonObject json对象
* @param const std::string & key 键
* @param std::string & value 值
* @return void
*/
void MessageTransition::jsonGetStringValue(neb::CJsonObject& jsonObject, const std::string& key, std::string& value)
{
	if (!jsonObject.Get(key, value))
	{
#ifdef MY_DEBUG
		std::cerr << "MessageTransition jsonGetStringValue failed!" << "key:" << key << std::endl;
#endif // MY_DEBUG
	}
}

/**
* @brief MessageTransition::creatRunChipicJsonMessage 创建一个运行chipic的json消息
* @param const std::string & m3dPath
* @param const int & threadCount
* @return std::string
*/
std::string MessageTransition::creatRunChipicJsonMessage(const std::string& m3dPath, const int& threadCount)
{
	neb::CJsonObject Message;
	Message.Add("cmd", "RunChipic");
	Message.Add("m3dPath", m3dPath);
	Message.Add("threadCount", threadCount);

	return Message.ToString();
}

/**
* @brief MessageTransition::creatCloseChipicJsonMessage 创建一个关闭chipic的消息
* @param const DWORD threadId
* @return std::string
*/
std::string MessageTransition::creatCloseChipicJsonMessage(const DWORD threadId)
{
	return creatCmdMessage("CloseChipic", threadId);
}
QString MessageTransition::gbkStdstringToQstring(const std::string &str)
{
	QTextCodec* pCodec = QTextCodec::codecForName("gb2312");
	if (!pCodec) return "";

	QString qstr = pCodec->toUnicode(str.c_str(), str.length());
	return qstr;
}

/**
* @brief MessageTransition::utf8StdstringToGbkStdstring
* @param const std::string & str
* @return std::string
*/
std::string MessageTransition::utf8StdstringToGbkStdstring(const std::string& str)
{
	auto gbk = QTextCodec::codecForName("gb2312");

	QString temp = QString::fromUtf8(str.c_str());
	std::string ret = gbk->fromUnicode(temp).data();
	return ret;
}

/**
* @brief MessageTransition::creatCmdMessage 创建一个cmd消息
* @param const std::string & Cmd
* @param const DWORD & threadId
* @return std::string
*/
std::string MessageTransition::creatCmdMessage(const std::string& Cmd, const DWORD& threadId /*= 0*/)
{
	neb::CJsonObject Message;
	Message.Add("cmd", Cmd);
	Message.Add("threadID", threadId);

	return Message.ToString();
}

/**
* @brief MessageTransition::creatChipicStartfinishedJsonMessage  创建一个chipic启动完成的消息
* @param const std::string & m3dPath
* @param const DWORD & threadId
* @param const int & threadCount
* @param const std::string & userName
* @return std::string
*/
std::string MessageTransition::creatChipicStartfinishedJsonMessage(const std::string& m3dPath, const DWORD& threadId, const int& threadCount, const std::string& userName)
{
	std::string json = creatCmdMessage("startFinished", threadId);
	neb::CJsonObject message(json);
	message.Add("m3dPath", m3dPath);
	message.Add("threadCount", threadCount);
	message.Add("userName", userName);
	return message.ToString();
}

/**
* @brief MessageTransition::creatLoginCmd 创建一个登录cmd
* @param const std::string username	用户名
* @param const std::string password 密码
* @return std::string
*/
std::string MessageTransition::creatLoginCmd(const std::string username, const std::string password)
{
	neb::CJsonObject json;

	addCmd(json, "login");
	addPassword(json, password);
	addUserName(json,username);

	return json.ToString();
}

/**
* @brief MessageTransition::creatRegisterCmd 创建一个注册cmd
* @param const std::string username
* @param const std::string password
* @return std::string
*/
std::string MessageTransition::creatRegisterCmd(const std::string username, const std::string password)
{
	neb::CJsonObject json;

	addCmd(json, "register");
	addPassword(json, password);
	addUserName(json, username);

	return json.ToString();
}

/**
* @brief MessageTransition::addCmd 向json中添加一个cmd
* @param neb::CJsonObject & json	json对象
* @param const std::string & cmd cmd
* @return bool
*/
bool MessageTransition::addCmd(neb::CJsonObject& json, const std::string& cmd)
{
	return json.Add("cmd", cmd);
}

/**
* @brief MessageTransition::getCmd 获取一个cmd
* @param neb::CJsonObject & json
* @param std::string & cmd
* @return bool
*/
bool MessageTransition::getCmd(const neb::CJsonObject& json, std::string& cmd)
{
	return json.Get("cmd", cmd);
}
