#include <qwidget.h>
#include <QApplication>
#include "SmartContorlUI.h"
int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	SmartContorlUI ui;
	ui.show();

	return a.exec();
}
