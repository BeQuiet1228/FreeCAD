#include "ControlTreeWidget.h"
#include <QString>
#include <HDF5Reader/hdf5io.h>
#include <iostream>
#include "Contorl/ContorlInterface.h"
#include <QFileInfo>
ControlTreeWidget::ControlTreeWidget(QWidget* parent)
	:QTreeWidget(parent)
{
	initItem();
	connect(this, SIGNAL(itemDoubleClicked(QTreeWidgetItem*, int)), this, SLOT(itemDouble_clicke(QTreeWidgetItem*, int)));
	
	auto control = ContorlInterface::GetInstance();
	auto chipicManager = control->getChipicManager();
	connect(chipicManager, SIGNAL(outputStructFileSignal(unsigned long)), this, SLOT(outputStructFile(unsigned long)));
	connect(chipicManager, SIGNAL(newResultFIleSignal(unsigned long)), this, SLOT(outputTempFile(unsigned long)));
}

ControlTreeWidget::~ControlTreeWidget()
{

}

void ControlTreeWidget::init(const Hdf5Data& data)
{
	auto listHead = data.headList;

	for each (std::string str in listHead)
	{
		if (addContourItem(str))
			continue;
		if (addPhaseSpaceItem(str))
			continue;
		if (addObserveItem(str))
			continue;
		if (addRangeItem(str))
			continue;
		if (addVectorItem(str))
			continue;
		if (addRangeItem(str))
			continue;
	}

	update();
}

void ControlTreeWidget::initItem()
{
	for (int i = 0; i < itemCount; i++)
	{
		items.push_back(new QTreeWidgetItem);
	}
	
	contourItem = items.at(0);
	contourItem->setText(0,"contour");

	phaseSpaceItem = items.at(1);
	phaseSpaceItem->setText(0,"phaseSpace");

	observeItem = items.at(2);
	observeItem->setText(0,"observe");

	rangeItem = items.at(3);
	rangeItem->setText(0,"range");

	vectorItem = items.at(4);
	vectorItem->setText(0,"vector");

	for each (QTreeWidgetItem* item in items)
	{
		addTopLevelItem(item);
	}

}

void ControlTreeWidget::sendControlMsg(QTreeWidgetItem* item)
{
	auto control = ContorlInterface::GetInstance();
	MsgType type;
	int index;
	
	if (!getTypeAndIndex(item, type, index))
		return;
	control->senWinMessage(109, type, index);

}

/**
* @brief ControlTreeWidget::getTypeAndIndex 根据item对象，获取类型和索引
* @param QTreeWidgetItem * item 
* @param MsgType & type 类型
* @param int & index 索引
* @return bool
*/
bool ControlTreeWidget::getTypeAndIndex(QTreeWidgetItem* item, MsgType& type, int& index)
{
	type = NONE;
	if (contourItem->indexOfChild(item) >=0)
	{
		index = contourItem->indexOfChild(item);
		type = CONTOUR;
	}else if (observeItem->indexOfChild(item) >= 0)
	{
		index = observeItem->indexOfChild(item);
		type = OBSERVE;
	}else if (vectorItem->indexOfChild(item) >= 0) {
		index = observeItem->indexOfChild(item);
		type = VECTOR;
	}else if (phaseSpaceItem->indexOfChild(item) >= 0) {
		index = observeItem->indexOfChild(item);
		type = PHASE_SPACE;
	}else if (rangeItem->indexOfChild(item) >= 0) {
		index = observeItem->indexOfChild(item);
		type = RANGE;
	}
	if (type == NONE)
		return false;
	return true;
}

bool ControlTreeWidget::addContourItem(const std::string& str)
{
	QString typeName, name, rank;
	typeName = "Contour";
	if (!analysisType(str, typeName, name, rank))
		return false;

	QTreeWidgetItem* childItem = new QTreeWidgetItem;
	childItem->setText(0,name);
	contourItem->addChild(childItem);

}

bool ControlTreeWidget::addPhaseSpaceItem(const std::string& str)
{
	QString typeName, name, rank;
	typeName = "PhaseSpace";
	if (!analysisType(str, typeName, name, rank))
		return false;

	QTreeWidgetItem* childItem = new QTreeWidgetItem;
	childItem->setText(0, name);
	phaseSpaceItem->addChild(childItem);

}

bool ControlTreeWidget::addObserveItem(const std::string& str)
{
	QString typeName, name, rank;
	typeName = "Observe";
	if (!analysisType(str, typeName, name, rank))
		return false;

	QTreeWidgetItem* childItem = new QTreeWidgetItem;
	childItem->setText(0, name);
	observeItem->addChild(childItem);
}

