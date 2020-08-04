#pragma  once
#include <memory>
#include <mutex>
#include <QObject>
#include <list>
class QTcpServer;
class QTcpSocket;
class NetworkSocket;
using NetworkSocketList = std::list<std::shared_ptr<NetworkSocket>>;
class NetworkServer:public QObject
{
	Q_OBJECT
private:
	NetworkServer();
public:
	~NetworkServer();
	NetworkServer(const NetworkServer&) = delete;
	NetworkServer operator=(const NetworkServer&) = delete;

	static std::shared_ptr<NetworkServer> GetInstance(){
		static std::once_flag flag;
		std::call_once(flag, [&](){
			_instance.reset(new NetworkServer);
		});

		return _instance;
	}

private:
	static std::shared_ptr<NetworkServer> _instance;
	//tcp服务端
	std::shared_ptr<QTcpServer> server;
	//已连接的socket
	NetworkSocketList socketList;
public:
	struct ConnectSocket{
		QTcpSocket * socket;
		QString userName, password;
		bool usable = false;
	};
public:
	//获取监听地址
	QString getListeneAddress();
	//获取监听端口
	int getListenePort();
	//开始监听
	void startListene();
	//设置监听地址及端口
	void setAddressAndPort(const QString& address, const int& prot);
private:
	std::list<ConnectSocket> listConnectSocket;

public slots:
	//新的连接
	void serverNewConnection();
};