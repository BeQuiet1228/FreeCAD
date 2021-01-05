#include <qwidget.h>
#include <QApplication>
#include <iostream>
#include "VolFunction.h"
int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	QWidget w;
	w.show();

	VolFunction line;

	
	line.point1.setValue("2mm", "2mm", "3mm");
	line.point2.setValue("2mm", "2mm", "3mm");
	//line.point3.setValue("2mm", "2mm", "3mm");
	//line.point4.setValue("2mm", "2mm", "3mm");
	//line.point5.setValue("2mm", "2mm", "3mm");
	line.setName("testLine");
	line.markGrid.setValue("DX1", "DX2", "DX3");
	std::cout << line.setFunction("x+y+z") << std::endl;

	std::cerr << line.toCommand();
	return a.exec();
}
