#include "ControlTreeWidget.h"
#include <QString>
ControlTreeWidget::ControlTreeWidget(QWidget* parent)
	:QTreeWidget(parent)
{
	
}

void ControlTreeWidget::init(const Hdf5Data& data)
{
	auto listHead = data.headList;

}

void ControlTreeWidget::initItem()
{
	for (int i = 0; i < itemCount; i++)
	{
		items.push_back(new QTreeWidgetItem);
	}
	
	contourItem = items.at(0);
	contourItem->setText("contour");

	phaseSpaceItem = items.at(1);
	phaseSpaceItem->setText("phaseSpace");

	observeItem = items.at(2);
	observeItem->setText("observe");

	rangeItem = items.at(3);
	rangeItem->setText("range");

	vectorItem = items.at(4);
	vectorItem->setText("vector");

	for each (QTreeWidgetItem* item in items)
	{
		addTopLevelItem(item);
	}

}

bool ControlTreeWidget::addContourItem(const std::string& str)
{
	QString qstr = QString::fromStdString(str);
	auto lists = qstr.split("=");
	
	if (lists.size() != 2)
		return false;

	qstr = lists.at(0);
	//获取名称和观测排序
	QString name = qstr.left(7);
	if (name != "contour")
		return false;
	QString rank = qstr.remove(name);

	QTreeWidgetItem* childItem = new QTreeWidgetItem;
	childItem->setText(lists.at(1));

}

