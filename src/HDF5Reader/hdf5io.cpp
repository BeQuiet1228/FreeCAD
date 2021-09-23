#include "hdf5io.h"
#include <memory>
#include <QString>
#include <QStringList>
#include <QTextCodec>
Hdf5IO::Hdf5IO(std::string fileName)
{
	setFilePath(fileName);
}

Hdf5IO::Hdf5IO()
{
	
}

Hdf5IO::~Hdf5IO()
{

}

void Hdf5IO::setFilePath(const std::string& path, FileOpenMod mod /*= OPEN_EXIST*/)
{
	auto gbk = QTextCodec::codecForName("gb2312");

	QString temp = QString::fromUtf8(path.c_str());
	std::string newPath = gbk->fromUnicode(temp).data();
	try
	{
		if(mod == OPEN_EXIST)
			Hdf5File.reset(new H5File(newPath, H5F_ACC_RDWR));
		else
			Hdf5File.reset(new H5File(newPath, H5F_ACC_TRUNC));

		this->hdf5DataList.clear();
	}
	catch (...)
	{
#ifdef MY_DEBUG
		std::cerr << "Hdf5IO::setFilePath open hdf5 file failed!" << std::endl;
#endif // DEBUG
	}

}

/*
 * 获取一个数据组
 */
Group Hdf5IO::getGroup(const Group &group,const std::string &groupName,bool &ok)
{
	Group g;
	try
	{
		g = group.openGroup(groupName);
		ok = true;
	}catch (...){
#ifdef MY_DEBUG
		std::cerr << "Hdf5IO::getGroup failde! group name:" + groupName << std::endl;
#endif
		ok = false;
	}
    return g;
}
/*
 * 获取一个数据组
 */
Group Hdf5IO::getGroup(const std::string &groupName,bool &ok)
{
	Group g;
	try
	{
		ok = true;
		g = OpenH5File(*Hdf5File,groupName,ok);
	}catch (...){
#ifdef MY_DEBUG
		std::cerr << "Hdf5IO::getGroup failde! group name:" + groupName << std::endl;
#endif
		ok = false;
	}
    return g;
}

/**
* @brief Hdf5IO::getGroup 从数据组中获取子组
* @param const Group & fatherGroup 数据组对象
* @param const std::string groupName 子组名称
* @param Group & group 
* @return bool
*/
bool Hdf5IO::getGroup(const Group& fatherGroup, const std::string groupName, Group& group)
{
	try
	{
		group = fatherGroup.openGroup(groupName);
	}
	catch (...){
#ifdef MY_DEBUG
		std::cerr << "Hdf5IO::getGroup failde! group name:" + groupName << std::endl;
#endif
		return false;
	}
	return true;
}

/**
* @brief Hdf5IO::getGroup 从this->Hdf5File中的数据组中获取子组
* @param const std::string groupName 子组的名称
* @param Group & group
* @return bool
*/
bool Hdf5IO::getGroup(const std::string groupName, Group& group)
{
	try{
		return getGroup(*Hdf5File, groupName, group);
	}catch (...){
#ifdef MY_DEBUG
		std::cerr << "Hdf5IO::getGroup failde! group name:" + groupName << std::endl;
#endif
		return false;
	}
	return true;
}

/**
* @brief Hdf5IO::getGroup 从h5file对象中获取一个组
* @param H5File & file h5
* @param const std::string & groupName
* @param Group & group
* @return bool
*/
bool Hdf5IO::getGroup(H5File& file, const std::string& groupName, Group& group)
{
	try
	{
		group = file.openGroup(groupName);
	}catch (...){
#ifdef MY_DEBUG
		std::cerr << "Hdf5IO::getGroup get group for h5file failde! group name:" + groupName;
#endif
		return false;
	}
	return true;
}

/**
* @brief Hdf5IO::getDataSet 获取一个数据库
* @param const Group & group 数据组对象
* @param const std::string & dataSetName 数据库名称
* @param DataSet & dataSet 
* @return bool
*/
bool Hdf5IO::getDataSet(const Group& group, const std::string& dataSetName, DataSet &dataSet)
{
	try
	{
		dataSet = group.openDataSet(dataSetName);
	}catch (...){
#ifdef MY_DEBUG
		std::cerr << "Hdf5IO::getDataSet get data set failde! data set name:" + dataSetName;
#endif
		return false;
	}

	return true;
}

/*
 * 获取一个数据组下有多少个子组
 */
