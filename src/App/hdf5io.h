#ifndef _HDF5IO_H_
#define _HDF5IO_H_

#include "H5Cpp.h"
 #include <QList>
using namespace H5;
using namespace std;
class Hdf5IO;

struct FigData{

	QList<QString> headList;
	QList<QList<float>> dataSetList;
	QList<QList<int>> dataSizeList;
};

struct FigNameInfo{

	string type;
	string groupName;
	QList<QString> headList;
};



class Hdf5IO{
public:
	Hdf5IO(string filename);
	FigData getFigData(const string &groupName, const string &subgroupName,const string &subsubgroupName);
	FigData getSingleFigData(const string &groupName, const string &subgroupName);
	QList<FigNameInfo> getFigNameInfo();
	void close();

private:
	H5File *Hdf5File;
	Group getGroup(const Group &group, const string &groupName);
	Group getGroup(const string &groupName);
	int getSubGroupCount(const Group &group);
	QList<float> getValue(const Group &group, const string &dataName);
	QList<float> getValue(const DataSet &dataSet);
	QList<int> getValueSize(const DataSet &dataSet);
	QList<QString> getHeadValue(const Group &group);
	Group OpenH5File(H5File &file, const string &groupName);
	Group OpenGroup(Group &group, const string &groupName);
	DataSet OpenGroupDataset(Group &group, const string &datasetName);
};
#endif