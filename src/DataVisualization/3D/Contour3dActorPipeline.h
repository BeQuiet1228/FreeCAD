#pragma once
#include "actorPipeline.h"
#include <vtkUnstructuredGridGeometryFilter.h>
#include "vtkSmartPointer.h"
#include "vtkPolyDataNormals.h"
#include "vtkContourFilter.h"
#include "vtkLookupTable.h"
#include "XmlGroup3D.h"
namespace DV3D
{
	using ContourValue = double;
	struct ContourRang
	{
		double valMin;
		double valMax;
	};
	class  Contour3dActorPipline :public ActorPipemline{
	public:
		Contour3dActorPipline();
		~Contour3dActorPipline();
	public:
		void update() override;
		void connect() override;
		void loadConfig();
		//设置取值面个数
		void setContourSurfarCount(const int& n);
		std::vector<ContourValue> getContourValues();
		void setContourValues(std::vector<ContourValue>& values);
		double* getScalarRang();
	protected:
		void initFilter();
		void updataLookupTable();
	private:
		vtkSmartPointer<vtkContourFilter> file;
		vtkSmartPointer<vtkPolyDataNormals> normal;
		vtkSmartPointer<vtkLookupTable> lookupTable;
		//double scalarMin, scalarMax;
		ContourRang rang;
		int contourSurfarCount;//默认构造时，等值面的取值数量
		bool isInit;//是否初始化的判断
		/*
			读取配置
		*/
		//std::vector<XmlData::ColorF> colors;
		std::vector<DV::XmlData::XmlColor> colors;
	};
};