int Hdf5IO::getSubGroupCount(const Group &group)
{
	int size = 0;
	try
	{
		size = group.getNumObjs();
	}catch (...)
	{
	
	}
    return size;
}

/**
* @brief Hdf5IO::getHeadValue 获取一个组的头部信息
* @param const Group & group
* @return std::vector<std::string>
*/
std::vector<std::string> Hdf5IO::getHeadValue(const Group &group)
{

    int headCount = group.getNumAttrs();    //获取头部信息的数量
	std::vector<std::string> headValue;
    for(int i = 0;i < headCount;i++)
    {
        Attribute at = group.openAttribute(i);
        std::string value;
        at.read(at.getStrType(),value);
		std::string name;
		at.getName(name);
        headValue.push_back(name+"="+value);
    }
    return headValue;
}

/**
* @brief Hdf5IO::getValue 获取数据库中的所有数值
* @param const Group & group 数据组
* @param const std::string & datasetName 数据库的名称
* @param VectorF & values 值
* @return bool 是否获取成功
*/
bool Hdf5IO::getValue(const Group& group, const std::string& datasetName, VectorF &values)
{
	try{
		DataSet dataset = group.openDataSet(datasetName);
		return getValue(dataset,values);
	}catch (...){
		return false;
	}
}

/**
* @brief Hdf5IO::getValue
* @param const DataSet & dataSet 数据库对象
* @param VectorF values
* @return bool
*/
bool Hdf5IO::getValue(const DataSet& dataSet, VectorF& values)
{
	//获取数据对象
	DataSpace dataSpace;
	try
	{
		dataSpace = dataSet.getSpace();
	}
	catch (...){
		std::cerr << "";
		return false;
	}
	//数据大小 行与列的长度
	hsize_t size[2];
	dataSpace.getSimpleExtentDims(size, 0);
	std::shared_ptr<float> value(new float[size[0] * size[1]]);

	dataSet.read(value.get(), PredType::NATIVE_FLOAT);

	values.reserve(size[0] * size[1]);
	for (int i = 0; i < size[0] * size[1]; i++)
	{
		values.push_back(value.get()[i]);

	}
	return true;
}

/**
* @brief Hdf5IO::getValue 获取一组数据集中所有的值
* @param const std::vector<DataSet> & dataSets  一组数据集
* @param list<std::shared_ptr<VectorF>> & listVales 获取到的值
* @return bool 是否获取成功
*/
bool Hdf5IO::getValue(const std::vector<DataSet>& dataSets, std::list<std::shared_ptr<VectorF>>& listVales)
{
	listVales.clear();

	bool ok = true;

	for (auto dataSetIter = dataSets.begin(); dataSetIter != dataSets.end(); dataSetIter++)
	{
		std::shared_ptr<VectorF> values(new VectorF);
		ok = ok && getValue(*dataSetIter, *(values.get()));
		listVales.push_back(values);
	}

	return ok;
}

/*
 * 打开一个h5文件，从中获取一个数据组
 */
Group Hdf5IO::OpenH5File(H5File &file, const std::string &groupName, bool &ok)
{
    std::cerr << "获取数据组：" + groupName;
    Group g;
    try
    {
       g = file.openGroup(groupName);
	   ok = true;
    }catch(...)
    {
#ifdef MY_DEBUG
       std::cerr << "获取数据组失败，数据组名:" + groupName;
#endif
	   ok = false;
    }

    return g;
}
/*
 * 打开一个数据组，从里面获取一个组
 */
Group Hdf5IO::OpenGroup(Group &group, const std::string &groupName,bool &ok)
{
    Group g;
    try
    {
       g = group.openGroup(groupName);
	   ok = true;
    }catch(...)
    {
#ifdef MY_DEBUG
       std::cerr << "获取数据组失败，数据组名:" + groupName;
#endif
	   ok = false;
    }

    return g;
}
/*
 * 打开一个数据组，获取其中的一个数据库
 */
DataSet Hdf5IO::OpenGroupDataset(Group &group, const std::string &datasetName, bool &ok)
{
    DataSet d;
    try
    {
       d = group.openDataSet(datasetName);
	   ok = true;
    }catch(...)
    {
#ifdef MY_DEBUG
       std::cerr << "获取数据库组失败，数据库名:" + datasetName;
#endif
	   ok = false;
    }

    return d;
}

