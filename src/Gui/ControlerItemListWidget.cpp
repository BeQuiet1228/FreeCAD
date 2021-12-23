#include "PreCompiled.h"
#include "ControlerItemListWidget.h"
#include "ui_ControlerItemListWidget.h"
#include "DockWindowManager.h"
#include <QListWidgetItem>
Gui::ControlerItemListWidget::ControlerItemListWidget(QWidget* parent /*= 0*/)
	:QWidget(parent),ui(new Ui::ControlerItemListWidget())
{
	ui->setupUi(this);
}

void Gui::ControlerItemListWidget::addWidget(QWidget* widget)
{
	auto item = new QListWidgetItem();
	item->setSizeHint(widget->size());
	ui->listWidget->addItem(item);
	ui->listWidget->setItemWidget(item, widget);
}


void Gui::ControlerItemListWidget::clearWidget()
{
	ui->listWidget->clear();
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

