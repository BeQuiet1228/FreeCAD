#include "phasorRenderer.h"
#include <qpen.h>
#include <QPainter>
#include "CustomConfig.h"
#include "C_encoding.h"
#include <QDebug>
#include "ContourRender.h"
#include"ConfigWidget.h"
namespace DV {
#ifndef M_PI_
#define  M_PI_ (3.141592653589793)
#endif // !M_PI_
#ifndef HORI_GRID
#define  HORI_GRID (30.0f)
#endif
#ifndef VERT_GRID
#define  VERT_GRID (30.0f)
#endif
	phasorRenderer::phasorRenderer(std::shared_ptr<phasorData> data)
		:Renderer(std::dynamic_pointer_cast<Data>(data)), colormapsite(0), lastcolormapsite(0)
	{
		penSize = 1;
		penColor = Qt::red;
		isAA = true;
	}
	phasorRenderer::~phasorRenderer() {
		if (colormapsite != 0)
		{
			QwtLinearColorMap* map = reinterpret_cast<QwtLinearColorMap*>(colormapsite);
			delete map;
		}
	}
	/**
	* @brief phasorRenderer::drawImage 绘制图片
	* @return bool
	*/
	bool phasorRenderer::drawImage() {
		return drawImageScence();
	}
	/**
	* @brief phasorRenderer::addListRang
	* @param std::list<Data::Rang> listRang
	* @return bool
	*/
	bool phasorRenderer::addListRang(std::list<Data::Rang> listRang) {
		return true;
	}
	/**
	* @brief phasorRenderer::drawPointImage 绘制取点画面
	* @return bool
	*/
	bool phasorRenderer::drawPointImage() {
		//新建画布 画笔
		float xScale, yScale;
		getTransitionScale(xScale, yScale);
		auto xr = getXRang();
		auto yr = getYRang();
		QImage img(getSize(), QImage::Format_ARGB32);
		img.fill(qRgba(0, 0, 0, 0));
		QPen pen(Qt::black);
		pen.setBrush(Qt::blue);
		pen.setWidth(5);
		QPainter painter(&img);
		painter.setPen(pen);
		//原始坐标
		QPointF A_pos = this->getFindPosition();
		//获取索引值
		int index = findApoint(A_pos);
		std::shared_ptr<phasorData> d = std::dynamic_pointer_cast<phasorData>(data);
		//获取原点
		QPointF p1 = d->findindexP1(index);
		A_pos = p1;
		transitionpointF(A_pos, xScale, yScale, xr, yr);
		//获取长度系数
		QPointF len_coef = d->findindexlen_coef(index);
		//坐标翻转
		A_pos.setY(getSize().height() - A_pos.y());
		painter.drawPoint(A_pos);

		std::map<QString, float> list;
		list["X"] = p1.x();
		list["Y"] = p1.y();
		list["X_COEF"] = len_coef.x();
		list["Y_COEF"] = len_coef.y();
		displayPointInformation(&painter, &A_pos, list);
		setImage(img);
		return true;
	}
	/**
	* @brief phasorRenderer::setDefaultRang 设置默认坐标系数值范围
	* @return bool
	*/
	bool phasorRenderer::setDefaultRang() {
		auto _phasorData = std::dynamic_pointer_cast<phasorData>(data);
		if (!_phasorData)
			return false;
		setXRang(_phasorData->getXRang());
		setYRang(_phasorData->getYRang());
		return true;
	}
	/**
	* @brief phasorRenderer::dataInit 数据初始化
	* @return void
	*/
	void phasorRenderer::dataInit() {
		Renderer::dataInit();
		auto _phasordata = std::dynamic_pointer_cast<phasorData>(data);
		if (_phasordata)
		{
			_phasordata->loadPoint();
		}
	}
	/**
	* @brief phasorRenderer::transitionpointF 直角坐标系点位转换为屏幕点位
	* @param QPointF & p
	* @param const float& xScale
	* @param const float& yScale
	* @param const Data::Rang xr
	* @param const Data::Rang yr
	* @return void
	*/
	void phasorRenderer::transitionpointF(QPointF& p, const float& xScale, const float& yScale, const Data::Rang xr, const Data::Rang yr)
	{
		p.setX(transitionX(p.x(), xScale, xr));
		p.setY(transitionY(p.y(), yScale, yr));
	}
	/**
	* @brief phasorRenderer::GetarrowTop 获取箭头上半段
	* @param QPointF endpoint
	* @param QPointF startpoint
	* @return QPointF
	*/
	QPointF phasorRenderer::GetarrowTop(QPointF endpoint, QPointF startpoint) {
		//先获取线段长度
		qreal _distance = sqrt((endpoint.x() - startpoint.x()) * (endpoint.x() - startpoint.x()) +
			(endpoint.y() - startpoint.y()) * (endpoint.y() - startpoint.y()));
		QLineF line(startpoint, endpoint);
		double angle = std::atan2(-line.dy(), line.dx());
		qreal arrowSize;
		if (_distance > 30)
			arrowSize = 10;
		else
			arrowSize = _distance / 3;
		QPointF arrowP1 = line.p2() - QPointF(sin(angle + M_PI_ / 3) * arrowSize,
			cos(angle + M_PI_ / 3) * arrowSize);
		return arrowP1;
	}
	/**
	* @brief phasorRenderer::GetarrowBottom 获取箭头下半段
	* @param QPointF endpoint
	* @param QPointF startpoint
	* @return QPointF
	*/
	QPointF phasorRenderer::GetarrowBottom(QPointF endpoint, QPointF startpoint) {
		qreal _distance = sqrt((endpoint.x() - startpoint.x()) * (endpoint.x() - startpoint.x()) +
			(endpoint.y() - startpoint.y()) * (endpoint.y() - startpoint.y()));
		QLineF line(startpoint, endpoint);
		double angle = std::atan2(-line.dy(), line.dx());
		qreal arrowSize;
		if (_distance > 30)
			arrowSize = 10;
		else
			arrowSize = _distance / 3;
		QPointF arrowP2 = line.p2() - QPointF(sin(angle + M_PI_ - M_PI_ / 3) * arrowSize,
			cos(angle + M_PI_ - M_PI_ / 3) * arrowSize);
		return arrowP2;
	}
	/**
	* @brief phasorRenderer::transionVector 向量坐标转换
	* @param QPointF endpoint
	* @param QPointF startpoint
	* @param const float& xScale
	* @param const float& yScale
	* @retrun void
	*/
	void phasorRenderer::transionVector(QPointF& endpoint, QPointF startpoint, const float& xScale, const float& yScale)
	{
		qreal x_distance = (endpoint.x() - startpoint.x()) * xScale;
		qreal y_distance = (endpoint.y() - startpoint.y()) * yScale;
		endpoint.setX(x_distance + startpoint.x());
		endpoint.setY(y_distance + startpoint.y());
	}
	/**
	* @brief phasorRenderer::drawImageScence 依据屏幕缩放绘制
	* @retrun bool
	*/
	bool phasorRenderer::drawImageScence() {
		//获取画布缩放
		float xScale(0.0), yScale(0.0);
		if (!getTransitionScale(xScale, yScale))
			return false;
		std::shared_ptr<phasorData> d = std::dynamic_pointer_cast<phasorData>(data);
		//获取x,y的取值范围
		auto xr = getXRang();
		auto yr = getYRang();
		//开始绘制
		QImage img(getSize(), QImage::Format_ARGB32);
		img.fill(qRgba(0, 0, 0, 0));
		QPainter painter(&img);
		painter.setRenderHint(QPainter::Antialiasing, isAA);
		std::vector<float> scaleval = d->getScaleVal();
		//ColorMap* map = new ColorMap();
		//QwtLinearColorMap* map = getQwtLinearColorMap();
		QwtLinearColorMap* map = reinterpret_cast<QwtLinearColorMap*>(colormapsite);
		if (colormapsite != lastcolormapsite)
		{
			if (lastcolormapsite != 0)
			{
				QwtLinearColorMap* lastmap = reinterpret_cast<QwtLinearColorMap*>(lastcolormapsite);
				delete lastmap;
			}
			lastcolormapsite = colormapsite;
		}
		std::vector<QColor> colorMap; colorMap.reserve(scaleval.size());
		for (auto iter = scaleval.begin(); iter != scaleval.end(); iter++)
			colorMap.push_back(map->color(QwtInterval(0.0, 1.0), *iter));
		//绘制向量
		QVector<QPointF> p1 = d->Getp1Point();
		QVector<QPointF> p2 = d->Getp2Point();
		//计算网格最大系数
		float maxCoef;
		{
			//计算网格大小
			float widthgrid = (d->getdefXrang().max - d->getdefXrang().min) * xScale / d->getXsize();
			float heightrid = (d->getdefYrang().max - d->getdefYrang().min) * yScale / d->getYsize();
			//这里修改效果
			if (widthgrid > heightrid)
			{
				maxCoef = heightrid;
			}
			else
			{
				maxCoef = widthgrid;
			}
			//maxCoef = sqrt(widthgrid*widthgrid + heightrid*heightrid);
		}
		switch (d->GetdisMode())
		{
		case phasorData::DISMODE::sizeToColor:
		{
			for (auto i = 0; i < p1.size(); i++)
			{
				QPen pen(colorMap[i]);
				pen.setWidth(penSize);
				painter.setPen(pen);
				transitionpointF(p1[i], xScale, yScale, xr, yr);
				p2[i].setX(p1[i].x() + p2[i].x() * maxCoef * 0.9);
				p2[i].setY(p1[i].y() - p2[i].y() * maxCoef * 0.9);
				painter.drawLine(p1[i], p2[i]);
				painter.drawLine(p2[i], GetarrowTop(p2[i], p1[i]));
				painter.drawLine(p2[i], GetarrowBottom(p2[i], p1[i]));
			}
		}
		break;
		case phasorData::DISMODE::sizeToLen:
		{
			QPen pen = painter.pen();
			pen.setColor(penColor);
			pen.setWidth(penSize);
			painter.setPen(pen);
			std::vector<float> sizeScale = d->getScaleVal();//获取大小系数
			for (auto i = 0; i < p1.size(); i++)
			{
				transitionpointF(p1[i], xScale, yScale, xr, yr);
				p2[i].setX(p1[i].x() + p2[i].x() * maxCoef * sizeScale[i]);
				p2[i].setY(p1[i].y() + p2[i].y() * maxCoef * sizeScale[i]);
				painter.drawLine(p1[i], p2[i]);
				painter.drawLine(p2[i], GetarrowTop(p2[i], p1[i]));
				painter.drawLine(p2[i], GetarrowBottom(p2[i], p1[i]));
			}
		}
		break;
		}
		auto nImg = img.mirrored(false, true);
		setImage(nImg);
		return true;
	}
	/**
	* @brief phasorRenderer::GetRectF_Scene 获取屏幕切割的网格
	* @param const Data::Rang xr
	* @param const Data::Rang yr
	* @return QVector<QRectF>
	*/
	QVector<QRectF> phasorRenderer::GetRectF_Scene() {
		QVector<QRectF> scene_Rect;
		float width = getSize().width();
		float height = getSize().height();
		int ver_num = width / VERT_GRID;
		int hori_num = height / HORI_GRID;
		for (auto y = 0; y <= hori_num; y++)
		{
			for (auto x = 0; x <= ver_num; x++)
			{
				QRectF _rectf;
				_rectf.setLeft(x * VERT_GRID);
				_rectf.setRight((x + 1) * VERT_GRID);
				_rectf.setBottom(y * HORI_GRID);
				_rectf.setTop((y + 1) * HORI_GRID);
				scene_Rect.push_back(_rectf);
			}
		}
		//网格缩放

		return scene_Rect;
	}
	/**
	* @brief phasorRenderer::findVecLines 索引出需要绘制的向量
	* @param QVector<QRectF> scene_rect 屏幕网格（10*10）
	* @param QVector<QPointF> p1 向量起点
	* @param QVector<QPointF> p2 向量终点
	* @return QVector<QLineF>
	*/
	QVector<QLineF> phasorRenderer::findVecLines(QVector<QRectF> scene_rect, QVector<QPointF> p1, QVector<QPointF> p2) {
		QVector<QLineF> lines;
		float xScale(0.0), yScale(0.0);
		getTransitionScale(xScale, yScale);
		auto xr = getXRang();
		auto yr = getYRang();
		QVector<qreal> rations;//比例系数
		std::shared_ptr<phasorData> d = std::dynamic_pointer_cast<phasorData>(data);
		//获取最大系数
		qreal MaxSver = 0;
		int maxindex = 0;
		for (auto i = 0; i < p1.size(); i++)
		{
			if (p1[i].x() >= xr.min && p1[i].x() <= xr.max
				&& p1[i].y() > yr.min && p1[i].y() <= yr.max)
			{
				qreal curSver = sqrt(p2[i].x() * p2[i].x() + p2[i].y() * p2[i].y());
				if (MaxSver < curSver)
				{
					maxindex = i;
					MaxSver = curSver;
				}
			}
		}
		qreal VecXcoef = abs(p2[maxindex].x());
		qreal VecYcorf = abs(p2[maxindex].y());
		for (auto i = 0; i < p1.size(); i++)
		{
			qreal ration =
				sqrt(p2[i].x() * p2[i].x() + p2[i].y() * p2[i].y()) / sqrt(VecXcoef * VecXcoef + VecYcorf * VecYcorf);
			rations.push_back(ration);
			transitionpointF(p1[i], xScale, yScale, xr, yr);
			p2[i].setX(p1[i].x() + HORI_GRID * rations[i] * (p2[i].x() / sqrt(p2[i].x() * p2[i].x() + p2[i].y() * p2[i].y())));
			p2[i].setY(p1[i].y() + VERT_GRID * rations[i] * (p2[i].y() / sqrt(p2[i].x() * p2[i].x() + p2[i].y() * p2[i].y())));
		}
		for (auto i = 0; i < p1.size(); i++)
		{
			lines.push_back(QLineF(p1[i], p2[i]));
			lines.push_back(QLineF(p2[i], GetarrowTop(p2[i], p1[i])));
			lines.push_back(QLineF(p2[i], GetarrowBottom(p2[i], p1[i])));
		}
		return lines;
	}
	/**
	* @brief phasorRenderer::transionVector 向量转换
	* @param QPointF& endipoint
	* @param QPointF startpoint
	* @param const float& lenScale
	* @return void
	*/
	void phasorRenderer::transionVector(QPointF& endipoint, QPointF startpoint, const float& lenScale) {
		//获取线段长度
		float x_lenght = abs(endipoint.x() - startpoint.x());
		float y_lenght = abs(endipoint.y() - startpoint.y());
		float line_lenght = sqrt(x_lenght * x_lenght + y_lenght * y_lenght);
		//获取缩放比例
		float curscale = line_lenght * lenScale;
		qreal x = (endipoint.x() - startpoint.x()) * (x_lenght / line_lenght) * lenScale;
		qreal y = (endipoint.y() - startpoint.y()) * (y_lenght / line_lenght) * lenScale;
		endipoint.setX(startpoint.x() + x);
		endipoint.setY(startpoint.y() + y);
	}
	/**
	* @brief phasorRenderer::findApoint 寻找最近的点位的索引
	* @param QPointF A_point
	* @return int
	*/
	int phasorRenderer::findApoint(QPointF A_point)
	{
		int index = 0;
		float xScale, yScale;
		getTransitionScale(xScale, yScale);
		auto xr = getXRang();
		auto yr = getYRang();
		std::shared_ptr<phasorData> d = std::dynamic_pointer_cast<phasorData>(data);
		QVector<QPointF> p1 = d->Getp1Point();
		//转换屏幕坐标
		for (auto iter = p1.begin(); iter != p1.end(); iter++)
			transitionpointF(*iter, xScale, yScale, xr, yr);
		//寻找最近的点
		qreal _mindistance = sqrt((A_point.x() - p1[0].x()) * (A_point.x() - p1[0].x()) + (A_point.y() - p1[0].y()) * (A_point.y() - p1[0].y()));
		for (auto i = 0; i < p1.size(); i++)
		{
			qreal curdistance = sqrt((A_point.x() - p1[i].x()) * (A_point.x() - p1[i].x()) + (A_point.y() - p1[i].y()) * (A_point.y() - p1[i].y()));
			if (_mindistance > curdistance)
			{
				_mindistance = curdistance;
				index = i;
			}
		}

		return index;
	}
	/**
	* @brief  phasorRenderer::loadconfig 读取配置
	* @return void
	*/
	void phasorRenderer::loadconfig()
	{
		Config::GetInstance()->loadConfig();
		auto group = Config::GetInstance()->getRootGroup();
		auto vectorGroup = group.getGroup("vector");
		penSize = atoi(vectorGroup.getGroup("vectorsize").getValue("value").c_str());
		penColor = QStringToQColor(QString::fromStdString(vectorGroup.getGroup("vectorColor").getValue("value")));
		isAA = atoi(vectorGroup.getGroup("AlisAttitude").getValue("isAlis").c_str());
		//矢量展示模式
		bool isSizeToColor = atoi(vectorGroup.getGroup("disMode").getValue("value").c_str());
		std::shared_ptr<phasorData> d = std::dynamic_pointer_cast<phasorData>(data);
		if (isSizeToColor)
			d->setdisMode(phasorData::DISMODE::sizeToColor);
		else
			d->setdisMode(phasorData::DISMODE::sizeToLen);
		auto ptr = ConfigWidget::getQwtLinearColorMap();
		if (ptr)
		{
			colormapsite = reinterpret_cast<unsigned long long>(ptr);
		}
	}

	/**
	* @brief  phasorRenderer::setDefaultRang 设置默认坐标取值范围
	* @param  QSize & size
	* @return bool
	*/
	bool phasorRenderer::setDefaultRang(QSize& size) {
		return setDefaultRang();
	}

	/**
	* @brief  phasorRenderer::getValueRange
	* @return Data::Rang
	*/
	Data::Rang phasorRenderer::getValueRange()
	{
		Data::Rang ra;
		ra.min = 0;
		ra.max = 1;
		return ra;
	}
	phasorData::DISMODE phasorRenderer::getMode()
	{
		std::shared_ptr<phasorData> d = std::dynamic_pointer_cast<phasorData>(data);
		return d->GetdisMode();
	}

	float phasorRenderer::getStructFaceAnchor()
	{
		std::shared_ptr<phasorData> d = std::dynamic_pointer_cast<phasorData>(data);
		return d->getStructFaceAnchor();
	}

};
