#pragma once
#include "qcustomplot.h"
class VariateChart{
public:
	VariateChart();
	~VariateChart();

public:
	void setData(const QVector<double>& key,const QVector<double>& value, const QString& name = "line");
	void setData(const QVector<double>& key,const QVector<double>& value, 
		const QColor& color, const QString& name = "line");
	void setData(const QVector<double>& key,const QVector<double>& value, const QColor& color, 
		const QCPScatterStyle::ScatterShape& pointShape,const QString& name = "line");
	void setDatas(const QVector<double>& key, const QVector<QVector<double>> &values, const QString& name);
	void show(){
		plot->show();
	}
	void close(){
		plot->close();
	}
	void clearGraph(){
		plot->clearGraphs();
	}
private:
	//控件对象
	QCustomPlot *plot;
	//线条样式
	QVector<QCPScatterStyle::ScatterShape> pointShapes;
	QVector<QColor> colors;

private:
	void initPointShape();
};