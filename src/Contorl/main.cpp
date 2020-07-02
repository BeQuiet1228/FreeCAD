#include "Contorl.h"
#include <qwidget.h>
#include "MessageTransition.h"
#include "LonelinessMode.h"
int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	Contorl w;
	w.show();
	
	Message msg;
	msg.threadId = 1;
	msg.Msg = 2;
	msg.wParam = 3;
	msg.lParam = 4;
	msg.text = "≤‚ ‘";
	std::string json = MessageTransition::winMessageTojson(msg);
	std::cerr << json;

	msg = MessageTransition::jsonToWinMessage(json);
	std::cerr << "cc";

	return a.exec();
}
