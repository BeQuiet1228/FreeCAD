#include "controler.h"
#include "widget3d.h"
#include "actorPipeline.h"
#include <cassert>
#include <vtkProperty.h>
DV3D::Controler::Controler()
	:widget3D(nullptr),bindingState(false),actorPipeline(nullptr)
{
	
}

DV3D::Controler::~Controler()
{
	unbing();
}

/**
* @brief DV3D::Controler::binding 为控制器绑定显示窗口
* @param Widget3D * widget3d
* @return void
*/
void DV3D::Controler::binding(Widget3D* widget3d)
{
	oneWayBinding(widget3d);
	this->widget3D->oneWayBinding(this);
	
}

/**
* @brief DV3D::Controler::unbing 解除显示窗口绑定
* @return void
*/
void DV3D::Controler::unbing()
{
	if (!bindingState)
		return;
	widget3D->oneWayUnbing(this);
	oneWayUnbing();
}

/**
* @brief DV3D::Controler::oneWayBinding 单向绑定显示窗口，这个函数在widget3d中被调用，防止循环调用
* @param Widget3D * widget3D
* @return void
*/
void DV3D::Controler::oneWayBinding(Widget3D* widget3D)
{
	if (bindingState)
		this->widget3D->oneWayUnbing(this);
	this->widget3D = widget3D;
	bindingState = true;
}

/**
* @brief DV3D::Controler::oneWayUnbing 单向解除绑定，这个函数在widget3d中被调用，防止循环调用
* @return void
*/
void DV3D::Controler::oneWayUnbing()
{
	if (!bindingState)
		return;
	bindingState = false;
	widget3D = nullptr;
}

bool DV3D::Controler::isBinding()
{
	return bindingState;
}

void DV3D::Controler::updateWidget3D()
{
	if (!isBinding())
		return;
	auto w3d = getWidget3D();
	w3d->reRender();
}

void DV3D::Controler::setActorPipeline(std::shared_ptr<ActorPipemline> line)
{
	this->actorPipeline = line;
	/*
		设置控制台的默认状态
	*/
	setInitState(line->getControlerData());
}

std::shared_ptr<DV3D::ActorPipemline> DV3D::Controler::getActorPipeline()
{
	assert(actorPipeline && "actorPipeline is nullptr!");
	return actorPipeline;
}

DV3D::Widget3D* DV3D::Controler::getWidget3D()
{
	assert(isBinding() && "controler is not binding!");
	return widget3D;
}

void DV3D::Controler::setVisible(const bool& b)
{
	auto actor = getActorPipeline()->getActor();
	if (b)
		actor->VisibilityOn();
	else
		actor->VisibilityOff();
	updateWidget3D();
}

bool DV3D::Controler::getVisible()
{
	auto actor = getActorPipeline()->getActor();
	return actor->GetVisibility();
}

void DV3D::Controler::setTransparent(const double& t)
{
	auto actor = getActorPipeline()->getActor();
	actor->GetProperty()->SetOpacity(t);
	updateWidget3D();
}

double DV3D::Controler::getTranparent()
{
	auto actor = getActorPipeline()->getActor();
	return actor->GetProperty()->GetOpacity();
}

void DV3D::Controler::setEdgeVisible(const bool& b)
{
	auto ac = getActorPipeline()->getActor();
	ac->GetProperty()->SetEdgeVisibility(b);
	updateWidget3D();
}

bool DV3D::Controler::getEdgeVisible()
{
	auto ac = getActorPipeline()->getActor();
	return ac->GetProperty()->GetEdgeVisibility();
}

void DV3D::Controler::setClipEnable(const bool& b)
{
	//如果剪切状态跟之前不一致，那么刷新管线
	if (getClipEnable() == b)
		return;

	getActorPipeline()->setClipperEnable(b);
	getActorPipeline()->update();

	updateWidget3D();
}

bool DV3D::Controler::getClipEnable()
{
	return	getActorPipeline()->getClipperEnable();
}


void DV3D::Controler::setInitState(XmlData::ControlerXml val)
{
	auto data = getActorPipeline()->getControlerData();
	setEdgeVisible(data.gridEnable);
	setClipEnable(data.clipEnable);
	setTransparent(data.alpha);
	vtkSmartPointer<vtkPlane> planF = vtkSmartPointer<vtkPlane>::New();
	planF->SetOrigin(data.centerPoint.x(),data.centerPoint.y(),data.centerPoint.z());
	planF->SetNormal(data.normalPoint.x(), data.normalPoint.y(), data.normalPoint.z());
}

