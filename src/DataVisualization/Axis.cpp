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
 //获取窗口的大小
    QSize clientsize=this->size();
    //获取客户区的长宽
    qreal width=clientsize.width();
    qreal height=clientsize.height();
    QPainter mPainter(this);
    switch (mAxisstyle) {
    case Axisleft:
        {
        //绘制坐标单位
        int length=Axisunit.length();
        QRectF Axisunitrect;
            mPainter.save();
            Axisunitrect.setLeft((qreal)(10+Axisunitfontsize));
            Axisunitrect.setRight((qreal)(Axisunitrect.left()+length*Axisunitfontsize));
            Axisunitrect.setBottom((qreal)(height/2-Axisunitfontsize*length/4));
            Axisunitrect.setTop((qreal)(Axisunitrect.bottom()-Axisunitfontsize/2));
            QFont verticalfont=mPainter.font();
            verticalfont.setPixelSize(Axisunitfontsize);
            mPainter.setFont(verticalfont);
            mPainter.translate(Axisunitrect.left(),Axisunitrect.bottom());
            mPainter.rotate(-90);
            //mPainter.drawText(verticalTextRect,verticalText);
            mPainter.drawText(QPointF(0.0,0.0),Axisunit);
            //旋转
            mPainter.restore();

    }
        break;
    case AxisRight:
    {
        int length=Axisunit.length();
        QRectF Axisunitrect;
        Axisunitrect.setRight((qreal)(width-10)-Axisunitfontsize);
        Axisunitrect.setLeft(Axisunitrect.right()-Axisunitfontsize*length);
        Axisunitrect.setBottom((qreal)(height/2-Axisunitfontsize*length/4));
        Axisunitrect.setTop((qreal)(Axisunitrect.bottom()-Axisunitfontsize/2));
        QFont verticalfont=mPainter.font();
        verticalfont.setPixelSize(Axisunitfontsize);
        mPainter.setFont(verticalfont);
        mPainter.translate(Axisunitrect.right(),Axisunitrect.bottom());
        mPainter.rotate(90);
        QFont horizontalfont=mPainter.font();
        horizontalfont.setPixelSize(Axisunitfontsize);
        mPainter.setFont(horizontalfont);
        mPainter.drawText(QPointF(0.0,0.0),Axisunit);
        //
        mPainter.restore();
    }
        break;
    case AxisTop:
    {
        int length=Axisunit.length();
        QRectF Axisunitrect;
            Axisunitrect.setLeft((qreal)(width/2)-(qreal)(length*Axisunitfontsize/4));
            Axisunitrect.setRight((qreal)(width/2)+(qreal)(length*Axisunitfontsize/4));
            Axisunitrect.setTop((qreal)(10));
            Axisunitrect.setBottom((qreal)(Axisunitrect.top())+(qreal)(Axisunitfontsize));
            QFont horizontalfont=mPainter.font();
            horizontalfont.setPixelSize(Axisunitfontsize);
            mPainter.setFont(horizontalfont);
            mPainter.drawText(Axisunitrect,Axisunit);
    }
        break;
    case AxisBottom:
    {
        int length=Axisunit.length();
        QRectF Axisunitrect;
            Axisunitrect.setLeft((qreal)(width/2)-(qreal)(length*Axisunitfontsize/4));
            Axisunitrect.setRight((qreal)(width/2)+(qreal)(length*Axisunitfontsize/4));
            Axisunitrect.setBottom((qreal)(height-10));
            Axisunitrect.setTop((qreal)(Axisunitrect.bottom())-(qreal)(Axisunitfontsize));
            QFont horizontalfont=mPainter.font();
            horizontalfont.setPixelSize(Axisunitfontsize);
            mPainter.setFont(horizontalfont);
            mPainter.drawText(Axisunitrect,Axisunit);
            //刻度
            qreal interval=(width-50-Axisunitfontsize)/(Axisnumber*5);
            qreal valinterval=(qreal)(axisvalrange.max-axisvalrange.min)/(qreal)Axisnumber;

    }
        break;
    }

    if(0==Axisnumber)
        return;
    //绘制坐标单位
    int length=Axisunit.length();
    //获取坐标的区间