/**
* @brief Hdf5IO::getAllSubGroupAndDataSet 获取该数据组下的所有子组和数据库 获取完之后 自动放入this->h5datalist中
* @param const Group & group 
* @param const std::vector<std::string> dataSetNames 数据库名称
* @return void
*/
void Hdf5IO::getAllSubGroupAndDataSet(const Group& group, const std::vector<std::string> dataSetNames)
{
	int count = getSubGroupCount(group);
	for (int i = 1; i < count + 1; i++)
	{
		Group subGroup;
		if (!getGroup(group, "subGroup" + std::to_string(i), subGroup))
			continue;

		std::vector<std::string> headList = getHeadValue(subGroup);
		//如果头数据为空，则说明该图为空
		if (headList.empty())
		{
			continue;
		}

		std::vector<DataSet> datas;
		for (auto i = dataSetNames.begin(); i != dataSetNames.end(); i++)
		{
			DataSet dataSet;
			if (!getDataSet(subGroup, *i, dataSet))
				continue;
			datas.push_back(dataSet);
		}	

		Hdf5Data data(this->Hdf5File);
		data.listDataSet = datas;
		data.group = subGroup;
		data.headList = headList;
		data.init();
		hdf5DataList.push_back(data);
	}
}

/*获取结构数据*/
void Hdf5IO::getStructData()
{
	Group group;
	if (!getGroup("Group_kmat", group))
		return;

	DataSet dataSet1, dataSet2, dataSet3, dataSet4;
		//获取数据库
	if (!(getDataSet(group, "I1MX", dataSet1)
		&& getDataSet(group, "I2MX", dataSet2)))
		return;	

	std::vector<std::string> headList = getHeadValue(group);

	//如果头数据为空，则说明该图为空
	if (!headList.empty())
	{
		Hdf5Data data(this->Hdf5File);
		if (getDataSet(group, "I1MX", dataSet1))
			data.listDataSet.push_back(dataSet1);
		if(getDataSet(group, "I2MX", dataSet2))
			data.listDataSet.push_back(dataSet2);
		if(getDataSet(group, "I3MX", dataSet3))
			data.listDataSet.push_back(dataSet3);
		if(getDataSet(group, "datasetKmt", dataSet4))
			data.listDataSet.push_back(dataSet4);
		data.group = group;
		data.name = "struct";
		data.headList = headList;
		data.init();
		hdf5DataList.push_back(data);
	}
}

/*获取par中的数据*/
void Hdf5IO::getParData()
{
	Group group;
	if(!getGroup("Group_part",group))
		return;
	int count = getSubGroupCount(group);
	for (int i = 1; i < count + 1; i++)
	{
		Group subGroup;
		if (!getGroup(group, "subGroup" + std::to_string(i), subGroup))
			continue;
		DataSet dataSet;
		if (!getDataSet(subGroup, "datasetPar", dataSet))
			continue;

		std::vector<std::string> headList = getHeadValue(subGroup);
		//如果头数据为空，则说明该图为空
		if (headList.empty())
		{
			continue;
		}

		Hdf5Data data(this->Hdf5File);
		data.listDataSet.push_back(dataSet);
		data.group = subGroup;
		data.headList = headList;
		data.init();
		hdf5DataList.push_back(data);
	}
}
/*获取fild中的数据*/
void Hdf5IO::getFildData()
{

	Group group,subGroup;
	if (!getGroup("Group_fild", group))
		return;
	//获取子组
	if (!getGroup(group, "2D_contour", subGroup))
		return;
	//配置子组中的数据库名
	std::vector<std::string> dataSetNames;
	dataSetNames.push_back("datasetEmA");
	dataSetNames.push_back("datasetEmB");
	dataSetNames.push_back("datasetEmC");
	//获取组中所有的子组以及数据库
	getAllSubGroupAndDataSet(subGroup, dataSetNames);

	if (!getGroup(group, "2D_vectors", subGroup))
		return;
	//获取组中所有的子组以及数据库
	getAllSubGroupAndDataSet(subGroup, dataSetNames);

	//这里没有获取三维等位图的数据，以后再添加
}

/**
* @brief Hdf5IO::getNameFromHeadList 在投部信息中获取观测别名
* @param const std::vector<std::string> & headList
* @return std::string
*/
std::string Hdf5IO::getNameFromHeadList(const std::vector<std::string>& headList)
{
	if (headList.size() < 14)
		return "";
	auto temp = headList.at(13);
	QString qs = QString::fromStdString(temp);
	qs = qs.simplified();
	qs = qs.split(":").last().toLower();

	return qs.toStdString();
}


