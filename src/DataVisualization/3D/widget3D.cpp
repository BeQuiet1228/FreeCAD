#include "widget3D.h"
#include "controler.h"
#include <vtkCamera.h>
#include <QVTKInteractor.h>
#include <vtkInteractorStyleJoystickCamera.h>
#include <vtkScalarsToColors.h>
#include"vtkAxesActor.h"
DV3D::Widget3D::Widget3D(QWidget* parent /*= 0*/)
	:QWidget(parent)
{
	renderer = vtkSmartPointer<vtkRenderer>::New();

	viewer3d = new QVTKWidget(this);
	viewer3d->GetRenderWindow()->AddRenderer(renderer);

	renderer->SetBackground(0.529, 0.8078, 0.92157);
	renderer->SetBackground2(1.0, 1.0, 1.0);
	renderer->SetGradientBackground(1);

	//初始化颜色条
	scalarBarActor = vtkSmartPointer<vtkScalarBarActor>::New();
	scalarBarActor->SetLookupTable(vtkScalarsToColors::New());
	scalarBarActor->SetNumberOfLabels(6);
	renderer->AddActor(scalarBarActor);


#if 0 //添加一个三维坐标系,用于判断方位
	vtkSmartPointer<vtkAxesActor> axes = vtkSmartPointer<vtkAxesActor>::New();
	renderer->AddActor(axes);
#endif
	initGUI();
}

DV3D::Widget3D::~Widget3D()
{
	unbingAllControler();
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
	while (controlerActor.size()!=0)
	{
		auto iter = controlerActor.begin();
		unbing(iter->first);
	}
		
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
	reRender();
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

	reRender();
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

