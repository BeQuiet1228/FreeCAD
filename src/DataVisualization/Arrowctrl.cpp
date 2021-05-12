#include "Arrowctrl.h"
#include <QMouseEvent>
#include <QDebug>
#include <QImage>
#include <QPainter>
#include <QPixmap>
QString pngresource[] = { ":/Arrow/arrow1.png" };
ArrowCtrl::ArrowCtrl(Direction direction, QWidget* parent) :QWidget(parent), mdirection(direction), nimg(nullptr)
{

}
ArrowCtrl::~ArrowCtrl(){
	marrowmap.clear();
	pos.clear();
	val.clear();
}
/**
* @brief  ArrowCtrl::paintEvent 重绘事件
* @param  QPaintEvent * event  
* @return void  
*/
void ArrowCtrl::paintEvent(QPaintEvent * event)
{
	QPainter painter(this);
	QPen pen;
	pen.setWidth(1);
	painter.setPen(pen);
	painter.drawImage(QPoint(0,0),*getimg());
}
/**
* @brief  ArrowCtrl::mouseMoveEvent 鼠标移动事件
* @param  QMouseEvent * event  
* @return void  
*/
void ArrowCtrl::mouseMoveEvent(QMouseEvent* event)
{
	QWidget::mouseMoveEvent(event);
	if (curarrow >=0)
	{
		QPointF p1 = pos[curarrow].center();
		if (event->posF().x() < 0)
			p1.setX(0.0);
		else if (event->posF().x() > this->size().width())
			p1.setX(this->size().width());
		else
		p1.setX(event->posF().x());
		pos[curarrow].moveCenter(p1);
		drawImage();
	}
}
/**
* @brief  ArrowCtrl::mousePressEvent 鼠标点击事件
* @param  QMouseEvent * event  
* @return void  
*/
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
/**
* @brief  ArrowCtrl::mouseReleaseEvent 鼠标释放
* @param  QMouseEvent * event  
* @return void  
*/
void ArrowCtrl::mouseReleaseEvent(QMouseEvent* event)
{
	QWidget::mouseReleaseEvent(event);
	if (curarrow!=-1)
	{
		curarrow = -1;
	}
}
/**
* @brief  ArrowCtrl::drawImage 绘图
* @return bool  
*/
bool ArrowCtrl::drawImage()
{
	//首先获取窗口大小
	QImage img(this->size(),QImage::Format_ARGB32);
	img.fill(qRgba(0, 0, 0, 0));
	QPainter painter(&img);
	painter.setRenderHint(QPainter::Antialiasing, true);
	for (int index = 0; index < pos.size();index++)
	{
		painter.drawPixmap(pos[index].topLeft(), marrowmap[index]);
	}
	setimg(img);
	update();
	return true;
}
/**
* @brief  ArrowCtrl::setlevel 设置等级
* @param  int number  
* @return void  
*/
void ArrowCtrl::setlevel(int number)
{
	levelnumber = number;
	marrowmap.clear();
	val.clear();
	pos.clear();
	marrowmap.reserve(levelnumber);
	val.reserve(levelnumber );
	pos.reserve(levelnumber );
	QSize pngsize(this->height(),this->height());
	float interval = 1.0 / (float)(number-1);
	//数据范围0~1
	for (int index = 0; index < number;index++)
	{
		QPixmap map(pngresource[0]);
		map = map.scaled(pngsize, Qt::KeepAspectRatio, Qt::SmoothTransformation);
		qDebug() << map.size();
		marrowmap.push_back(map);
		val.push_back(0 + interval*index);
		QRectF rectF(val[index]*this->size().width()-marrowmap[index].size().width()/2,
			this->size().height()-marrowmap[index].size().height(),marrowmap[index].size().width(),marrowmap[index].size().height());
		pos.push_back(rectF);
	}
	drawImage();
}
void ArrowCtrl::resizeEvent(QResizeEvent * event)
{
	QSize pngsize(this->height(), this->height());
	for (int index = 0; index < levelnumber;index++)
	{
		marrowmap[index] = marrowmap[index].scaled(pngsize,Qt::KeepAspectRatio, Qt::SmoothTransformation);
		QRectF rectF(val[index] * this->size().width() - marrowmap[index].size().width() / 2, 
			this->size().height() - marrowmap[index].size().height(), marrowmap[index].size().width(), marrowmap[index].size().height());
		pos[index]=(rectF);
	}
	drawImage();
}

void ArrowCtrl::setimg(QImage& img){
	std::lock_guard<std::mutex> am(imgmutex);
	if (nimg)
	{
		delete nimg;
		nimg = new QImage(img);
	}
	else
		nimg = new QImage(img);
}
QImage* ArrowCtrl::getimg(){
	std::lock_guard<std::mutex> am(imgmutex);
	return nimg;
}
#include"moc_Arrowctrl.cpp"