#pragma once
#ifndef COLORTAB_H_
#define COLORTAB_H_
#include <QWidget>
class QwtScaleWidget;
class QwtScaleEngine;
class ColorTab :public QWidget
{
	Q_OBJECT
public:
	explicit ColorTab(QWidget* parent=nullptr);
	~ColorTab();
public:
	void initUI();
	virtual void resizeEvent(QResizeEvent * event) override;
	void setColors(std::vector<float>& vals,std::vector<QColor>&);
	std::vector<QColor> GetColors(std::vector<float> vals);
	void setColorStyle(int);
	public Q_SLOTS:
void changmoveColor(std::vector<float>& val,std::vector<QColor>& colors,const QColor& firstColor,const QColor& endColor);
private:
	QwtScaleWidget* scaleWidget;
	QwtScaleEngine* scaleEngine;
	int style;
};
#endif