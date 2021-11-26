#pragma once
#ifndef CYLINDER_PLAN_CONSTRUCT_H_
#define CYLINDER_PLAN_CONSTRUCT_H_
#include"CylinderStructDataSetConstructor.h"
namespace DV3D
{
	class CylinderPlanConstruct :public CylinderStructDataSetConstructor
	{
	public:
		CylinderPlanConstruct();
		~CylinderPlanConstruct();
	public:
		vtkSmartPointer<vtkDataSet> creatDataset();
	};
};
#endif