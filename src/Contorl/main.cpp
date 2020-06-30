#include "Contorl.h"
#include <qwidget.h>

int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	Contorl w;
	w.show();
	return a.exec();
}
