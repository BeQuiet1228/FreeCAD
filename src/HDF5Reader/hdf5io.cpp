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
	Hdf5File = nullptr;
}

Hdf5IO::~Hdf5IO()
{
	if (Hdf5File != nullptr)
		delete Hdf5File;
}
#include <QDebug>
/**
* @brief Hdf5IO::setFilePath 设置h5文件路径 路径中如果有中文 必须是utf8格式的 
* @param const std::string & path
* @return void
*/
void Hdf5IO::setFilePath(const std::string& path)
{
	auto gbk = QTextCodec::codecForName("gb2312");
	if (nullptr==gbk)
	{
		//没有gb2312的字符集
	//	return;
	}
	QString temp = QString::fromUtf8(path.c_str());
	qDebug() << temp;
	std::string newPath = gbk->fromUnicode(temp).data();
	//std::string newPath = "F:/wdtproject/PICGUI/TEMP(1).H5";
	deleteH5File();
	Hdf5File = new H5File(newPath, H5F_ACC_RDWR);
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
		std::cerr << "Hdf5IO::getGroup failde! group name:" + groupName << std::endl;
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
		std::cerr << "Hdf5IO::getGroup failde! group name:" + groupName << std::endl;
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
		std::cerr << "Hdf5IO::getGroup failde! group name:" + groupName << std::endl;
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
		std::cerr << "Hdf5IO::getGroup failde! group name:" + groupName << std::endl;
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
		std::cerr << "Hdf5IO::getGroup get group for h5file failde! group name:" + groupName;
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
		std::cerr << "Hdf5IO::getDataSet get data set failde! data set name:" + dataSetName;
		return false;
	}

	return true;
}

/*
 * 获取一个数据组下有多少个子组
 */
int Hdf5IO::getSubGroupCount(const Group &group)
{
    return group.getNumObjs();
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
        headValue.push_back(value);
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
       std::cerr << "获取数据组失败，数据组名:" + groupName;
	   ok = false;
    }

    return g;
}
/*
 * 打开一个数据组，从里面获取一个组
 */
Group Hdf5IO::OpenGroup(Group &group, const std::string &groupName,bool &ok)
{
    std::cerr << "获取数据组：" + groupName;
    Group g;
    try
    {
       g = group.openGroup(groupName);
	   ok = true;
    }catch(...)
    {
       std::cerr << "获取数据组失败，数据组名:" + groupName;
	   ok = false;
    }

    return g;
}
/*
 * 打开一个数据组，获取其中的一个数据库
 */
DataSet Hdf5IO::OpenGroupDataset(Group &group, const std::string &datasetName, bool &ok)
{
    std::cerr << "获取数据库：" + datasetName;
    DataSet d;
    try
    {
       d = group.openDataSet(datasetName);
	   ok = true;
    }catch(...)
    {
       std::cerr << "获取数据库组失败，数据库名:" + datasetName;
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

		Hdf5Data data;
		data.listDataSet = datas;
		data.group = subGroup;
		data.headList = headList;
		data.initInformation();
		data.name = getNameFromHeadList(headList);
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
		&& getDataSet(group, "I2MX", dataSet2)
		&& getDataSet(group, "I3MX", dataSet3)
		&& getDataSet(group, "datasetKmt", dataSet4)))
		return;	

	std::vector<std::string> headList = getHeadValue(group);

	//如果头数据为空，则说明该图为空
	if (!headList.empty())
	{
		Hdf5Data data;
		data.listDataSet.push_back(dataSet1);
		data.listDataSet.push_back(dataSet2);
		data.listDataSet.push_back(dataSet3);
		data.listDataSet.push_back(dataSet4);
		data.group = group;
		data.headList = headList;
		data.initInformation();
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

		Hdf5Data data;
		data.listDataSet.push_back(dataSet);
		data.group = subGroup;
		data.headList = headList;
		data.initInformation();
		data.name = getNameFromHeadList(headList);
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

/**
* @brief Hdf5IO::deleteH5File 释放调h5文件 并关闭所有的组与数据库
* @return void
*/
void Hdf5IO::deleteH5File()
{
	if (Hdf5File != nullptr)
	{
		hdf5DataList.clear();
		Hdf5File->close();
		delete Hdf5File;
		Hdf5File = nullptr;	
	}
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

	//Group rangeGroup;
	//if (!getGroup(grdGroup, "2D_rangers", rangeGroup))
	//	return;
	//getAllSubGroupAndDataSet(rangeGroup, datasetNames);
}
/*
 * 初始化所有的图的数据组、数据库、头部信息
 */
void Hdf5IO::initHdf5Data()
{

    // 获取结构数据
     {
		 getStructData();
     }
    //获取所有grd的数据组
    {
		//getGrdData();
    }
    //获取par的数据组
    {
		getParData();
    }
    //获取二维等位图数据
    {
		//getFildData();
    }
}

/**
* @brief Hdf5Data::initInformation 根据头信息初始化基本信息
* @return void
*/
void Hdf5Data::initInformation()
{
	if (headList.size() == 0)
		return;
	QString str = QString::fromStdString(headList.at(0));
	QStringList sl = str.split("$");

	if (sl.size() < 2)
		return;
	QString temp = sl.at(1);
	if (temp == "CYLINDRICAL")
		coordinateSystem = CYLINDER;
	else if (temp == "POLAR")
		coordinateSystem = POLAR;
	else if (temp == "CARTESIAN")
		coordinateSystem = CARTESIAN;

	if (sl.size() < 3)
		return;
	name = sl.at(2).toStdString();
}
