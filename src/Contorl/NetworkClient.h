#pragma once
#include <memory>
#include <mutex>
#include <QObject>
#include "NetworkSocket.h"
#include "CJsonObject.hpp"
class QTcpSocket;
class NetworkClientDialog;
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
	//登录提示框
	std::shared_ptr<NetworkClientDialog> loginDialog;
	//当前登录账户的用户名
	std::string userName;
public:
	//获取监听地址
	static QString getListeneAddress();
	//获取监听端口
	static int getListenePort();
	//设置监听地址及端口
	static void setAddressAndPort(const QString& address, const int& prot);
	//开始监听
	void startConnect();
	//客户端的连接状态
	bool isConnect();
	//客户端是否可用
	bool usable();
	//发送json消息
	void sendJonsMessage(const std::string json);
	//显示登录窗口
	void showLocginDialog();
public:
	//客户端是否已经登录
	bool login;
private:
	//处理消息
	bool disposeCmdMessage(NetworkSocket::SocketMessageBody messageBody);
	//处理登录消息
	void disposeLoginMessage(const neb::CJsonObject jsonObject);
	//处理注册消息
	void disposeRegisterMessage(const neb::CJsonObject jsonObject);
	//处理服务器发来得文件消息
	bool disposeFileMessage(NetworkSocket::SocketMessageBody messageBody);
	//显示提示框
	void showMessageBox(std::string tr);
	//发送m3d文件
	void sendM3dFile(const std::string& path);
public Q_SLOTS:
	void receiveMessageFinished(NetworkSocket::SocketMessageBody messageBody);
	//登录提示框按钮被点击
	void loginDialogButtonClicked();
	//与服务器连接断开
	void serviceClose();
};