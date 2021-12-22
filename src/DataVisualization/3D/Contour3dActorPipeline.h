#pragma once
#include "actorPipeline.h"
#include <vtkUnstructuredGridGeometryFilter.h>
#include "vtkSmartPointer.h"
#include "vtkPolyDataNormals.h"
#include "vtkContourFilter.h"
namespace DV3D
{
	using ContourValue = double;
	struct ContourRang
	{
		double valMin;
		double valMax;
	};
	class  Contour3dActorPipline :public ActorPipemline {
	public:
		Contour3dActorPipline();
		~Contour3dActorPipline();
	public:
		void update() override;
		void connect() override;
		//设置取值面个数
		void setContourSurfarCount(const int& n);
		std::vector<ContourValue> getContourValues();
		void setContourValues(std::vector<ContourValue>& values);
	protected:
		void initFilter();
	private:
		vtkSmartPointer<vtkContourFilter> file;
		//double scalarMin, scalarMax;
		ContourRang rang;
		int contourSurfarCount;//默认构造时，等值面的取值数量
		bool isInit;//是否初始化的判断
	};
};