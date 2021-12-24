#include "PreCompiled.h"
#include "ControlerItemListWidget.h"
#include "ui_ControlerItemListWidget.h"
#include "DockWindowManager.h"
#include "DataVisualization/3D/ControlerItem.h"
Gui::ControlerItemListWidget::ControlerItemListWidget(QWidget* parent /*= 0*/)
	:QWidget(parent),ui(new Ui::ControlerItemListWidget())
{
	ui->setupUi(this);
}

void Gui::ControlerItemListWidget::addWidget(DV3D::ControlerItem* widget)
{
	auto item = new QListWidgetItem();
	addItemWidget(widget, item);
}


void Gui::ControlerItemListWidget::clearWidget()
{
	ui->listWidget->clear();
}

void Gui::ControlerItemListWidget::addItemWidget(DV3D::ControlerItem* widget, QListWidgetItem* item)
{
	item->setSizeHint(widget->size());
	ui->listWidget->addItem(item);
	ui->listWidget->setItemWidget(item, widget);

	std::map<DV3D::ControlerItem*, QListWidgetItem*>::value_type temp(widget, item);
	widgetMap.insert(temp);
	connect(widget, SIGNAL(itemClose()), this, SLOT(itemClose()));
	
}

void Gui::ControlerItemListWidget::itemClose()
{
	auto controlerItem = dynamic_cast<DV3D::ControlerItem*>(sender());
	if (!controlerItem)
		return;
	auto iter = widgetMap.find(controlerItem);
	if (iter == widgetMap.end())
		return;
	int index = ui->listWidget->row(iter->second);
	auto item = ui->listWidget->takeItem(index);
	delete item;
	widgetMap.erase(iter);
}

/**
* @brief Gui::CreatControlerListWidget 创建一个listitemWidget 并添加到悬浮窗口中
* @return Gui::ControlerItemListWidget*
*/
Gui::ControlerItemListWidget* Gui::CreatControlerListWidget()
{
	auto listItem = new ControlerItemListWidget;
	listItem->setObjectName(QString::fromLocal8Bit("ControlerItemListWidget"));
	DockWindowManager::instance()->addDockWindow("3dControler", listItem, Qt::DockWidgetArea::RightDockWidgetArea)->show();

	return listItem;
}

void Gui::hideControlerListWidget()
{
	auto widget = DockWindowManager::instance()->getDockWindow("3dControler");
	if (!widget)
		return;
	auto docWidget = dynamic_cast<QDockWidget*>(widget->parent());
	docWidget->hide();
}

void Gui::showControlerListWidget()
{
	auto widget = DockWindowManager::instance()->getDockWindow("3dControler");
	if (!widget)
		return;
	auto docWidget = dynamic_cast<QDockWidget*>(widget->parent());
	docWidget->show();
}