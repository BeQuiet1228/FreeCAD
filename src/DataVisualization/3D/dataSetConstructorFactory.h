#pragma  once
#include <memory>
#include "dataSetConstructor.h"
#include "HDF5Reader/hdf5io.h"
namespace DV3D {

	class DataSetConstructorFactory {
	public:
		DataSetConstructorFactory() = default;
		~DataSetConstructorFactory() = default;

	public:
		static std::shared_ptr<DataSetConstructor> CreatConstructor(Hdf5Data& h5data);

	private:
		//创建结构图构造器
		static bool creatStrucConstructor(std::shared_ptr<DataSetConstructor>* constructor, Hdf5Data& h5data);
		//寻找字符串中的长度信息
		static int findStringAttribute(const std::string& str);

	};

}