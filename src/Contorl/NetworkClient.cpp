#include "NetworkClient.h"
#include <QTcpSocket>

std::shared_ptr<NetworkClient> NetworkClient::_instance;

NetworkClient::~NetworkClient()
{
	delete socket;
}

NetworkClient::NetworkClient()
{
	socket = new QTcpSocket;
}

#include "moc_NetworkClient.cpp"
