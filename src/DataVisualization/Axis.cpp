#include "axis.h"
#include<QRect>
#include<QSize>
#include<QPainter>
#include<QMouseEvent>
#include <QRegExp>
#include <QValidator>
#include <QRegExpValidator>
#include "CustomConfig.h"
#include "C_encoding.h"
#define ZERO_F (0.000000000001f)	//定义浮点数的零
//局部函数--只限当前cpp内部使用
int getIntegerBits(__int64 data);

Axis::Axis(QWidget *parent) :
QWidget(parent)/*,horizontalAxis(0),verticalAxis(0),isstart(false)*/, CanvasWidget(nullptr), minWidth(0.0f), minHeight(0.0f), lastminWidth(0.0f), lastminHeight(0.0f){
	lines.clear();
	m_axisval.clear();
	CanvasSize = new QSizeF(this->width(), this->height());
	Axisnumber = 5;
	mAxisunit = "X(x)";
	Axisunitfontsize = 20;
	mAxisstyle = AxisBottom;
	axisvalrange.min = 0;
	axisvalrange.max = 100;
	//正则表达式---只能输入数值
	QRegExp rx("^(-?|\\d)(\\d+)?(\\.\\d+)?$");
	QValidator * validator = new QRegExpValidator(rx, this);
	minLineedit=new QLineEdit(this);
	minLineedit->setValidator(validator);
	minLineedit->setVisible(false);
	maxLineedit=new QLineEdit(this);
	maxLineedit->setValidator(validator);
	maxLineedit->setVisible(false);
	//设置样式
	minLineedit->setObjectName("minLineEdit");
	minLineedit->setStyleSheet(
		"QLineEdit#minLineEdit{"
		"color:blue;"
		"border:1px solid #0000ff;"
		"border-radius:6px;"
		"}");
	maxLineedit->setObjectName("maxLineEdit");
	maxLineedit->setStyleSheet(
		"QLineEdit#maxLineEdit{"
		"color:red;"
		"border:1px solid #ff0000;"
		"border-radius:6px;"
		"}"
		);
	minRectf=new QRectF();
	maxRectf=new QRectF();
	curAxisRang=axisvalrange;
	//新增读取配置
	axisColor = Qt::black;
	axisvalColor = Qt::black;
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
	QPainter mPainter(this);
	QPen lastpen = mPainter.pen();
	mPainter.setPen(GetPen(axisColor, 1));
	if (!lines.empty())
		mPainter.drawLines(lines);
	//画刻度数值
	mPainter.setPen(GetPen(axisvalColor, 1));
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
		mPainter.rotate(90);
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
	loadconfig();
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
void Axis::setAxisText(QString AxisUnitText){
	mAxisunit = AxisUnitText;//单位
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
	curAxisRang = axisvalrange;
	minLineedit->setVisible(false);
	maxLineedit->setVisible(false);
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
			(i % 5 == 0) ? (line = QLineF(nextpoint.x(), nextpoint.y(), nextpoint.x() - 10, nextpoint.y())) : (line = QLineF(nextpoint.x(), nextpoint.y(), nextpoint.x() - 5, nextpoint.y()));
			lines.push_back(line);
		}
		lines.push_back(QLineF(_rect.right() - 1, _rect.top() + 1, _rect.right() - 1, _rect.bottom() - 1));
		minWidth = 11;
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
			(i % 5 == 0) ? (line = QLineF(nextpoint.x(), nextpoint.y(), nextpoint.x() + 10, nextpoint.y())) : (line = QLineF(nextpoint.x(), nextpoint.y(), nextpoint.x() + 5, nextpoint.y()));
			lines.push_back(line);
		}
		lines.push_back(QLineF(_rect.left() + 1, _rect.top() + 1, _rect.left() + 1, _rect.bottom() - 1));
		minWidth = 11;
	}
		break;

	case AxisTop:
	{
		qreal interval = (_rect.width() - 2) / (Axisnumber * 5);
		//设置刻度单位得显示门限
		QPointF startpoint = QPointF(_rect.left() + 1, _rect.bottom() - 1);
		QPointF nextpoint = startpoint;
		for (auto i = 0; i <= Axisnumber * 5; i++)
		{
			nextpoint.setX(startpoint.x() + i*interval);
			QLineF line;
			(i % 5 == 0) ? (line = QLineF(nextpoint.x(), nextpoint.y(), nextpoint.x(), nextpoint.y() - 10)) : (line = QLineF(nextpoint.x(), nextpoint.y(), nextpoint.x(), nextpoint.y() - 5));
			lines.push_back(line);
		}
		lines.push_back(QLineF(_rect.left() + 1, _rect.bottom() - 1, _rect.right() - 1, _rect.bottom() - 1));
		minHeight = 11;
	}
		break;
	case AxisBottom:
	{
		qreal interval = (_rect.width() - 2) / (Axisnumber * 5);
		//设置刻度单位得显示门限
		QPointF startpoint = QPointF(_rect.left() + 1, _rect.top() + 1);
		QPointF nextpoint = startpoint;
		for (auto i = 0; i <= Axisnumber * 5; i++)
		{
			nextpoint.setX(startpoint.x() + i*interval);
			QLineF line;
			(i % 5 == 0) ? (line = QLineF(nextpoint.x(), nextpoint.y(), nextpoint.x(), nextpoint.y() + 10)) : (line = QLineF(nextpoint.x(), nextpoint.y(), nextpoint.x(), nextpoint.y() + 5));
			lines.push_back(line);
		}
		lines.push_back(QLineF(_rect.left() + 1, _rect.top() + 1, _rect.right() - 1, _rect.top() + 1));
		minHeight = 11;
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
	//获取宽高
	int maxlenaxisval = 0;
	QString max_val;
	QFont wordfont;
	wordfont.setPointSize(10);
	QFontMetrics fm(wordfont);
	m_axisval.clear();
	qreal interval = (axisvalrange.max - axisvalrange.min) / (Axisnumber);
	qreal Axisinterval;
	QVector<QString> _axisval = GetScientific_notation();
	
	//获取最大的刻度字符
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
			QRect rect = fm.boundingRect(mmaxisval.valsize);
			int mwidth = rect.width() + 10;
			if (number>0&&number<maxnumber)
			{
				mmaxisval.postion = QPointF(startposition.x()-mwidth, startposition.y() - number*Axisinterval);
			}
			else if (0==number)
			{
				mmaxisval.postion = QPointF(startposition.x() - mwidth, startposition.y() - number*Axisinterval - 5);
				//获取最小数据的左边范围
				minRectf->setRight(_rect.right() - 11);
				minRectf->setLeft(_rect.left()+1);
				minRectf->setBottom(_rect.bottom()-1);
				minRectf->setTop(minRectf->bottom() - rect.height()*2);
			}
			else{
				mmaxisval.postion = QPointF(startposition.x() - mwidth, startposition.y() - number*Axisinterval+5);
				maxRectf->setLeft(_rect.left()+1);
				maxRectf->setRight(_rect.right()-11);
				maxRectf->setBottom(mmaxisval.postion.y()+rect.height());
				maxRectf->setTop(1);
			}
			m_axisval.push_back(mmaxisval);
		};
		/***************************************************************/
		for (auto i = 0; i <= Axisnumber; i++)
		{
			func(i, Axisnumber);
			if (_axisval[i].length()>maxlenaxisval)
			{
				maxlenaxisval = _axisval[i].length();
				max_val = _axisval[i];
			}
		}
		//获取到最大的像素
		QRect rect = fm.boundingRect(max_val);
		minWidth = minWidth+rect.width() + 10;
	}
		break;
	case AxisRight:
	{
		Axisinterval = (_rect.height() - 2) / (Axisnumber);
		qreal startval = axisvalrange.min;
		qreal nextval = startval;
		QPointF startposition = QPointF(_rect.left() + 11, _rect.bottom()+4);
		QPointF nextPosition = startposition;
		/**************************************************************************/
		//lambda(记录刻度文字与相对的布局的坐标位置)
		auto func = [&](int number,int maxnumber)->void{
			AXISVAL mmaxisval;
			mmaxisval.valsize = _axisval[number];/*QString("%1").arg(startval + number*interval)*/;
			QRect rect = fm.boundingRect(mmaxisval.valsize);
			if (number > 0 && number < maxnumber)
				mmaxisval.postion = QPointF(startposition.x(), startposition.y() - number*Axisinterval);
			else if (0 == number)
				mmaxisval.postion = QPointF(startposition.x(), startposition.y() - number*Axisinterval - 5);
			else
				mmaxisval.postion = QPointF(startposition.x(), startposition.y() - number*Axisinterval +5);
			m_axisval.push_back(mmaxisval);
		};
		/**************************************************************************/

		for (auto i = 0; i <= Axisnumber; i++)
		{
			func(i, Axisnumber);
			if (_axisval[i].length()>maxlenaxisval)
			{
				max_val = _axisval[i];
				maxlenaxisval = _axisval[i].length();
			}
		}
		QRect rect = fm.boundingRect(max_val);
		minWidth = minWidth + rect.width() + 10;
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
			QRect rect = fm.boundingRect(mmaxisval.valsize);
			float width = rect.width()+10;
			if (number<maxNumber&& number>0)
			{
				mmaxisval.postion = QPointF(nextPosition.x() - width/2, startposition.y());
			}
			else if (number==0)
			{
				mmaxisval.postion = QPointF(nextPosition.x(), startposition.y());
			}
			else
			{
				mmaxisval.postion = QPointF(nextPosition.x() - width, startposition.y());
			}
			m_axisval.push_back(mmaxisval);
		};
		/************************************************************************/

		for (auto i = 0; i <= Axisnumber; i++)
			func(i,Axisnumber);
		//第一个刻度和最后一个刻度需要移动位置
		QRect rect = fm.boundingRect(_axisval[0]);
		minHeight = minHeight + rect.height()+10;
	}
		break;
	case AxisBottom:
	{
		Axisinterval = (_rect.width() - 2) / (Axisnumber);
		qreal startval = axisvalrange.min;
		QPointF startposition = QPointF(_rect.left() + 1, _rect.top() + 20);
		QPointF nextPosition = startposition;
		/*************************************************************************/
		auto func = [&](int number,int maxnumber)->void{
			nextPosition.setX(startposition.x() + number*Axisinterval);
			AXISVAL mmaxisval;
			mmaxisval.valsize = _axisval[number]; /*QString("%1").arg(startval + number*interval)*/;
			QRect rect = fm.boundingRect(mmaxisval.valsize);
			int width = rect.width()+10;
			if (number>0 &&number<maxnumber)
			{
				mmaxisval.postion = QPointF(nextPosition.x() -width/2, startposition.y());
			}
			else if (0==number)
			{
				mmaxisval.postion = QPointF(nextPosition.x(), startposition.y());
				minRectf->setLeft(mmaxisval.postion.x());
				minRectf->setRight(minRectf->left()+width*2);
				minRectf->setBottom(mmaxisval.postion.y()+rect.height());
				minRectf->setTop(minRectf->bottom()-rect.height()*2);
			}
			else
			{
				mmaxisval.postion = QPointF(nextPosition.x() - width, startposition.y());
				maxRectf->setRight(nextPosition.x());
				maxRectf->setLeft(maxRectf->right() - width * 2);
				maxRectf->setBottom(mmaxisval.postion.y() + rect.height());
				maxRectf->setTop(minRectf->bottom() - rect.height() * 2);
			}
			m_axisval.push_back(mmaxisval);
		};
		/************************************************************************/
		for (auto i = 0; i <= Axisnumber; i++)
		{
			func(i, Axisnumber);
		}
		QRect rect = fm.boundingRect(_axisval[0]);
		minHeight = minHeight + rect.height()+10;
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
	
	QFont wordfont;
	//wordfont.setFamily(“宋体”);
	wordfont.setPointSize(Axisunitfontsize);
	QFontMetrics fm(wordfont);
	QRectF __rect;
	switch (_Axisstyle)
	{
	case Axisleft:
	{
		QRect rect = fm.boundingRect(mAxisunit);
		float width = rect.width();
		float height = rect.height();	
		__rect.setLeft(_rect.right()-minWidth-20);
		__rect.setRight(__rect.left()+rect.width());
		__rect.setTop((_rect.top() + _rect.bottom()) / 2 - width / 2);
		__rect.setBottom(__rect.top()+height);
		AXISVAL mmaxisval;
		mmaxisval.valsize = mAxisunit;
		mmaxisval.postion = QPointF(__rect.left(), __rect.bottom());
		Axisunit = mmaxisval;
		minWidth = minWidth + rect.height();
	}
		break;
	case AxisRight:
	{
		QRect rect = fm.boundingRect(mAxisunit);	
		__rect.setLeft(_rect.left()+minWidth);
		__rect.setRight(__rect.left()+rect.width());
		__rect.setTop((_rect.top()+_rect.bottom())/2-rect.width()/2);
		__rect.setBottom(__rect.top()+rect.height());
		AXISVAL mmaxisval;
		mmaxisval.valsize = mAxisunit;
		mmaxisval.postion = QPointF(__rect.left(), __rect.bottom());
		Axisunit = mmaxisval;
		minWidth = minWidth + rect.height();
	}
		break;
	case AxisTop:
	{
		QRect rect = fm.boundingRect(mAxisunit);
		__rect.setBottom(_rect.bottom()-minHeight); 
		__rect.setTop(__rect.bottom()-rect.height());
		__rect.setLeft((_rect.left() + _rect.right())/2-rect.width()/2);
		__rect.setRight(__rect.left()+rect.width());
		AXISVAL mmaxisval;
		mmaxisval.valsize = mAxisunit;
		mmaxisval.postion = QPointF(__rect.left(), __rect.bottom());
		Axisunit = mmaxisval;
		minHeight = minHeight + rect.height();
	}
		break;
	case AxisBottom:
	{
		QRect rect = fm.boundingRect(mAxisunit);
		__rect.setTop(_rect.top()+minHeight+10);
		__rect.setBottom(__rect.top()+rect.height());
		__rect.setLeft((_rect.left()+_rect.right())/2-rect.width()/2);
		__rect.setRight(__rect.left()+rect.width());
		AXISVAL mmaxisval;
		mmaxisval.valsize = mAxisunit;
		mmaxisval.postion = QPointF(__rect.left(), __rect.top());
		Axisunit = mmaxisval;
		minHeight = minHeight + rect.height();
	}
		break;
	}
	if (minHeight!=lastminHeight ||minWidth!=lastminWidth)
	{
		this->setMinimumSize(QSize(minWidth,minHeight));
		lastminHeight = minHeight;
		lastminWidth = minWidth;
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
	AxisRect.setLeft(0);
	AxisRect.setTop(0);
	AxisRect.setRight(this->size().width());
	AxisRect.setBottom(this->size().height());
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
	//这里增加获取宽高
	QVector<QString> valstr_list;
	//获取数值区间
	qreal max = axisvalrange.max;
	qreal min = axisvalrange.min;
	//计算每个大刻度之间的间值
	qreal interval = (max - min) / (qreal)Axisnumber;
	QVector<qreal> rang_f;
#pragma region 计算方式
	if (interval>ZERO_F)//间值大于0
	{
		int index = 0;
		double temp_interval = interval;
		__int64 _interval_i=interval;
		//获取整数部分
		while (_interval_i<=0)
		{
			if (temp_interval==0)
			{
				break;
			}
			_interval_i = __int64(temp_interval*=10);
			index++;
		}
		//获取至少要保留的位数index
		if (index>0&&index<=3)
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
		else if (index>3)
		{
			//当位数大于三位时
			int min_i = (int)min;
			qreal min_f = abs(min);
			int minindex = 0;
			if (min_f!=0.0f)
			{
				while (min_i == 0)
				{
					min_i = int(min_f *= 10);
					minindex++;
				}
			}
			QString _str;
			//获取最小值的有效位
			_str = QString("%1").arg(min, 0, 'E', abs(index - minindex));
			valstr_list.push_back(_str);
			for (auto i = 1; i < Axisnumber;i++)
			{
				qreal nexf = min + interval*i;
				_str = QString("%1").arg(nexf, 0, 'E', abs(index - minindex));
				valstr_list.push_back(_str);
			}
			_str = QString("%1").arg(max, 0, 'E', abs(index - minindex));
			valstr_list.push_back(_str);
		}
		else
		{
			//间值大于0，需要进行判断
			int interval_bit = getIntegerBits((__int64)interval);
			int min_bit = getIntegerBits((__int64)min);
			QString _str;
			(min_bit>interval_bit) ? (_str = QString("%1").arg(min, min_bit - interval_bit, 'E', 2)) : (_str=QString("%1").arg(min));
			valstr_list.push_back(_str);
			for (auto i = 1; i < Axisnumber; i++)
			{
				float curval = min + interval*i;
				int curval_bit = getIntegerBits((__int64)curval);
				_str = QString("%1").arg((min + interval*i),curval_bit-interval_bit, 'E',2);
				valstr_list.push_back(_str);
			}
			_str = QString("%1").arg(max,2,'E',1);
			valstr_list.push_back(_str);
		}
	}
	else
	{
		int min_int = getIntegerBits((__int64)min);
		QString str;
		if (min_int < 4)
			str = QString("%1").arg(min);
		else
			str = QString("%1").arg(min,0,'E',2);
		for (auto i = 0; i < Axisnumber+1;i++)
			valstr_list.push_back(str);
	}
#pragma endregion
	return valstr_list;
}
void Axis::resizeEvent(QResizeEvent* event)
{
	CanvasSize->setWidth(this->width());
	CanvasSize->setHeight(this->height());
	AxisResize(true);
	_update();
	minLineedit->resize(QSize(minRectf->width(),minRectf->height()));
	minLineedit->move(QPoint(minRectf->left(),minRectf->top()));
	maxLineedit->resize(QSize(maxRectf->width(),maxRectf->height()));
	maxLineedit->move(QPoint(maxRectf->left(),maxRectf->top()));
}
void Axis::autoMinAndMAxSize()
{
	QFont wordfont;
	wordfont.setPointSize(Axisunitfontsize);
	QFontMetrics fm(wordfont);
	QRect rect = fm.boundingRect(mAxisunit);
	switch (mAxisstyle)
	{
	case Axisleft:
	case AxisRight:
	{
		minHeight = rect.width()*Axisnumber;
		minWidth = 100;
	}
		break;
	case AxisTop:
	case AxisBottom:
	{
		minWidth = rect.width()*Axisnumber;
		minHeight = 60;
	}
		
		break;
	}
	this->setMaximumSize(QSize(16777215, 16777215));
	this->setMinimumSize(QSize(minWidth, minHeight));
}
/**
* @brief getIntegerBits 获取整数的位数
* @param __int64& data 数据
* @return int
*/
int getIntegerBits(__int64 data)
{
	__int64  tempdata = abs(data);
	int index;
	for (index = 0;tempdata>0;index++)
	{
		tempdata /= 10;
	}
	return index;
}
/**
* @brief Axis::mouseDoubleClickEvent 鼠标双击
* @param QMouseEvent *event
* @return void
*/
void Axis::mouseDoubleClickEvent(QMouseEvent *event){
	QWidget::mouseDoubleClickEvent(event);
#ifdef MY_DEBUG
	printf("x=%f,y=%f\n",event->posF().x(),event->posF().y());
	printf("minRectf\n");
	printf("left=%f,top=%f,right=%f,bottom=%f",minRectf->left(),minRectf->top(),minRectf->right(),minRectf->bottom());
#endif
	if (event->button()==Qt::LeftButton)
	{
		if (minRectf->contains(event->posF()))
		{
			minLineedit->resize(QSize(minRectf->width(),minRectf->height()));
			minLineedit->move(QPoint(minRectf->left(),minRectf->top()));
			minLineedit->setText(QString("%1").arg(axisvalrange.min));
			minLineedit->setVisible(true);
			minLineedit->setFocus();
		}
		else if (maxRectf->contains(event->posF()))
		{
			maxLineedit->resize(QSize(maxRectf->width(), maxRectf->height()));
			maxLineedit->move(QPoint(maxRectf->left(),maxRectf->top()));
			maxLineedit->setText(QString("%1").arg(axisvalrange.max));
			maxLineedit->setVisible(true);
			maxLineedit->setFocus();
		}
		else
			axisRangeChange();
	}
}
void Axis::keyReleaseEvent(QKeyEvent *event)
{
	QWidget::keyPressEvent(event);
	//按下enter键
	if (event->key() == Qt::Key_Return||event->key()==Qt::Key_Enter)
		axisRangeChange();
}
void Axis::axisRangeChange()
{
	if (minLineedit->isVisible())
	{
		curAxisRang.min = minLineedit->text().toFloat();
		minLineedit->setVisible(false);
	}
	if (maxLineedit->isVisible())
	{
		curAxisRang.max = maxLineedit->text().toFloat();
		maxLineedit->setVisible(false);
	}
	if (curAxisRang != axisvalrange)
	{
		emit sendAxisRang(curAxisRang.min, curAxisRang.max);
		axisvalrange = curAxisRang;
		_update();
	}
}
void Axis::loadconfig()
{
	Config::GetInstance()->loadConfig();
	auto Group = Config::GetInstance()->getRootGroup();
	auto axisGroup = Group.getGroup("axis");
	//获取刻度颜色
	axisColor = QStringToQColor(QString::fromStdString(axisGroup.getValue("axisColor")));
	int UnitSize = atoi(axisGroup.getValue("axisSize").c_str());
#ifdef MY_DEBUG
	printf("UnitSize---%d\n",UnitSize);
#endif // MY_DEBUG

	axisvalColor = QStringToQColor(QString::fromStdString(axisGroup.getValue("axisvalColor")));
	Axisunitfontsize = UnitSize;
}
QPen Axis::GetPen(QColor& rgba,int width)
{
	QPen pen(rgba);
	pen.setWidth(width);
	return pen;
}
#include "moc_Axis.cpp"
