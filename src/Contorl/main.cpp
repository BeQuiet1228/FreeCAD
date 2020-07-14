#include "Contorl.h"
#include <qwidget.h>
#include "MessageTransition.h"
#include "LonelinessMode.h"
#include "ContorlDataBar.h"
#include "ContorlButtonBar.h"
#include "ContorlInterface.h"
int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	Contorl w;
	w.contorlButtonBar.show();
	w.contorlDataBar.show();
	ContorlInterface in;
	return a.exec();
}
