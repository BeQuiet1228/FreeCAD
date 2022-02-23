#include "ui_ControlerItem.h"
#include "ControlerItem.h"
#include <cassert>
#include "ControlerAction.h"
#include <iostream>
#include <QSize>
#include "controler.h"
DV3D::ControlerItem::ControlerItem(QWidget* parent /*=0*/)
	:QWidget(parent),ui(new Ui::ControlerItem())
{
	ui->setupUi(this);
	initGui();
	setAttribute(Qt::WA_DeleteOnClose);
}

DV3D::ControlerItem::~ControlerItem()
{
	
}

std::shared_ptr<DV3D::Controler> DV3D::ControlerItem::getControler()
{
	assert(controler && "controler is null!");
	return controler;
}

void DV3D::ControlerItem::setControler(std::shared_ptr<Controler> controler)
{
	this->controler = controler;

	//刷新所有按钮状态
	for (auto iter = toolButtonMap.begin(); iter != toolButtonMap.end(); iter++)
	{
		iter->second->initState(controler);
		iter->second->update(iter->first);
	}
	ui->horizontalSlider->setValue(controler->getTranparent() * 100);
}

void DV3D::ControlerItem::addAction(std::shared_ptr<ControlerAction> action)
{
	QToolButton* btn = new QToolButton(this);
	connect(btn, SIGNAL(clicked(bool)), this, SLOT(toolButtonClicked(bool)));
	ui->toolbarLayout->addWidget(btn);

	action->update(btn);
	auto value = ToolButtonMap::value_type(btn, action);
	toolButtonMap.insert(value);
}

void DV3D::ControlerItem::setName(const QString& name)
{
	ui->labelName->setText(name);
}

void DV3D::ControlerItem::resizeEvent(QResizeEvent* event)
{
	QWidget::resizeEvent(event);
	
	QSize size;
	size.setHeight(this->size().height() - 18);
	size.setWidth(size.height());
	ui->toolButtonVisible->setIconSize(size);
	ui->toolButtonVisible->setFixedSize(size);
}

void DV3D::ControlerItem::initGui()
{
	//绑定拖动条
	connect(ui->horizontalSlider, SIGNAL(valueChanged(int)), this, SLOT(transParentSliderValueChange(int)));
	ui->toolbarLayout->setAlignment(Qt::AlignLeft);
	//创建是否可见按钮
	visibleAction.reset(new ControlerVisible());
	visibleAction->update(ui->toolButtonVisible);
	connect(ui->toolButtonVisible, SIGNAL(clicked(bool)), this, SLOT(toolButtonClicked(bool)));
	auto value = ToolButtonMap::value_type(ui->toolButtonVisible, visibleAction);
	toolButtonMap.insert(value);

	//绑定关闭按钮
	connect(ui->toolButtonClose, SIGNAL(clicked(bool)), this, SLOT(closeButtonClicked(bool)));
}

/**
* @brief DV3D::ControlerItem::toolButtonClicked 按钮被点击，调用action触发并刷新btn的状态
* @return void
*/
void DV3D::ControlerItem::toolButtonClicked(bool)
{
	auto sd = sender();
	for (auto iter = toolButtonMap.begin(); iter != toolButtonMap.end(); iter++)
	{
		if(iter->first != sd)
			continue;
		iter->second->active(controler);
		iter->second->update(iter->first);
	}
}

void DV3D::ControlerItem::transParentSliderValueChange(int value)
{
	controler->setTransparent((double)value / 100);
}

void DV3D::ControlerItem::closeButtonClicked(bool)
{
	emit itemClose();
	controler->unbing();
	close();
}
