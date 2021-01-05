#include "PreCompiled.h"
#ifndef _PreComp_
#endif

#include "hdf5io.h"

#include <iostream>
#include<io.h>
#include <memory>
#include <qmessagebox.h>
#include <qdebug.h>
using namespace std;

Hdf5IO::Hdf5IO(string fileName)
{
	Hdf5File = new H5File(fileName, H5F_ACC_RDWR);
}

/*
获取一个数据组
*/
Group Hdf5IO::getGroup(const Group &group, const string &groupName)
{
	return group.openGroup(groupName);
}

/*
获取一个数据组
*/
Group Hdf5IO::getGroup(const string &groupName)
{
	return OpenH5File(*Hdf5File, groupName);
}

/*
获取一个数据组下有多少个子组
*/
int Hdf5IO::getSubGroupCount(const Group &group)
{
	try
	{
		return group.getNumObjs();
	}
	catch (...)
	{
		return 0;
	}
}

/*
获取一个组的头部信息
*/
QList<QString> Hdf5IO::getHeadValue(const Group &group)
{
	QList<QString> headValue;
	try
	{
		int headCount = group.getNumAttrs(); //获取头部信息的数量
		for (int i = 0; i < headCount; i++){
			Attribute attribute = group.openAttribute(i);
			string value;
			attribute.read(attribute.getStrType(), value);
			headValue.append(QString::fromStdString(value));
		}
	}
	catch (...)
	{
		std::cerr << "Failed to retrieve group";
	}
	
	
	/*if (headValue.isEmpty()){
		headValue.append("");
	}*/
	return headValue;
}
/*
获取数据组中的数据
*/
QList<float> Hdf5IO::getValue(const Group &group, const std::string &dataName)
{
	DataSet dataset;
	try
	{
		dataset = group.openDataSet(dataName);
		
	}
	catch (...)
	{
		std::cerr << "Failed to retrieve dataSet, dataSetName: " + dataName;
	}
	return getValue(dataset);

}

/*
获取数据组中的数据
*/
QList<float> Hdf5IO::getValue(const DataSet &dataSet)
{
	QList<float> listValue;
	try
	{
		hsize_t size[2];
		DataSpace dataSpace = dataSet.getSpace();
		dataSpace.getSimpleExtentDims(size, 0);
		std::shared_ptr<float> value(new float[size[0] * size[1]]);

		dataSet.read(value.get(), PredType::NATIVE_FLOAT);

		for (int i = 0; i < size[0] * size[1]; i++)
		{
			listValue.append(value.get()[i]);

		}
		
	}
	catch (...)
	{
		std::cerr << "Failed to retrieve dataSet";
		
	}
	return listValue;

}

/*
获取数据组中的数据的维度
*/
QList<int> Hdf5IO::getValueSize(const DataSet &dataSet)
{
	QList<int> listSize;
	try
	{
		hsize_t size[2];
		DataSpace dataSpace = dataSet.getSpace();
		dataSpace.getSimpleExtentDims(size, 0);


		listSize.append(size[0]);
		listSize.append(size[1]);

	}
	catch (...)
	{
		std::cerr << "Failed to retrieve dataSet";
	}
	/*if (listSize.isEmpty()){
		listSize.append(0);
	}*/
	return listSize;

}

/*
打开一个h5文件，从中获得一个数据组
*/
Group Hdf5IO::OpenH5File(H5File &file, const std::string &groupName)
{
	Group g;
	try
	{
		g = file.openGroup(groupName);
	}
	catch (...)
	{
		//qDebug() << "Failed to retrieve group, groupName: " + QString::fromStdString(groupName);
		std::cerr << "Failed to retrieve group, groupName: " + groupName;
	}
	return g;
}
/*
打开一个数据组，从里面获取一个组
*/
Group Hdf5IO::OpenGroup(Group &group, const std::string &groupName)
{
	Group g;
	try
	{
		g = group.openGroup(groupName);
	}
	catch (...)
	{
		//qDebug() << "Failed to retrieve group, groupName: " + QString::fromStdString(groupName);
		std::cerr << "Failed to retrieve group, groupName: " + groupName;

	}
	return g;

}

