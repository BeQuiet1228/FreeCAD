#include "ControlTreeWidget.h"
#include <QString>
#include <HDF5Reader/hdf5io.h>
#include <iostream>
#include "Contorl/ContorlInterface.h"
ControlTreeWidget::ControlTreeWidget(QWidget* parent)
	:QTreeWidget(parent)
{
	connect(this, SIGNAL(itemDoubleClicked(QTreeWidgetItem*, int)), this, SLOT(itemDouble_clicke(QTreeWidgetItem*, int)));
	
	auto control = ContorlInterface::GetInstance();
	auto chipicManager = control->getChipicManager();
	if(connect(chipicManager, SIGNAL(chipicAnalysisFinished(unsigned long)), this, SLOT(controlAnalysis(unsigned long))))
		std::cerr<< " ";
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

void ControlTreeWidget::itemDouble_clicke(QTreeWidgetItem* item, int column)
{
	sendControlMsg(item);
}


void ControlTreeWidget::controlAnalysis(unsigned long threadID)
{
	Hdf5IO hdf5io;
	hdf5io.setFilePath("C:/PICGUIC_L/Example/3d/MILO_P/TEMP.H5");
	hdf5io.initHdf5Data();
	auto data = *(hdf5io.hdf5DataList.begin());
	initItem();
	init(data);
}

