#include "NetworkEmitter.h"
#include "NetworkClient.h"
NetworkEmitter::NetworkEmitter()
{

}

NetworkEmitter::~NetworkEmitter()
{

}

void NetworkEmitter::sendMessage(const std::string& json)
{
	auto client = NetworkClient::GetInstance();
	client->sendJonsMessage(json);
}

/**
* @brief NetworkEmitter::getEmitterId »ñÈ¡·¢ÉäÆ÷id
* @return int
*/
int NetworkEmitter::getEmitterId()
{
	return 2;
}

