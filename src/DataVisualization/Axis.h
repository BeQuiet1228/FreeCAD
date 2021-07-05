#pragma  once
#include <QWidget>
enum Axisstyle
{
	Axisleft,
	AxisRight,
	AxisTop,
	AxisBottom
};
typedef struct valrange{
	double min;
	double max;
	valrange& operator =(const valrange& that)
	{
		this->min = that.min;
		this->max = that.max;
		return *this;
	}
	bool operator !=(const valrange& that)
	{
		return !((this->min == that.min) && (this->max == that.max));
	}
}VARRANGE;

class QGridLayout;
class ScaleWidget;
class AxisLable;
class Axis : public QWidget
{
	Q_OBJECT
public:
	explicit Axis(QWidget *parent = nullptr);
	~Axis();
public:
	void setAxisRange(double min,double max);
	void setAxisText(QString);
	void setAxixStyle(Axisstyle);
	void SetAxisNumber(int);
	void loadconfig();
	void _update();
public:
	virtual void resizeEvent(QResizeEvent*) override;
	virtual void mouseDoubleClickEvent(QMouseEvent*) override;
public Q_SLOTS:
	void axiscloseEvent();
private:
	unsigned __int32 AxisNum;
	QString mAxisunit;
	valrange axisvalrange;
	Axisstyle mAxisstyle;
	QGridLayout* mqgridlayout;
	ScaleWidget* mQwtScaleWidget;
	AxisLable* mAxisLable;
};
