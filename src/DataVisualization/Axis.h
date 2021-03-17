#pragma  once
#include <QWidget>
#include<QString>
typedef struct
{
	double min;
	double max;
}valrange;
enum Axisstyle
{
	Axisleft,
	AxisRight,
	AxisTop,
	AxisBottom
};

class Axis:public QWidget{
public:
	Axis(QWidget* parent = 0);
	~Axis();
public:
	//添加功能函数
	void setAxisText(QString, int fontsize);
	void setAxisRange(double min,double max);
	//设置大刻度个数
	void SetAxisNumber(int);
	//刷新
	void _update();
	//设置刻度风格
	void setAxisStyle(Axisstyle);
public:
	void paintEvent(QPaintEvent* event);
private:
	unsigned int Axisnumber;//大刻度个数
	QString Axisunit;//单位
	int Axisunitfontsize;//单位字体大小
	valrange axisvalrange;//刻度数值区间
	QRectF AxisRect;//刻度所占窗体大小
	Axisstyle mAxisstyle;//刻度风格
};