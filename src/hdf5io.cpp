#include "hdf5io.h"
#include <memory>
Hdf5IO::Hdf5IO(std::string fileName)
{
    Hdf5File = new H5File(fileName,H5F_ACC_RDWR);
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
	}
	catch (...)
	{
		std::cerr << "获取数据组失败，数据组名:" + groupName;
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
	}
	catch (...)
	{
		std::cerr << "获取数据组失败，数据组名:" + groupName;
		ok = false;
	}
    return g;
}
/*
 * 获取一个数据组下有多少个子组
 */
int Hdf5IO::getSubGroupCount(const Group &group)
{
    return group.getNumObjs();
}
/*
 * 获取一个组的头部信息
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
/*
 * 获取数据库中的数据
 *
 */
std::vector<float> Hdf5IO::getVlue(const Group &group,const std::string &dataName)
{
    DataSet dataset = group.openDataSet(dataName);
    return getVlue(dataset);
}

/*
 * 获取数据库中的数据
 */
std::vector<float> Hdf5IO::getVlue(const DataSet &dataSet)
{
    hsize_t size[2];
    DataSpace dataSpace;

    try
    {
        dataSpace = dataSet.getSpace();
    }catch(...)
    {
        std::cerr << "获取数据组失败，数据组名:";
        std::vector<float> fbc;

        return fbc;
    }

    dataSpace.getSimpleExtentDims(size,0);
    std::shared_ptr<float> value(new float[size[0]*size[1]]);

    dataSet.read(value.get(),PredType::NATIVE_FLOAT);

    std::vector<float> listVlue;
    for(int i = 0;i < size[0] * size[1];i++)
    {
        listVlue.push_back(value.get()[i]);

    }
    return listVlue;
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
/*获取结构数据*/
void Hdf5IO::getStructData()
{
	bool ok;
	Group group = getGroup("Group_kmat",ok);
	if (!ok)
		return;
	{
		DataSet dataSet1 = OpenGroupDataset(group, "I1MX",ok);
		if (!ok)
			return;
		DataSet dataSet2 = OpenGroupDataset(group, "I2MX",ok);
		if (!ok)
			return;
		DataSet dataSet3 = OpenGroupDataset(group, "I3MX",ok);
		if (!ok)
			return;
		DataSet dataSet4 = OpenGroupDataset(group, "datasetKmt",ok);
		if (!ok)
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
			hdf5DataList.push_back(data);
		}
	}
}

/*获取par中的数据*/
void Hdf5IO::getParData()
{
	bool ok;

	Group group = getGroup("Group_part",ok);
	if (!ok)
		return;
	int count = getSubGroupCount(group);
	for (int i = 1; i < count + 1; i++)
	{
		Group subGroup = OpenGroup(group,"subGroup" + std::to_string(i),ok);
		if (!ok)
			continue;
		DataSet dataSet = OpenGroupDataset(subGroup, "datasetPar",ok);
		if (!ok)
			continue;
		std::vector<std::string> headList = getHeadValue(subGroup);

		//如果头数据为空，则说明该图为空
		if (headList.empty())
		{
			continue;
		}

		Hdf5Data data;
		data.dataSet = dataSet;
		data.group = subGroup;
		data.headList = headList;
		hdf5DataList.push_back(data);
	}
}
/*获取fild中的数据*/
void Hdf5IO::getFildData()
{
	bool ok;

	Group group = getGroup("Group_fild",ok);
	if (!ok)
		return;
	group = OpenGroup(group, "2D_contour",ok);
	if (!ok)
		return;
	int count = getSubGroupCount(group);
	for (int i = 1; i < count + 1; i++)
	{
		Group subGroup = OpenGroup(group,"subGroup" + std::to_string(i),ok);
		if (!ok)
			continue;
		DataSet dataSetA = OpenGroupDataset(subGroup, "datasetEmA",ok);
		if (!ok)
			continue;
		DataSet dataSetB = OpenGroupDataset(subGroup, "datasetEmB",ok);
		if (!ok)
			continue;
		DataSet dataSetC = OpenGroupDataset(subGroup, "datasetEmC",ok);
		if (!ok)
			continue;

		std::vector<std::string> headList = getHeadValue(subGroup);

		//如果头数据为空，则说明该图为空
		if (headList.empty())
		{
			continue;
		}

		Hdf5Data data;
		data.listDataSet.push_back(dataSetA);
		data.listDataSet.push_back(dataSetB);
		data.listDataSet.push_back(dataSetC);
		data.group = subGroup;
		data.headList = headList;
		hdf5DataList.push_back(data);
	}
}

/*获取grd中的所有数据*/
void Hdf5IO::getGrdData()
{
	bool ok;

	Group grdGroup = getGroup("Group_grid", ok);
	if (!ok)
		return;

	Group ObserveGroup = OpenGroup(grdGroup, "2D_observe", ok);
	if (ok)
	{
		int count = getSubGroupCount(ObserveGroup);
		for (int i = 1; i < count + 1; i++)
		{
			Group subGroup = OpenGroup(ObserveGroup,"subGroup" + std::to_string(i), ok);
			if (!ok)
				continue;
			DataSet dataSet = OpenGroupDataset(subGroup, "datasetGrd", ok);
			if (!ok)
				continue;
			std::vector<std::string> headList = getHeadValue(subGroup);

			//如果头数据为空，则说明该图为空
			if (headList.empty())
			{
				continue;
			}

			Hdf5Data data;
			data.dataSet = dataSet;
			data.group = subGroup;
			data.headList = headList;
			hdf5DataList.push_back(data);
		}
	}

	Group rangGroup = OpenGroup(grdGroup, "2D_observe", ok);

	if (ok)
	{
		int count = getSubGroupCount(rangGroup);
		for (int i = 1; i < count + 1; i++)
		{
			Group subGroup = OpenGroup(rangGroup, QString("subGroup%1").arg(i).toStdString(), ok);
			if (!ok)
				continue;
			DataSet dataSet = OpenGroupDataset(subGroup, "datasetGrd", ok);
			if (!ok)
				continue;
			std::vector<std::string> headList = getHeadValue(subGroup);

			//如果头数据为空，则说明该图为空
			if (headList.empty())
			{
				continue;
			}

			Hdf5Data data;
			data.dataSet = dataSet;
			data.group = subGroup;
			data.headList = headList;
			hdf5DataList.push_back(data);
		}
	}

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
	//	this->getGrdData();
    }
    //获取par的数据组
    {
		getParData();
    }
    //获取二维等位图数据
    {
		getFildData();
    }
}

