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

vtkSmartPointer<vtkActor> DV3D::Controler::getActor()
{
	assert(actorPipeline && "actorPipeline can not be nullptr!");
	return actorPipeline->getActor();
}

bool DV3D::Controler::isBinding()
{
	return bindingState;
}

void DV3D::Controler::setActorPipeline(std::shared_ptr<ActorPipemline> line)
{
	this->actorPipeline = line;
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
}

double DV3D::Controler::getTranparent()
{
	auto actor = getActorPipeline()->getActor();
	return actor->GetProperty()->GetOpacity();
}