DataSet Hdf5IO::copyDataSet(DataSet& dataset, Group& toGroup, const std::string& newDataSetName)
{
	//数据大小 行与列的长度
	DataSpace dataSpace = dataset.getSpace();

	hsize_t size[2];
	dataSpace.getSimpleExtentDims(size, 0);
	float* values(new float[size[0] * size[1]]);
	dataset.read(values, PredType::NATIVE_FLOAT);

	DataSpace sapce(2, size);
	DataType dataType(PredType::NATIVE_FLOAT);
	DataSet toDataSet(toGroup.createDataSet(newDataSetName, dataType, dataSpace));
	toDataSet.write(values, dataType);

	delete[] values;

	return toDataSet;
}

void Hdf5IO::copyGroup(Group& group, Group& toGroup)
{
	unsigned int attrSpace = 128;

	int atCount = group.getNumAttrs();
	for (int i = 0; i < atCount; i++)
	{
		Attribute attr = group.openAttribute(i);

		hsize_t dims[1] = {1};
		DataSpace attr_dataspace = DataSpace(1, dims);
		DataType dataType(H5T_STRING,128);

		Attribute toAttr = toGroup.createAttribute(attr.getName(), dataType,attr_dataspace);
		std::string value;
		attr.read(attr.getStrType(), value);
		toAttr.write(dataType, value);
	}
}


Hdf5Data Hdf5IO::copyToHdf5IO(Hdf5IO& hdf5IO, Hdf5Data& data)
{
	int groupSize = hdf5IO.Hdf5File->getNumObjs();
	std::string groupName = "DataGroup" + QString::number(groupSize).toStdString();
	Group toGroup(hdf5IO.Hdf5File->createGroup(groupName));
	copyGroup(data.group, toGroup);

	Hdf5Data newH5data(hdf5IO.Hdf5File);

	auto datalist = data.listDataSet;
	for (int i = 0; i < datalist.size(); i++)
	{
		auto dataset = datalist.at(i);
		std::string dataSetName = data.group.getObjnameByIdx(i);
		DataSet newDataSet = copyDataSet(dataset, toGroup, dataSetName);
		newH5data.listDataSet.push_back(newDataSet);
	}
	newH5data.group = toGroup;
	auto headlist = getHeadValue(toGroup);
	newH5data.headList = headlist;
	newH5data.init();
	return newH5data;
}

void Hdf5IO::copyToHdf5IO(Hdf5IO& hdf5IO, std::vector<Hdf5Data>& datas)
{
	for each (Hdf5Data data in datas)
	{
		copyToHdf5IO(hdf5IO, data);
	}
}

/**
* @brief Hdf5IO::creatNewHdf5File 
* @param const std::string & fileName
* @return void
*/
void Hdf5IO::creatNewHdf5File(const std::string& fileName)
{
	auto gbk = QTextCodec::codecForName("gb2312");

	QString temp = QString::fromUtf8(fileName.c_str());
	std::string newPath = gbk->fromUnicode(temp).data();
	int res=H5Fcreate(newPath.c_str(), H5F_ACC_TRUNC, H5P_DEFAULT, H5P_DEFAULT);
}

void Hdf5IO::creatHdf5File(const std::string& fileName)
{
	auto gbk = QTextCodec::codecForName("gb2312");

	QString temp = QString::fromUtf8(fileName.c_str());
	std::string newPath = gbk->fromUnicode(temp).data();
	H5Fcreate(newPath.c_str(), H5F_ACC_RDWR, H5P_DEFAULT, H5P_DEFAULT);
}

/**
* @brief Hdf5IO::deleteH5File 释放调h5文件 并关闭所有的组与数据库
* @return void
*/
void Hdf5IO::deleteH5File()
{
	Hdf5File.reset();
	hdf5DataList.clear();
}

/**
* @brief Hdf5IO::getGrdData
* @return void
*/
void Hdf5IO::getGrdData()
{
	Group grdGroup;
	if (!getGroup("Group_grid", grdGroup))
		return;

	Group ObserveGroup;
	if (!getGroup(grdGroup, "2D_observe", ObserveGroup))
		return;
	//获取grd组中的数据
	std::vector<std::string> datasetNames;
	datasetNames.push_back("datasetGrd");
	getAllSubGroupAndDataSet(ObserveGroup, datasetNames);

	Group rangeGroup;
	if (!getGroup(grdGroup, "2D_rangers", rangeGroup))
		return;
	getAllSubGroupAndDataSet(rangeGroup, datasetNames);
}
/*
 * 初始化所有的图的数据组、数据库、头部信息
 */
