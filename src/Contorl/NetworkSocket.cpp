#include "NetworkSocket.h"
#include <QTcpSocket>
#include <iostream>
NetworkSocket::NetworkSocket()
{
	//tcp包头
	BLOCK_HEADE.append(0x55);
	BLOCK_HEADE.append(0x54);
	BLOCK_HEADE.append(0x53);
	BLOCK_HEADE.append(0x52);
	BLOCK_HEADE.append(0x51);
	//tcp包分割段
	BLOCK_SPECE.append(0x35);
	BLOCK_SPECE.append(0x36);
	BLOCK_SPECE.append(0x37);
	BLOCK_SPECE.append(0x38);
	BLOCK_SPECE.append(0x39);
	//tcp包尾
	BLOCK_END.append(0x21);
	BLOCK_END.append(0x22);
	BLOCK_END.append(0x23);
	BLOCK_END.append(0x24);
	BLOCK_END.append(0x25);
}

NetworkSocket::~NetworkSocket()
{
	if (socket != nullptr)
		delete socket;
}

/**
* @brief NetworkSocket::setSocket 设置socket 并绑定接收信息槽
* @param QTcpSocket * tcpSocket
* @return void
*/
void NetworkSocket::setSocket(QTcpSocket * tcpSocket)
{
	this->socket = tcpSocket;
	connect(socket, SIGNAL(readyRead()), this, SLOT(readReady()));
}

/**
* @brief NetworkSocket::sendMessage 发送tcp消息
* @param const std::string & json json段
* @param const QByteArray & byteArray 其他信息段
* @return bool 成功返回true
*/
bool NetworkSocket::sendMessage(const std::string& json, const QByteArray& byteArray)
{
	if (socket == nullptr)
		return false;
	
	//发送包头
	socketWriteIsSuccess(socket->write(BLOCK_HEADE));
	//发送json消息
	socketWriteIsSuccess(socket->write(json.c_str()));
	//发送分割
	socketWriteIsSuccess(socket->write(BLOCK_SPECE));
	//发送其他信息段
	socketWriteIsSuccess(socket->write(byteArray));
	//发送包尾
	socketWriteIsSuccess(socket->write(BLOCK_END));
}

/**
* @brief NetworkSocket::analysisBlock 解析一个块的信息
* @param const QByteArray & block
* @return void
*/
void NetworkSocket::analysisBlock(const QByteArray& block)
{
	if (block.indexOf(BLOCK_SPECE) >= 0)
	{
		auto list = byteArraySplit(block, BLOCK_SPECE);
		messageBody.state = JSON;
		addMessageBodyData(list.at(0));
		messageBody.state = DATA;
		addMessageBodyData(list.at(1));
	}else{
		addMessageBodyData(block);
	}

}

/**
* @brief NetworkSocket::addMessageBodyData 将数据放入消息体
* @param const QByteArray & data
* @return void
*/
void NetworkSocket::addMessageBodyData(const QByteArray& data)
{

	std::cerr << QString(data.toHex()).toStdString() << std::endl;

	int index = 0;
	switch (messageBody.state)
	{
	case DATA:
		//检测是否有包尾  如果有表示一个包接收完，则将包处理并将清空当前包
		index = data.indexOf(BLOCK_END);
		if (index >= 0)
		{
			auto temp = data.left(index);
			messageBody.data += temp;
			receiveOneMessageFinished(messageBody);
			messageBody.state = JSON;
			messageBody.data.clear();
			messageBody.json.clear();
			break;
		}
		messageBody.data += data;
		break;
	case JSON:
		messageBody.json += data;
		break;
	default:
		break;
	}
}

/**
* @brief NetworkSocket::receiveOneMessageFinished 完成一个包的接收
* @param const SocketMessageBody & msgBody
* @return void
*/
void NetworkSocket::receiveOneMessageFinished(const SocketMessageBody& msgBody)
{
#ifdef MY_DEBUG
	std::cerr << QString(msgBody.json).toStdString() << std::endl;
#endif // MY_DEBUG

}

/**
* @brief NetworkSocket::usable 判断连接是否可用
* @return bool
*/
bool NetworkSocket::usable()
{
	return socket->isOpen();
}

/**
* @brief NetworkSocket::socketWriteIsSuccess 判断ok的值 然后打印写入结果
* @param const int & ok
* @return void
*/
void NetworkSocket::socketWriteIsSuccess(const int& ok)
{
#ifdef MY_DEBUG
	if (!ok)
		std::cerr << "socket write failed!" << std::endl;
#endif // MY_DEBUG

}

/**
* @brief NetworkSocket::byteArraySplit 使用bytearray切割bytearray
* @param const QByteArray & byteArray 元数据
* @param const QByteArray & split 切割符
* @return QList<QByteArray>
*/
QList<QByteArray> NetworkSocket::byteArraySplit(const QByteArray& byteArray, const QByteArray& split)
{
	QList<QByteArray> byteArrayList;
	auto temp = byteArray;

	for (int index = temp.indexOf(split); index >= 0; index = temp.indexOf(split))
	{
		if (index == 0)
		{
			temp = temp.right(temp.length() - split.length());
		}else{
			auto t = temp.left(index );
			temp = temp.right(temp.length() - split.length() - (index ));
			byteArrayList.append(t);
		}
	}

	byteArrayList.append(temp);
	return byteArrayList;
}

void NetworkSocket::readReady()
{	
	QByteArray array = socket->readAll();
	auto list = byteArraySplit(array, BLOCK_HEADE);
	
	for (auto i = list.begin(); i != list.end(); i++)
	{
		this->analysisBlock(*i);
	}
}

#include "moc_NetworkSocket.cpp"
