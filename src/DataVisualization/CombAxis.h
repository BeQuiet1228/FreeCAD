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
	explicit CombAxis(Axisstyle astyle=AxisBottom,QWidget* parent = nullptr);
	~CombAxis();
	void initUI(Axisstyle);
protected:
	void setLeft();
	void setRight();
	void setTop();
	void setBottom();
private:
	QGridLayout* layout;
	Axis* mAxis;
	TLabel* mtlabel;

};
#endif
