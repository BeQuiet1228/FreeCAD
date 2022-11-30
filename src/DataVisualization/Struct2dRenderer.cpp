#include "Struct2dRenderer.h"
#include <qpen.h>
#include <QPainter>
#include "CustomConfig.h"
#include "C_encoding.h"
#include "StructRender.h"
#include <QDebug>
#include "StructData.h"
#include "QVector"
#include "QPainterPath"
namespace DV {
	void chang2colormap(QPixmap& map, QColor& color);
	QString line2icon[] = { ":/struct/C.png", ":/struct/a.png", ":/struct/s.png" };

	Struct2DRenderer::Struct2DRenderer(std::shared_ptr<Struct2dData> data) :
		Renderer(std::dynamic_pointer_cast<Data> (data)) {

		color_tab[1] = QColor(125, 125, 125, 255);
		color_tab[3] = QColor(255, 0, 255, 0);
		color_tab[4] = QColor(255, 125, 125, 255);
		color_tab[5] = QColor(125, 125, 255, 255);
		color_tab[9] = QColor(255, 255, 0, 255);
		QPen pen(Qt::red);
		//虚线
		pen.setStyle(Qt::DashLine);
		pen.setWidth(5);

	}
	Struct2DRenderer::~Struct2DRenderer() {  }
	bool Struct2DRenderer::drawImage() {
		float xScale, yScale;
		if (!getTransitionScale(xScale, yScale))
			return false;
		std::shared_ptr<Struct2dData> d = std::dynamic_pointer_cast<Struct2dData>(data);
		//获取x,y的取值范围
		auto xr = getXRang();
		auto yr = getYRang();
		//开始绘制
		QImage img(getSize(), QImage::Format_ARGB32);
		img.fill(qRgba(0.0, 0.0, 0.0, 0.0));
		QPainter painter(&img);
		painter.setCompositionMode(QPainter::CompositionMode_SourceOver);

		//多边形绘制
		std::vector<QImage> imgs;
		std::map<int, std::map<int, std::vector<QPointF>>> map = d->GetAllinfo();
		for (auto iter = map.begin(); iter != map.end(); iter++)
		{
			//根据多边形的网格的编号绘制
			for (auto iterpro = iter->second.begin(); iterpro != iter->second.end(); iterpro++)
			{
				/*
				 * 2022.2.25
				 * 由于介质是分网格输出的数据，所以可以直接画在主画布上。
				 * 由于之前的代码结构混乱，现在只能使用临时代码完成功能。
				 */
				//如果介质和新材料 那么直接画的主画布上
				if ((iterpro->first&0xc) !=0)
				{
					auto colorbrush = color_tab.find(iterpro->first);
					auto colorpen = color_pen.find(iterpro->first);
					painter.setBrush(colorbrush.value());
					painter.setPen(colorpen.value());

					auto points = iterpro->second;
					for (auto iter = points.begin(); iter != points.end(); iter++)
						transitionPoint(*iter, xScale, xr, yScale, yr);
					//绘制多边形
					QPolygonF innerpolyF(QVector<QPointF>::fromStdVector(points));
					QPainterPath painterPath;
					//绘制多边形
					painterPath.addPolygon(innerpolyF);
					painter.drawPath(painterPath);
				}
				else {
					QImage img1(getSize(), QImage::Format_ARGB32);
					QPainter painter1(&img1);
					createImg(iterpro, xr, yr, xScale, yScale, img1, painter1);
					painter.drawImage(0, 0, img1);
				}
				
			}
		}
		//绘制线段
		std::map<int, std::map<int, std::vector<QPointF>>> mlines = d->getLineF();
		for (auto iter = mlines.begin(); iter != mlines.end(); iter++)
		{
			for (auto iter2 = iter->second.begin(); iter2 != iter->second.end(); iter2++)
			{
				auto iterColor = pixmap.find(iter2->first);
				if (iterColor == pixmap.end() && 2 != iter2->second.size())
					continue;
				QLineF line(iter2->second[0], iter2->second[1]);
				transitionLineF(line, xScale, yScale, xr, yr);
				QLine iline = QLine(QPoint(line.p1().x(), line.p1().y()), QPoint(line.p2().x(), line.p2().y()));
				DrawLine(painter, line, iter2->first);

			}
		}
		auto nImg = img.mirrored(false, true);
		setImage(nImg);
		return true;

	}
	/**
	* @brief Struct2DRenderer::addListRang
	* @param std::list<Data::Rang> listRang
	* @return bool
	*/
	bool Struct2DRenderer::addListRang(std::list<Data::Rang> listRang) {
		return true;
	}
	/**
	* @brief Struct2DRenderer::drawPointImage 点位绘制
	* @return bool
	*/
	bool Struct2DRenderer::drawPointImage() {
		//新建画布

		QImage img(getSize(), QImage::Format_ARGB32);
		img.fill(qRgba(0, 0, 0, 0));
		QPen pen(Qt::red);
		pen.setBrush(Qt::blue);
		pen.setWidth(5);
		QPainter painter(&img);
		painter.setPen(pen);
		//原始坐标
		QPointF A_pos = this->getFindPosition();
		QPointF d_pos = QPointF(0.0, 0.0);
		//获取当前点位
		/**************************/
		d_pos = GetApos(A_pos);
		/***************************/
		A_pos.setY(getSize().height() - A_pos.y());
		painter.drawPoint(A_pos);
		drawDisplayPoint(painter, A_pos, d_pos);
		setImage(img);
		return true;
	}
	/**
	* @brief Struct2DRenderer::setDefaultRang 设置默认数据区间
	* @return bool
	*/
	bool Struct2DRenderer::setDefaultRang() {
		auto _Struct2DData = std::dynamic_pointer_cast<Struct2dData>(data);
		if (!_Struct2DData)
			return false;
		if (_Struct2DData->istrue)
		{
			Data::Rang xr;
			Data::Rang yr;
			xr.min = _Struct2DData->mstart.x();
			xr.max = _Struct2DData->mend.x();
			yr.min = _Struct2DData->mstart.y();
			yr.max = _Struct2DData->mend.y();
			setXRang(xr);
			setYRang(yr);
		}
		else
		{
			setXRang(_Struct2DData->getXRang());
			setYRang(_Struct2DData->getYRang());
		}

		return true;
	}
	/**
	* @brief Struct2DRenderer::dataInit 数值初始化
	* return void
	*/
	void Struct2DRenderer::dataInit() {
		Renderer::dataInit();
		auto _Struct2DData = std::dynamic_pointer_cast<Struct2dData>(data);
		if (_Struct2DData)
		{
			_Struct2DData->loadPoint();
		}
	}
	/**
	* @brief Struct2DRenderer::Getlines 获取线段
	* @param std::vector<QPointF> points
	* @return QVector<QLineF>
	*/
	QVector<QLineF> Struct2DRenderer::Getlines(std::vector<QPointF> points) {
		QVector<QLineF> lines;
		for (auto i = 0; i < points.size() - 1; i++)
		{
			lines.push_back(QLineF(points[i], points[i + 1]));
		}
		return lines;
	}
	/**
	* @brief Struct2DRenderer::drawDisplayPoint 绘制显示信息
	* @param QPainter& painter
	* @param const QPointF& position
	* @param const QPointF& d
	* @return void
	*/
	void Struct2DRenderer::drawDisplayPoint(QPainter& painter, const QPointF& position, const QPointF& d)
	{
		//设置画笔的颜色
		QPen pen;
		pen.setColor(QColor(102, 205, 170));
		pen.setWidth(2);
		painter.setPen(pen);
		painter.setBrush(QBrush(QColor(255, 250, 240)));
		//建立话画框
		QRectF displayRect;
		displayRect.setX(position.x() + 10);
		displayRect.setY(position.y() - 5);
		//如果这个点在边界上  那么调整话框的位置
		auto size = getSize();
		if (displayRect.y() > (size.height() - 60))
		{
			displayRect.setY(displayRect.y() - 70);
		}
		if (displayRect.x() > (size.width() - 130))
		{
			displayRect.setX(displayRect.x() - 150);
		}
		displayRect.setWidth(110);
		displayRect.setHeight(50);
		painter.drawRect(displayRect);
		//绘制显示信息
		QFont f;
		f.setPixelSize(17);
		painter.setFont(f);
		painter.drawText(displayRect.x() + 10,
			displayRect.y() + 20,
			QString("X:%1").arg(d.x(), 0, 'E', 2)
		);
		painter.drawText(displayRect.x() + 10,
			displayRect.y() + 40,
			QString("Y:%1").arg(d.y(), 0, 'E', 2)
		);
	}
	/**
	* @brief Struct2DRenderer::GetApos 获取最接近的点
	* @param QPointF& A_pos 屏幕上的点
	* @return QPointF 真实坐标
	*/
	QPointF Struct2DRenderer::GetApos(QPointF& A_pos)
	{
		float xScale, yScale;
		getTransitionScale(xScale, yScale);
		auto xr = getXRang();
		auto yr = getYRang();
		std::shared_ptr<Struct2dData> d = std::dynamic_pointer_cast<Struct2dData> (data);
		std::map<int, std::map<int, std::vector<QPointF>>> map = d->GetAllinfo();
		std::map<int, std::map<int, std::vector<QPointF>>> lines = d->getLineF();

		//获取全部的点位
		std::vector<QPointF> poss;
		//
		for (auto iter = map.begin(); iter != map.end(); iter++)
		{
			for (auto iter2 = iter->second.begin(); iter2 != iter->second.end(); iter2++)
			{
				auto itercolor = color_tab.find(iter2->first);
				if (itercolor == color_tab.end())
					continue;
				poss.insert(poss.end(), iter2->second.begin(), iter2->second.end());
			}
		}
		for (auto iter = lines.begin(); iter != lines.end(); iter++)
		{
			auto itercolor = pixmap.find(iter->first);
			if (itercolor != pixmap.end())
			{
				for (auto iter2 = iter->second.begin(); iter2 != iter->second.end(); iter2++)
				{
					poss.insert(poss.end(), iter2->second.begin(), iter2->second.end());
				}
			}
		}
		unsigned int minDistance = ~0;
		QPointF srcpos;
		for (auto iter = poss.begin(); iter != poss.end(); iter++)
		{
			QPointF p1 = *iter;
			transitionPoint(p1, xScale, xr, yScale, yr);
			unsigned int Cur_Distance = sqrt((p1.x() - A_pos.x()) * (p1.x() - A_pos.x()) + (p1.y() - A_pos.y()) * (p1.y() - A_pos.y()));
			if (minDistance > Cur_Distance)
			{
				srcpos = *iter;
				minDistance = Cur_Distance;
			}
		}
		QPointF dpos = srcpos;
		QPointF apos = dpos;
		transitionPoint(apos, xScale, xr, yScale, yr);
		A_pos = apos;
		return dpos;
	}
	
