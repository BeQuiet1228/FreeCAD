#include "NetworkServer.h"
#include <QTcpServer>
#include <qsettings.h>
#include <QTcpSocket>
#include <iostream>
#include "NetworkSocket.h"
#include "MessageSender.h"
#include "JsonMessageGetter.h"
#include "MessageTransition.h"
#include "NetworkUser.h"
std::shared_ptr<NetworkServer> NetworkServer::_instance;

NetworkServer::~NetworkServer()
{
}

NetworkServer::NetworkServer()
{
	//初始化服务器对象
	server.reset(new QTcpServer);
	//链接有新链接槽
	connect(server.get(), SIGNAL(newConnection()), this, SLOT(serverNewConnection()));
	//连接本地消息槽
	connect(JsonMessageGetter::GetInstance().get(), SIGNAL(hasNewMessage()), this, SLOT(hasLocalMessage()));
}

/**
* @brief NetworkServer::getListeneAddress 从注册表返回监听地址
* @return QString
*/
QString NetworkServer::getListeneAddress()
{
	QSettings setting("PICGUI", "NetworkServerConfig");

	QString address = setting.value("address","default").toString();

	if (address == "default")
		address = "127.0.0.1";

	return address;	
}

/**
* @brief NetworkServer::getListenePort 从注册表返回监听端口
* @return int
*/
int NetworkServer::getListenePort()
{
	QSettings setting("PICGUI", "NetworkServerConfig");

	int port = setting.value("port", 0).toInt();

	if (port == 0)
		port = 8866;

	return port;
}

/**
* @brief NetworkServer::startListene 开始监听 监听地址与端口从注册表读入
* @return void
*/
void NetworkServer::startListene()
{
	if (server->isListening())
		server->close();
	server->listen(QHostAddress(getListeneAddress()), getListenePort());
}

/**
* @brief NetworkServer::setAddressAndPort 向注册表写入监听地址与端口
* @param const QString & address
* @param const int & prot
* @return void
*/
void NetworkServer::setAddressAndPort(const QString& address, const int& prot)
{
	QSettings setting("PICGUI", "NetworkServerConfig");

	setting.setValue("address", address);
	setting.setValue("port", prot);
}


/**
* @brief NetworkServer::disposeCmdMessage 处理命令消息
* @param const std::string & json
* @return bool
*/
bool NetworkServer::disposeCmdMessage(const std::string& json)
{
	std::string cmd;
	neb::CJsonObject jsonObject(json);
	//判断是否为cmd消息
	if (!(MessageTransition::getCmd(jsonObject, cmd)))
		return false;
	//处理对应消息
	if (disposeLoginMessage(jsonObject, cmd))
		return true;
	if (disposeRegisterMessage(jsonObject, cmd))
		return true;

	return false;
}

/**
* @brief NetworkServer::disposeLoginMessage 处理登录消息
* @param const std::string & json
* @param const std::string & cmd
* @return bool
*/
bool NetworkServer::disposeLoginMessage(const neb::CJsonObject& json, const std::string& cmd)
{
	if (cmd != "login")
		return false;
	std::string userName, password;
	bool ok = MessageTransition::getUserName(json, userName)&&MessageTransition::getPassword(json,password);

	//如果获取账号或者密码失败则返回
	if (!ok)
	{
#ifdef MY_LOG
		std::cerr << "NetworkServer::disposeLoginMessage,get userName and password failed!json:" <<
			json.ToString() << std::endl;
#endif // MY_LOG
		return false;
	}

	//获取发送消息的socket
	NetworkSocket *s = getSocketSender();
	if (s == nullptr)
	{
#ifdef MY_LOG
		std::cerr << "NetworkServer::disposeLoginMessage get sender failed!" << std::endl;
#endif // MY_LOG
		return false;
	}
	//将账号密码放入socket 并验证
	s->user->setNameAndPassword(userName, password);
	neb::CJsonObject jsonobject;
	MessageTransition::addCmd(jsonobject, "login");
	//0 代表登录成功 1代表登录失败
	if (s->user->verification())
	{
		MessageTransition::addErrorCode(jsonobject, "0");
	}else{
		MessageTransition::addErrorCode(jsonobject, "1");
#ifdef MY_LOG
		std::cerr << "NetworkServer::disposeLoginMessage login failed!" << std::endl;
#endif // MY_LOG

	}
	s->sendJsonMessage(jsonobject.ToString());
}

/**
* @brief NetworkServer::disposeRegisterMessage 处理注册消息
* @param const neb::CJsonObject & json 
* @param const std::string & cmd
* @return bool
*/
bool NetworkServer::disposeRegisterMessage(const neb::CJsonObject& json, const std::string& cmd)
{
	if (cmd != "register")
		return false;
	std::string userName, password;
	bool ok = MessageTransition::getUserName(json, userName) && MessageTransition::getPassword(json, password);

	//如果获取账号或者密码失败则返回
	if (!ok)
	{
#ifdef MY_LOG
		std::cerr << "NetworkServer::disposeRegisterMessage,get userName and password failed!json:" <<
			json.ToString() << std::endl;
#endif // MY_LOG
		return false;
	}

	//获取发送消息的socket
	NetworkSocket *s = getSocketSender();
	if (s == nullptr)
	{
#ifdef MY_LOG
		std::cerr << "NetworkServer::disposeRegisterMessage get sender failed!" << std::endl;
#endif // MY_LOG
		return false;
	}

	s->user->setNameAndPassword(userName, password);
	auto errcode = s->user->registerUser();
	
	neb::CJsonObject jsonObject;
	MessageTransition::addCmd(jsonObject, "register");
	MessageTransition::addErrorCode(jsonObject, std::to_string((int)errcode));
	s->sendJsonMessage(jsonObject.ToString());
}

