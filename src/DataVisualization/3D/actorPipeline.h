#pragma  once
#include "object.h"
#include <vtkMapper.h>
#include <vtkDataSet.h>
#include <vtkActor.h>
#include <vtkSmartPointer.h>
#include <memory>
#include <vtkAlgorithmOutput.h>
#include <vtkPlane.h>
#include "XmlGroup3D.h"
namespace DV3D {
	class Clipper;

	/*
	actor 生成管线
	在这里管理actor的生成过程，包括数据的处理、剪切等
	*/
	class ActorPipemline :public Object{
	public:
		ActorPipemline();
		~ActorPipemline();


	public:
		//get set
		vtkSmartPointer<vtkActor>  getActor();
		void setActor(vtkSmartPointer<vtkActor> ac);

		vtkSmartPointer<vtkMapper> getMapper();
		void setMapper(vtkSmartPointer<vtkMapper> mp);

		vtkSmartPointer<vtkDataSet> getDataSet();
		void setDataSet(vtkSmartPointer<vtkDataSet> dataset);

		bool getClipperEnable();
		void setClipperEnable(const bool& b);

		void setClipper(std::shared_ptr<Clipper> clipper);
		void getClipPlane(vtkSmartPointer<vtkPlane>& palne);
		//更新渲染管线
		virtual void update() = 0;
		//链接管线
		virtual void connect() = 0;
		//设置剪切面
		void setClipPlane(vtkSmartPointer<vtkPlane> plane);
		//获取控制台参数
		virtual XmlData::ControlerXml getControlerData() = 0;
	protected:
		//将剪切器数据连接到映射器
		void connectClipperToMapper(vtkAlgorithmOutput* input);
		void connectClipperToMapper(vtkDataObject* data);
	private:
		//演员
		vtkSmartPointer<vtkActor> actor;
		//映射器
		vtkSmartPointer<vtkMapper> mapper;
		//数据
		vtkSmartPointer<vtkDataSet> dataSet;
		//剪切器
		std::shared_ptr<Clipper> clipper;
		//剪切器状态
		bool clipperEnable;
	};
}