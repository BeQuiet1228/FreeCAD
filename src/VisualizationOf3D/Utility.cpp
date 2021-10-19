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
std::vector<TreeItem*>& BaseWidget::GetTreeItems()
{
	return items;
}
TreeItem::TreeItem():QStandardItem()
{
	initUI();
}
TreeItem::TreeItem(const QString& text):QStandardItem(text)
{
	initUI();
}
TreeItem::TreeItem(const QIcon& icon, const QString& text):QStandardItem(icon,text)
{
	initUI();
}
TreeItem::TreeItem(int rows, int columns):QStandardItem(rows,columns)
{
	initUI();
}
TreeItem::~TreeItem()
{
	pID = 0;
}
void TreeItem::initUI() 
{
	pID = 0;
}
#include "moc_Utility.cpp"