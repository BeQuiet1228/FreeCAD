#include "rightScaleWidget.h"
#include <QMouseEvent>
#include "AxisLable.h"
#include "qwt_color_map.h"
#include "qwt/qwt_scale_engine.h"
#include "ConfigWidget.h"
namespace DV {
	rightScaleWidget::rightScaleWidget(QWidget* parent)
		:ScaleWidget(parent)
	{
		initUI();
	}
	rightScaleWidget::rightScaleWidget(QwtScaleDraw::Alignment a, QWidget* parent)
		: ScaleWidget(a, parent)
	{
		initUI();
	}
	void rightScaleWidget::initUI()
	{
		mAxisLable = new AxisLable();
		mAxisLable->setModal(true);
		mAxisLable->resize(300, 200);
		connect(mAxisLable, SIGNAL(signalCloseEvent()), this, SLOT(slotCloseEvent()));
	}
	void rightScaleWidget::mouseDoubleClickEvent(QMouseEvent* e)
	{
		if (e->button() != Qt::LeftButton)
			return;
		double min = scaleDraw()->getMinval();
		double max = scaleDraw()->getMaxval();

		mAxisLable->setMinval(QString("%1").arg(min, 0, 'f', GetdecimalBit(min)));
		mAxisLable->setMaxval(QString("%1").arg(max, 0, 'f', GetdecimalBit(max)));
		mAxisLable->show();
	}
	int rightScaleWidget::GetdecimalBit(double& value)
	{
		__int64 valinter = static_cast<__int64>(value);
		double fspace = abs(value - static_cast<double>(valinter));
		unsigned __int32 index = 0;
		while (fspace > 0.0f)
		{
			index++;
			fspace *= 10;
			valinter = static_cast<__int64> (fspace);
			fspace = fspace - static_cast<double>(valinter);
		}
		return index;
	}
	void rightScaleWidget::slotCloseEvent()
	{
		double min = mAxisLable->getMinval();
		double max = mAxisLable->getMaxval();
		//调整颜色块
		double lastmin = scaleDraw()->getMinval();
		double lastmax = scaleDraw()->getMaxval();
		const QwtLinearColorMap* map = dynamic_cast<const QwtLinearColorMap*>(colorMap());
		QwtLinearColorMap::Mode mode = map->mode();
		std::vector<double> colrstop = map->colorStops().toStdVector();
		std::map<double, QColor> mapkey;
		{
			//重新插入ColorMap;

			for (auto iter = colrstop.begin(); iter != colrstop.end(); iter++)
			{
				double val = (lastmax - lastmin) * (*iter) + lastmin;
				QColor color = map->color(QwtInterval(0.0, 1.0), *iter);
				if (val >= min && val <= max)
				{
					mapkey.insert(std::pair<double, QColor>(val, color));
				}
			}
			if (mapkey.empty())
				return;
			QwtLinearColorMap* newColorMap = new QwtLinearColorMap(
				map->color(QwtInterval(lastmin, lastmax), min),
				map->color(QwtInterval(lastmin, lastmax), max)
			);
			for (auto iter = mapkey.begin(); iter != mapkey.end(); iter++)
			{
				double val = (iter->first - min) / (max - min);
				newColorMap->addColorStop(val, iter->second);
			}
			newColorMap->setMode(mode);
			QwtLinearScaleEngine* scaleEngine = new QwtLinearScaleEngine;
			setColorMap(QwtInterval(min, max), newColorMap);
			setScaleDiv(scaleEngine->divideScale(min, max, 6, 8, 0));
			setRange(min, max);
			automatic();
		}
		emit signalsetAxisRightRange(min, max);
		//mAxisLable->hide();
	}
	void rightScaleWidget::automatic()
	{
		switch (mAlignment)
		{
		case QwtScaleDraw::RightScale:
		{
			scaleDraw()->setAlignment(QwtScaleDraw::RightScale);
			QPointF pos = scaleDraw()->pos();
			pos.setY(0);
			scaleDraw()->move(pos);
			scaleDraw()->setLength(this->height() - 1);
			scaleDraw()->setPenWidth(1);
		}
		break;
		}
	}
	rightScaleWidget::~rightScaleWidget()
	{
		delete mAxisLable;
	}
};

#include "moc_rightScaleWidget.cpp"