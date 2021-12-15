#pragma  once
#include <QWidget>
namespace DV {
	enum Axisstyle
	{
		Axisleft,
		AxisRight,
		AxisTop,
		AxisBottom
	};
	typedef struct valrange {
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
};


#include"ScaleWidget.h"
namespace DV {
	class ScaleWidget;
	class AxisLable;
	class TDialog;
	class Axis :
		public ScaleWidget
	{
		Q_OBJECT
	public:
		explicit Axis(QWidget* parent = nullptr);
		~Axis();
	public:
		void setAxisRange(double min, double max);
		void setAxixStyle(Axisstyle);
		void SetAxisNumber(int);
		void loadconfig();
		void _update();
	public:
		virtual void resizeEvent(QResizeEvent*) override;
		virtual void mouseDoubleClickEvent(QMouseEvent*) override;
	Q_SIGNALS:
		void sendAxisRang(const float&, const float&);
		//void signalsetAxisRightRange(const float& min, const float& max);
	public Q_SLOTS:
		void axiscloseEvent();
	private:
		unsigned __int32 AxisNum;
		valrange axisvalrange;
		Axisstyle mAxisstyle;
		//ScaleWidget* mQwtScaleWidget;
		AxisLable* mAxisLable;
		QColor axisColor;//刻度颜色
		QColor axisvalColor;//数值颜色
		int axisvalSize;//数值大小
		QString unitFont;
	};
};

