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
#include "File.h"
#include <QDir>
#include <QFileInfo>
#include "RunChipic3dListener.h"
std::shared_ptr<NetworkServer> NetworkServer::_instance;

NetworkServer::~NetworkServer()
{
	server->close();
}

NetworkServer::NetworkServer()
{
	//初始化服务器对象
	server.reset(new QTcpServer);
	//链接有新链接槽
	connect(server.get(), SIGNAL(newConnection()), this, SLOT(serverNewConnection()));
	//连接本地消息槽
	connect(JsonMessageGetter::GetInstance().get(), SIGNAL(hasNewMessage()), this, SLOT(hasLocalMessage()));
	workPath = getWorkPath().toLocal8Bit();
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
	if (!server->listen(QHostAddress(getListeneAddress()), getListenePort()))
	{
#ifdef MY_LOG
		std::cerr << "NetworkServer::startListene, listen is failed! address:"
			<< getListeneAddress().toStdString() << ",port:"
			<< getListenePort() << ",Error code:"
			<< server->serverError() << std::endl;
#endif // MY_LOG

	}
}

/**
* @brief NetworkServer::killService 结束服务器监听 并强制终止已运行的chipic
* @return void
*/
void NetworkServer::killService()
{
	//关闭所有正在运行的chipic
	for (auto userIter = userMap.begin(); userIter != userMap.end(); userIter++)
	{
		auto user = userIter->second;
		for (auto chipicData = user->threadIdMap.begin(); chipicData != user->threadIdMap.end(); chipicData++)
		{
			std::string msg = MessageTransition::creatCloseChipicJsonMessage(chipicData->first);
			auto sender = MessageSender::GetInstance();
			sender->sendJsonMessage(msg);
		}
	}
	for (auto i = socketList.begin(); i != socketList.end(); i++)
	{
		(*i)->setDeleteSocket(true);
	}
	socketList.clear();
	server->close();
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
* @brief NetworkServer::setWorkPath 设置服务器工作路径
* @param const QString & workPath
* @return void
*/
void NetworkServer::setWorkPath(const QString& workPath)
{
	QSettings setting("PICGUI", "NetworkServerConfig");

	setting.setValue("workPath", workPath);

	this->workPath = workPath.toLocal8Bit();
}

/**
* @brief NetworkServer::getWorkPath 获取工作路径
* @return QT_NAMESPACE::QString
*/
QString NetworkServer::getWorkPath()
{
	QSettings setting("PICGUI", "NetworkServerConfig");

	return setting.value("workPath", "C:/chipicServiceWorkPath/").toString();
}

/**
* @brief NetworkServer::disposeCmdMessage 处理命令消息
* @param const std::string & json
* @return bool true 表示消息无需后续处理
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
	if (disposeRunchipicMessage(jsonObject, cmd))
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
		/*
			如果登录成功，则检查登录历史。
			查看该账号知否之前有登录过，再查看是否有未停止的chipic正在与运行。
			如果有，则将之前的登录信息给到现在的socket。
		*/
		do 
		{
			auto iter = userMap.find(s->user->userName);
			if (iter == userMap.end())
			{
				userMap.insert(UserMap::value_type(s->user->userName, s->user));
				break;
			}
			//将之前的账号信息指针给到现在的socket
			s->user = iter->second;
			//检查是否有在运行的chipic
			if (iter->second->threadIdMap.size() == 0)
				break;
			
			//将该账号上正在运行的chipic信息发送到客户端
			std::map<unsigned long, NetworkUser::ChipicData> &chipicDataMap = s->user->threadIdMap;

			for (auto i = chipicDataMap.begin(); i != chipicDataMap.end(); i++)
			{
				auto chipicData = i->second;

				std::string clientM3dPath = chipicData.clientPath + "/" + chipicData.m3dFileName;
				std::string msg = MessageTransition::creatChipicStartfinishedJsonMessage(
					clientM3dPath, chipicData.threadID, chipicData.threadCount, s->user->userName);
				s->sendJsonMessage(msg);
				/*
					也许有发文件的需求，后续再这里调用sendfile函数即可！
				*/
			}			
			
		} while (false);

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
	std::string cmd = "default", threadId,m3dPath;
	MessageTransition::getCmd(json, cmd);

	if (cmd != "startFinished")
		return false;

	MessageTransition::getThreadID(json, threadId);
	MessageTransition::getPath(json, m3dPath);
	unsigned long  id = std::stoul(threadId);



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

	//获取服务器路径,以用于匹配chipicData对象
	std::string servicFilePath;
	MessageTransition::getPath(json, servicFilePath);

	//将threadid 赋予socket 然后将消息发送出去
	(*i)->user->addThreadId(id,servicFilePath);

	//将消息中的路径替换为客户端的上的路径
	NetworkUser::ChipicData chipicData;
	if (!(*i)->user->getChipicDataForThreadID(std::stoul(threadId), chipicData))
	{
#ifdef MY_LOG
		std::cerr << "NetworkServer::startFinishedCmd get chipic data failed!" << std::endl;
#endif // MY_LOG
		return false;
	}
	neb::CJsonObject jsonObject(json);
	MessageTransition::setPath(jsonObject, chipicData.clientPath + "/" + chipicData.m3dFileName);
	(*i)->sendJsonMessage(jsonObject.ToString());
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

	auto socket = findSocketObjectForThreadID(threadId);
	if (!socket)
		return false;
	socket->sendJsonMessage(json);
}

