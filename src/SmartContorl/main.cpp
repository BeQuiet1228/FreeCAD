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
	
	QCustomPlot *customPlot = new QCustomPlot;
	customPlot->legend->setVisible(true);
	customPlot->legend->setFont(QFont("Helvetica", 9));
	customPlot->legend->setRowSpacing(-3);
	QVector<QCPScatterStyle::ScatterShape> shapes;
	shapes << QCPScatterStyle::ssCross;
	shapes << QCPScatterStyle::ssPlus;
	shapes << QCPScatterStyle::ssCircle;
	shapes << QCPScatterStyle::ssDisc;
	shapes << QCPScatterStyle::ssSquare;
	shapes << QCPScatterStyle::ssDiamond;
	shapes << QCPScatterStyle::ssStar;
	shapes << QCPScatterStyle::ssTriangle;
	shapes << QCPScatterStyle::ssTriangleInverted;
	shapes << QCPScatterStyle::ssCrossSquare;
	shapes << QCPScatterStyle::ssPlusSquare;
	shapes << QCPScatterStyle::ssCrossCircle;
	shapes << QCPScatterStyle::ssPlusCircle;
	shapes << QCPScatterStyle::ssPeace;
	shapes << QCPScatterStyle::ssCustom;

	QPen pen;
	// add graphs with different scatter styles:
	for (int i = 0; i < shapes.size(); ++i)
	{
		customPlot->addGraph();
		pen.setColor(QColor(qSin(i*0.3) * 100 + 100, qSin(i*0.6 + 0.7) * 100 + 100, qSin(i*0.4 + 0.6) * 100 + 100));
		// generate data:
		QVector<double> x(10), y(10);
		for (int k = 0; k < 10; ++k)
		{
			x[k] = k / 10.0 * 4 * 3.14 + 0.01;
			y[k] = 7 * qSin(x[k]) / x[k] + (shapes.size() - i) * 5;
		}
		customPlot->graph()->setData(x, y);
		customPlot->graph()->rescaleAxes(true);
		customPlot->graph()->setPen(pen);
		customPlot->graph()->setName(QString("test%1").arg(i));
		customPlot->graph()->setLineStyle(QCPGraph::lsLine);
		// set scatter style:
		if (shapes.at(i) != QCPScatterStyle::ssCustom)
		{
			customPlot->graph()->setScatterStyle(QCPScatterStyle(shapes.at(i), 10));
		}
		else
		{
			QPainterPath customScatterPath;
			for (int i = 0; i < 3; ++i)
				customScatterPath.cubicTo(qCos(2 * M_PI*i / 3.0) * 6, qSin(2 * M_PI*i / 3.0) * 9, qCos(2 * M_PI*(i + 0.9) / 3.0) * 9, qSin(2 * M_PI*(i + 0.9) / 3.0) * 9, 0, 0);
			customPlot->graph()->setScatterStyle(QCPScatterStyle(customScatterPath, QPen(Qt::black, 0), QColor(40, 70, 255, 50), 10));
		}
	}
	// set blank axis lines:
	customPlot->rescaleAxes();
	customPlot->xAxis->setTicks(true);
	customPlot->yAxis->setTicks(true);
	customPlot->xAxis->setTickLabels(true);
	customPlot->yAxis->setTickLabels(true);
	// make top right axes clones of bottom left axes:
	customPlot->axisRect()->setupFullAxesBox();

	//customPlot->show();

	return a.exec();
}
