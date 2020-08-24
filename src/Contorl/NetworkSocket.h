#pragma once
#include <QObject>
#include <QByteArray>
#include <QList>
#include <memory>
class QTcpSocket;
class NetworkUser;
class NetworkSocket:public QObject
{
	Q_OBJECT
public:
	enum SocketMessageBodyState{
		HEAD = 0,	//等待接收消息头
		JSON,		//等待接收json消息
		DATA		//等待接收其他消息
	};
	struct SocketMessageBody
	{
		SocketMessageBody(){
			state = JSON;
		}
		//消息体状态
		SocketMessageBodyState state;
		//json
		QByteArray json;
		//其他信息
		QByteArray data;
	};
public:
	NetworkSocket();
	~NetworkSocket();

private:
	//socket指针
	QTcpSocket *socket  = nullptr;
	//tcp包头
	QByteArray BLOCK_HEADE;
	//tcp包分割段
	QByteArray BLOCK_SPECE;
	//tcp包尾
	QByteArray BLOCK_END;
	//接收socket消息体
	SocketMessageBody messageBody;
	//socket是否已连接
	bool socktetIsConnect = false;
public:
	//账号
	std::shared_ptr<NetworkUser> user;
public:
	//设置qtcpsocket
	void setSocket(QTcpSocket *tcpSocket);
	//发送消息
	bool sendMessage(const std::string& json, const QByteArray& byteArray);
	//发送json消息
	bool sendJsonMessage(const std::string& json);
	//解析一个消息块
	void analysisBlock(const QByteArray& block);
	//将数据放入消息体中
	void addMessageBodyData(const QByteArray& data);
	//接收完成一个消息
	void receiveOneMessageFinished(const SocketMessageBody& msgBody);
	//判断连接是否可用
	bool usable();
	//连接socket服务端
	bool socketConnect(const QString& ip, const QString& port);
private:
	//
	void socketWriteIsSuccess(const int& ok);
	//切割字符数组
	QList<QByteArray> byteArraySplit(const QByteArray& byteArray,const QByteArray& split);
public slots :
	void readReady();
	void socketDisconnect();
Q_SIGNALS:
	void receiveMessageFinished(NetworkSocket::SocketMessageBody);
};