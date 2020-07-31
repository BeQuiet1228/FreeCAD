#pragma once
#include <QObject>
#include <QByteArray>
class QTcpSocket;
class NetworkSocket:public QObject
{
	Q_OBJECT
public:
	NetworkSocket();
	~NetworkSocket();

private:
	//socket指针
	QTcpSocket *socket  = nullptr;
	//tcp包头
	const char BLOCK_HEADE[5] = {0x55,0x54,0x53,0x52,0x51};
	//tcp包分割段
	const char BLOCK_SPECE[5] = { 0x35, 0x36, 0x37, 0x38, 0x39 };
	//tcp包尾
	const char BLOCK_END[5] = { 0x45, 0x46, 0x47, 0x48, 0x49};
public:
	//设置qtcpsocket
	void setSocket(QTcpSocket *tcpSocket);
	//发送json消息
	bool sendMessage(const std::string& json, const QByteArray& byteArray);

private:
	void socketWriteIsSuccess(const int& ok);
public slots :
	void readReady();
};