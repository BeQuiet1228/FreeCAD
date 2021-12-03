#include "widget3D.h"
#include "controler.h"
#include <vtkCamera.h>
DV3D::Widget3D::Widget3D()
{
	renderer = vtkSmartPointer<vtkRenderer>::New();
	renderWindow = vtkSmartPointer<vtkRenderWindow>::New();
	renderWindow->AddRenderer(renderer);
	viewer3d = new QVTKWidget(this);
	viewer3d->SetRenderWindow(renderWindow);

	renderer->SetBackground(0.0,0.0,0.0);
	renderer->ResetCamera();
	renderer->GetActiveCamera()->Elevation(60.0);
	renderer->GetActiveCamera()->Azimuth(30.0);
	renderer->GetActiveCamera()->Dolly(1.2);

	initGUI();
}

DV3D::Widget3D::~Widget3D()
{
	
}

/**
* @brief DV3D::Widget3D::binding 双向绑定控制器
* @param Controler * controler
* @return void
*/
void DV3D::Widget3D::binding(Controler* controler)
{
	oneWayBinding(controler);
	controler->oneWayBinding(this);
}

/**
* @brief DV3D::Widget3D::unbing 解除控制器绑定
* @param Controler * controler
* @return void
*/
void DV3D::Widget3D::unbing(Controler* controler)
{
	oneWayUnbing(controler);
	controler->oneWayUnbing();
}

void DV3D::Widget3D::unbingAllControler()
{
	for (auto iter = controlerActor.begin(); iter != controlerActor.end(); iter++)
		unbing(iter->first);
}

void DV3D::Widget3D::reRender()
{
	viewer3d->GetInteractor()->Render();
}

void DV3D::Widget3D::initGUI()
{
	centerLayout = new QVBoxLayout(this);
	this->setLayout(centerLayout);
	centerLayout->addWidget(viewer3d);

	//test
	this->resize(500,500);
}

/**
* @brief DV3D::Widget3D::oneWayUnbing 取消控制器绑定，并移除对应的actor
* @param Controler * controler
* @return void
*/
void DV3D::Widget3D::oneWayUnbing(Controler* controler)
{
	auto citer = controlerActor.find(controler);
	if (citer == controlerActor.end())
		return;

	renderer->RemoveActor(citer->second);
	controlerActor.erase(citer);
}
/**
* @brief DV3D::Widget3D::oneWayBinding 将控制器绑定到widget，并为其绑定渲染器和渲染窗口
* @param Controler * controler
* @return void
*/
void DV3D::Widget3D::oneWayBinding(Controler* controler)
{
	auto citer = controlerActor.find(controler);
	if (citer != controlerActor.end())
		return;

	auto actor = controler->getActor();
	renderer->AddActor(actor);
	
	auto value = std::map<Controler*, vtkSmartPointer<vtkActor>>::value_type(controler, actor);
	controlerActor.insert(value);
}

/**
* @brief DV3D::Widget3D::synchronousControlerActor 如果acotr的指针发生变化，那么将旧的acotr移除，更新为新的acotr
* @return void
*/
void DV3D::Widget3D::synchronousControlerActor()
{
	for (auto iter = controlerActor.begin(); iter != controlerActor.end(); iter++)
	{
		if (iter->second != iter->first->getActor())
		{
			renderer->RemoveActor(iter->second);
			renderer->AddActor(iter->first->getActor());
			iter->second = iter->first->getActor();
		}
	}

}

