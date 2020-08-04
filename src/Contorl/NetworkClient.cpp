#include "NetworkClient.h"
#include <QTcpSocket>
#include <QSettings>
#include <QHostAddress>
#include "NetworkSocket.h"
#include "iostream"
std::shared_ptr<NetworkClient> NetworkClient::_instance;

NetworkClient::~NetworkClient()
{
}

NetworkClient::NetworkClient()
{
	socket.reset(new NetworkSocket);
}


/**
* @brief NetworkClient::getListeneAddress 从注册表获取已设置的连接地址
* @return QString
*/
QString NetworkClient::getListeneAddress()
{
	QSettings setting("PICGUI", "NetworkClientConfig");

	QString address = setting.value("address", "default").toString();

	if (address == "default")
		address = "127.0.0.1";

	return address;
}

/**
* @brief NetworkClient::getListenePort 从注册表获取监听地址
* @return int
*/
int NetworkClient::getListenePort()
{
	QSettings setting("PICGUI", "NetworkClientConfig");

	int port = setting.value("port", 0).toInt();

	if (port == 0)
		port = 8866;

	return port;
}

/**
* @brief NetworkClient::startConnect 从配置中获取端口跟地址 开始连接
* @return void
*/
void NetworkClient::startConnect()
{
	auto s = new QTcpSocket;
	s->connectToHost(QHostAddress(getListeneAddress()), getListenePort());
	socket->setSocket(s);

}

/**
* @brief NetworkClient::setAddressAndPort 设置连接端口跟地址，内容将保存到注册表
* @param const QString & address
* @param const int & prot
* @return void
*/
void NetworkClient::setAddressAndPort(const QString& address, const int& prot)
{
	QSettings setting("PICGUI", "NetworkClientConfig");

	setting.setValue("address", address);
	setting.setValue("port", prot);
}

/**
* @brief NetworkClient::isConnect
* @return bool 连接成功返回true
*/
bool NetworkClient::isConnect()
{
	return socket->usable();
}

#include "moc_NetworkClient.cpp"
