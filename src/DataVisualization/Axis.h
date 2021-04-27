#pragma  once
#include <QWidget>
#include<QVector>
#include <QLineEdit>
enum Axisstyle
{
	Axisleft,
	AxisRight,
	AxisTop,
	AxisBottom
};
typedef struct{
	QString valsize;
	QPointF postion;
}AXISVAL;
typedef struct valrange{
	double min;
	double max;
	valrange& operator =(const valrange& that)
	{
		this->min = that.min;
		this->max = that.max;
		return *this;
	}
}VARRANGE;

class Axis : public QWidget
{
	Q_OBJECT
public:
	explicit Axis(QWidget *parent = nullptr);
	~Axis();
private:
public:
	//添加功能函数
	void setAxisText(QString, int fontsize=20);
	void setAxisRange(double min, double max);
	//设置大刻度个数
	void SetAxisNumber(int);
	void _update();
	void setAxixStyle(Axisstyle);
	void AxisCanvans(QSizeF);
	void SetCanvas(QWidget* mCanvas);
	void AxisResize(bool, QSize _size = QSize(0, 0));
	void autoMinAndMAxSize();
private:
	QVector<QLineF> Getlines(Axisstyle, QRectF);
	QVector<AXISVAL> getAxisVal(Axisstyle, QRectF);
	AXISVAL GetAxisUnit(Axisstyle _Axisstyle, QRectF _rect);
public:
	void paintEvent(QPaintEvent* event);
protected:
	virtual void resizeEvent(QResizeEvent* event)override;
	virtual void mouseDoubleClickEvent(QMouseEvent *event) override;
		//获取科学计数法的字符串
	QVector<QString> GetScientific_notation();
private:
	bool isstart;
	unsigned int Axisnumber;//大刻度个数
	QString mAxisunit;//单位
	int Axisunitfontsize;//单位字体大小
	valrange axisvalrange;//刻度数值区间
	QRectF AxisRect;
	Axisstyle mAxisstyle;
private:
	QVector<QLineF> lines;
	QVector<AXISVAL> m_axisval;
	AXISVAL Axisunit;
	QSizeF* CanvasSize;
	QWidget* CanvasWidget;
	//设置最小宽高
	float minWidth;
	float minHeight;
	//之前的最小宽高
	float lastminWidth;
	float lastminHeight;
private:
	valrange curAxisRang;
	//增加实时取值功能2021/4/27
	QLineEdit* minLineedit;
	QLineEdit* maxLineedit;
	QRectF* minRectf;
	QRectF* maxRectf;


};