/**
* @brief NetworkServer::disposeRunchipicMessage 处理客户端发来的启动消息
* @param const neb::CJsonObject & json
* @param const std::string & cmd
* @return bool ture 表示不做后续处理
*/
bool NetworkServer::disposeRunchipicMessage(const neb::CJsonObject& json, const std::string& cmd)
{
	if (cmd != "RunChipic")
		return false;
#if MY_LOG
	std::cerr << "NetworkServer::disposeRunchipicMessage ,"
		<< json.ToString() << std::endl;
#endif

	//获取带文件名的路径
	std::string filePath;
	MessageTransition::getPath(json, filePath);

	QFileInfo fileInfo(QString::fromLocal8Bit(filePath.c_str()));
	//获取带后缀的文件名
	QString m3dFileName = fileInfo.fileName();
	//获取不带后缀的文件名
	QString fileName = fileInfo.baseName();
	//获取不包含文件名的路径
	QString path = QString::fromLocal8Bit(filePath.c_str()).remove(m3dFileName);
	//去掉路径中的斜杠
	path = path.left(path.length() - 1);

	auto sender = getSocketSender();
	if (sender == nullptr)
	{
#ifdef MY_LOG
		std::cerr << "NetworkServer::disposeRunchipicMessage get sender is nullptr" << std::endl;
#endif // MY_LOG
		return false;
	}

	//拼接服务端的路径
	std::string userName = sender->user->userName;
	//不带文件名的服务端路径
	std::string servicePath = workPath + userName;
	//带文件名的服务端完整路径
	std::string serviceFilePath = servicePath + "/" + std::string(m3dFileName.toLocal8Bit());

	QDir dir;
	if (!dir.exists(QString::fromLocal8Bit(serviceFilePath.c_str())))
	{
#ifdef MY_LOG
		std::cerr << "NetworkServer::disposeRunchipicMessage service file path is not exists! path:"
			<< serviceFilePath << std::endl;
#endif // MY_LOG
		return true;
	}

	//获取线程数
	std::string temp;
	MessageTransition::getThreadCount(json, temp);
	int threadCount = std::stoi(temp);

	//根据信息构建一个chipic信息对象
	NetworkUser::ChipicData chipicData;
	chipicData.clientPath = path.toLocal8Bit();
	chipicData.fileName = fileName.toLocal8Bit();
	chipicData.m3dFileName = m3dFileName.toLocal8Bit();
	chipicData.servicePath = servicePath;
	chipicData.threadCount = threadCount;
	//将信息对象 放入list
	sender->user->chipicDataList.push_back(chipicData);

	//将json消息中的客户端路径 修改为服务端上的路径 然后将消息发送出去
	auto newJson = json;
	MessageTransition::setPath(newJson, serviceFilePath);
	//添加用户名
	MessageTransition::addUserName(newJson, sender->user->userName);

	auto messageSender = MessageSender::GetInstance();
	messageSender->sendJsonMessage(newJson.ToString());
	return true;
}

