#include "RenderGrid.h"
#include <memory>
#include <QPainter>
#include <QPen>
#include <QImage>
namespace DV {
	RenderGrid::RenderGrid(const unsigned int& xl, const unsigned int& yl)
		: Renderer(std::shared_ptr<Data>()), xLevel(xl), yLevel(yl)
	{

	}

	bool RenderGrid::drawImage()
	{
		//ÐÂ½¨»­²¼ »­±Ê
		auto size = getSize();
		QImage img(size, QImage::Format_ARGB32);
		img.fill(qRgba(0, 0, 0, 0));
		QPen pen(Qt::gray);
		pen.setWidth(1);
		pen.setStyle(Qt::DashLine);
		QPainter painter(&img);
		painter.setRenderHint(QPainter::Antialiasing, true);;
		painter.setPen(pen);

		float block = size.width() / xLevel;
		for (int i = 1; i < xLevel; i++)
		{
			float xPos = block * i;
			painter.drawLine(xPos, 0, xPos, size.height());
		}

		block = size.height() / yLevel;
		for (int i = 1; i < yLevel; i++)
		{
			float yPos = block * i;
			painter.drawLine(0, yPos, size.width(), yPos);
		}

		setImage(img);
		return true;
	}

	bool RenderGrid::drawPointImage()
	{
		return true;
	}

	bool RenderGrid::setDefaultRang()
	{
		return true;
	}

	void RenderGrid::dataInit()
	{

	}


};
