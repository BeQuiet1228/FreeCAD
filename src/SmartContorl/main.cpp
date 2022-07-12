#include <qwidget.h>
#include <QApplication>
#include <QFile>
#include "GeneticAlgorithm.h"
#include "SmartContorlUI.h"
#include "GeneticAlgorithmUI.h"
#include "MultipleTargetGeneticAlgorithmUI.h"
//#include "FileMaker.h"
//#include "qcustomplot.h"
#include"smartCalc.h"
int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
// 	QWidget w;
// 	w.show();

// 	GeneticAlgorithm g;
// 	g.test();

	MultipleTargetGeneticAlgorithmUI w;
	w.show();

// 	QFile file("testdsadas.tt");
// 	file.open(QIODevice::ReadWrite);
// 	file.close();


	return a.exec();
}
