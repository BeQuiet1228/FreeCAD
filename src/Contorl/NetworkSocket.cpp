#include "NetworkSocket.h"
#include <QTcpSocket>
#include <iostream>
NetworkSocket::NetworkSocket()
{

}

NetworkSocket::~NetworkSocket()
{
	if (socket != nullptr)
		delete socket;
}

/**
* @brief NetworkSocket::setSocket 设置socket 并绑定接收信息槽
* @param QTcpSocket * tcpSocket
* @return void
*/
void NetworkSocket::setSocket(QTcpSocket * tcpSocket)
{
	this->socket = tcpSocket;
	connect(socket, SIGNAL(readyRead()), this, SLOT(readReady()));
}

/**
* @brief NetworkSocket::sendMessage 发送tcp消息
* @param const std::string & json json段
* @param const QByteArray & byteArray 其他信息段
* @return bool 成功返回true
*/
bool NetworkSocket::sendMessage(const std::string& json, const QByteArray& byteArray)
{
	if (socket == nullptr)
		return false;
	
	//发送包头
	socketWriteIsSuccess(socket->write(BLOCK_HEADE));
	//发送json消息
	socketWriteIsSuccess(socket->write(json.c_str()));
	//发送分割
	socketWriteIsSuccess(socket->write(BLOCK_SPECE));
	//发送其他信息段
	socketWriteIsSuccess(socket->write(byteArray.data()));
	//发送包尾
	socketWriteIsSuccess(socket->write(BLOCK_END));
}

void NetworkSocket::socketWriteIsSuccess(const int& ok)
{
#ifdef MY_DEBUG
	if (!ok)
		std::cerr << "socket write failed!" << std::endl;
#endif // MY_DEBUG

}

void NetworkSocket::readReady()
{

}

