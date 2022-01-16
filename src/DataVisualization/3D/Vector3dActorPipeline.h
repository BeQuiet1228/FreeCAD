#pragma once
#include "actorPipeline.h"
#include "vtkArrowSource.h"
#include "vtkLookupTable.h"
#include"QColor"
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
		std::vector <QColor> colorfs;
		vtkSmartPointer<vtkLookupTable> lookupTable;
	};
}