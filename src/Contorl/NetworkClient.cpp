#include "NetworkClient.h"
#include <QTcpSocket>
#include <QSettings>
#include <QHostAddress>
#include "NetworkSocket.h"
#include "iostream"
#include "JsonMessageGetter.h"
#include "CJsonObject.hpp"
#include "NetworkClientLoginDailog.h"
#include "MessageTransition.h"
#include <QMessageBox>
#include "NetworkUser.h"
std::shared_ptr<NetworkClient> NetworkClient::_instance;

NetworkClient::~NetworkClient()
{
}

NetworkClient::NetworkClient()
{
	//初始化socket
	socket.reset(new NetworkSocket);
	//链接消息收槽
	connect(socket.get(), SIGNAL(receiveMessageFinished(NetworkSocket::SocketMessageBody)), this, SLOT(receiveMessageFinished(NetworkSocket::SocketMessageBody)));
	//初始化提示框
	loginDialog.reset(new NetworkClientDialog);
	loginDialog->setIpAndPort(getListeneAddress(),QString::number( getListenePort()));
	connect(loginDialog.get(), SIGNAL(pushButtonClicked()), this, SLOT(loginDialogButtonClicked()));
	//初始化登录状态
	login = false;
}


/**
* @brief NetworkClient::getListeneAddress 从注册表获取已设置的连接地址
* @return QString
*/
QString NetworkClient::getListeneAddress()
{
	QSettings setting("PICGUI", "NetworkClientConfig");

	QString address = setting.value("address", "default").toString();

	if (address == "default")
		address = "127.0.0.1";

	return address;
}

/**
* @brief NetworkClient::getListenePort 从注册表获取监听地址
* @return int
*/
int NetworkClient::getListenePort()
{
	QSettings setting("PICGUI", "NetworkClientConfig");

	int port = setting.value("port", 0).toInt();

	if (port == 0)
		port = 8866;

	return port;
}

/**
* @brief NetworkClient::startConnect 从配置中获取端口跟地址 开始连接
* @return void
*/
void NetworkClient::startConnect()
{
	auto s = new QTcpSocket;
	s->connectToHost(QHostAddress(getListeneAddress()), getListenePort());
	socket->setSocket(s);

	loginDialog->show();
}

/**
* @brief NetworkClient::setAddressAndPort 设置连接端口跟地址，内容将保存到注册表
* @param const QString & address
* @param const int & prot
* @return void
*/
void NetworkClient::setAddressAndPort(const QString& address, const int& prot)
{
	QSettings setting("PICGUI", "NetworkClientConfig");

	setting.setValue("address", address);
	setting.setValue("port", prot);
}

/**
* @brief NetworkClient::isConnect
* @return bool 连接成功返回true
*/
bool NetworkClient::isConnect()
{
	return socket->usable();
}

bool NetworkClient::usable()
{
	return false;
}

/**
* @brief NetworkClient::sendJonsMessage 发送json消息
* @param const std::string json
* @return void
*/
void NetworkClient::sendJonsMessage(const std::string json)
{

	/*
		由于服务端需要给多个账户提供服务,所以在发送运行chipic的命令时需要在命令
		中加上用户名,用于返回启动成功时,寻找对应的用户名的socket.
		其他消息不用加用户名时因为可以用threadId来区分.
	*/

	//获取消息中的命令,判断是是不是RunChipic命令
	neb::CJsonObject jsonObject(json);
	std::string cmd;
	if (MessageTransition::getCmd(jsonObject, cmd))
	{
		//如果是启动命令 则加上一个用户名
		if (cmd == "RunChipic")
		{
			MessageTransition::addUserName(jsonObject, this->userName);
		}
	}

	//如果客户端处于未登录状态,则不能发送除了登录和注册以外的信息
	if (cmd != "login" && cmd != "register" && login)
	{
		showMessageBox("未连接到服务端或者未登录,无法进行当前操作!");
		return;
	}

	socket->sendMessage(json, "  ");
}

