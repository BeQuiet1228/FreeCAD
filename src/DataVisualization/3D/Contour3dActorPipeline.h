#pragma once
#include "actorPipeline.h"
#include <vtkUnstructuredGridGeometryFilter.h>
#include "vtkSmartPointer.h"
#include "vtkPolyDataNormals.h"
#include "vtkContourFilter.h"
namespace DV3D
{
	class  Contour3dActorPipline :public ActorPipemline {
	public:
		Contour3dActorPipline();
		~Contour3dActorPipline();
	public:
		void update() override;
		void connect() override;
		//设置取值面个数
		void setContourSurfarCount(const int& n);
	private:
		vtkSmartPointer<vtkContourFilter> file;
		double scalarMin, scalarMax;
		int contourSurfarCount;
	};
};