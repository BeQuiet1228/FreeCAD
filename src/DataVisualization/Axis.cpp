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
#include <QDebug>
#include "AxisLable.h"
#define ZERO_F (0.000000000001f)	//定义浮点数的零
#define DEBUG_EDIT (0)
//局部函数--只限当前cpp内部使用
int getIntegerBits(__int64 data);
QFont GetFont(int size);
QPen GetPen(QColor& rgba, int width);
typedef struct Axisparams{
	//单位字体大小
	int AxisUnitSize;
	//刻度的颜色
	QColor AxisColor;
	//刻度数值的颜色
	QColor AxisValColor;
	//刻度数值大小
	int AxisValSize;
	Axisparams(){
		AxisUnitSize = 20;
		AxisColor = QColor(0,0,0);
		AxisValSize = 10;
		AxisValColor = QColor(0, 0, 0);
	}
}AXISPARAMS;

//配置参数
Axisparams axisParams;
/**
* @brief  Axis::Axis 构造
* @param  QWidget * parent  
* @return   
*/
Axis::Axis(QWidget *parent) :
QWidget(parent)/*,horizontalAxis(0),verticalAxis(0),isstart(false)*/, CanvasWidget(nullptr), minWidth(0.0f), minHeight(0.0f), lastminWidth(0.0f), lastminHeight(0.0f){
	lines.clear();
	m_axisval.clear();
	CanvasSize = new QSizeF(this->width(), this->height());
	Axisnumber = 5;
	mAxisunit = "X(x)";
	mAxisstyle = AxisBottom;
	axisvalrange.min = 0;
	axisvalrange.max = 100;
	mAxisLable=new AxisLable();
	mAxisLable->resize(300,200);
	connect(mAxisLable, SIGNAL(signalCloseEvent()), this, SLOT(axiscloseEvent()));
#if DEBUG_EDIT
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
	//新增刻度单位可修改
	AxisUnitRectf = new QRectF();
	AxisUnitedit = new QLineEdit(this);
	AxisUnitedit->setObjectName("axisunitEdit");
	AxisUnitedit->setStyleSheet(
		"QLineEdit#axisunitEdit{"
		"color:black;"
		"border:1px solid #000000;"
		"border-radius:6px;"
		"}"
		);
	AxisUnitedit->setVisible(false);
	//设置文字居中
	AxisUnitedit->setAlignment(Qt::AlignCenter);
	maxLineedit->setAlignment(Qt::AlignCenter);
	minLineedit->setAlignment(Qt::AlignCenter);
#endif
}
/**
* @brief  Axis::~Axis 析构
* @return   
*/
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
	mPainter.setPen(GetPen(axisParams.AxisColor, 1));
	if (!lines.empty())
		mPainter.drawLines(lines);
	//画刻度数值
	mPainter.setPen(GetPen(axisParams.AxisValColor, 1));
	mPainter.setFont(GetFont(axisParams.AxisValSize));
	foreach(AXISVAL i, m_axisval)
		mPainter.drawText(i.postion, i.valsize);
	//画单位
	QFont mfont = mPainter.font();
	mfont.setPixelSize(axisParams.AxisUnitSize);
	mPainter.setFont(mfont);
	switch (mAxisstyle)
	{
	case Axisleft:
	{
		mPainter.save();
		mPainter.translate(Axisunit.postion);
		mPainter.rotate(-90);
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
#if DEBUG_EDIT
	minLineedit->setVisible(false);
	maxLineedit->setVisible(false);
#endif
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
		qreal interval = (_rect.height()) / (Axisnumber * 5);
		QPointF startpoint = QPointF(_rect.right(), _rect.bottom());
		QPointF nextpoint = startpoint;
		for (auto i = 0; i <= Axisnumber * 5; i++)
		{
			QLineF line;
			nextpoint.setY(startpoint.y() - i*interval);
			(i % 5 == 0) ? (line = QLineF(nextpoint.x(), nextpoint.y(), nextpoint.x() - 10, nextpoint.y())) : (line = QLineF(nextpoint.x(), nextpoint.y(), nextpoint.x() - 5, nextpoint.y()));
			lines.push_back(line);
		}
		lines.push_back(QLineF(_rect.right(), _rect.top(), _rect.right(), _rect.bottom()));
		minWidth = 10;
	}
		break;
	case AxisRight:
	{
		//获取间距
		qreal interval = (_rect.height()) / (Axisnumber * 5);
		QPointF startpoint = QPointF(_rect.left(), _rect.bottom());
		QPointF nextpoint = startpoint;
		for (auto i = 0; i <= Axisnumber * 5; i++)
		{
			QLineF line;
			nextpoint.setY(startpoint.y() - interval*i);
			(i % 5 == 0) ? (line = QLineF(nextpoint.x(), nextpoint.y(), nextpoint.x() + 10, nextpoint.y())) : (line = QLineF(nextpoint.x(), nextpoint.y(), nextpoint.x() + 5, nextpoint.y()));
			lines.push_back(line);
		}
		lines.push_back(QLineF(_rect.left() + 1, _rect.top() + 1, _rect.left() + 1, _rect.bottom() - 1));
		minWidth = 10;
	}
		break;

	case AxisTop:
	{
		qreal interval = (_rect.width()) / (Axisnumber * 5);
		//设置刻度单位得显示门限
		QPointF startpoint = QPointF(_rect.left(), _rect.bottom());
		QPointF nextpoint = startpoint;
		for (auto i = 0; i <= Axisnumber * 5; i++)
		{
			nextpoint.setX(startpoint.x() + i*interval);
			QLineF line;
			(i % 5 == 0) ? (line = QLineF(nextpoint.x(), nextpoint.y(), nextpoint.x(), nextpoint.y() - 10)) : (line = QLineF(nextpoint.x(), nextpoint.y(), nextpoint.x(), nextpoint.y() - 5));
			lines.push_back(line);
		}
		lines.push_back(QLineF(_rect.left(), _rect.bottom(), _rect.right(), _rect.bottom()));
		minHeight = 10;
	}
		break;
	case AxisBottom:
	{
		qreal interval = (_rect.width()) / (Axisnumber * 5);
		//设置刻度单位得显示门限
		QPointF startpoint = QPointF(_rect.left(), _rect.top());
		QPointF nextpoint = startpoint;
		for (auto i = 0; i <= Axisnumber * 5; i++)
		{
			nextpoint.setX(startpoint.x() + i*interval);
			QLineF line;
			(i % 5 == 0) ? (line = QLineF(nextpoint.x(), nextpoint.y(), nextpoint.x(), nextpoint.y() + 10)) : (line = QLineF(nextpoint.x(), nextpoint.y(), nextpoint.x(), nextpoint.y() + 5));
			lines.push_back(line);
		}
		lines.push_back(QLineF(_rect.left(), _rect.top(), _rect.right(), _rect.top()));
		minHeight = 10;
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
	wordfont.setPixelSize(axisParams.AxisValSize);
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
		//减去刻度
		QPointF startposition = QPointF(_rect.right() - 11, _rect.bottom()-1);
		QPointF nextPosition = startposition;
		/***************************************************************/
		//获取左边的方向的刻度数值和位置
		auto func = [&](int number,int maxnumber)->void{
			AXISVAL mmaxisval;
			mmaxisval.valsize = _axisval[number];
			QRect rect = fm.boundingRect(mmaxisval.valsize);
			int mwidth = rect.width();
			if (number>0&&number<maxnumber)
			{
				mmaxisval.postion = QPointF(startposition.x()-mwidth, startposition.y() - number*Axisinterval+rect.height()/2);
			}
			else if (0==number)
			{
				mmaxisval.postion = QPointF(startposition.x() - mwidth, startposition.y() - number*Axisinterval);
#if DEBUG_EDIT
				//获取最小数据的左边范围
				minRectf->setRight(_rect.right() - 11);
				minRectf->setLeft(_rect.left()+1);
				minRectf->setBottom(_rect.bottom()-1);
				minRectf->setTop(minRectf->bottom() - rect.height()*2);
#endif
			}
			else{
				mmaxisval.postion = QPointF(startposition.x() - mwidth, startposition.y() - number*Axisinterval+rect.height());
#if DEBUG_EDIT
				maxRectf->setLeft(_rect.left()+1);
				maxRectf->setRight(_rect.right()-11);
				maxRectf->setBottom(mmaxisval.postion.y()+rect.height());
				maxRectf->setTop(1);
#endif
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
		minWidth = minWidth+rect.width();
	}
		break;
	case AxisRight:
	{
		Axisinterval = (_rect.height() - 2) / (Axisnumber);
		qreal startval = axisvalrange.min;
		qreal nextval = startval;
		QPointF startposition = QPointF(_rect.left() + 11, _rect.bottom());
		QPointF nextPosition = startposition;
		/**************************************************************************/
		//lambda(记录刻度文字与相对的布局的坐标位置)
		auto func = [&](int number,int maxnumber)->void{
			AXISVAL mmaxisval;
			mmaxisval.valsize = _axisval[number];
			QRect rect = fm.boundingRect(mmaxisval.valsize);
			if (number > 0 && number < maxnumber)
				mmaxisval.postion = QPointF(startposition.x(), startposition.y() - number*Axisinterval+rect.height()/2);
			else if (0 == number)
				mmaxisval.postion = QPointF(startposition.x(), startposition.y() - number*Axisinterval);
			else
				mmaxisval.postion = QPointF(startposition.x(), startposition.y() - number*Axisinterval+rect.height());
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
		minWidth = minWidth + rect.width();
	}
		break;
	case AxisTop:
	{
		Axisinterval = (_rect.width() - 2) / (Axisnumber);
		qreal startval = axisvalrange.min;
		QPointF startposition = QPointF(_rect.left() + 1, _rect.bottom() - 11);
		QPointF nextPosition = startposition;
		
		/***********************************************************************/
		//获取AxisTop风格的刻度值以及坐标位置
		auto func = [&](int number,int maxNumber)->void{
			nextPosition.setX(startposition.x() + number*Axisinterval);
			AXISVAL mmaxisval;
			mmaxisval.valsize =_axisval[number] /*QString("%1").arg(startval + number*interval)*/;
			QRect rect = fm.boundingRect(mmaxisval.valsize);
			if (number<maxNumber&& number>0)
			{
				mmaxisval.postion = QPointF(nextPosition.x() - rect.width()/2, startposition.y());
			}
			else if (number==0)
			{
				mmaxisval.postion = QPointF(nextPosition.x(), startposition.y());
			}
			else
			{
				mmaxisval.postion = QPointF(nextPosition.x() - rect.width(), startposition.y());
			}
			m_axisval.push_back(mmaxisval);
		};
		/************************************************************************/

		for (auto i = 0; i <= Axisnumber; i++)
			func(i,Axisnumber);
		//第一个刻度和最后一个刻度需要移动位置
		QRect rect = fm.boundingRect(_axisval[0]);
		minHeight = minHeight + rect.height();
	}
		break;
	case AxisBottom:
	{
		Axisinterval = (_rect.width() - 2) / (Axisnumber);
		qreal startval = axisvalrange.min;
		QPointF startposition = QPointF(_rect.left() + 1, _rect.top() + 11);
		QPointF nextPosition = startposition;
		/*************************************************************************/
		auto func = [&](int number,int maxnumber)->void{
			nextPosition.setX(startposition.x() + number*Axisinterval);
			AXISVAL mmaxisval;
			mmaxisval.valsize = _axisval[number]; /*QString("%1").arg(startval + number*interval)*/;
			QRect rect = fm.boundingRect(mmaxisval.valsize);
			int width = rect.width();
			if (number>0 &&number<maxnumber)
			{
				mmaxisval.postion = QPointF(nextPosition.x()-rect.width()/2, startposition.y()+rect.height());
			}
			else if (0==number)
			{
				mmaxisval.postion = QPointF(nextPosition.x(), startposition.y()+rect.height());
#if DEBUG_EDIT
				minRectf->setLeft(mmaxisval.postion.x());
				minRectf->setRight(minRectf->left()+width*2);
				minRectf->setBottom(mmaxisval.postion.y()+rect.height());
				minRectf->setTop(minRectf->bottom()-rect.height()*2);
#endif
			}
			else
			{
				mmaxisval.postion = QPointF(nextPosition.x()-rect.width(), startposition.y()+rect.height());
#if DEBUG_EDIT
				maxRectf->setRight(nextPosition.x());
				maxRectf->setLeft(maxRectf->right() - width * 2);
				maxRectf->setBottom(mmaxisval.postion.y() + rect.height());
				maxRectf->setTop(minRectf->bottom() - rect.height() * 2);
#endif
			}
			m_axisval.push_back(mmaxisval);
		};
		/************************************************************************/
		for (auto i = 0; i <= Axisnumber; i++)
		{
			func(i, Axisnumber);
		}
		QRect rect = fm.boundingRect(_axisval[0]);
		minHeight = minHeight + rect.height();
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
	wordfont.setPixelSize(axisParams.AxisUnitSize);
	QFontMetrics fm(wordfont);
	QRectF __rect;
	switch (_Axisstyle)
	{
	case Axisleft:
	{
		QRect rect = fm.boundingRect(mAxisunit);
		float width = rect.width();
		float height = rect.height();	
		__rect.setLeft(_rect.right()-minWidth-rect.height());
		__rect.setRight(__rect.left()+rect.width());
		__rect.setBottom((_rect.top() + _rect.bottom())/2+width/2);
		__rect.setTop(__rect.bottom()-height);
		AXISVAL mmaxisval;
		mmaxisval.valsize = mAxisunit;
		mmaxisval.postion = QPointF(__rect.left(), __rect.bottom());
		Axisunit = mmaxisval;
		minWidth = minWidth + rect.height();
		//
#if DEBUG_EDIT
		AxisUnitRectf->setLeft(__rect.left()-height);
		AxisUnitRectf->setRight(AxisUnitRectf->left()+height);
		AxisUnitRectf->setBottom(__rect.bottom());
		AxisUnitRectf->setTop(AxisUnitRectf->bottom()-width);
#endif
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
		//
#if DEBUG_EDIT
		AxisUnitRectf->setLeft(__rect.left());
		AxisUnitRectf->setRight(AxisUnitRectf->left() +rect.height());
		AxisUnitRectf->setTop(__rect.bottom());
		AxisUnitRectf->setBottom(AxisUnitRectf->top() + rect.width());
#endif
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
		//
#if DEBUG_EDIT
		AxisUnitRectf->setLeft(__rect.left());
		AxisUnitRectf->setRight(__rect.right());
		AxisUnitRectf->setTop(__rect.top());
		AxisUnitRectf->setBottom(__rect.bottom());
#endif
	}
		break;
	case AxisBottom:
	{
		QRect rect = fm.boundingRect(mAxisunit);
		__rect.setTop(_rect.top()+minHeight);
		__rect.setBottom(__rect.top()+rect.height());
		__rect.setLeft((_rect.left()+_rect.right())/2-rect.width()/2);
		__rect.setRight(__rect.left()+rect.width());
		AXISVAL mmaxisval;
		mmaxisval.valsize = mAxisunit;
		mmaxisval.postion = QPointF(__rect.left(), __rect.bottom());
		Axisunit = mmaxisval;
		minHeight = minHeight + rect.height();
		//
#if DEBUG_EDIT
		AxisUnitRectf->setLeft(__rect.left());
		AxisUnitRectf->setRight(__rect.right());
		AxisUnitRectf->setTop(__rect.top());
		AxisUnitRectf->setBottom(__rect.bottom());
#endif
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
	AxisRect.setRight(this->size().width()-1);
	AxisRect.setBottom(this->size().height()-1);
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
			(min_bit>=interval_bit) ? (_str = QString("%1").arg(min, min_bit - interval_bit, 'E', 2)) : (_str=QString("%1").arg(min));
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
/**
* @brief  Axis::resizeEvent 自适应函数
* @param  QResizeEvent * event  
* @return void  
*/
void Axis::resizeEvent(QResizeEvent* event)
{
	CanvasSize->setWidth(this->width());
	CanvasSize->setHeight(this->height());
	AxisResize(true);
	_update();
#if DEBUG_EDIT
	if (minLineedit->isVisible())
	{
		minLineedit->resize(QSize(minRectf->width(), minRectf->height()));
		minLineedit->move(QPoint(minRectf->left(), minRectf->top()));
	}
	if (maxLineedit->isVisible())
	{
		maxLineedit->resize(QSize(maxRectf->width(), maxRectf->height()));
		maxLineedit->move(QPoint(maxRectf->left(), maxRectf->top()));
	}
	if (AxisUnitedit->isVisible())
	{
		switch (mAxisstyle)
		{
		case Axisleft:
		case AxisRight:{
			AxisUnitedit->resize(QSize(this->width() - 2, AxisUnitRectf->width()));
			AxisUnitedit->move(1, AxisUnitRectf->center().y() - AxisUnitedit->height() / 2);
		}
			break;
		case AxisTop:
		case AxisBottom:{
			AxisUnitedit->resize(QSize(this->width() / 4, AxisUnitRectf->height()));
			AxisUnitedit->move(QPoint(AxisUnitRectf->center().x() - AxisUnitedit->width() / 2, AxisUnitRectf->top()));
		}break;
		}
	}
#endif
}
/**
* @brief  Axis::autoMinAndMAxSize 设置自动填充大小
* @return void  
*/
void Axis::autoMinAndMAxSize()
{
	QFont wordfont;
	wordfont.setPointSize(axisParams.AxisUnitSize);
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
#if DEBUG_EDIT
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
		else if (AxisUnitRectf->contains(event->posF()))
		{
			if (AxisUnitedit->isVisible()) return;
			switch (mAxisstyle)
			{
			case AxisRight:
			case Axisleft:
			{
				AxisUnitedit->resize(QSize(this->width() - 2, AxisUnitRectf->width()));
				AxisUnitedit->move(1, AxisUnitRectf->center().y() - AxisUnitedit->height() / 2);
			}break;
			case AxisTop:
			case AxisBottom:
			{
				AxisUnitedit->resize(QSize(this->width() / 4, AxisUnitRectf->height()));
				AxisUnitedit->move(QPoint(AxisUnitRectf->center().x() -AxisUnitedit->width()/2, AxisUnitRectf->top()));
			}
				break;
			}
			AxisUnitedit->setText(QString("%1").arg(Axisunit.valsize));
			AxisUnitedit->setVisible(true);
			AxisUnitedit->setFocus();
		}
		else
			axisRangeChange();
	}
#endif
	if (event->button() == Qt::LeftButton)
	{
		if (mAxisLable->isVisible())
		{
			axiscloseEvent();
		}
		else
		{
			mAxisLable->setMinval(QString("%1").arg(axisvalrange.min));
			mAxisLable->setMaxval(QString("%1").arg(axisvalrange.max));
			mAxisLable->setAxisUnitval(QString("%1").arg(Axisunit.valsize));
			mAxisLable->show();

		}
	}
}
/**
* @brief  Axis::keyReleaseEvent 按键事件
* @param  QKeyEvent * event  
* @return void  
*/
void Axis::keyReleaseEvent(QKeyEvent *event)
{
	QWidget::keyPressEvent(event);
	//按下enter键
	if (event->key() == Qt::Key_Return||event->key()==Qt::Key_Enter)
		axisRangeChange();
}
/**
* @brief  Axis::axisRangeChange 刻度区间变化
* @return void  
*/
void Axis::axisRangeChange()
{
#if DEBUG_EDIT
	//刻度值范围发生变化
	{
		if (minLineedit->isVisible() && maxLineedit->isVisible())
		{
			if (minLineedit->text().toFloat() < maxLineedit->text().toFloat())
			{
				curAxisRang.max = maxLineedit->text().toFloat();
				curAxisRang.min = minLineedit->text().toFloat();
			}
			minLineedit->setVisible(false);
			maxLineedit->setVisible(false);
		}
		else if (minLineedit->isVisible())
		{
			if (minLineedit->text().toFloat() < curAxisRang.max)
				curAxisRang.min = minLineedit->text().toFloat();
			minLineedit->setVisible(false);
		}
		else if (maxLineedit->isVisible())
		{
			if (maxLineedit->text().toFloat() > curAxisRang.min)
				curAxisRang.max = maxLineedit->text().toFloat();
			maxLineedit->setVisible(false);
		}
	}
	//刻度的单位发送变化
	{
		if (AxisUnitedit->isVisible())
		{
			mAxisunit = AxisUnitedit->text();
			_update();
			AxisUnitedit->setVisible(false);
		}
	}
	if (curAxisRang != axisvalrange)
	{
		emit sendAxisRang(curAxisRang.min, curAxisRang.max);
		axisvalrange = curAxisRang;
		_update();
	}
#endif
}
/**
* @brief  Axis::loadconfig 读取配置
* @return void  
*/
void Axis::loadconfig()
{
	if (Config::GetInstance()->loadConfig())
	{
		auto Group = Config::GetInstance()->getRootGroup();
		auto axisGroup = Group.getGroup("axis");
		//获取刻度颜色
		axisParams.AxisColor = QStringToQColor(QString::fromStdString(axisGroup.getGroup("axisColor").getValue("value")));
		int UnitSize = atoi(axisGroup.getGroup("axisSize").getValue("value").c_str());
		axisParams.AxisValColor = QStringToQColor(QString::fromStdString(axisGroup.getGroup("axisvalColor").getValue("value")));
		axisParams.AxisUnitSize = UnitSize;
		axisParams.AxisValSize = atoi(axisGroup.getGroup("axisvalSize").getValue("value").c_str());
		axisParams.AxisValSize = ((axisParams.AxisValSize < 10) ? 10 : (axisParams.AxisValSize));
	}
}
void Axis::axiscloseEvent()
{
	valrange temp;
	temp.min = mAxisLable->getMinval();
	temp.max = mAxisLable->getMaxval();
	if (temp != axisvalrange && temp.min <= temp.max)
	{
		emit sendAxisRang(temp.min, temp.max);
		axisvalrange = temp;
	}
	mAxisunit = mAxisLable->getAxisUnitval();
	mAxisLable->hide();
	_update();
}
/**
* @brief  GetPen 获取画笔
* @param  QColor & rgba  
* @param  int width  
* @return QT_NAMESPACE::QPen  
*/
QPen GetPen(QColor& rgba,int width)
{
	QPen pen(rgba);
	pen.setWidth(width);
	return pen;
}
/**
* @brief  GetFont  获取字体
* @param  QColor & color  
* @param  int size  
* @return QT_NAMESPACE::QFont  
*/
QFont GetFont(int size)
{
	QFont mfont;
	mfont.setPixelSize(size);
	return mfont;
}

#include "moc_Axis.cpp"
