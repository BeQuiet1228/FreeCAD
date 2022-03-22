#include "ScalarTableItem.h"
DV::ScalarTableItem::ScalarTableItem(double val, int type /*= Type*/):
	QTableWidgetItem(type), 
	scalarValue(val)
{

}

DV::ScalarTableItem::~ScalarTableItem()
{

}

void DV::ScalarTableItem::setValue(double value)
{
	scalarValue = value;
}

double& DV::ScalarTableItem::getValue()
{
	return scalarValue;
}

DV::ScalarTableItem::ScalarTableItem(const ScalarTableItem& other):
	QTableWidgetItem(other),
	scalarValue(other.scalarValue)
{

}

DV::ScalarTableItem::ScalarTableItem(const QIcon& icon, const QString& text, double val, int type /*= Type*/):
	QTableWidgetItem(icon,text,type),
	scalarValue(val)
{

}

DV::ScalarTableItem::ScalarTableItem(const QString& text, double val, int type /*= Type*/):
	QTableWidgetItem(text,type),
	scalarValue(val)
{

}
