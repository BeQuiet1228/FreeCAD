#include "VariateChart.h"
#include <QPen>
VariateChart::VariateChart()
{
	plot = new QCustomPlot;
	initPointShape();

	plot->xAxis->setTicks(true);
	plot->yAxis->setTicks(true);
	plot->xAxis->setTickLabels(true);
	plot->yAxis->setTickLabels(true);
}

VariateChart::~VariateChart()
{
	delete plot;
}


/**
* @brief VariateChart::setData 设置一条线的数据
* @param const QVector<double> & key x轴数据
* @param const QVector<double> & value y轴数据
* @param const QColor & color 线的颜色
* @param const QCPScatterStyle::ScatterShape & pointShape 点的样式
* @param const QString & name 名称
* @return void
*/
void VariateChart::setData(const QVector<double>& key, const QVector<double>& value, const QColor& color, const QCPScatterStyle::ScatterShape& pointShape, const QString& name /*= "line"*/)
{
	QPen pen;
	pen.setColor(color);

	plot->addGraph();
	plot->graph()->setData(key, value);
	plot->graph()->setPen(pen);
	plot->graph()->setName(name);
	plot->graph()->setLineStyle(QCPGraph::lsLine);
	plot->graph()->rescaleAxes(true);
	plot->graph()->setScatterStyle(pointShape);

	plot->rescaleAxes();
}

void VariateChart::setData(const QVector<double>& key, const QVector<double>& value, const QColor& color, const QString& name /*= "line"*/)
{
	setData(key, value, color, QCPScatterStyle::ssStar, name);
}

void VariateChart::setData(const QVector<double>& key, const QVector<double>& value, const QString& name /*= "line"*/)
{
	QColor color = Qt::red;
	setData(key, value, color, name);

}

/**
* @brief VariateChart::setDatas 将多条线的数据放入控件
* @param const QVector<double> & key x轴数据
* @param const QVector<QVector<double>> & values y轴的数据集
* @param const QString & name 名称 该函数会自动在名称后加上数字后缀
* @return void
*/
void VariateChart::setDatas(const QVector<double>& key, const QVector<QVector<double>> &values, const QString& name)
{
	int count = 1;
	for (auto i = values.begin(); i != values.end(); i++)
	{
		QColor color(qSin(count*0.3) * 100 + 100, qSin(count*0.6 + 0.7) * 100 + 100, qSin(count*0.4 + 0.6) * 100 + 100);
		setData(key, *i,color,pointShapes.at(count),QString(name + "%1").arg(count));
		count++;
	}
}

/**
* @brief VariateChart::initPointShape 初始化点样式
* @return void
*/
void VariateChart::initPointShape()
{
	pointShapes << QCPScatterStyle::ssCross;
	pointShapes << QCPScatterStyle::ssPlus;
	pointShapes << QCPScatterStyle::ssCircle;
	pointShapes << QCPScatterStyle::ssDisc;
	pointShapes << QCPScatterStyle::ssSquare;
	pointShapes << QCPScatterStyle::ssDiamond;
	pointShapes << QCPScatterStyle::ssStar;
	pointShapes << QCPScatterStyle::ssTriangle;
	pointShapes << QCPScatterStyle::ssTriangleInverted;
	pointShapes << QCPScatterStyle::ssCrossSquare;
	pointShapes << QCPScatterStyle::ssPlusSquare;
	pointShapes << QCPScatterStyle::ssCrossCircle;
	pointShapes << QCPScatterStyle::ssPlusCircle;
	pointShapes << QCPScatterStyle::ssPeace;
	pointShapes << QCPScatterStyle::ssCustom;

}