	/**
	* @time	2022/01/05
	* @brief DV::Struct2DRenderer::drawPolygons 绘制多边形
	* @param QPainter & painter
	* @param QPolygonF & innerpolyF 多边形数据
	* @return void
	*/
	void Struct2DRenderer::drawPolygons(QPainter& painter, QPolygonF& innerpolyF)
	{
		QPainterPath painterPath;
		//绘制多边形
		painterPath.addPolygon(innerpolyF);
		painter.drawPath(painterPath);
		QVector<QLineF> linex = GetCurLine_x();
		QVector<QLineF> liney = GetCutLine_y();
		//绘制网格
		painter.drawLines(linex);
		painter.drawLines(liney);
	}

	/**
	* @brief Struct2DRenderer::createImg 创建图像
	* @param std::map<int
	* @param std::vector<QPointF>>::iterator & it 顶点数据，若只有两个顶点时绘制线段，否则绘制多边形
	* @param Data::Rang & xr
	* @param Data::Rang & yr
	* @param float & xScale
	* @param float & yScale
	* @return QT_NAMESPACE::QImage
	* @time	2021/12/13
	*/
	void Struct2DRenderer::createImg(
		std::map<int, std::vector<QPointF>>::iterator& it,
		Data::Rang& xr,
		Data::Rang& yr,
		float& xScale,
		float& yScale,
		QImage& img,
		QPainter& painter
		)
	{
		img.fill(qRgba(0.0, 0.0, 0.0, 0.0));
		//获取画刷颜色
		auto colorbrush = color_tab.find(it->first);
		auto colorpen = color_pen.find(it->first);
		if (colorbrush == color_tab.end() || colorpen == color_pen.end())
			return ;
		//画师设置
		painter.setPen(QPen(colorpen.value()));
		painter.setBrush(QBrush(colorbrush.value()));
		painter.setCompositionMode(QPainter::CompositionMode_SourceOver);
		auto points = it->second;
		for (auto iter = points.begin(); iter != points.end(); iter++)
			transitionPoint(*iter, xScale, xr, yScale, yr);
		//绘制线段
		if (it->second.size() == 2 && colorpen != color_pen.end())
		{
			QPen pen;
			pen.setColor(colorpen.value());
			pen.setStyle(Qt::DashLine);
			pen.setWidth(5);
			painter.setPen(pen);
			painter.drawLine(QLineF(*points.begin(), *(points.begin() + 1)));
			return;
		}
		//绘制多边形
		QPolygonF innerpolyF(QVector<QPointF>::fromStdVector(points));
		QPainterPath path;
		path.addPolygon(innerpolyF);//添加多边形数据
		painter.setClipPath(path);//将多边形数据裁剪出来
		//绘制多边形	
		drawPolygons(painter, innerpolyF);
		return ;
	}

