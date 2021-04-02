#include "axis.h"
#include<QRect>
#include<QSize>
#include<QPainter>

#define ZERO_F (0.000000000001f)	//定义浮点数的零
Axis::Axis(QWidget *parent) :
QWidget(parent)/*,horizontalAxis(0),verticalAxis(0),isstart(false)*/, CanvasWidget(nullptr)
{
	lines.clear();
	m_axisval.clear();
	CanvasSize = new QSizeF(this->width(), this->height());
	Axisnumber = 7;
	mAxisunit = "X(x)";
	Axisunitfontsize = 20;
	mAxisstyle = AxisBottom;
}
Axis::~Axis()
{

}
/**
* @brief Axis::painEvent 重绘函数
* @param QPainEvent* event  重绘事件指针
* @return void
*/
void Axis::paintEvent(QPaintEvent* event)
{
	//获取窗口的大小
	//QSize clientsize = this->size();
	//获取客户区的长宽
	QPainter mPainter(this);
	if (!lines.empty())
		mPainter.drawLines(lines);
	//画刻度数值
	foreach(AXISVAL i, m_axisval)
		mPainter.drawText(i.postion, i.valsize);
	//画单位
	QFont mfont = mPainter.font();
	mfont.setPixelSize(Axisunitfontsize);
	mPainter.setFont(mfont);
	switch (mAxisstyle)
	{
	case Axisleft:
	{
		mPainter.save();
		mPainter.translate(Axisunit.postion);
		mPainter.rotate(90);
		mPainter.drawText(QPointF(0, 0), Axisunit.valsize);
		mPainter.restore();
	}
		break;
	case AxisRight:
	{
		mPainter.save();
		mPainter.translate(Axisunit.postion);
		mPainter.rotate(-90);
		mPainter.drawText(QPointF(0, 0), Axisunit.valsize);
		mPainter.restore();
	}
		break;
	case AxisTop:
	{
		mPainter.drawText(Axisunit.postion, Axisunit.valsize);
	}
		break;
	case AxisBottom:
	{
		mPainter.drawText(Axisunit.postion, Axisunit.valsize);
	}
		break;
	}
}

