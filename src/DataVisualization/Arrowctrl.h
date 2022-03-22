#pragma once
#ifndef _ARROW_CTRL_H_
#define _ARROW_CTRL_H_
#include <QWidget>
#include <QPointF>
#include <mutex>
#include "exportConfig.hpp"
class QAction;
class QMenu;
namespace DV {
	class DATA_VISUALIZATION_EXPORT ArrowCtrl :public QWidget
	{
		Q_OBJECT
	public:
		enum Direction {
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
		virtual void mousePressEvent(QMouseEvent* event) override;
		virtual void mouseDoubleClickEvent(QMouseEvent* event) override;
		virtual void mouseReleaseEvent(QMouseEvent* event) override;
		void mouseRightClicked(QMouseEvent* event);
		void paintEvent(QPaintEvent* event);
		void setlevel(int number);
		void resizeEvent(QResizeEvent* event);
		void setvals(std::vector<float>&, std::vector<QColor>&);
		void setColorMap();
		std::vector<float> getValue();
		void SetFirstColor(QColor& color);
		void SetEndColor(QColor& color);
	protected:
		void initUI();
		bool drawImage();
		void setimg(QImage& img);
		QImage* getimg();
	Q_SIGNALS:
		void changMoveColor(std::vector<float>&, std::vector<QColor>&, const QColor& firstColor, const QColor& endColor);
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
		//
		int actionindex;
		QPointF actionpos;
		QAction* buttonActionAdd;
		QAction* buttonActionDelete;
		QMenu* buttonMenu;
		//
		QColor firstColor;
		QColor endColor;
	};
};

#endif
