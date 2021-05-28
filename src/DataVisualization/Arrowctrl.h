#pragma once
#ifndef _ARROW_CTRL_H_
#define _ARROW_CTRL_H_
#include <QWidget>
#include <QPointF>
#include <mutex>
class QAction;
class QMenu;
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
	virtual void mouseDoubleClickEvent(QMouseEvent* event) override;
	virtual void mouseReleaseEvent(QMouseEvent* event) override;
	void mouseRightClicked(QMouseEvent* event);
	void paintEvent(QPaintEvent * event);
	void setlevel(int number);
	void resizeEvent(QResizeEvent * event);
	void setVal(std::vector<float>&);
	std::vector<float> getVal();
protected:
	void initUI();
	bool drawImage();
	void setimg(QImage& img);
	QImage* getimg();
Q_SIGNALS:
	void changMoveColor(std::vector<float>&,std::vector<QColor>&);
public Q_SLOTS:
	void addTriggered();
	void deleteTriggered();
private:
	QImage* nimg;
	Direction mdirection;
	int levelnumber;
	int curarrow;
	std::vector<QPixmap> marrowmap;
	std::vector<QColor> mapColor;
	std::vector<QRectF> pos;
	std::vector<float> val;
	std::mutex imgmutex;
	//添加右键菜单
	//删除索引值
	int actionindex;
	//添加坐标
	QPointF actionpos;
	QAction* buttonActionAdd;
	QAction* buttonActionDelete;
	//声明菜单
	QMenu* buttonMenu;
};
#endif
