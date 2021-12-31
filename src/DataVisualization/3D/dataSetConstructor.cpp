#include "dataSetConstructor.h"

DV3D::DataSetConstructor::DataSetConstructor()
{
	setObjectName("DataSetConstructor");
}

DV3D::DataSetConstructor::~DataSetConstructor()
{

}



void DV3D::DataSetConstructorH5::setHdf5Data(Hdf5Data& h5d)
{
	this->h5data = h5d;
}


Hdf5Data DV3D::DataSetConstructorH5::getHdf5Data()
{
	return h5data;
}

void DV3D::DataSetConstructorFor2DData::setSourceData(std::shared_ptr<DV::Data> d)
{
	this->data = d;
}

std::shared_ptr<DV::Data> DV3D::DataSetConstructorFor2DData::getSourceData()
{
	return this->data;
}

void DV3D::DataSetConstructorH5S::setHdf5Datas(std::vector<Hdf5Data> h5ds)
{
	for (auto iter = h5ds.begin(); iter != h5ds.end(); iter++)
	{
		if (iter->name != "struct")
			h5datas.push_back(*iter);
		else
			structH5data = *iter;
	}
}

std::vector<Hdf5Data> DV3D::DataSetConstructorH5S::getHdf5Datas()
{
	return h5datas;
}
Hdf5Data DV3D::DataSetConstructorH5S::getStructData()
{
	return structH5data;
}