	/**
	* @brief Struct2DRenderer::DrawLine 绘制，端口，电源，导电杆三种属性的线段
	* @param QPainter & painter
	* @param QLineF & line
	* @param int mPorper
	* @return void
	* @time	2021/12/13
	*/
	void Struct2DRenderer::DrawLine(QPainter& painter, QLineF& line, int mPorper)
	{
		QSize pngSize = pixmap[mPorper].size();
		QPointF p1 = line.p1();
		QPointF p2 = line.p2();
		//纵向
		if (p1.x() == p2.x())
		{
			auto intervalnumber = abs(p1.y() - p2.y()) / pixmap[mPorper].size().height();
			auto startpos = (p1.y() > p2.y()) ? (p2.y()) : (p1.y());
			auto endpos = (p1.y() > p2.y()) ? (p1.y()) : (p2.y());
			for (auto index = 0; index < intervalnumber; index++)
			{
				QRect rect;
				rect.setLeft(p1.x() - pngSize.width() / 2);
				rect.setRight(rect.left() + pngSize.width());
				rect.setTop(startpos + index * pngSize.height());
				if (rect.top() + pngSize.height() >= endpos)
				{
					rect.setBottom(endpos);
					QPixmap map = pixmap[mPorper].copy(0, 0, pngSize.width(), endpos - rect.top());
					painter.drawPixmap(rect, map);
				}
				else
				{
					rect.setBottom(rect.top() + pngSize.height());
					painter.drawPixmap(rect, pixmap[mPorper]);
				}

			}
		}
		//横向
		else if (p1.y() == p2.y())
		{
			auto intervalnumber = abs(p1.x() - p2.x()) / pixmap[mPorper].size().width();
			auto startpos = (p1.x() > p2.x()) ? (p2.x()) : (p1.x());
			auto endpos = (p1.x() > p2.x()) ? (p1.x()) : (p2.x());
			//图像翻转
			QMatrix rm;
			rm.rotate(90);
			QPixmap mapy = pixmap[mPorper].transformed(QPixmap::trueMatrix(rm, pngSize.width(), pngSize.height()));
			for (auto index = 0; index < intervalnumber; index++)
			{
				QRect rect;
				rect.setTop(p1.y() - pngSize.height() / 2);
				rect.setBottom(rect.top() + pngSize.height());
				rect.setLeft(startpos + index * pngSize.width());
				if (rect.left() + pngSize.width() >= endpos)
				{
					rect.setRight(endpos);
					QPixmap map = mapy.copy(0, 0, endpos - rect.left(), rect.height());
					painter.drawPixmap(rect, map);
				}
				else
				{
					rect.setRight(rect.left() + pngSize.width());
					painter.drawPixmap(rect, mapy);
				}

			}
		}
	}
	void Struct2DRenderer::transitionPoint(QPointF& point, const float& xScale, const Data::Rang& xr, const float& yScale, const Data::Rang& yr)
	{
		point.setX(transitionX(point.x(), xScale, xr));
		point.setY(transitionY(point.y(), yScale, yr));
	}
	float Struct2DRenderer::transitionX(const float& x, const float& xScale, const Data::Rang& xr)
	{
		return (x - xr.min) * xScale;
	}
	float Struct2DRenderer::transitionY(const float& y, const float& yScale, const Data::Rang& yr)
	{
		return (y - yr.min) * yScale;
	}

