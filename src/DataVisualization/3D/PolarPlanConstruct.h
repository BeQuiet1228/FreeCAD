#pragma once
#ifndef POLAR_PLAN_CONSTRUCT_H_
#define POLAR_PLAN_CONSTRUCT_H_
#include"PolarStructDataSetConstructor.h"
namespace DV3D
{
	class PolarPlanConstruct:public PolarStructDaraSetConstruct
	{
	public:
		PolarPlanConstruct();
		~PolarPlanConstruct();
	public:
		vtkSmartPointer<vtkDataSet> creatDataset();
	};
};
#endif