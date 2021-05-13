#pragma once
#ifndef _ARROW_CTRL_H_
#define _ARROW_CTRL_H_
#include <QWidget>
#include <QPointF>
#include <mutex>
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
	void setlevel(int number);
	void resizeEvent(QResizeEvent * event);
	void setVal(std::vector<float>&);
	std::vector<float> getVal();
protected:
	bool drawImage();
	void setimg(QImage& img);
	QImage* getimg();
private:
	QImage* nimg;
	Direction mdirection;
	int levelnumber;
	int curarrow;
	std::vector<QPixmap> marrowmap;
	std::vector<QRectF> pos;
	std::vector<float> val;
	std::mutex imgmutex;
};
#endif