/*
打开一个数据组，获取其中的一个数据库
*/
DataSet Hdf5IO::OpenGroupDataset(Group &group, const std::string &datasetName)
{
	DataSet d;
	try
	{
		d = group.openDataSet(datasetName);
	}
	catch (...)
	{
		//qDebug() << "Failed to retrieve data, data groupName: " + QString::fromStdString(datasetName);
		std::cerr << "Failed to retrieve data, data groupName: " + datasetName;
	}
	return d;
}

void Hdf5IO::close()
{
	Hdf5File->close();
}

/*
获取子组下对应的数据信息
*/
FigData Hdf5IO::getFigData(const string &groupName, const string &subgroupName, const string &subsubgroupName)
{
	FigData figData;
	try
	{
		Group group = getGroup(groupName);
		if (groupName != "Group_kmat")
		{
			if (groupName == "Group_part")
			{
				group = OpenGroup(group, subsubgroupName);
			}
			else	
			{
				group = OpenGroup(group, subgroupName);
				group = OpenGroup(group, subsubgroupName);
			}
		}
	
		QList<QString> headList = getHeadValue(group);
		QList<QList<float>> dataSetList;
		QList<QList<int>> dataSizeList;
	
		char memb_name[1024];
		for (int i = 0; i < group.getNumObjs(); i++)
		{

		
			group.getObjnameByIdx(i, memb_name, (size_t)1024);
			DataSet dataSet = OpenGroupDataset(group, memb_name);
			QList<float> valueList = getValue(dataSet);
			dataSetList.append(valueList);
			QList<int> size = getValueSize(dataSet);
			dataSizeList.append(size);

		}
		//给某一块内存空间进行清空
		memset(memb_name, 0, (size_t)1024);

		
		figData.headList = headList;
		figData.dataSetList = dataSetList;
		figData.dataSizeList = dataSizeList;
	}
	catch (...)
	{
		//qDebug() << "Failed to retrieve data, data groupName: " + QString::fromStdString(datasetName);
		std::cerr << "Failed to retrieve data in" + groupName + "/" + subgroupName + "/" + subsubgroupName;
	}
	return figData;
}


/*
获取子组下对应的所有数据信息
*/
FigData Hdf5IO::getSingleFigData(const string &groupName, const string &subgroupName)
{
	FigData figData;
	try
	{
		char memb_name[1024];
		Group group = getGroup(groupName);

		if (groupName != "Group_kmat")
		{
			if (groupName != "Group_part")

			{
				group = OpenGroup(group, subgroupName);
			}
		}
		int count = getSubGroupCount(group);
		for (int i = 0; i < count; i++)
		{

			group.getObjnameByIdx(i, memb_name, (size_t)1024);
			Group subGroup = OpenGroup(group, memb_name);

			QList<QString> headList = getHeadValue(subGroup);
			headList.append(QString::fromStdString(memb_name));
			QList<QList<float>> dataSetList;
			QList<QList<int>> dataSizeList;

			for (int i = 0; i < subGroup.getNumObjs(); i++)
			{

				subGroup.getObjnameByIdx(i, memb_name, (size_t)1024);
				DataSet dataSet = OpenGroupDataset(subGroup, memb_name);
				QList<float> valueList = getValue(dataSet);
				dataSetList.append(valueList);
				QList<int> size = getValueSize(dataSet);
				dataSizeList.append(size);

			}
			FigData figData;

			figData.headList = headList;
			figData.dataSetList = dataSetList;
			figData.dataSizeList = dataSizeList;

			//给某一块内存空间进行清空
			memset(memb_name, 0, (size_t)1024);

			return figData;
		}
	}
	catch (...)
	{
		//qDebug() << "Failed to retrieve data, data groupName: " + QString::fromStdString(datasetName);
		std::cerr << "Failed to retrieve data in" + groupName + "/" + subgroupName;
	}
	return figData;
		
	
}