	/**
	* @brief Struct2DRenderer::transitionLineF
	* @param QLineF & line
	* @param const float & xScale
	* @param const float & yScale
	* @param const Data::Rang & xr
	* @param const Data::Rang & yr
	* @return void
	* @Time 2021/7/19
	*/
	void Struct2DRenderer::transitionLineF(QLineF& line, const float& xScale, const float& yScale, const Data::Rang& xr, const Data::Rang& yr)
	{
		QPointF p1 = line.p1();;
		QPointF p2 = line.p2();
		p1.setX(transitionX(p1.x(), xScale, xr));
		p1.setY(transitionY(p1.y(), yScale, yr));
		p2.setX(transitionX(p2.x(), xScale, xr));
		p2.setY(transitionY(p2.y(), yScale, yr));
		line.setP1(p1);
		line.setP2(p2);
	}
	QVector<QLineF> Struct2DRenderer::GetCurLine_x() {
		QVector<QLineF> lines;
		float xScale, yScale;
		getTransitionScale(xScale, yScale);
		auto xr = getXRang();
		auto yr = getYRang();
		std::shared_ptr<Struct2dData> d = std::dynamic_pointer_cast<Struct2dData>(data);
		std::vector<QPointF> Allpoint = d->ALLPOINTF();
		int posxSizeX = d->getposxSize();
		int posxSizeY = d->getposySize();
		for (auto y = 0; y < posxSizeY; y++)
		{
			QPointF _left = Allpoint[y * posxSizeX];
			QPointF _right = Allpoint[(y + 1) * posxSizeX - 1];
			transitionPoint(_left, xScale, xr, yScale, yr);
			transitionPoint(_right, xScale, xr, yScale, yr);
			lines.push_back(QLineF(_left, _right));
		}
		return lines;
	}
	QVector<QLineF> Struct2DRenderer::GetCutLine_y() {
		QVector<QLineF> lines;
		float xScale, yScale;
		getTransitionScale(xScale, yScale);
		auto xr = getXRang();
		auto yr = getYRang();
		std::shared_ptr<Struct2dData> d = std::dynamic_pointer_cast<Struct2dData>(data);
		std::vector<QPointF> Allpoint = d->ALLPOINTF();
		int posxsize = d->getposxSize();
		int posysize = d->getposySize();
		for (auto x = 0; x < posxsize; x++)
		{
			QPointF bottom = Allpoint[x];
			QPointF top = Allpoint[(posysize - 1) * posxsize + x];
			transitionPoint(top, xScale, xr, yScale, yr);
			transitionPoint(bottom, xScale, xr, yScale, yr);
			lines.push_back(QLineF(top, bottom));
		}
		return lines;
	}

