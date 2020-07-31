#pragma once
#include <memory>
#include <mutex>
#include <QObject>
class QTcpSocket;
class NetworkClient:public QObject
{
	Q_OBJECT
private:
	NetworkClient();
public:
	~NetworkClient();
	NetworkClient(const NetworkClient&) = delete;
	NetworkClient operator = (const NetworkClient&) = delete;

	static std::shared_ptr<NetworkClient>  GetInstance(){
		static std::once_flag flag;
		std::call_once(flag, [&](){
			_instance.reset(new NetworkClient);
		});

		return _instance;
	}

private:
	static std::shared_ptr<NetworkClient> _instance;
	
	QTcpSocket *socket;

};