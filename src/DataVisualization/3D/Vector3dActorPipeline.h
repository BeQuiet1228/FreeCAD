#pragma once
#include "actorPipeline.h"
#include "vtkArrowSource.h"
#include "UnifyXmlConfig3D.h"
#include "vtkLookupTable.h"
namespace DV3D
{
	class Vector3dActorPipeline:public ActorPipemline,public UnifyXmlConfig3D
	{
	public:
		Vector3dActorPipeline();
		~Vector3dActorPipeline();
	public:
		void update() override;
		void connect() override;
		void loadConfig();
		void updataLookupTable();
	private:
		std::vector<ColorF> colorfs;
		vtkSmartPointer<vtkLookupTable> lookupTable;
	};
}