	/**
	* @brief  Struct2DRenderer::loadconfig 加载配置
	* @return void
	*/
	void Struct2DRenderer::loadconfig() {
		Config::GetInstance()->loadConfig();
		ConfigGroup mGroup = Config::GetInstance()->getRootGroup();
		ConfigGroup structConfig = mGroup.getGroup("struct");
#define LoadColor(a)\
	color_tab[(a)]=QStringToQColor(QString::fromStdString(structConfig.getGroup(#a+12).getValue("value")));\
	color_pen[(a)]=QStringToQColor(QString::fromStdString(structConfig.getGroup(#a "LINE"+12).getValue("value")));

		LoadColor(StructData::PERFECTCONDUCTOR);
		LoadColor(StructData::CONDUCTORNEW);
		LoadColor(StructData::DIOLECTRIC);
		LoadColor(StructData::PERMEABILITY);
		LoadColor(StructData::DIELECTIRANDCONDUCTANCE);
		LoadColor(StructData::FREESPACE);
		LoadColor(StructData::FOIL);
		LoadColor(StructData::VACUO);
		//线段
		//PORT 2**8/256，2**9/512，2**10/1024
		//DRIVER--2^11/2048,2^12/4096,2^13/8192
		//INDUCTOR--2^14/16384,2^15/32768,2^16/65536

		QPixmap mapc(line2icon[0]);
		QPixmap mapa(line2icon[1]);
		QPixmap maps(line2icon[2]);
		QSize pngsize(16, 16);

		chang2colormap(maps, QStringToQColor(QString::fromStdString(structConfig.getGroup("PORT").getValue("value"))));
		chang2colormap(mapa, QStringToQColor(QString::fromStdString(structConfig.getGroup("DRIVER").getValue("value"))));
		chang2colormap(mapc, QStringToQColor(QString::fromStdString(structConfig.getGroup("INDUCTOR").getValue("value"))));

		mapc = mapc.scaled(pngsize, Qt::KeepAspectRatio, Qt::SmoothTransformation);
		mapa = mapa.scaled(pngsize, Qt::KeepAspectRatio, Qt::SmoothTransformation);
		maps = maps.scaled(pngsize, Qt::KeepAspectRatio, Qt::SmoothTransformation);

		QMatrix rm;
		rm.rotate(180);
		mapc = mapc.transformed(QPixmap::trueMatrix(rm, pngsize.width(), pngsize.height()));
		mapa = mapa.transformed(QPixmap::trueMatrix(rm, pngsize.width(), pngsize.height()));
		maps = maps.transformed(QPixmap::trueMatrix(rm, pngsize.width(), pngsize.height()));
		pixmap[256] = pixmap[512] = pixmap[1024] = maps;
		pixmap[2048] = pixmap[4096] = pixmap[8192] = mapa;
		pixmap[16384] = pixmap[32768] = pixmap[65536] = mapc;
#undef LoadColor(a)
		isAA = atoi(structConfig.getValue("isAlis").c_str());
	}

	/**
	* @brief chang2colormap
	* @param QPixmap & map
	* @param QColor & color
	* @return void
	* @Time 2021/7/19
	*/
	void chang2colormap(QPixmap& map, QColor& color)
	{
		//默认为红色
		QImage img = map.toImage();
		QColor colorred = QStringToQColor("ffdc3023");
		for (auto w = 0; w < img.width(); w++)
		{
			for (auto h = 0; h < img.height(); h++)
			{
				//qDebug() << QString::number(img.pixel(w, h), 16);
				if (img.pixel(w, h) == colorred.rgb())
				{
					img.setPixel(w, h, color.rgba());
				}
			}
		}
		map = QPixmap::fromImage(img);
	}
}