void Hdf5IO::initHdf5Data()
{
#if 0
    // 获取结构数据
     {
		 getStructData();
     }
    //获取所有grd的数据组
    {
		getGrdData();
    }
    //获取par的数据组
    {
		getParData();
    }
    //获取二维等位图数据
    {
		getFildData();
    }
#endif
#if 1
	LoadH5Resource();
#endif
}


/**
* @brief Hdf5Data::initInformation 初始化通用数据信息
* @return bool
*/
bool Hdf5Data::initInformation()
{
	if (headList.size() == 0)
		return false;
	QString str = QString::fromStdString(headList.at(0));
	QStringList sl = str.split("=");
	if (sl.size() < 2)
		return false;
	str = sl.at(1);

	sl = str.split("$");

	if (sl.size() < 2)
		return false;
	QString temp = sl.at(1);
	if (temp == "CYLINDRICAL")
		coordinateSystem = CYLINDER;
	else if (temp == "POLAR")
		coordinateSystem = POLAR;
	else if (temp == "CARTESIAN")
		coordinateSystem = CARTESIAN;

	if (sl.size() < 3)
		return false;
	name = sl.at(2).toStdString();

	//获取图表别名
	if (headList.size() < 14)
		return true;
	str = QString::fromStdString(headList.at(13));
	sl = str.split(":");
	if (sl.size() < 2)
		return true;
	petName = sl.at(1).toLower().simplified().toStdString();

	return true;
}

bool Hdf5Data::initM3dStructInformation()
{
	if (headList.size() < 4)
		return false;
	QString str = QString::fromStdString(headList.at(3));
	str = str.simplified();
	QStringList sl = str.split("=");
	if (sl.size() < 2)
		return false;
	if (sl.at(0) != "system")
		return false;
	str = sl.at(1);
	sl = str.split("$");
	if (sl.size() < 3)
		return false;
	str = sl.at(1);
	str = str.simplified();
	if (str == "cylindrical")
		coordinateSystem = CYLINDER;
	else if (str == "polar")
		coordinateSystem = POLAR;
	else if (str == "cartesian")
		coordinateSystem = CARTESIAN;

	if (sl.at(2) != "STRUCTRUE")
		return false;

	name = "struct";
	return true;
}

bool Hdf5Data::initM2dStructInformation()
{
	if (headList.size() < 4)
		return false;
	QString str = QString::fromStdString(headList.at(2));
	str = str.simplified();
	QStringList sl = str.split("=");
	if (sl.size() < 2)
		return false;
	if (sl.at(0) != "system")
		return false;
	str = sl.at(1);
	sl = str.split("$");
	if (sl.size() < 3)
		return false;
	str = sl.at(1);
	str = str.simplified();
	if (str == "cylindrical")
		coordinateSystem = CYLINDER;
	else if (str == "polar")
		coordinateSystem = POLAR;
	else if (str == "cartesian")
		coordinateSystem = CARTESIAN;

	if (sl.at(2) != "STRUCTRUE")
		return false;

	name = "struct";
	return true;
}

/**
* @brief Hdf5Data::init 初始化数据信息
* @return void
*/
void Hdf5Data::init()
{
	if (initInformation())
		return;
	if (initM3dStructInformation())
		return;
	if (initM2dStructInformation())
		return;
}
/**
* @brief Hdf5IO::creatNewH5File
* @param const std::string & fileName
* @return int
* @Time 2021/6/30
*/
int Hdf5IO::creatNewH5File(const std::string& fileName){
	auto gbk = QTextCodec::codecForName("gb2312");

	QString temp = QString::fromUtf8(fileName.c_str());
	std::string newPath = gbk->fromUnicode(temp).data();
	return H5Fcreate(newPath.c_str(), H5F_ACC_TRUNC, H5P_DEFAULT, H5P_DEFAULT);
}
/**
* @brief Hdf5IO::openH5File
* @param const std::string & fileName
* @return int
* @Time 2021/6/30
*/
int Hdf5IO::openH5File(const std::string &fileName)
{
	/*return H5Fopen(const char *filename, unsigned flags,
		hid_t access_plist);*/
	return 0;
}
/**
* @brief Hdf5IO::closeH5File
* @param int H5id
* @return int
* @Time 2021/6/30
*/
int Hdf5IO::closeH5File(int H5id)
{
	return H5Fclose(H5id);

}

