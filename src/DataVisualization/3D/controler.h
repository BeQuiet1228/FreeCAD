#pragma once
#include <object.h>
#include <memory>
#include <vtkSmartPointer.h>
#include <vtkActor.h>
#include <vtkPlane.h>
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
		//刷新3d窗口
		void updateWidget3D();

		//设置渲染管线
		void setActorPipeline(std::shared_ptr<ActorPipemline> line);
		std::shared_ptr<ActorPipemline> getActorPipeline();
		//设置actor是否可见
		void setVisible(const bool& b);
		bool getVisible();
		//设置透明度
		void setTransparent(const double& t);
		double getTranparent();
		//设置线是否可见
		void setEdgeVisible(const bool& b);
		bool getEdgeVisible();
		//设置剪切
		void setClipEnable(const bool& b);
		bool getClipEnable();
		void setClipPlane(vtkSmartPointer<vtkPlane> palne);
	private:
		//单向绑定
		void oneWayBinding(Widget3D* widget3D);
		//单向解除绑定
		void oneWayUnbing();
		
		vtkSmartPointer<vtkActor> getActor();
	protected:
		//获取3d窗口
		Widget3D* getWidget3D();

	private:
		//渲染管线
		std::shared_ptr<ActorPipemline> actorPipeline;
		//显示窗口
		Widget3D* widget3D;
	private:
		bool bindingState;
	};

}