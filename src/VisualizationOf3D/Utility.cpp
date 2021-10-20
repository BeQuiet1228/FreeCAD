#include "Utility.h"
#include "QStandardItem"
#include "QDebug"
BaseWidget::BaseWidget(QWidget* parent):QWidget(parent){
	//mwidget = nullptr;
	items.clear();
}
BaseWidget::~BaseWidget() {
	items.clear();
}
void BaseWidget::slotitemStateChange(QStandardItem* item)
{

}
/**
* @brief BaseWidget::GetTreeItems »ñÈ¡¿Ø¼þ
* @return std::vector<TreeItem*>&
*/

std::vector<TreeItem*>& BaseWidget::GetTreeItems()
{
	return items;
}
TreeItem::TreeItem():QStandardItem()
{
	pID = 0;
}
TreeItem::TreeItem(const QString& text):QStandardItem(text)
{
	pID = 0;
}
TreeItem::TreeItem(const QIcon& icon, const QString& text):QStandardItem(icon,text)
{
	pID = 0;
}
TreeItem::TreeItem(int rows, int columns):QStandardItem(rows,columns)
{
	pID = 0;
}
TreeItem::~TreeItem()
{
	pID = 0;
}
#include "moc_Utility.cpp"