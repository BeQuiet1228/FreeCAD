#pragma once
#ifdef _HDF5_READER_
#define CONTROL_EXPORT __declspec(dllexport)
#else
#define CONTROL_EXPORT   __declspec(dllimport)
#endif 


#include "H5Cpp.h"
#include <iostream>
#include <vector>
#include <list>
#include <map>
#include <memory>

using namespace  H5;
class Hdf5IO;
using VectorF = std::vector<float>;

class CONTROL_EXPORT Hdf5Data
{
public:
	Hdf5Data(std::shared_ptr<H5File> h5){
		this->hdf5File = h5;
	}
	Hdf5Data() = default;

public:
	enum CoordinateSystem{
		CARTESIAN = 0,
		CYLINDER,
		POLAR
	};

public:
	//数据分组对象
    Group group;
	//头部信息
    std::vector<std::string> headList;
	//h5文件对象 
    std::shared_ptr<H5File> hdf5File;
	//数据集对象
    std::vector<DataSet> listDataSet;
	//图名称
	std::string name;
	//图别名
	std::string petName;
	//坐标系类型
	CoordinateSystem coordinateSystem;

public:
	void save(const std::string& path,bool newFIle = false);
	//初始化基本信息
	bool initInformation();
	bool initPlanemation();
	bool initM3dStructInformation();
	bool initM2dStructInformation();
	void init();

	void initAttrFromList(Group& newgroup, std::vector<std::string> List);
	void addSubGroup(const std::string faterGroup, const std::string groupname, std::shared_ptr<VectorF> values, std::vector<std::string> HList);
	void addNewGroup();
};

class CONTROL_EXPORT Hdf5IO
{
public:
	enum FileOpenMod
	{
		CREAT_NEW_FILE = 0,
		OPEN_EXIST
	};
public:
	Hdf5IO();
    Hdf5IO(std::string fileName);
	~Hdf5IO();
	//设置文件路径
	void setFilePath(const std::string& path,FileOpenMod mod = OPEN_EXIST);
    void initHdf5Data();
	
    std::vector<Hdf5Data> hdf5DataList;
	//获取数据库中的值
	static bool getValue(const Group& group, const std::string& datasetName,VectorF &values);
	static bool getValue(const DataSet& dataSet,VectorF& values);
	static bool getValue(const std::vector<DataSet>& dataSets, std::list<std::shared_ptr<VectorF>>& listVales);

	//释放h5文件
	void deleteH5File();
private:
	std::shared_ptr<H5File> Hdf5File;
	//获取一个数据组
	bool getGroup(const Group& fatherGroup, const std::string groupName, Group& group);
	bool getGroup(const std::string groupName, Group& group);
	bool getGroup(H5File& file, const std::string& groupName, Group& group);

	//获取一个数据库
	bool getDataSet(const Group& group, const std::string& dataSetName, DataSet &dataSet);
	Group getGroup(const Group &group, const std::string &groupName, bool &ok);
	Group getGroup(const std::string &groupName, bool &ok);
	int getSubGroupCount(const Group &group);
    static std::vector<std::string> getHeadValue(const Group &group);
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

	//使用headlist获取观测的名称
	std::string getNameFromHeadList(const std::vector<std::string>& headList);

public:
	static Hdf5Data copyToHdf5IO(Hdf5IO& hdf5IO,Hdf5Data& data);
	static DataSet copyDataSet(DataSet& dataset, Group& toGroup, const std::string& newDataSetName);
	static void copyGroup(Group& group, Group& toGroup);
	static void copyToHdf5IO(Hdf5IO& hdf5IO, std::vector<Hdf5Data>& datas);
	static void creatNewHdf5File(const std::string& fileName);
	static void creatHdf5File(const std::string& fileName);
	//新增代码
	static int creatNewH5File(const std::string& fileName);
	static int openH5File(const std::string &fileName);
	static int closeH5File(int H5id);

	static Hdf5Data Hdf5IO::addNewGroup(Hdf5IO& hdf5IO, Hdf5Data& data, std::shared_ptr<VectorF> values, std::vector<std::string> HList);

private:
	//新增方法2021/6/30
	void LoadH5Resource();
	std::list<Group> getGrouplist();
	std::list<Group> getGrouplist(Group);
	std::vector<DataSet> getDataSetlist(Group);
	void digGroup(Group);
};

class CONTROL_EXPORT H5DataHead {
public:
	H5DataHead() = default;
	~H5DataHead() = default;

public:
	//获取$分割的属性
	static std::string  getAttributeForIndex(std::string str,int index);
	
};