#include "NetworkEmitter.h"
#include "NetworkClient.h"
NetworkEmitter::NetworkEmitter()
{
	auto client = NetworkClient::GetInstance();

	client->startConnect();
}

NetworkEmitter::~NetworkEmitter()
{

}

void NetworkEmitter::sendMessage(const std::string& json)
{
	auto client = NetworkClient::GetInstance();
	client->sendJonsMessage(json);
}

