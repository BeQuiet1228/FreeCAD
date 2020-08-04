#include "NetworkServer.h"
#include <QTcpServer>
#include <qsettings.h>
#include <QTcpSocket>
#include <iostream>
#include "NetworkSocket.h"
std::shared_ptr<NetworkServer> NetworkServer::_instance;

NetworkServer::~NetworkServer()
{
}

NetworkServer::NetworkServer()
{
	server.reset(new QTcpServer);

	connect(server.get(), SIGNAL(newConnection()), this, SLOT(serverNewConnection()));
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
* @brief NetworkServer::serverNewConnection tcp服务器有新的链接槽
* @return void
*/
void NetworkServer::serverNewConnection()
{
	auto socket = server->nextPendingConnection();

	std::shared_ptr<NetworkSocket> networkSocket(new NetworkSocket);
	networkSocket->setSocket(socket);
	socketList.push_back(networkSocket);
	networkSocket->sendMessage("你好啊！"," ");
#ifdef MY_DEBUG
	std::cerr << "NetworkServer::serverNewConnection()，address:"
		<< socket->peerAddress().toString().toStdString()
		<< ",port:" << socket->peerPort() << std::endl;
#endif // MY_DEBUG

}


#include "moc_NetworkServer.cpp"
