#include <qwidget.h>
#include <QApplication>
#include "SmartContorlUI.h"
#include "FileMaker.h"
#include "qcustomplot.h"
int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	SmartContorlUI ui;
	ui.show();
	return a.exec();
}
