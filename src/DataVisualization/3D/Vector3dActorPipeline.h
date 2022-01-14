#pragma once
#include "actorPipeline.h"
#include "vtkArrowSource.h"
#include "vtkLookupTable.h"
#include "XmlGroup3D.h"
namespace DV3D
{
	class Vector3dActorPipeline:public ActorPipemline
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
		//std::vector<XmlData::ColorF> colorfs;
		std::vector <DV::XmlData::XmlColor > colorfs;
		vtkSmartPointer<vtkLookupTable> lookupTable;
	};
}