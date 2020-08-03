#include <qwidget.h>
#include <QApplication>
#include <iostream>
#include "Line.h"
#include "Point.h"
#include "VolPyramid.h"
int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	QWidget w;
	w.show();

	VolPyramid line;

	line.point1.setValue("2mm", "1mm", "0mm");
	line.point2.setValue("2mm", "1mm", "0mm");
	line.point3.setValue("2mm", "1mm", "0mm");
	line.point4.setValue("2mm", "1mm", "0mm");
	line.point5.setValue("2mm", "1mm", "0mm");
	line.setName("testLine");
	line.markGrid.setValue("DX1", "DX2", "DX3");

	std::cerr << line.toCommand();
	return a.exec();
}
