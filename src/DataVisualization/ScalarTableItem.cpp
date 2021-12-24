#include "ScalarTableItem.h"
DV::ScalarTableItem::ScalarTableItem(int type /*= Type*/):
	QTableWidgetItem(type)
{}

DV::ScalarTableItem::~ScalarTableItem()
{

}

DV::ScalarTableItem::ScalarTableItem(const QTableWidgetItem& other):
	QTableWidgetItem(other)
{}

DV::ScalarTableItem::ScalarTableItem(const QIcon& icon, const QString& text, int type /*= Type*/) :
	QTableWidgetItem(icon,text,type)
{}

DV::ScalarTableItem::ScalarTableItem(const QString& text, int type /*= Type*/):
	QTableWidgetItem(text,type)
{}

