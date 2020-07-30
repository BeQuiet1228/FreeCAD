#include <qwidget.h>
#include <QApplication>
#include <iostream>
#include "Line.h"
int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	QWidget w;
	w.show();

	Line line;

	line.point1.setValue("2mm", "3mm", "4mm");
	line.point2.setName("textPint");
	line.setName("testLine");
	line.markGrid.setValue("DX1", "DX2", "DX3");

	std::cerr << line.toCommand();
	return a.exec();
}