/**
* @brief NetworkServer::disposeM3dFileMessage 接收m3d文件
* @param NetworkSocket::SocketMessageBody & messageBody
* @return bool
*/
bool NetworkServer::disposeM3dFileMessage(NetworkSocket::SocketMessageBody& messageBody)
{
	neb::CJsonObject jsonObjcet(messageBody.json.data());

	std::string cmd;
	if (!MessageTransition::getCmd(jsonObjcet, cmd))
		return false;
	if (cmd != "m3dFile")
		return false;
	//获取文件名
	std::string fileName;
	if (!MessageTransition::getFileName(jsonObjcet, fileName))
	{
#ifdef MY_LOG
		std::cerr << "NetworkServer::diposeM3dFileMessage get file name failed!" << std::endl;
#endif // MY_LOG
		return false;
	}

	//获取发送信号的socket
	auto sender = getSocketSender();
	if (sender == nullptr)
	{
#ifdef MY_LOG
		std::cerr << "NetworkServer::diposeM3dFileMessage sender is nullptr!" << std::endl;
#endif // MY_LOG
		return false;
	}


#ifdef MY_LOG
	std::cerr << "NetworkServer::disposeM3dFileMessage ," <<
		jsonObjcet.ToString() << std::endl;
#endif

	//拼接路径
	std::string filePath = workPath + sender->user->userName;
	
	//检查路径是否存在 如果不存在 则创建
	QDir dir;
	if (!dir.exists(QString::fromLocal8Bit(filePath.c_str())))
		dir.mkpath(QString::fromLocal8Bit(filePath.c_str()));

	//写入文件
	File file;
	//如果文件索引为0 则将原来存在的文件删掉、新建一个文件
	int index = 1;
	auto ttt = jsonObjcet.ToString();
	MessageTransition::getIndex(jsonObjcet, index);
	if (index == 0)
	{
		File f;
		f.removeFile(filePath + "/" + fileName);
	}
	if (!file.openForAppend(filePath + "/" + fileName))
	{
#ifdef MY_LOG
		std::cerr << "NetworkServer::diposeM3dFileMessage sender open file failed! path:" 
			<< filePath << std::endl;
#endif // MY_LOG
		return false;
	}
	file.writeData(messageBody.data);
	return true;
}

