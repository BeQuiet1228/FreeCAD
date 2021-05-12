#include "Arrowctrl.h"
#include <QMouseEvent>
#include <QDebug>
#include <QImage>
#include <QPainter>
#include <QPixmap>
std::string pngresource[] = { ":/Arrow/arrow1.png" };
ArrowCtrl::ArrowCtrl(Direction direction, QWidget* parent) :QWidget(parent), mdirection(direction)
{

}
ArrowCtrl::~ArrowCtrl(){

}
void ArrowCtrl::paintEvent(QPaintEvent * event)
{

}
void ArrowCtrl::mouseMoveEvent(QMouseEvent* event)
{
	QWidget::mouseMoveEvent(event);

}
void ArrowCtrl::mousePressEvent(QMouseEvent* event)
{
	QWidget::mousePressEvent(event);
	if (event->button() != Qt::LeftButton && curarrow!=-1)
		return;
	for (int index = 0; index < pos.size(); index++)
	{
		if (pos[index].contains(event->posF()))
		{
			curarrow = index;
			return;
		}
	}
}
void ArrowCtrl::mouseReleaseEvent(QMouseEvent* event)
{
	QWidget::mouseReleaseEvent(event);
	if (curarrow!=-1)
	{
		QPointF p1 = pos[curarrow].center();
		p1.setX(event->posF().x());
		pos[curarrow].moveCenter(p1);
		drawImage();
	}
}
bool ArrowCtrl::drawImage()
{
	//首先获取窗口大小
	QImage img(this->size(),QImage::Format_ARGB32);
	img.fill(qRgba(0, 0, 0, 0));
	QPainter painter(&img);
	for (int index = 0; index < pos.size();index++)
	{
		painter.drawPixmap(pos[index].center(), marrowmap[index]);
	}
	img.save("C:/Users/ASUS/Desktop/save/arrow.png");
	update();
	return true;
}
void ArrowCtrl::setlevel(int number)
{

}
#include"moc_Arrowctrl.cpp"