/**
* @brief Axis::_update 刷新函数
* @return void
*/
void Axis::_update()
{
	//是否需要调整大小
	lines = Getlines(mAxisstyle, AxisRect);

	getAxisVal(mAxisstyle, AxisRect);
	GetAxisUnit(mAxisstyle, AxisRect);
	update();
}
/**
* @brief Axis::setAxixStyle 设置刻度种类
* @param Axisstyle _Axisstyle 刻度方向枚举
* @return void
*/
void Axis::setAxixStyle(Axisstyle _Axisstyle)
{
	mAxisstyle = _Axisstyle;
}
/**
* @brief Axis::setAxisText 设置刻度单位符号
* @param QString AxisUnitTest 包含刻度的单位的字符串
* @param int fontsize 单位的字体大小
* @return void
*/
void Axis::setAxisText(QString AxisUnitText, int fontsize){
	mAxisunit = AxisUnitText;//单位
	Axisunitfontsize = fontsize;//字体大小
}
/**
* @brief Axis::setAxisRange 设置刻度的数值区间
* @param double min 数值区间的最小值
* @param double max 数值区间的最大值
* @return void
*/
void Axis::setAxisRange(double min, double max){
	axisvalrange.min = min;
	axisvalrange.max = max;
}
/**
* @brief Axis::SetAxisNumber 设置大刻度个数
* @param int _Axisnumber 大刻度个数
* @return void
*/
void Axis::SetAxisNumber(int _Axisnumber){
	Axisnumber = _Axisnumber;
}
/**
* @brief Axis::Getlines 获取需要绘制的线段的队列
* @param Axisstyle _Axisstyle 刻度方向的枚举
* @return void
*/
QVector<QLineF> Axis::Getlines(Axisstyle _Axisstyle, QRectF _rect){
	lines.clear();
	//获取线段间隔
	switch (_Axisstyle) {
	case Axisleft:
	{
		//获取间距
		qreal interval = (_rect.height() - 2) / (Axisnumber * 5);
		QPointF startpoint = QPointF(_rect.right() - 1, _rect.bottom() - 1);
		QPointF nextpoint = startpoint;
		for (auto i = 0; i <= Axisnumber * 5; i++)
		{
			QLineF line;
			nextpoint.setY(startpoint.y() - i*interval);
			(i % 5 == 0) ? (line = QLineF(nextpoint.x(), nextpoint.y(), nextpoint.x() - 10, nextpoint.y())) : (line = QLineF(nextpoint.x(), nextpoint.y(), nextpoint.x() - 6, nextpoint.y()));
			lines.push_back(line);
		}
		lines.push_back(QLineF(_rect.right() - 1, _rect.top() + 1, _rect.right() - 1, _rect.bottom() - 1));
	}
		break;
	case AxisRight:
	{
		//获取间距
		qreal interval = (_rect.height() - 2) / (Axisnumber * 5);
		QPointF startpoint = QPointF(_rect.left() + 1, _rect.bottom() - 1);
		QPointF nextpoint = startpoint;
		for (auto i = 0; i <= Axisnumber * 5; i++)
		{
			QLineF line;
			nextpoint.setY(startpoint.y() - interval*i);
			(i % 5 == 0) ? (line = QLineF(nextpoint.x(), nextpoint.y(), nextpoint.x() + 10, nextpoint.y())) : (line = QLineF(nextpoint.x(), nextpoint.y(), nextpoint.x() + 6, nextpoint.y()));
			lines.push_back(line);
		}
		lines.push_back(QLineF(_rect.left() + 1, _rect.top() + 1, _rect.left() + 1, _rect.bottom() - 1));
	}
		break;

	case AxisTop:
	{
		qreal interval = (_rect.width() - 2) / (Axisnumber * 5);
		QPointF startpoint = QPointF(_rect.left() + 1, _rect.bottom() - 1);
		QPointF nextpoint = startpoint;
		for (auto i = 0; i <= Axisnumber * 5; i++)
		{
			nextpoint.setX(startpoint.x() + i*interval);
			QLineF line;
			(i % 5 == 0) ? (line = QLineF(nextpoint.x(), nextpoint.y(), nextpoint.x(), nextpoint.y() - 10)) : (line = QLineF(nextpoint.x(), nextpoint.y(), nextpoint.x(), nextpoint.y() - 6));
			lines.push_back(line);
		}
		lines.push_back(QLineF(_rect.left() + 1, _rect.bottom() - 1, _rect.right() - 1, _rect.bottom() - 1));
	}
		break;
	case AxisBottom:
	{
		qreal interval = (_rect.width() - 2) / (Axisnumber * 5);
		QPointF startpoint = QPointF(_rect.left() + 1, _rect.top() + 1);
		QPointF nextpoint = startpoint;
		for (auto i = 0; i <= Axisnumber * 5; i++)
		{
			nextpoint.setX(startpoint.x() + i*interval);
			QLineF line;
			(i % 5 == 0) ? (line = QLineF(nextpoint.x(), nextpoint.y(), nextpoint.x(), nextpoint.y() + 10)) : (line = QLineF(nextpoint.x(), nextpoint.y(), nextpoint.x(), nextpoint.y() + 6));
			lines.push_back(line);
		}
		lines.push_back(QLineF(_rect.left() + 1, _rect.top() + 1, _rect.right() - 1, _rect.top() + 1));
	}
		break;
	}
	return lines;
}
/**
* @brief Axis::getAxisVal 获取需要绘制的刻度的数值
* @param Axisstyle _Axisstyle 刻度的方向枚举
* @param QRecF _rect 包含整个刻度的矩形空间
* @return QVector<AXISVAL> 包含所有的需要绘制的刻度数值和位置信息队列
*/
QVector<AXISVAL> Axis::getAxisVal(Axisstyle _Axisstyle, QRectF _rect)
{
	m_axisval.clear();
	qreal interval = (axisvalrange.max - axisvalrange.min) / (Axisnumber);
	qreal Axisinterval;
	QVector<QString> _axisval = GetScientific_notation();
	switch (_Axisstyle)
	{
	case Axisleft:
	{
		Axisinterval = (_rect.height() - 2) / (Axisnumber);
		qreal startval = axisvalrange.min;
		qreal nextval = startval;
		QPointF startposition = QPointF(_rect.right() - 11, _rect.bottom() + 4);
		QPointF nextPosition = startposition;
		/***************************************************************/
		//获取左边的方向的刻度数值和位置
		auto func = [&](int number,int maxnumber)->void{
			AXISVAL mmaxisval;
			mmaxisval.valsize = _axisval[number]; /*QString("%1").arg(startval + number*interval)*/;
			if (number>0&&number<maxnumber)
			{
				mmaxisval.postion = QPointF(startposition.x() - mmaxisval.valsize.length() * 5 - 5, startposition.y() - number*Axisinterval);
			}
			else if (0==number)
			{
				mmaxisval.postion = QPointF(startposition.x() - mmaxisval.valsize.length() * 5 - 5, startposition.y() - number*Axisinterval - 5);
			}
			else{
				mmaxisval.postion = QPointF(startposition.x() - mmaxisval.valsize.length() * 5 - 5, startposition.y() - number*Axisinterval+5);
			}
			m_axisval.push_back(mmaxisval);
		};
		/***************************************************************/
		
		for (auto i = 0; i <= Axisnumber; i++)
			func(i,Axisnumber);
		//刻度开始的地方---需要往右挪动

	}
		break;
	case AxisRight:
	{
		Axisinterval = (_rect.height() - 2) / (Axisnumber);
		qreal startval = axisvalrange.min;
		qreal nextval = startval;
		QPointF startposition = QPointF(_rect.left() + 11, _rect.bottom() + 4);
		QPointF nextPosition = startposition;
		/**************************************************************************/
		//lambda(记录刻度文字与相对的布局的坐标位置)
		auto func = [&](int number,int maxnumber)->void{
			AXISVAL mmaxisval;
			mmaxisval.valsize = _axisval[number];/*QString("%1").arg(startval + number*interval)*/;
			if (number > 0 && number < maxnumber)
				mmaxisval.postion = QPointF(startposition.x(), startposition.y() - number*Axisinterval);
			else if (0 == number)
				mmaxisval.postion = QPointF(startposition.x(), startposition.y() - number*Axisinterval - 5);
			else
				mmaxisval.postion = QPointF(startposition.x(), startposition.y() - number*Axisinterval - 5);
			m_axisval.push_back(mmaxisval);
		};
		/**************************************************************************/

		for (auto i = 0; i <= Axisnumber; i++)
			func(i,Axisnumber);
		//第一个刻度和最后的一个刻度需要移动位置

	}
		break;
	case AxisTop:
	{
		Axisinterval = (_rect.width() - 2) / (Axisnumber);
		qreal startval = axisvalrange.min;
		QPointF startposition = QPointF(_rect.left() + 1, _rect.bottom() - 10);
		QPointF nextPosition = startposition;
		
		/***********************************************************************/
		//获取AxisTop风格的刻度值以及坐标位置
		auto func = [&](int number,int maxNumber)->void{
			nextPosition.setX(startposition.x() + number*Axisinterval);
			AXISVAL mmaxisval;
			mmaxisval.valsize =_axisval[number] /*QString("%1").arg(startval + number*interval)*/;
			if (number<maxNumber&& number>0)
			{
				mmaxisval.postion = QPointF(nextPosition.x() - mmaxisval.valsize.length() * 10 / 4, startposition.y());
			}
			else if (number==0)
			{
				mmaxisval.postion = QPointF(nextPosition.x(), startposition.y());
			}
			else
			{
				mmaxisval.postion = QPointF(nextPosition.x() - mmaxisval.valsize.length()*10/2,startposition.y());
			}
			m_axisval.push_back(mmaxisval);
		};
		/************************************************************************/

		for (auto i = 0; i <= Axisnumber; i++)
			func(i,Axisnumber);
		//第一个刻度和最后一个刻度需要移动位置
	}
		break;
	case AxisBottom:
	{
		Axisinterval = (_rect.width() - 2) / (Axisnumber);
		qreal startval = axisvalrange.min;
		QPointF startposition = QPointF(_rect.left() + 1, _rect.top() + 20);
		QPointF nextPosition = startposition;

		/*************************************************************************/
		//存储AxisBottom方向的刻度值以及坐标
		auto func = [&](int number,int maxnumber)->void{
			nextPosition.setX(startposition.x() + number*Axisinterval);
			AXISVAL mmaxisval;
			mmaxisval.valsize = _axisval[number]; /*QString("%1").arg(startval + number*interval)*/;
			if (number>0 &&number<maxnumber)
			{
				mmaxisval.postion = QPointF(nextPosition.x() - mmaxisval.valsize.length() * 10 / 4, startposition.y());
			}
			else if (0==number)
			{
				mmaxisval.postion = QPointF(nextPosition.x(), startposition.y());
			}
			else
			{
				mmaxisval.postion = QPointF(nextPosition.x() - mmaxisval.valsize.length() * 10 / 2, startposition.y());
			}
			m_axisval.push_back(mmaxisval);
		};
		/************************************************************************/

		for (auto i = 0; i <= Axisnumber; i++)
			func(i,Axisnumber);
		//第一刻度和最后一个刻度需要移动位置
	}
		break;
	}
	return m_axisval;
}
/**
* @brief Axis::GetAxisUnit 获取重绘刻度单位的相关信息
* @param Axisstyle _Axisstyle 刻度的方向枚举
* @param QRectF _rect 包含整个刻度的矩形空间
* @return AXISVAL 返回重绘刻度单位的相关信息
*/
AXISVAL Axis::GetAxisUnit(Axisstyle _Axisstyle, QRectF _rect){
	QRectF __rect;
	switch (_Axisstyle)
	{
	case Axisleft:
	{
		__rect.setLeft(_rect.left() + Axisunitfontsize);
		__rect.setRight(__rect.left() + Axisunitfontsize*mAxisunit.length() / 2);
		__rect.setBottom((_rect.top() + _rect.height() / 2) + Axisunitfontsize*mAxisunit.length() / 4);
		__rect.setTop(__rect.bottom() - Axisunitfontsize);
		AXISVAL mmaxisval;
		mmaxisval.valsize = mAxisunit;
		mmaxisval.postion = QPointF(__rect.left(), __rect.bottom());
		Axisunit = mmaxisval;
	}
		break;
	case AxisRight:
	{
		__rect.setRight(_rect.right() - Axisunitfontsize);
		__rect.setLeft(__rect.right() - Axisunitfontsize*mAxisunit.length() / 2);
		__rect.setBottom((_rect.top() + _rect.height() / 2) + Axisunitfontsize*mAxisunit.length() / 4);
		__rect.setTop(__rect.bottom() - Axisunitfontsize);
		AXISVAL mmaxisval;
		mmaxisval.valsize = mAxisunit;
		mmaxisval.postion = QPointF(__rect.right(), __rect.bottom());
		Axisunit = mmaxisval;
	}
		break;
	case AxisTop:
	{
		__rect.setTop(_rect.top());
		__rect.setBottom(__rect.top() + Axisunitfontsize);
		__rect.setLeft((_rect.left() + _rect.width() / 2) - Axisunitfontsize*mAxisunit.length() / 4);
		__rect.setRight(__rect.left() + Axisunitfontsize*mAxisunit.length() / 2);
		AXISVAL mmaxisval;
		mmaxisval.valsize = mAxisunit;
		mmaxisval.postion = QPointF(__rect.left(), __rect.bottom());
		Axisunit = mmaxisval;
	}
		break;
	case AxisBottom:
	{
		__rect.setBottom(_rect.bottom());
		__rect.setTop(__rect.bottom() - Axisunitfontsize);
		__rect.setLeft((_rect.left() + _rect.width() / 2) - Axisunitfontsize*mAxisunit.length() / 4);
		__rect.setRight(__rect.left() + Axisunitfontsize*mAxisunit.length() / 2);
		AXISVAL mmaxisval;
		mmaxisval.valsize = mAxisunit;
		mmaxisval.postion = QPointF(__rect.left(), __rect.bottom());
		Axisunit = mmaxisval;
	}
		break;
	}
	return Axisunit;
}
/**
* @brief Axis::AxisResize 刻度组件的大小调整
* @param bool ada 是否自适应（需要知道画布的大小）
* @param QSize _size 刻度的大小参数，默认为（w=0,h=0）,ada为自适应时不需要填写
* @return void
*/
void Axis::AxisResize(bool ada, QSize _size)
{
	if (CanvasSize != nullptr&& ada)
	{
		switch (mAxisstyle)
		{
		case Axisleft:
		case AxisRight:
		{
			//            this->resize(Axisunitfontsize + 50, CanvasSize->height());
			//AxisRect.setLeft(0);
			//AxisRect.setRight(this->size().width());
			//AxisRect.setTop(10);
			//AxisRect.setBottom(this->size().height() - 10);
		}
			break;
		case AxisTop:
		case AxisBottom:
		{
			//this->resize(CanvasSize->width(), Axisunitfontsize + 50);
			//AxisRect.setLeft(10);
			//AxisRect.setRight(this->size().width() - 10);
			//AxisRect.setTop(0);
			//AxisRect.setBottom(this->size().height());
		}
			break;
		}

	}
	else
		this->resize(_size);

		AxisRect.setLeft(0);
		AxisRect.setTop(0);
		AxisRect.setRight(this->size().width());
		AxisRect.setBottom(this->size().height());

	//	AxisRect.setTopLeft(QPointF(0,0));
	//	AxisRect.setBottomRight(QPointF(this->size().width(),this->size().height()));
}
/**
* @brief Axis::AxisCanvas 传入画布的大小
* @param QSizeF _QSizeF 画布的大小信息
* return void
*/
void Axis::AxisCanvans(QSizeF _QSizeF)
{
	CanvasSize->setWidth(_QSizeF.width());
	CanvasSize->setHeight(_QSizeF.height());
}
/**
* @brief Axis::SetCanvas 传入画布的控件指针
* @param QWidget* mCanvas 画布组件
* @return void
*/
void Axis::SetCanvas(QWidget* mCanvas)
{
	CanvasWidget = mCanvas;
}
/**
* @brief Axis::GetScientific_notation 获取数值-科学计数法
* @return QVector<QString> 
*/
QVector<QString> Axis::GetScientific_notation()
{
	QVector<QString> valstr_list;
	//获取数值区间
	qreal max = axisvalrange.max;
	qreal min = axisvalrange.min;
	//计算每个大刻度之间的间值
	qreal interval = (max - min) / (qreal)Axisnumber;
	QVector<qreal> rang_f;
	if (interval>ZERO_F)//间值大于0
	{
		int index = 0;
		qreal temp_interval = interval;
		int _interval_i=interval;
		//获取整数部分
		while (_interval_i<=0)
		{
			_interval_i = int(temp_interval*=10);
			index++;
		}
		//获取至少要保留的位数index
		if (index<=3)
		{
			//直接装填
			QString _str;
			_str = QString::number(min, 'f', index);
			valstr_list.push_back(_str);
			for (auto i = 1; i < Axisnumber;i++)
			{
				_str = QString::number((min + interval*i), 'f', index);
				valstr_list.push_back(_str);
			}
			_str = QString::number(max,'f',index);
			valstr_list.push_back(_str);
		}
		else
		{
			//当位数大于三位时
			int min_i = (int)min;
			qreal min_f = min;
			int minindex = 0;
			while (min_i==0)
			{
				min_i = int(min_f *= 10);
				minindex++;
			}

			QString _str;
			//获取最小值的有效位
			_str = QString("%1").arg(min, 0, 'E', index-minindex);
			valstr_list.push_back(_str);
			for (auto i = 1; i < Axisnumber;i++)
			{
				qreal nexf = min + interval*i;
				_str = QString("%1").arg(nexf,0,'E',index-minindex);
				valstr_list.push_back(_str);
			}
			_str = QString("%1").arg(max, 0, 'E', index-minindex);
			valstr_list.push_back(_str);
		}
	}
	return valstr_list;
}

void Axis::resizeEvent(QResizeEvent* event)
{
	CanvasSize->setWidth(this->width());
	CanvasSize->setHeight(this->height());
	AxisResize(true);
	_update();
}
#include "moc_Axis.cpp"
