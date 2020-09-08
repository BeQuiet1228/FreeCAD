#pragma once

#include "H5Cpp.h"
#include <iostream>
#include <vector>
using namespace  H5;
class Hdf5IO;
using VectorF = std::vector<float>;
 struct Hdf5Data
{
    Group group;
    DataSet dataSet;
    std::vector<std::string> headList;
    Hdf5IO *hdf5Io;
    std::vector<DataSet> listDataSet;
};

class Hdf5IO
{
public:
    Hdf5IO(std::string fileName);
    void initHdf5Data();
    std::vector<Hdf5Data> hdf5DataList;
	//获取数据库中的值
	bool getValue(const Group& group, const std::string& datasetName,VectorF &values);
	bool getValue(const DataSet& dataSet,VectorF& values);
    std::vector<float> getVlue(const Group &group,const std::string &dataName);
    std::vector<float> getVlue(const DataSet &dataSet);
private:
    H5File *Hdf5File;
	//获取一个数据组
	bool getGroup(const Group& fatherGroup, const std::string groupName, Group& group);
	bool getGroup(const std::string groupName, Group& group);
	bool getGroup(H5File& file, const std::string& groupName, Group& group);

	//获取一个数据库
	bool getDataSet(const Group& group, const std::string& dataSetName, DataSet &dataSet);
	Group getGroup(const Group &group, const std::string &groupName, bool &ok);
	Group getGroup(const std::string &groupName, bool &ok);
	int getSubGroupCount(const Group &group);
    std::vector<std::string> getHeadValue(const Group &group);
    Group OpenH5File(H5File &file,const std::string &groupName,bool &ok);
	Group OpenGroup(Group &group, const std::string &groupName,bool &ok);
    DataSet OpenGroupDataset(Group &group,const std::string &datasetName,bool &ok);

	//从一个组中获取所有的子组，和子组的数据库
	void getAllSubGroupAndDataSet(const Group& group,const std::vector<std::string> dataSetNames);
	//获取结构数据
	void getStructData();
	//获取grd中的数据
	void getGrdData();
	//获取par中的数据
	void getParData();
	//获取fild中的数据
	void getFildData();

};