/**
* @brief NetworkServer::disposeH5FileMessage 处理本地发来的h5文件消息 在发送文件回执命令前先将文件发往客户端
* @param const std::string & json
* @return bool
*/
bool NetworkServer::disposeH5FileMessage(const std::string& json)
{
	auto winMessage = MessageTransition::jsonToWinMessage(json);
	if (winMessage.threadId == 0)
		return false;
	//是否为结构图消息
	bool structBool = (winMessage.Msg == 208 && winMessage.wParam ==100 && winMessage.lParam == 0);
	//是否为结果图消息
	bool resultBool = (winMessage.Msg == 209 && winMessage.wParam != -1000 && winMessage.lParam != -1000);
	//是否为计算完成消息
	bool finished = (winMessage.Msg == 208 && winMessage.wParam == 200 && winMessage.lParam == 0);
	//如果不为以上类型 处理失败
	if (!(structBool || resultBool || finished))
		return false;

	//获取对应的socket对象
	auto socket = findSocketObjectForThreadID(winMessage.threadId);
	NetworkUser::ChipicData chipicData;
	if (!(socket->user->getChipicDataForThreadID(winMessage.threadId, chipicData)))
		return false;

	//拼接路径
	std::string clientFilePath, serviceFilePath;
	std::string typeName;
	//如果是传输计算结果那么文件名称和临时文件的名称不一样
	typeName = finished ? ".h5" : "_Temp.h5";
#ifdef MY_LOG
	std::cerr << "NetworkServer::disposeH5FileMessage ,"
		<< json << std::endl;
#endif

	if (chipicData.threadCount == 1)
	{
		serviceFilePath = chipicData.servicePath + "/" + chipicData.fileName + typeName;
		clientFilePath = chipicData.clientPath + "/" + chipicData.fileName + typeName;
		
	}else{
		serviceFilePath = chipicData.servicePath + "/1/" + chipicData.fileName + typeName;
		clientFilePath = chipicData.clientPath + "/1/" + chipicData.fileName + typeName;
	}

	QDir dir;
	if (!dir.exists(QString::fromLocal8Bit(serviceFilePath.c_str())))
	{
#ifdef MY_LOG
		std::cerr << "NetworkServer::disposeH5FileMessage service path not exists!path:"
			<< serviceFilePath << std::endl;
#endif // MY_LOG

		return false;
	}

	//发送文件
	this->sendFile(clientFilePath, serviceFilePath, socket);

	//如果为计算完成消息，则关闭chipic
	if (finished)
	{
		closeChipic(winMessage.threadId);
		return true;
	}

	//发送看图消息
	socket->sendJsonMessage(json);

	return true;
}


/**
* @brief NetworkServer::diposeChipicClose chipic关闭事件
* @param const std::string & json 消息 
* @return bool true 处理成功
*/
bool NetworkServer::diposeChipicClose(const std::string& json)
{
	/*
		服务器需要在listener被释放的时候
		将userData中的对应数据也释放掉。
		否则重新连接时，会将无效的user数据传输到客户端，导致第二次使用时出错。
	*/
	std::string cmd;
	MessageTransition::getCmd(json,cmd);
	if (cmd != "CloseChipic")
		return false;
#ifdef MY_LOG
	std::cerr << "NetworkServer::diposeChipicClose ," << json << std::endl;

#endif

	std::string temp;
	MessageTransition::getThreadID(json, temp);
	unsigned long threadID = std::stoul(temp);

	auto socket = findSocketObjectForThreadID(threadID);
	if (!socket)
		return false;
	socket->waitForWrite();
	socket->sendJsonMessage(json);
	

	for (auto i = userMap.begin(); i != userMap.end(); i++)
	{
		if (i->second->findThreadId(threadID))
		{
			i->second->removeThreadId(threadID);
			break;
		}
	}
	return true;
}

/**
* @brief NetworkServer::findSocketObjectForThreadID 通过线程id寻找可用的socket对象
* @param const unsigned long & threadID
* @return std::shared_ptr<NetworkSocket> 如果找不到 智能指针则为空
*/
std::shared_ptr<NetworkSocket> NetworkServer::findSocketObjectForThreadID(const unsigned long& threadID)
{
	auto i = socketList.begin();
	for (; i != socketList.end(); i++)
	{
		if ((*i)->user->findThreadId(threadID))
			break;
	}

	std::shared_ptr<NetworkSocket> socket;

	if (i != socketList.end())
	{
		socket = *i;
		return socket;
	}

#ifdef MY_LOG
	std::cerr << "NetworkServer::disposeLocalMessage get socket failed! threadId:"
		<< threadID << std::endl;
#endif // MY_LOG
	return socket;
}


