#include "MessageTransition.h"


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
#ifdef _DEBUG
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
#ifdef _DEBUG
		std::cerr << "MessageTransition jsonGetStringValue failed!" << "key:" << key << std::endl;
#endif // _DEBUG
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

	neb::CJsonObject temp;
	temp.Add("m3dPath", m3dPath);
	temp.Add("threadCount", threadCount);

	Message.Add("Text", temp.ToString());

	return Message.ToString();
}

/**
* @brief MessageTransition::creatCloseChipicJsonMessage 创建一个关闭chipic的消息
* @param const DWORD threadId
* @return std::string
*/
std::string MessageTransition::creatCloseChipicJsonMessage(const DWORD threadId)
{
	neb::CJsonObject Message;
	Message.Add("cmd", "CloseChipic");
	Message.Add("threadID", threadId);

	return Message.ToString();
}
