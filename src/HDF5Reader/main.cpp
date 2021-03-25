#include <iostream>
#include "H5Cpp.h"
#include "hdf5io.h"
using namespace H5;
int main(){
	std::string path = "D:/wandaotongProject/MILO_C_Temp.h5";
	Hdf5IO io(path);

	io.initHdf5Data();
	auto data = io.hdf5DataList;
	VectorF value;
	io.getValue(data.at(0).listDataSet.at(0), value);
	printf("%f\n",value[0]);
	printf("%f\n", value[1]);
	printf("%f\n", value[2]);
}