/**
* @brief NetworkClient::showLocginDialog
* @return void
*/
void NetworkClient::showLocginDialog()
{
	loginDialog->show();
}
/**
* @brief NetworkClient::disposeCmdMessage 处理消息
* @param NetworkSocket::SocketMessageBody messageBody
* @return bool 消息已被处理,无需其他操作
*/
bool NetworkClient::disposeCmdMessage(NetworkSocket::SocketMessageBody messageBody)
{
	neb::CJsonObject json(messageBody.json.data());
	std::string temp;
	if (!MessageTransition::getCmd(json, temp))
		return false;
	if (temp == "login")
	{
		disposeLoginMessage(json);
		return true;
	}else if (temp == "register"){
		disposeRegisterMessage(json);
		return true;
	}

	return false;
}


/**
* @brief NetworkClient::disposeLoginMessage 处理登录命令消息
* @param const neb::CJsonObject jsonObject
* @return void
*/
void NetworkClient::disposeLoginMessage(const neb::CJsonObject jsonObject)
{
	//获取消息中得错误代码
	std::string errorCode;
	if (!MessageTransition::getErrorCOde(jsonObject, errorCode))
	{
#ifdef MY_LOG
		std::cerr << "NetworkClient::disposeLoginMessage get error code failed!" <<std::endl;
#endif // MY_LOG
		return;
	}

	int code = std::stoi(errorCode);
	if (code == 0)
	{
		showMessageBox("登录成功!");
		login = true;
		loginDialog->close();
	}else{
		showMessageBox("登录失败,请检车用户名与密码是否正确!");
	}

}

/**
* @brief NetworkClient::disposeRegisterMessage 处理注册命令消息
* @param const neb::CJsonObject jsonObject
* @return void
*/
void NetworkClient::disposeRegisterMessage(const neb::CJsonObject jsonObject)
{
	//获取消息中得错误代码
	std::string errorCode;
	if (!MessageTransition::getErrorCOde(jsonObject, errorCode))
	{
#ifdef MY_LOG
		std::cerr << "NetworkClient::disposeLoginMessage get error code failed!" << std::endl;
#endif // MY_LOG
		return;
	}
	int code = std::stoi(errorCode);

	switch (NetworkUser::ErrorCode(code))
	{
	case NetworkUser::NOT_ERROR:
		showMessageBox("注册成功,并已自动登录!");
		login = true;
		break;
	case NetworkUser::DEFAULT_PASSWORD:
		showMessageBox("不能使用默认密码!");
		break;
	case NetworkUser::NAME_EXIST:
		showMessageBox("用户名已存在");
		break;
	default:
		break;
	}
}

/**
* @brief NetworkClient::showMessageBox 显示提示框 且阻塞
* @param std::string tr
* @return void
*/
void NetworkClient::showMessageBox(std::string tr)
{
	QMessageBox box;
	box.setWindowTitle(QString::fromLocal8Bit("提示框:"));
	box.setText(QString::fromLocal8Bit(tr.c_str()));
	box.exec();
}

void NetworkClient::receiveMessageFinished(NetworkSocket::SocketMessageBody messageBody)
{
	if (disposeCmdMessage(messageBody))
		return;
	auto msgGetter = JsonMessageGetter::GetInstance();
	msgGetter->addJsonMessage(messageBody.json.data());
}

/**
* @brief NetworkClient::loginDialogButtonClicked 登录窗口确认槽
* @return void 
*/
void NetworkClient::loginDialogButtonClicked()
{
	if (loginDialog->state == NetworkClientDialog::LOGIN)
	{
		//如果窗口为登录状态则发送登录消息
		QString userName,password;
		loginDialog->getUserNameAndPassword(userName, password);

		std::string json = MessageTransition::creatLoginCmd(userName.toStdString(), password.toStdString());
		socket->sendJsonMessage(json);
	}else if (loginDialog->state == NetworkClientDialog::REGISTER){
		//如果为注册状态 则发送注册信息
		QString userName, password1, password2;
		loginDialog->getUserNameAndPassword(userName, password1, password2);
		//如果两次输入密码不一致,则提醒用户重新输入
		if (password2 != password1)
		{
			showMessageBox("两次输入密码不一致,请重新输入");
			return;
		}
		//发送注册消息
		std::string json = MessageTransition::creatRegisterCmd(userName.toStdString(), password1.toStdString());
		socket->sendJsonMessage(json);
	}
}

#include "moc_NetworkClient.cpp"
