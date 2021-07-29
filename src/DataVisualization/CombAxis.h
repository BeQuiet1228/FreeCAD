#pragma once
#ifndef COMBAXIS_H_
#define COMBAXIS_H_
#include <qwidget.h>
#include"Axis.h"
#include"TLabel.h"
class QGridLayout;
class CombAxis: public QWidget
{
	Q_OBJECT
public :
	CombAxis(QWidget* parent = nullptr);
	~CombAxis();
public:
	//使用Axis原来的接口
	void setAxixStyle(Axisstyle mAxisstyle);
	void setAxisRange(float min,float max);
	void _update();
	void SetAxisNumber(unsigned int);
	void setColorBarEnabled(bool);
	void setMargin(float);
	void setSpacing(float);
	void setBorderDist(float start,float end);
	void loadconfig();
	//QLabel的相关接口
	void setAxisText(QString str);
	//单独的接口
	void setView(Axisstyle);
protected:
	void setLeft();
	void setRight();
	void setTop();
	void setBottom();
private:
	QGridLayout* layout;
public:
	Axis* mAxis;
	TLabel* mtlabel;
};
#endif