/**
* @brief NetworkServer::sendFile 发送一个文件到客户端
* @param const std::string & targetPath 目标路径 发送到客户端上的什么路径
* @param const std::string & filePath 当前文件路径
* @param std::shared_ptr<NetworkSocket> socket 对应发送的socket
* @return void
*/
void NetworkServer::sendFile(const std::string& targetPath, const std::string& filePath, std::shared_ptr<NetworkSocket> socket)
{
	//向json中添加命令
	neb::CJsonObject jsonObject;
	MessageTransition::addCmd(jsonObject, "File");

	MessageTransition::addPath(jsonObject, targetPath);

	//分包发送文件
	File file;
	file.openForReadonly(filePath);
	QByteArray bytes;
	//包的索引
	int blockIndex = 0;
	MessageTransition::addIndex(jsonObject, blockIndex);
	while (file.readNextData(bytes))
	{
		if (!MessageTransition::setIndex(jsonObject, blockIndex))
		{
#ifdef MY_LOG
			std::cerr << "NetworkServer::disposeH5FileMessage ,set block index failde! json:"
				<< jsonObject.ToString() << std::endl;
#endif // MY_LOG
			return;
		}
		socket->sendMessage(jsonObject.ToString(), bytes);
		blockIndex++;
	}
}


/**
* @brief NetworkServer::closeChipic 关闭一个chipic
* @param const unsigned long & ID 
* @return void
*/
void NetworkServer::closeChipic(const unsigned long& ID)
{

	//创建一个关闭消息
	auto json = MessageTransition::creatCloseChipicJsonMessage(ID);
	//关闭正在运行的
	auto sender = MessageSender::GetInstance();
	sender->sendJsonMessage(json);
}
/**
* 这个消息主要是为了防止消息队列溢出，这种类型的消息在服务端就处理了
*/
bool NetworkServer::disposChipicPuse(const std::string& json)
{
	auto msg = MessageTransition::jsonToWinMessage(json);
	if (msg.Msg != 250 || msg.wParam != 1)
		return false;
	
	Message m;
	m.threadId = msg.threadId;
	m.Msg = 150;
	m.wParam = 0;
	m.lParam = 0;
	auto j = MessageTransition::winMessageTojson(m);
	MessageSender::GetInstance()->sendJsonMessage(j);

	return true;
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
	//设置当networksocket被释放的时候不释放socketzhizhen
	networkSocket->setDeleteSocket(false);
	networkSocket->setSocket(socket);
	
	/*
		这里增加一个定时器，定时发送空白包。
		原因是因为遇到一个解决不了的问题。
		即在某些情况下，调用socket.write()不会立即将消息发送出去。可能会等上好几分钟再发出去，或者
		干脆一直不发出去，直到调用第二次write，跟随第二条消息一起发出去。
		所以这里发送空白包，如果前面有未发送出去的包，将之一起发送出去。
	*/
	networkSocket->startTimer(2000);

	socketList.push_back(networkSocket);
	//链接接受消息槽
	connect(networkSocket.get(), SIGNAL(receiveMessageFinished(NetworkSocket::SocketMessageBody)), this, SLOT(receiveMessageFinished(NetworkSocket::SocketMessageBody)));
	connect(networkSocket.get(), SIGNAL(disconnect()), this, SLOT(socketDisconnect()));
#ifdef MY_LOG
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
	if (disposeM3dFileMessage(msgBody))
		return ;
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
	if (disposChipicPuse(json))
		return;
	//处理hdf5文件消息
	if(disposeH5FileMessage(json))
		return;
	if (diposeChipicClose(json))
		return;
	if (disposeLocalMessage(json))
		return;
}

/**
* @brief NetworkServer::socketDisconnect socket断开槽
* @return void
*/
void NetworkServer::socketDisconnect()
{
	//获取发送信号的对象
	auto sender = this->sender();
	auto networkSocket = dynamic_cast<NetworkSocket *>(sender);

	if (!networkSocket)
		return;

	//遍历所有的socket 找到对应的socket 然后释放掉
	for (auto i = socketList.begin(); i != socketList.end();i++)
	{
		if ((*i).get() == networkSocket)
		{
			socketList.erase(i);
			return;
		}
	}

}

void NetworkServer::sendCloseChipicMessage(const unsigned long& threaID)
{
	auto j = MessageTransition::creatCloseChipicJsonMessage(threaID);
	JsonMessageGetter::GetInstance()->addJsonMessage(j);
}

#include "moc_NetworkServer.cpp"