/**
* @brief Hdf5IO::LoadH5Resource 加载H5资源
* @return void
* @Time 2021/6/30
*/
void Hdf5IO::LoadH5Resource()
{
	if (nullptr == this->Hdf5File)
		return;
	std::list<Group> groups = getGrouplist();//获取根节点下的所有组
	//处理所有的Group
	for (auto iter = groups.begin(); iter != groups.end();iter++)
		digGroup(*iter);
}

/**
* @brief Hdf5IO::digGroup
* @param Group group
* @return void
* @Time 2021/6/30
*/
void Hdf5IO::digGroup(Group group)
{
#if 0
	这里增加判断下层的是数据还是组
	std::list<Group> subgroups = getGrouplist(group);
	std::vector<DataSet> datas = getDataSetlist(group);
	if (!datas.empty())
	{
		Hdf5Data data(this->Hdf5File);
		data.listDataSet = datas;
		data.group = group;
		std::vector<std::string> headList = getHeadValue(group);
		data.headList = headList;
		data.init();
		hdf5DataList.push_back(data);
	}
	if (subgroups.empty())
		return;
	//采用递归式处理
	for (auto iter = subgroups.begin(); iter != subgroups.end(); iter++)
		digGroup(*iter);
#else
	/*****************************************/
	//首先判断下层有没有数据或者组
	int childCount = group.getNumObjs();
	if (0 >= childCount)
		return;
	//下层有数据，则判断是组还是数据
	//先判断若是数据的话
	DataSet temp;
	bool res = getDataSet(group,group.getObjnameByIdx(0),temp);
	//如果确实为数据
	if (res)
	{
		std::vector<DataSet> datasets;
		for (int index = 0; index < childCount; index++)
		{
			DataSet data;
			getDataSet(group,group.getObjnameByIdx(index),data);
			datasets.push_back(data);
		}
		//初始化
		Hdf5Data data(this->Hdf5File);
		data.listDataSet = datasets;
		data.group = group;
		data.headList = getHeadValue(group);
		data.init();
		hdf5DataList.push_back(data);
		return;
	}
	//不是数据，是组
	else
	{
		for (int index = 0; index < childCount; index++)
		{
			Group g;
			getGroup(group,group.getObjnameByIdx(index),g);
			digGroup(g);
		}
	}
#endif
}
/**
* @brief Hdf5IO::getGroups
* @return std::list<H5::Group>
* @Time 2021/6/30
*/
std::list<Group> Hdf5IO::getGrouplist()
{
	std::list<Group> groups;
	int count = this->Hdf5File->getNumObjs();
	for (auto index = 0; index < count;index++)
	{
		Group subgroup;
		std::string groupName = Hdf5File->getObjnameByIdx(index);
		getGroup(groupName,subgroup);
		int childcount = subgroup.getNumObjs();
		if (childcount>0)//有子节点，不是dataset
		{
			groups.push_back(subgroup);
		}
	}
	return groups;
}
/**
* @brief Hdf5IO::getGrouplist
* @param Group group
* @return std::list<H5::Group>
* @Time 2021/6/30
*/
std::list<Group> Hdf5IO::getGrouplist(Group group)
{
	std::list<Group> groups;
	int count = group.getNumObjs();
	for (auto index = 0; index < count;index++)
	{
		Group subgroup;
		std::string subGroupName = group.getObjnameByIdx(index);
		auto res=getGroup(group,subGroupName,subgroup);
		if (!res)
			continue;
		int childcount = subgroup.getNumObjs();
		if (childcount>0)
			groups.push_back(subgroup);
	}
	return groups;
}

/**
* @brief Hdf5IO::getDataSetlist 获取数据队列
* @param Group group
* @return std::vector<H5::DataSet>
* @Time 2021/6/30
*/
std::vector<DataSet> Hdf5IO::getDataSetlist(Group group)
{
	std::vector<DataSet> datasetlist;
	int count = group.getNumObjs();
	for (auto index = 0; index < count;index++)
	{
		DataSet data;
		std::string datasetName = group.getObjnameByIdx(index);
		auto res = getDataSet(group, datasetName, data);
		if (!res)
			continue;
		datasetlist.push_back(data);
	}
	return datasetlist;
}