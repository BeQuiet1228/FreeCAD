#include "Axis.h"
Axis::Axis(QWidget* parent /*= 0*/)
	:QWidget(parent)
{

}

Axis::~Axis()
{

}

void Axis::setAxisText(QString AxisUnitText, int fontsize){
	Axisunit = AxisUnitText;//单位
	Axisunitfontsize = fontsize;//字体大小
}
void Axis::setAxisRange(double min, double max){
	axisvalrange.min = min;
	axisvalrange.max = max;
}
void Axis::SetAxisNumber(int _Axisnumber){
	Axisnumber = _Axisnumber;
}
void Axis::_update(){
	//是否需要调整大小
	QWidget* parent = (QWidget*)this->parent();
	QSize parentsize = parent->size();//获取父级窗口大小
	switch (mAxisstyle)
	{
	case Axisleft:
	{
		AxisRect.setLeft(0);
		AxisRect.setTop(0);
		AxisRect.setBottom(parent->height());
		AxisRect.setRight(Axisunitfontsize + 50);
	}
		break;
	case AxisRight:
	{
		AxisRect.setRight(parentsize.width());
		AxisRect.setTop(0);
		AxisRect.setBottom(parentsize.height());
		AxisRect.setLeft(AxisRect.right() - (Axisunitfontsize + 50));
	}
		break;
	case AxisTop:
	{
		AxisRect.setLeft(Axisunitfontsize + 50);
		AxisRect.setRight(parentsize.width() - (Axisunitfontsize + 50));
		AxisRect.setTop(0);
		AxisRect.setBottom(AxisRect.top() + (Axisunitfontsize + 50));
	}
		break;
	case AxisBottom:
	{
		AxisRect.setLeft(Axisunitfontsize + 50);
		AxisRect.setRight(parentsize.width() - (Axisunitfontsize + 50));
		AxisRect.setBottom(parentsize.height());
		AxisRect.setTop(AxisRect.bottom() - (Axisunitfontsize + 50));
	}
		break;
	default:
		return;
	}
	//此处添加位置数据
	update();
}
void Axis::setAxisStyle(Axisstyle _Axisstyle){
	mAxisstyle = _Axisstyle;
}
void Axis::paintEvent(QPaintEvent* event){
	//重绘




}