//    //画横坐标刻度
//    //长刻度为10，短刻度为6
//    QVector<qreal> horizontalAxislist;
//    if(horizontalvalrange.min>=horizontalvalrange.max)
//        return;
//    qreal Horizontalinterval=(width-50-verticalfontsize)/(horizontalAxis*5);
//    qreal Horizontalvalinter=(qreal)(horizontalvalrange.max-horizontalvalrange.min)/(qreal)horizontalAxis;
//    //画线
//    mPainter.drawLine(50+verticalfontsize,horizontalTextRect.top()-50,width,horizontalTextRect.top()-50);
//    //画纵线
//    mPainter.drawLine(50+verticalfontsize,horizontalTextRect.top()-50,50+verticalfontsize,0);

//    QPointF startpoint;
//    startpoint.setX(50+verticalfontsize);
//    startpoint.setY(horizontalTextRect.top()-50);
//    QPointF nexthorizonpoint;
//    nexthorizonpoint=startpoint;
//    //画横轴刻度
//    QFont axisfont= mPainter.font();
//    axisfont.setPixelSize(10);
//    mPainter.setFont(axisfont);
//    for(auto i=1;i<=horizontalAxis*5;i++)
//    {
//        nexthorizonpoint.setX(nexthorizonpoint.x()+Horizontalinterval);
//        if(i%5==0)
//        {
//            (mPainter.drawLine(nexthorizonpoint.x(),nexthorizonpoint.y(),nexthorizonpoint.x(),nexthorizonpoint.y()+10));
//            //绘制数值
//            qreal curval=(i/5)*Horizontalvalinter;
//            QString curvalstr=QString("%1").arg(curval);
//            mPainter.drawText(QPointF(nexthorizonpoint.x()-(curvalstr.length())*10/4,nexthorizonpoint.y()+10+10),curvalstr);
//        }
//        else {
//            ((mPainter.drawLine(nexthorizonpoint.x(),nexthorizonpoint.y(),nexthorizonpoint.x(),nexthorizonpoint.y()+6)));
//        }
//    }
//    //写刻度
//    qreal Verticalinterval=startpoint.y()/(verticalAxis*5);
//    qreal Verticalvalinterval=(verticalvalrange.max-verticalvalrange.min)/verticalAxis;
//    QPointF nextverticalpoint=startpoint;
//    for(auto i=1;i<=verticalAxis*5;i++)
//    {
//        nextverticalpoint.setY(nextverticalpoint.y()-Verticalinterval);
//        if(i%5==0)
//        {
//            (mPainter.drawLine(nextverticalpoint.x(),nextverticalpoint.y(),nextverticalpoint.x()-10,nextverticalpoint.y()));
//            //绘制数值
//            qreal curval=(i/5)*Verticalvalinterval;
//            QString curvalstr=QString("%1").arg(curval);
//            mPainter.drawText(QPointF(nextverticalpoint.x()-10-curvalstr.length()*10/2,nextverticalpoint.y()+5),curvalstr);
//        }
//        else
//        {
//            ((mPainter.drawLine(nextverticalpoint.x(),nextverticalpoint.y(),nextverticalpoint.x()-6,nextverticalpoint.y())));
//        }
//    }
}
//void Axis::sethorizontalAxisText(QString _text,int fontsize)  {
//    horizontalText=_text;
//    horizontalfontsize=fontsize;
//}
//void Axis::setverticalAxisText(QString _text,int fontsize)    {
//    verticalText=_text;
//    verticalfontsize=fontsize;
//}
//void Axis::sethorizontalAxisRange(double min,double max){
//    horizontalvalrange.min=min;
//    horizontalvalrange.max=max;
//}
//void Axis::setverticalAxisRange(double min,double max)  {
//    verticalvalrange.min=min;
//    verticalvalrange.max=max;
//}



}