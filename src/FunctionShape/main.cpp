#include <stdio.h>
#include "InitVtk.hpp"
#include <vtkRenderer.h>
#include <vtkActor.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWindowInteractor.h>
#include <vtkPolyDataMapper.h>
#include <vtkSphere.h>
#include <vtkSampleFunction.h>
#include <vtkContourFilter.h>
#include <vtkProperty.h>
#include <vtkNew.h>
#include "MyFunction.h"
#include "TestFunctionExport.h"
int main() {

	//测试点获取
	TestExport test;
	auto vd = test.creatVtkData();

	//创建一个隐函数
	MyFuntion* function;
	function = new MyFuntion3();

	//对函数进行采样
	vtkNew<vtkSampleFunction> sample;
	sample->SetSampleDimensions(10, 10, 10);
	sample->SetImplicitFunction(function);
	//设置函数采样范围
	double value = 2.0;
	double xmin = -value, xmax = value, ymin = -value, ymax = value,
		zmin = -value, zmax = value;
	sample->SetModelBounds(xmin, xmax, ymin, ymax, zmin, zmax);
	//sample->CappingOff();
	sample->CappingOn();
	sample->SetCapValue(0);

	//提取等值面
	vtkNew<vtkContourFilter> filter;
	filter->SetInputConnection(sample->GetOutputPort());
	filter->SetValue(0, 0);


	vtkNew<vtkPolyDataMapper> mapper;
	mapper->SetInputConnection(filter->GetOutputPort());
	mapper->ScalarVisibilityOff();

	vtkNew<vtkActor> actor;
	actor->SetMapper(mapper.Get());

	vtkNew<vtkRenderer> renderer;
	vtkNew<vtkRenderWindow> window;
	window->AddRenderer(renderer.Get());

	vtkNew<vtkRenderWindowInteractor> interactor;
	interactor->SetRenderWindow(window.Get());

	renderer->AddActor(actor.Get());
	window->Render();
	interactor->Start();

	return 0;
}