/**
* @brief NetworkServer::getSocketSender 获取当前发送信号得socket
* @return NetworkSocket *	如果获取不成功则返回一个nullptr
*/
NetworkSocket * NetworkServer::getSocketSender()
{
	auto sender = this->sender();
	auto socket = dynamic_cast<NetworkSocket*>(sender);

	if (socket)
	{
		return socket;
	}
	else{
		socket = nullptr;
		return socket;
	}
}

/**
* @brief NetworkServer::startFinishedCmd从本地发来的startFinished命令.
主要为socket添加一个threadid,这样后面的消息才能根据相应的threadid找到对应的oscket.
* @param const std::string & json
* @return bool
*/
bool NetworkServer::startFinishedCmd(const std::string& json)
{
	//获取 cmd threadid userName
	std::string cmd = "default", threadId;
	MessageTransition::getCmd(json, cmd);
	MessageTransition::getThreadID(json, threadId);
	unsigned long  id = std::stoul(threadId);

	if (cmd != "startFinished")
		return false;

	std::string userName;
	if (!MessageTransition::getUserName(json, userName))
	{
#ifdef MY_LOG
		std::cerr << "NetworkServer::startFinishedCmd get cmd startFinished user name failed!" << std::endl;
#endif // MY_LOG
		return false;
	}
	//使用userName 匹配对应的socket
	auto i = socketList.begin();
	for (; i != socketList.end(); i++)
	{
		if ((*i)->user->userName == userName)
			break;
	}

	if (i == socketList.end())
	{
#ifdef MY_LOG
		std::cerr << "NetworkServer::startFinishedCmd get socket with user name failed!" << std::endl;
#endif // MY_LOG
		return false;
	}
	//将threadid 赋予socket 然后将消息发送出去
	(*i)->user->addThreadId(id);
	(*i)->sendJsonMessage(json);
	return true;
}

/**
* @brief NetworkServer::disposeLocalMessage 处理本地消息
* @param const std::string & json
* @return bool
*/
bool NetworkServer::disposeLocalMessage(const std::string& json)
{
	std::string temp;
	
	if (!MessageTransition::getThreadID(json, temp))
	{
#ifdef MY_LOG
		std::cerr << "NetworkServer::disposeLocalMessage get threadid failed! json:"
			<< json << std::endl;
#endif // MY_LOG
		return false;
	}
	unsigned long threadId = std::stoul(temp);

	auto i = socketList.begin();
	for (; i != socketList.end(); i++)
	{
		if ((*i)->user->findThreadId(threadId))
			break;
	}

	if (i == socketList.end())
	{
#ifdef MY_LOG
		std::cerr << "NetworkServer::disposeLocalMessage get socket failed! threadId:"
			<< threadId << std::endl;
#endif // MY_LOG
		return false;
	}

	(*i)->sendJsonMessage(json);
}

/**
* @brief NetworkServer::serverNewConnection tcp服务器有新的链接槽
* @return void
*/
void NetworkServer::serverNewConnection()
{
	//获取链接socket对象
	auto socket = server->nextPendingConnection();
	//将对象放入list
	std::shared_ptr<NetworkSocket> networkSocket(new NetworkSocket);
	networkSocket->setSocket(socket);
	socketList.push_back(networkSocket);
	//链接接受消息槽
	connect(networkSocket.get(), SIGNAL(receiveMessageFinished(NetworkSocket::SocketMessageBody)), this, SLOT(receiveMessageFinished(NetworkSocket::SocketMessageBody)));
#ifdef MY_DEBUG
	std::cerr << "NetworkServer::serverNewConnection()，address:"
		<< socket->peerAddress().toString().toStdString()
		<< ",port:" << socket->peerPort() << std::endl;
#endif // MY_DEBUG

}


/**
* @brief NetworkServer::receiveMessageFinished 接受消息完成槽
* @param NetworkSocket::SocketMessageBody msgBody
* @return void
*/
void NetworkServer::receiveMessageFinished(NetworkSocket::SocketMessageBody msgBody)
{

	if(disposeCmdMessage(msgBody.json.data()))
		return;
	auto sender = MessageSender::GetInstance();
	sender->sendJsonMessage(msgBody.json.data());

}

/**
* @brief NetworkServer::hasLocalMessage 含有本地消息时触发
* @return void
*/
void NetworkServer::hasLocalMessage()
{
	/*
		如果是启动完成消息,则将userName和threadId取出,根据userName寻找到对应的socket,然后将threadid赋予.
		如果是其他消息,则只去除threadid,根据threadId找到相应的socket,然后使用其发消息.
	*/
	auto gtter = JsonMessageGetter::GetInstance();
	std::string json;
	if (!gtter->getJsonMessage(json))
		return;
	//处理启动完成消息
	if (startFinishedCmd(json))
		return;
	if (disposeLocalMessage(json))
		return;
}

#include "moc_NetworkServer.cpp"
