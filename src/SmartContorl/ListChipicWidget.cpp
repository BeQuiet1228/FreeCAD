#include "ListChipicWidget.h"
SMC::ListChipicWidget::ListChipicWidget(QWidget* parent /*= 0*/)
	:QListWidget(parent)
{

}

SMC::ListChipicWidget::~ListChipicWidget()
{

}

void SMC::ListChipicWidget::addListWidgetItem(QListWidgetItem* item, QWidget* widget)
{
	addItem(item);
	setItemWidget(item, widget);
}

#include "moc_ListChipicWidget.cpp"