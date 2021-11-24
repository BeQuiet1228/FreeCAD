#pragma  once
#include "object.h"
#include <vtkMapper.h>
#include <vtkDataSet.h>
#include <vtkActor.h>
#include <vtkSmartPointer.h>
namespace DV3D {
	/*
	actor 生成管线
	在这里管理actor的生成过程，包括数据的处理、剪切等
	*/
	class ActorPipemline :public Object{
	public:
		ActorPipemline();
		~ActorPipemline();


	public:
		vtkSmartPointer<vtkActor>  getActor() {
			return actor;
		}
		void setActor(vtkSmartPointer<vtkActor> ac) {
			this->actor = ac;
		}
		vtkSmartPointer<vtkMapper> getMapper() {
			return mapper;
		}
		void setMapper(vtkSmartPointer<vtkMapper> mp) {
			this->mapper = mp;
		}
		vtkSmartPointer<vtkDataSet> getDataSet() {
			return dataSet;
		}
		void setDataSet(vtkSmartPointer<vtkDataSet> dataset) {
			this->dataSet = dataset;
		}

		//更新渲染管线
		virtual void update() = 0;
		//链接管线
		virtual void connect() = 0;
	private:
		//演员
		vtkSmartPointer<vtkActor> actor;
		//映射器
		vtkSmartPointer<vtkMapper> mapper;
		//数据
		vtkSmartPointer<vtkDataSet> dataSet;
	};
}