#pragma once
#ifndef CYLINDER_STRUCT_DATASET_CONSTRUCTOR_H_
#define CYLINDER_STRUCT_DATASET_CONSTRUCTOR_H_
#include"PolarStructDataSetConstructor.h"
namespace DV3D
{
	class CylinderStructDataSetConstructor: public PolarStructDaraSetConstruct
	{
	public :
		CylinderStructDataSetConstructor();
		~CylinderStructDataSetConstructor();
	public :
		virtual PolarDatas getPolarDatas();
		virtual PolarIndes getPolarIndex();
	};
};

#endif 