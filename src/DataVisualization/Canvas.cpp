#include "Canvas.h"
#include <QMetaType>
#include <mutex>
Canvas::Canvas(QWidget* parent /*= 0*/)
	:QWidget(parent)
{
	
}

Canvas::~Canvas()
{

}

/**
* @brief Canvas::addIteam 添加一个item 如果rank已经存在 那么会覆盖掉之前的 
* @param const CanvasItem & iteam
* @return void
*/
void Canvas::addIteam(const CanvasItem& iteam)
{
	auto iter = this->items.find(iteam.rank);
	if (iter != this->items.end())
		items.erase(iter);
	items.insert(std::map<unsigned int, CanvasItem>::value_type(iteam.rank, iteam));
}

void Canvas::paintEvent(QPaintEvent *event)
{
	QPainter painter(this);
	for (auto item = items.begin(); item != items.end(); item++)
	{
		painter.setPen(item->second.pen);
		painter.drawImage(item->second.pos, *(item->second.image.get()));
	}
	painter.drawRect(0, 0, this->width()-2, this->height()-2);
}

/**
* @brief CanvasItem::registerMetaTye 注册自定义信号参数
* @return void
*/
void CanvasItem::registerMetaTye()
{
	static std::once_flag flag;
	std::call_once(flag, [&](){
		qRegisterMetaType<CanvasItem>("CanvasItem");
	});
}


bool CanvasItem::operator==(const CanvasItem& item)
{
	return this->rank == item.rank;
}

bool CanvasItem::operator>(const CanvasItem& item)
{
	return this->rank > item.rank;
}

bool CanvasItem::operator<(const CanvasItem& item)
{
	return this->rank < item.rank;
}

CanvasItem::CanvasItem()
	:image(nullptr), rank(0), pos(0, 0)
{

}
