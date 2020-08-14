#pragma  once
#include <memory>
#include <mutex>
#include <QObject>
#include <list>
#include "NetworkSocket.h"
#include "CJsonObject.hpp"
class QTcpServer;
class QTcpSocket;
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
	//处理cmd消息
	bool disposeCmdMessage(const std::string& json);
	//处理登录消息
	bool disposeLoginMessage(const neb::CJsonObject& json,const std::string& cmd);
	//处理注册消息
	bool disposeRegisterMessage(const neb::CJsonObject& json, const std::string& cmd);
	//获取当前发送信号的socket指针
	NetworkSocket *getSocketSender();
	//处理本地发来的startFini命令
	bool startFinishedCmd(const std::string& json);
	//处理本地消息
	bool disposeLocalMessage(const std::string& json);
	//处理runchipic消息
	bool disposeRunchipicMessage(const neb::CJsonObject& json, const std::string& cmd);
	//处m3dfile消息
	bool disposeM3dFileMessage(NetworkSocket::SocketMessageBody& messageBody);
private:
	std::list<ConnectSocket> listConnectSocket;

public slots:
	//新的连接
	void serverNewConnection();
	//接受socket到消息
	void receiveMessageFinished(NetworkSocket::SocketMessageBody msgBody);
	//有本地游戏
	void hasLocalMessage();
};