#pragma once
#include "qcustomplot.h"
#include <QDialog>
class VariateChart:public QDialog{
public:
	VariateChart(QWidget* parent = 0);
	~VariateChart();

public:
	void setData(const QVector<double>& key,const QVector<double>& value, const QString& name = "line");
	void setData(const QVector<double>& key,const QVector<double>& value, 
		const QColor& color, const QString& name = "line");
	void setData(const QVector<double>& key,const QVector<double>& value, const QColor& color, 
		const QCPScatterStyle::ScatterShape& pointShape,const QString& name = "line");
	void setDatas(const QVector<double>& key, const QVector<QVector<double>> &values, const QString& name);

	void clearGraph(){
		plot->clearGraphs();
	}

	void showPlot(){
		this->show();
	}
private:
	//控件对象
	QCustomPlot *plot;
	//线条样式
	QVector<QCPScatterStyle::ScatterShape> pointShapes;
	QVector<QColor> colors;

private:
	void initPointShape();
	QCPScatterStyle::ScatterShape getPointShape(const unsigned int& index);
};