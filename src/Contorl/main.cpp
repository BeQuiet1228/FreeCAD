#include "Contorl.h"
#include <qwidget.h>
#include "MessageTransition.h"
#include "LonelinessMode.h"
#include "ContorlDataBar.h"
#include "ContorlButtonBar.h"
#include "ContorlInterface.h"
#include "NetworkClient.h"
#include "NetworkServer.h"
#include "LocalEimtter.h"
#include "MessageSender.h"
#include "NetworkClientLoginDailog.h"
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
	server->startListene();

	auto client = NetworkClient::GetInstance();
	client->startConnect();

	//auto sender = MessageSender::GetInstance();
	//LocalEmitter *emiter = new LocalEmitter;
	//sender->setEmitter(emiter);

	//NetworkClientDialog d;
	//d.show();

	return a.exec();
}
