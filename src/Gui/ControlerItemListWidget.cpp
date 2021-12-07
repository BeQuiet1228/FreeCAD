#include "ControlerItemListWidget.h"
#include "ui_ControlerItemListWidget.h"
#include <QListWidgetItem>
Gui::ControlerItemListWidget::ControlerItemListWidget(QWidget* parent /*= 0*/)
	:QWidget(parent),ui(new Ui::ControlerItemListWidget())
{
	ui->setupUi(this);
}

void Gui::ControlerItemListWidget::addWidget(QWidget* widget)
{
	auto item = new QListWidgetItem();
	ui->listWidget->addItem(item);
	ui->listWidget->setItemWidget(item, widget);
}

