#include "ui_ControlerItem.h"
#include "ControlerItem.h"
#include <cassert>
#include "ControlerAction.h"
#include <iostream>
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
	controler->unbing();
	close();
}
