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