bool ControlTreeWidget::addRangeItem(const std::string& str)
{
	QString typeName, name, rank;
	typeName = "Range";
	if (!analysisType(str, typeName, name, rank))
		return false;

	QTreeWidgetItem* childItem = new QTreeWidgetItem;
	childItem->setText(0, name);
	rangeItem->addChild(childItem);
}

bool ControlTreeWidget::addVectorItem(const std::string& str)
{
	QString typeName, name, rank;
	typeName = "Vector";
	if (!analysisType(str, typeName, name, rank))
		return false;

	QTreeWidgetItem* childItem = new QTreeWidgetItem;
	childItem->setText(0, name);
	vectorItem->addChild(childItem);
}

/**
* @brief ControlTreeWidget::analysisType 解析观测文本
* @param const std::string & str 观测文本
* @param const QString & typeName 观测类型
* @param QString & name 观测名称
* @param QString & rank 观测排序
* @return bool 是否解析成功
*/
bool ControlTreeWidget::analysisType(const std::string& str, const QString& typeName, QString& name, QString& rank)
{
	QString qstr = QString::fromStdString(str);
	auto lists = qstr.split("=");

	if (lists.size() != 2)
		return false;

	qstr = lists.at(0);
	//获取名称和观测排序
	QString temp = qstr.left(typeName.length());
	if (temp != typeName)
		return false;
	rank = qstr.remove(temp);
	name = lists.at(1);
	return true;
}

/**
* @brief ControlTreeWidget::makeFilePath 生成chipic输出的临时文件路径，并生成对应的临时数据集合的文件路径 放再tempFilePtah里
* @param unsigned long threadID
* @return QString
*/
QString ControlTreeWidget::makeFilePath(unsigned long threadID)
{
	auto control = ContorlInterface::GetInstance();
	QString m3dPath = control->getM3dPathForThreadID(threadID);

	//去掉文件名的后缀
	QString temp = m3dPath;
	QFileInfo fileInfo(temp);
	QString name = fileInfo.fileName();
	name = name.left(name.size() - 4);

	QString m3dFileName = name.toLocal8Bit();
	QString path = fileInfo.absolutePath();

	//获取线程数，因为并行时输出文件的路径不一样
	int threadCount = control->getChipicThreadCount(threadID);
	if (threadCount < 1)
		return "";
	QString tempFilePath;
	if (threadCount > 1)
		tempFilePath = path + "/1/" + m3dFileName + "_Temp.h5";
	else
		tempFilePath = path + "/" + m3dFileName + "_Temp.h5";

	//生成新的临时文件路径
	QString newTempPath = path + "/" + m3dFileName + "_gather.h5";

	this->tempFilePath = newTempPath;

	return tempFilePath;
}

void ControlTreeWidget::itemDouble_clicke(QTreeWidgetItem* item, int column)
{
	sendControlMsg(item);
}


void ControlTreeWidget::outputStructFile(unsigned long threadID)
{
	QString filePath = makeFilePath(threadID);
	if (filePath == "")
		return;

	//打开结构图文件 获取结构图对象
	Hdf5IO tempIO;
	tempIO.setFilePath(filePath.toStdString());
	tempIO.initHdf5Data();
	if (tempIO.hdf5DataList.size() < 1)
		return;

	//创建一个新的h5文件 存储临时的数据
	Hdf5IO::creatNewHdf5File(this->tempFilePath.toStdString());
	Hdf5IO newHdf5IO;
	newHdf5IO.setFilePath(this->tempFilePath.toStdString());
	auto structData = tempIO.hdf5DataList.begin();
	auto newStructData = Hdf5IO::copyToHdf5IO(newHdf5IO, *structData);
	init(newStructData);
}

void ControlTreeWidget::outputTempFile(unsigned long threadID)
{
	QString filePath = makeFilePath(threadID);
	if (filePath == "")
		return;
	//打开结构图文件 获取结构图对象
	Hdf5IO tempIO;
	tempIO.setFilePath(filePath.toStdString());
	tempIO.initHdf5Data();
	if (tempIO.hdf5DataList.size() < 1)
		return;

	//打开h5文件 存储临时的数据
	Hdf5IO newHdf5IO;
	newHdf5IO.setFilePath(this->tempFilePath.toStdString());
	auto structData = tempIO.hdf5DataList.begin();
	auto newStructData = Hdf5IO::copyToHdf5IO(newHdf5IO, *structData);
}


