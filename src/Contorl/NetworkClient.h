#pragma once
#include <memory>
#include <mutex>
#include <QObject>
class QTcpSocket;
class NetworkSocket;
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
	
	std::shared_ptr<NetworkSocket> socket;
	
public:
	//获取监听地址
	QString getListeneAddress();
	//获取监听端口
	int getListenePort();
	//开始监听
	void startConnect();
	//设置监听地址及端口
	void setAddressAndPort(const QString& address, const int& prot);
	//客户端的连接状态
	bool isConnect();

};