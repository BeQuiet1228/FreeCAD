#pragma once
#include <object.h>
#include <memory>
#include <vtkSmartPointer.h>
#include <vtkActor.h>
namespace DV3D {
	class ActorPipemline;
	class Widget3D;
}
namespace DV3D {
	/*
	控制器
	为acotr暴露出一些操作接口，如调整是否显示、调整颜色、透明度
	并且为ActorPipeline提供对外操作的接口，可控制其中的管道顺序及中间过程的增加和减少
	*/

	class Controler :public Object {
		friend class Widget3D;
	public:
		Controler();
		~Controler();

	public:
		//双向绑定显示窗口
		void binding(Widget3D* widget3d);
		//双向解除绑定
		void unbing();
		//绑定状态
		bool isBinding();

		//设置渲染管线
		void setActorPipeline(std::shared_ptr<ActorPipemline> line) {
			this->actorPipeline = line;
		};
	private:
		//单向绑定
		void oneWayBinding(Widget3D* widget3D);
		//单向解除绑定
		void oneWayUnbing();
		
		vtkSmartPointer<vtkActor> getActor();

	protected:
		//渲染管线
		std::shared_ptr<ActorPipemline> actorPipeline;
		//显示窗口
		Widget3D* widget3D;
	private:
		bool bindingState;
	};

}