/*
* 获取所有跟图名相关的信息
*/
QList<FigNameInfo> Hdf5IO::getFigNameInfo()
{
	QList<FigNameInfo> figNameInfoList;
	
	try
	{
	char memb_name[1024];

	//获取二维等位图数据
	{
		Group group = getGroup("Group_fild");
		group = OpenGroup(group, "2D_contour");
		int count = getSubGroupCount(group);
		for (int i = 0; i < count; i++)
		{

			group.getObjnameByIdx(i, memb_name, (size_t)1024);
			Group subGroup = OpenGroup(group, memb_name);

			QList<QString> headList = getHeadValue(subGroup);
			FigNameInfo data;
			data.type = "2D_contour";
			data.groupName = memb_name;
			data.headList = headList;
			figNameInfoList.append(data);
		}

	}

	//获取三维等位图数据
	{

		Group group = getGroup("Group_fild");
		group = OpenGroup(group, "3D_fieldem");
		int count = getSubGroupCount(group);

		for (int i = 0; i < count; i++)
		{

			group.getObjnameByIdx(i, memb_name, (size_t)1024);
			Group subGroup = OpenGroup(group, memb_name);

			QList<QString> headList = getHeadValue(subGroup);
			FigNameInfo data;


			data.type = "3D_fieldem";
			data.groupName = memb_name;
			// 在headlist最后加上改子组下的dataset名
			subGroup.getObjnameByIdx(0, memb_name, (size_t)1024);
			headList.append(QString::fromStdString(memb_name));
			data.headList = headList;
			figNameInfoList.append(data);
		}
	}

	//获取2D_observe
	{
		Group group = getGroup("Group_grid");
		group = OpenGroup(group, "2D_observe");
		int count = getSubGroupCount(group);

		
		for (int i = 0; i < count; i++)
		{

			group.getObjnameByIdx(i, memb_name, (size_t)1024);
			Group subGroup = OpenGroup(group, memb_name);
			QList<QString> headList = getHeadValue(subGroup);
			FigNameInfo data;
			data.type = "2D_observe";
			data.groupName = memb_name;
			data.headList = headList;
			figNameInfoList.append(data);
		}
	}

	//获取par的数据组
	{
		Group group = getGroup("Group_part");
		int count = getSubGroupCount(group);
		
		for (int i = 0; i < count; i++)
		{

			group.getObjnameByIdx(i, memb_name, (size_t)1024);
			Group subGroup = OpenGroup(group, memb_name);
			QList<QString> headList = getHeadValue(subGroup);
			FigNameInfo data;
			data.type = "2D_phaseSpace";
			data.groupName = memb_name;
			data.headList = headList;
			figNameInfoList.append(data);
		}
	}

	//获取2D_rangers
	{
		Group group = getGroup("Group_grid");
		group = OpenGroup(group, "2D_rangers");
		int count = getSubGroupCount(group);

		
		for (int i = 0; i < count; i++)
		{

			group.getObjnameByIdx(i, memb_name, (size_t)1024);
			Group subGroup = OpenGroup(group, memb_name);
			QList<QString> headList = getHeadValue(subGroup);
			FigNameInfo data;
			data.type = "2D_rangers";
			data.groupName = memb_name;
			data.headList = headList;
			figNameInfoList.append(data);
		}
	}


	//获取2D_vectors
	{
		Group group = getGroup("Group_fild");
		group = OpenGroup(group, "2D_vectors");
		int count = getSubGroupCount(group);
		for (int i = 0; i < count; i++)
		{

			group.getObjnameByIdx(i, memb_name, (size_t)1024);
			Group subGroup = OpenGroup(group, memb_name);

			QList<QString> headList = getHeadValue(subGroup);
			FigNameInfo data;
			data.type = "2D_vectors";
			data.groupName = memb_name;
			data.headList = headList;
			figNameInfoList.append(data);
		}
	}

	// 获取结构数据
	{
		Group group = getGroup("Group_kmat");
		{

			QList<QString> headList = getHeadValue(group);
			FigNameInfo data;
			data.type = "2D_struct";
			data.groupName = "2D_struct";
			data.headList = headList;
			figNameInfoList.append(data);
		}
	}
	//给某一块内存空间进行赋值
	memset(memb_name, 0, (size_t)1024);
	
	return figNameInfoList;
	}
	catch (...)
	{
		//qDebug() << "Failed to retrieve data, data groupName: " + QString::fromStdString(datasetName);
		std::cerr << "Failed to retrieve data";
	}
}
