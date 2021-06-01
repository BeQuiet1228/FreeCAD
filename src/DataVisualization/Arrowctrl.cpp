#include "Arrowctrl.h"
#include <QMouseEvent>
#include <QDebug>
#include <QImage>
#include <QPainter>
#include <QPixmap>
#include <QColorDialog>
#include<QMenu>
#include <QAction>
QString pngresource[] = { ":/Arrow/arrow1.png" };
/**
* @brief  ArrowCtrl::ArrowCtrl
* @param  Direction direction  
* @param  QWidget * parent  
* @return   
*/
ArrowCtrl::ArrowCtrl(Direction direction, QWidget* parent) :QWidget(parent), mdirection(direction), nimg(nullptr), actionindex(-1)
{
	
	firstColor=QColor(Qt::darkBlue);
	endColor=QColor(Qt::darkRed);
	initUI();
}
/**
* @brief  ArrowCtrl::~ArrowCtrl
* @return   
*/
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
		val[curarrow] = p1.x() / this->width();
		drawImage();
		setColorMap();
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
	switch (event->button())
	{
	case Qt::LeftButton:
	{
		if (curarrow != -1)
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
		return;
	case Qt::RightButton:
	{
		mouseRightClicked(event);
	}
		return;
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
	mapColor.clear();
	mapColor.reserve(levelnumber);
	val.reserve(levelnumber );
	pos.reserve(levelnumber );
	QSize pngsize(this->height(),this->height());
	float interval = 1.0 / (float)(number-1);
	//数据范围0~1
	for (int index = 0; index < number;index++)
	{
		QPixmap map(pngresource[0]);
		map = map.scaled(pngsize, Qt::KeepAspectRatio, Qt::SmoothTransformation);
		//颜色替换
		//qDebug() << map.size();
		marrowmap.push_back(map);
		mapColor.push_back(QColor(Qt::black));
		val.push_back(0 + interval*index);
		QRectF rectF(val[index]*this->size().width()-marrowmap[index].size().width()/2,
			this->size().height()-marrowmap[index].size().height(),marrowmap[index].size().width(),marrowmap[index].size().height());
		pos.push_back(rectF);
	}
	drawImage();
}
/**
* @brief  ArrowCtrl::resizeEvent 
* @param  QResizeEvent * event  
* @return void  
*/
void ArrowCtrl::resizeEvent(QResizeEvent * event)
{
	QSize pngsize(this->height(), this->height());
	for (int index = 0; index < pos.size();index++)
	{
		marrowmap[index] = marrowmap[index].scaled(pngsize,Qt::KeepAspectRatio, Qt::SmoothTransformation);
		QRectF rectF(val[index] * this->size().width() - marrowmap[index].size().width() / 2, 
			this->size().height() - marrowmap[index].size().height(), marrowmap[index].size().width(), marrowmap[index].size().height());
		pos[index]=(rectF);
	}
	drawImage();
}
/**
* @brief  ArrowCtrl::setimg 设置图像
* @param  QImage & img  
* @return void  
*/
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
/**
* @brief  ArrowCtrl::getimg 获取图像
* @return QT_NAMESPACE::QImage*  
*/
QImage* ArrowCtrl::getimg(){
	std::lock_guard<std::mutex> am(imgmutex);
	return nimg;
}
void ArrowCtrl::setvals(std::vector<float>& vals, std::vector<QColor>& colors)
{
	if (vals.empty())
		return;
	firstColor=*colors.begin();
	endColor=*(colors.end()-1);
	val.clear(); val.reserve(vals.size());
	mapColor.clear(); mapColor.reserve(vals.size());
	marrowmap.clear(); marrowmap.reserve(vals.size());
	pos.clear(); pos.reserve(vals.size());
	for (auto index = 1; index < vals.size() - 1;index++)
	{
		mapColor.push_back(colors[index]);
		val.push_back(vals[index]);
	}
	//添加箭头
	QSize pngsize(this->height(), this->height());
	for (int index = 0; index < val.size(); index++)
	{
		QPixmap map(pngresource[0]);
		map = map.scaled(pngsize, Qt::KeepAspectRatio, Qt::SmoothTransformation);
		
		//替换颜色
		QImage img = map.toImage();
		QColor color(Qt::black);
		for (int w = 0; w < img.width(); ++w)
		{
			for (int h = 0; h < img.height(); h++)
			{
				if (img.pixel(w, h) ==color.rgb())
				{
					img.setPixel(w, h, mapColor[index].rgba());
				}
			}
		}
		marrowmap.push_back(QPixmap::fromImage(img));
		QRectF rectF(val[index] * this->size().width() - marrowmap[index].size().width() / 2,
			this->size().height() - marrowmap[index].size().height(), marrowmap[index].size().width(), marrowmap[index].size().height());
		pos.push_back(rectF);
	}
	drawImage();
}
/**
* @brief  mouseDoubleClickEvent 鼠标双击事件
* @param  QMouseEvent * event  
* @return void  
*/
void ArrowCtrl::mouseDoubleClickEvent(QMouseEvent* event){
	QWidget::mouseDoubleClickEvent(event);
	if (event->button() != Qt::LeftButton)
		return;
	curarrow = -1;
	int indexarrow = -1;
	for (int index = 0; index < pos.size(); index++)
	{
		if (pos[index].contains(event->posF()))
		{
			indexarrow = index;
			break;
		}
	}
	if (indexarrow == -1)
		return;
	//打开一个颜色窗口
	QColor color = QColorDialog::getColor(Qt::black,this,"color",QColorDialog::ShowAlphaChannel);
	QColor WhiteColor(Qt::white);
	QImage img=marrowmap[indexarrow].toImage();
	for (int w = 0; w < img.width(); ++w)
	{
		for (int h = 0; h < img.height(); h++)
		{
			if (img.pixel(w,h)==mapColor[indexarrow].rgb())
			{
				img.setPixel(w, h, color.rgba());
			}
		}
	}
	marrowmap[indexarrow] = QPixmap::fromImage(img);
	mapColor[indexarrow] = color;
	drawImage();
	//改变颜色
	setColorMap();
}
/**
* @brief  ArrowCtrl::initUI 初始化UI
* @return void  
*/
void ArrowCtrl::initUI()
{
	setlevel(3);
	//初始化动作
	buttonActionAdd = new QAction("add",this);
	buttonActionDelete = new QAction("delete",this);
	//初始化菜单
	buttonMenu = new QMenu(this);
	//添加动作到菜单
	buttonMenu->addAction(buttonActionDelete);
	buttonMenu->addAction(buttonActionAdd);
	//链接信号槽
	connect(buttonActionAdd, SIGNAL(triggered()), this, SLOT(addTriggered()));
	connect(buttonActionDelete, SIGNAL(triggered()), this, SLOT(deleteTriggered()));
	connect(this, SIGNAL(customContextMenuRequested(const QPoint&)), buttonMenu, SLOT(MenuClicked(const QPoint&)));
}
/**
* @brief  ArrowCtrl::addTriggered 添加
* @return void  
*/
void ArrowCtrl::addTriggered()
{
	QPixmap map(pngresource[0]);
	QSize pngsize(this->height(),this->height());
	map = map.scaled(pngsize, Qt::KeepAspectRatio, Qt::SmoothTransformation);
	marrowmap.push_back(map);
	mapColor.push_back(QColor(Qt::black));
	QRectF rectf(actionpos.x(),this->size().height()-map.size().height(),map.width(),map.height());
	pos.push_back(rectf);
	actionindex = -1;
	drawImage();
	setColorMap();
	val.push_back(actionpos.x()/this->width());
}
/**
* @brief  ArrowCtrl::deleteTriggered 删除
* @return void  
*/
void ArrowCtrl::deleteTriggered()
{
	//删除箭头,颜色,矩形
	if (actionindex!=-1)
	{
		marrowmap.erase(marrowmap.begin() + actionindex);
		mapColor.erase(mapColor.begin() + actionindex);
		pos.erase(pos.begin() + actionindex);
		val.erase(val.begin()+actionindex);
	}
	actionindex = -1;
	drawImage();
	//
	setColorMap();
}
/**
* @brief  ArrowCtrl::mouseRightClicked 鼠标右键事件
* @param  QMouseEvent * event  
* @return void  
*/
void ArrowCtrl::mouseRightClicked(QMouseEvent* event)
{
	actionpos = event->posF();
	QPoint menupos = this->mapToGlobal(event->pos());
	for (int index = 0; index < pos.size(); index++)
	{
		if (pos[index].contains(event->posF()))
		{
			actionindex = index;
			break;
		}
	}
	if (actionindex!=-1)
	{
		buttonActionDelete->setEnabled(true);
		buttonActionAdd->setEnabled(false);
	}
	else
	{
		buttonActionAdd->setEnabled(true);
		buttonActionDelete->setEnabled(false);
	}
	buttonMenu->exec(menupos);
}
/**
* @brief  ArrowCtrl::setColorMap 设置颜色表
* @return void  
*/
void ArrowCtrl::setColorMap()
{
	std::vector<float> vall;
	for (auto index = 0; index < pos.size(); index++)
	{
		vall.push_back(pos[index].center().x() / (float)this->size().width());
	}
	emit changMoveColor(vall, mapColor,firstColor,endColor);
}

/**
* @brief  ArrowCtrl::getValue 获取数据
* @return std::vector<float>  
*/
std::vector<float> ArrowCtrl::getValue(){
	std::vector<float> vals;
	vals.insert(vals.end(),val.begin(),val.end());
	std::sort(vals.begin(), vals.end());
	if (*(vals.end() - 1) != 1.0f)vals.push_back(1.0f);
	if (*vals.begin() != 0) vals.push_back(0.0f);
	std::sort(vals.begin(), vals.end());
	return vals;
}
/**
* @brief  ArrowCtrl::SetFirstColor 设置起始颜色
* @param  QColor & color  
* @return void  
*/
void ArrowCtrl::SetFirstColor(QColor& color){
	firstColor=color;
	setColorMap();
}
/**
* @brief  ArrowCtrl::SetEndColor 设置结束色
* @param  QColor & color  
* @return void  
*/
void ArrowCtrl::SetEndColor(QColor& color){
	endColor = color;
	setColorMap();
}
#include"moc_Arrowctrl.cpp"