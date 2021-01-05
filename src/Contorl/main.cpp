#include "Contorl.h"
#include <qwidget.h>
#include "MessageTransition.h"
#include "ContorlDataBar.h"
#include "ContorlButtonBar.h"
#include "ContorlInterface.h"
#include "NetworkClient.h"
#include "NetworkServer.h"
#include "LocalEimtter.h"
#include "MessageSender.h"
#include "NetworkClientLoginDailog.h"
#include "ServiceUI.h"
int main(int argc, char *argv[])
{
	QApplication a(argc, argv);

#ifdef SERVICE
	ServiceUI qw;
	qw.show();


	auto sender = MessageSender::GetInstance();
	LocalEmitter *emiter = new LocalEmitter;
	sender->setEmitter(emiter);

#else

	Contorl w;
	w.contorlButtonBar->show();
	w.contorlDataBar->show();
	auto contorl = ContorlInterface::GetInstance();


#endif // SERVICE


	return a.exec();
}
