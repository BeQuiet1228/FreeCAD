#pragma once
#include "object.h"
#include <vtkAlgorithmOutput.h>
#include <vtkPlane.h>
#include <vtkSmartPointer.h>
#include <vtkTableBasedClipDataSet.h>
#include <vtkDataSet.h>
namespace DV3D {
	/*
		管道类
		定义输入输出接口，参数使用vtk标准输入输出数据
	*/
	class Pipeline :Object {
	public:
		Pipeline() = default;
		~Pipeline() = default;
	public:
		//设置输入端口
		virtual vtkAlgorithmOutput* getOutpuPort() = 0;
		//获取输出端口
		virtual void setInputConnection(vtkAlgorithmOutput* input) = 0;
		//设置输入数据
		virtual void setInputData(vtkDataObject* data) = 0;
	};
	/*
		剪切器
		负责对模型切割
	*/
	class Clipper :public Pipeline{
	public:
		Clipper();
		~Clipper() = default;

	public:
		vtkAlgorithmOutput* getOutpuPort() override;
		void setInputConnection(vtkAlgorithmOutput* input) override;
		void setInputData(vtkDataObject* data) override;
		
		//设置剪切面
		void setClipPlane(vtkSmartPointer<vtkPlane> plane);
	private:
		//剪切面
		vtkSmartPointer<vtkPlane> clipperPlane;
		//剪切工具
		vtkSmartPointer<vtkTableBasedClipDataSet> vtkClipper;
	};
}

