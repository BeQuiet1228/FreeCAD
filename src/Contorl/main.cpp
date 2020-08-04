#include "Contorl.h"
#include <qwidget.h>
#include "MessageTransition.h"
#include "LonelinessMode.h"
#include "ContorlDataBar.h"
#include "ContorlButtonBar.h"
#include "ContorlInterface.h"
#include "NetworkClient.h"
#include "NetworkServer.h"
int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	//Contorl w;
	//w.contorlButtonBar->show();
	//w.contorlDataBar->show();
	//auto contorl = ContorlInterface::GetInstance();

	QWidget w;
	w.show();

	auto server = NetworkServer::GetInstance();
	auto client = NetworkClient::GetInstance();
	server->startListene();
	client->startConnect();

	return a.exec();
}
