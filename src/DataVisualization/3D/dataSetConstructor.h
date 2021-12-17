#pragma once
#include "object.h"
#include <memory>
#include <vtkDataSet.h>
#include <vtknew.h>
#include <vtkSmartPointer.h>
#include <HDF5Reader/hdf5io.h>
namespace DV
{
	class Data;
};
namespace DV3D {
	/*
	vtkDataSet构造器
	通过其他类型的数据构造出vtkDataSet数据
	*/
	class DataSetConstructor:public Object {
	public:
		DataSetConstructor();
		~DataSetConstructor();

	public:
		//生成vtk数据对象
		virtual vtkSmartPointer<vtkDataSet> creatDataset() = 0;
	};
	

	//通过Hdf5Data数据构造出vtkDataSet数据
	class DataSetConstructorH5 : public DataSetConstructor {
	public:
		DataSetConstructorH5() = default;
		~DataSetConstructorH5() = default;

	public:
		//设置原始数据
		void setHdf5Data(Hdf5Data& h5d);
		Hdf5Data getHdf5Data();
	private:
		Hdf5Data h5data;
	};


	//通过DataVisualization项目中的Data数据构造vtkDataSet数据
	class DataSetConstructorFor2DData :public DataSetConstructor {
	public:
		DataSetConstructorFor2DData() = default;
		~DataSetConstructorFor2DData() = default;

	public:
		//设置原始数据对象
		void setSourceData(std::shared_ptr<DV::Data> d);
		std::shared_ptr<DV::Data> getSourceData();
	private:
		std::shared_ptr<DV::Data> data;
	};

}

