#pragma once
#include <QWidget>
#include <QVTKWidget.h>
#include <vtkRenderer.h>
#include <vtkSmartPointer.h>
#include <vtkRenderWindow.h>
#include <vtkActor.h>
#include <map>
namespace DV3D {
	class Controler;
}
namespace DV3D {
	/*
		3D窗口类
		提供窗口布局，及交互方式
	*/
	class Widget3D :public QWidget {
		friend class Controler;
	public:
		Widget3D();
		~Widget3D();

	public:
		//绑定控制器
		void binding(Controler* controler);
		//解除绑定
		void unbing(Controler* controler);
		//解除所有控制器的绑定
		void unbingAllControler();
		//重新渲染
		void reRender();

	private:
		//单向解除绑定
		void oneWayUnbing(Controler* controler);
		//单向绑定
		void oneWayBinding(Controler* controler);
		//同步控制器的actor
		void synchronousControlerActor();
	public:
		//渲染器
		vtkSmartPointer<vtkRenderer> renderer;
		//渲染窗口
		QVTKWidget* viewer3d;
		vtkSmartPointer<vtkRenderWindow> renderWindow;
		//控制器
		std::map<Controler*, vtkSmartPointer<vtkActor>> controlerActor;
	};

}