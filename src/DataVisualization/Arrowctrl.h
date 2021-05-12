#pragma once
#ifndef _ARROW_CTRL_H_
#define _ARROW_CTRL_H_
#include <QWidget>
class ArrowCtrl :public QWidget
{
	Q_OBJECT
public:
	enum Direction{
		LeftToRight,
		RightToLeft,
		TopToBottom,
		BottomToTop,
	};
public:
	explicit ArrowCtrl(Direction, QWidget* parent = nullptr);
	~ArrowCtrl();
public:
	virtual void mouseMoveEvent(QMouseEvent* event) override;
	virtual void mousePressEvent(QMouseEvent *event) override;
	virtual void mouseReleaseEvent(QMouseEvent* event) override;
	void paintEvent(QPaintEvent * event);
private:
	Direction mdirection;

};

#endif
