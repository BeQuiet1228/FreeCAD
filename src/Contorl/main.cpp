#include "Contorl.h"
#include <qwidget.h>
#include "MessageTransition.h"
#include "LonelinessMode.h"
#include "ContorlDataBar.h"
#include "ContorlButtonBar.h"
int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	Contorl w;
	w.show();
	return a.exec();
}
