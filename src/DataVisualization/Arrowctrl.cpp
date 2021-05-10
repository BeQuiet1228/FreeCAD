#include "Arrowctrl.h"
std::string pngresource[] = { ":/Arrow/arrow1.png" };
ArrowCtrl::ArrowCtrl(Direction direction, QWidget* parent) :QWidget(parent), mdirection(direction)
{

}
ArrowCtrl::~ArrowCtrl(){

}
void ArrowCtrl::paintEvent(QPaintEvent * event)
{
	printf("重绘\n");
}
void ArrowCtrl::mouseMoveEvent(QMouseEvent* event)
{
	printf("鼠标移动\n");
}
void ArrowCtrl::mousePressEvent(QMouseEvent* event)
{
	printf("鼠标按下");
}
void ArrowCtrl::mouseReleaseEvent(QMouseEvent* event)
{
	printf("鼠标释放");
}
#include"moc_Arrowctrl.cpp"