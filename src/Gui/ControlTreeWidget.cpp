#include "PreCompiled.h"
#include "MainWindow.h"
#ifndef _PreComp_
# include <boost/signals.hpp>
# include <boost/bind.hpp>
# include <QAbstractItemView>
# include <QActionEvent>
# include <QApplication>
# include <QDesktopWidget>
# include <QEvent>
# include <QMessageBox>
# include <QTimer>
# include <QToolBar>
# include <QToolButton>
#endif
#include "ControlTreeWidget.h"
#include <QString>
#include <HDF5Reader/hdf5io.h>
#include <iostream>
#include "Contorl/ContorlInterface.h"
#include <QFileInfo>
#include "Gui/Application.h"
#include "DataVisualization/C_encoding.h"
#include "DocumentPic.h"
#include "DataVisualizationTree.h"
#include <HDF5Reader/hdf5io.h>
ControlTreeWidget::ControlTreeWidget(QWidget* parent)
	:QTreeWidget(parent),tempHdf5IO(nullptr)
{
	QTreeWidget::setHeaderLabel(DV::GetEncodingstr(" ", ENCODING_GB2312));
	initItem();
	connect(this, SIGNAL(itemDoubleClicked(QTreeWidgetItem*, int)), this, SLOT(itemDouble_clicke(QTreeWidgetItem*, int)));
	
	auto control = ContorlInterface::GetInstance();
	auto chipicManager = control->getChipicManager();
	connect(chipicManager, SIGNAL(outputStructFileSignal(unsigned long)), this, SLOT(outputStructFile(unsigned long)));
	connect(chipicManager, SIGNAL(newResultFIleSignal(unsigned long)), this, SLOT(outputTempFile(unsigned long)));
	bool b1 = connect(chipicManager, SIGNAL(openH5Result(std::string)), this, SLOT(openResultFile(std::string)));
	//定时器超时
	auto b = connect(&timer, SIGNAL(timeout()), this, SLOT(treeDoubleClickTimeOut()));

}

ControlTreeWidget::~ControlTreeWidget()
{
	for (auto item = items.begin(); item != items.end();)
	{
		auto ptr = item->second;
		item = items.erase(item);
		delete ptr;
	}
}

void ControlTreeWidget::init(const Hdf5Data& data)
{
	//初始化之前，先清理之前的子选项
	clearSubItem();

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
		if (addParticle3DItem(str))
			continue;
		if (addVector3DItem(str))
			continue;
		if (addContour3DItem(str))
			continue;
	}
	update();
}

void ControlTreeWidget::initItem()
{	
	auto item = new QTreeWidgetItem();
	item->setText(0,DV::GetEncodingstr("等位图", ENCODING_GB2312));
	items.insert(std::map<MsgType, QTreeWidgetItem*>::value_type(CONTOUR, item));

	item = new QTreeWidgetItem();
	item->setText(0, DV::GetEncodingstr("相空间图", ENCODING_GB2312));
	items.insert(std::map<MsgType, QTreeWidgetItem*>::value_type(PHASE_SPACE, item));

	item = new QTreeWidgetItem();
	item->setText(0, DV::GetEncodingstr("时间观测图", ENCODING_GB2312));
	items.insert(std::map<MsgType, QTreeWidgetItem*>::value_type(OBSERVE, item));

	item = new QTreeWidgetItem();
	item->setText(0, DV::GetEncodingstr("空间观测图", ENCODING_GB2312));
	items.insert(std::map<MsgType, QTreeWidgetItem*>::value_type(RANGE, item));

	item = new QTreeWidgetItem();
	item->setText(0, DV::GetEncodingstr("矢量图", ENCODING_GB2312));
	items.insert(std::map<MsgType, QTreeWidgetItem*>::value_type(VECTOR, item));

	item = new QTreeWidgetItem();
	item->setText(0, DV::GetEncodingstr("3D相空间图", ENCODING_GB2312));
	items.insert(std::map<MsgType, QTreeWidgetItem*>::value_type(PARTICLE_3D, item));

	item = new QTreeWidgetItem();
	item->setText(0, DV::GetEncodingstr("3D等位图", ENCODING_GB2312));
	items.insert(std::map<MsgType, QTreeWidgetItem*>::value_type(CONTOUR_3D, item));

	item = new QTreeWidgetItem();
	item->setText(0, DV::GetEncodingstr("3D矢量图", ENCODING_GB2312));
	items.insert(std::map<MsgType, QTreeWidgetItem*>::value_type(VECTOR_3D, item));

	for (auto iter = items.begin(); iter != items.end(); iter++)
	{
		addTopLevelItem(iter->second);
	}
}

void ControlTreeWidget::sendControlMsg(QTreeWidgetItem* item)
{
	auto control = ContorlInterface::GetInstance();
	MsgType type;
	int index;
	
	if (!getTypeAndIndex(item, type, index))
		return;
	control->senWinMessage(109, type, index + 1);
	setTreeUnuseable();
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
	for (auto iter = items.begin(); iter != items.end(); iter++)
	{
		index = iter->second->indexOfChild(item);
		if (index < 0)
			continue;
		type = iter->first;
		return true;
	}

	return false;
}

void ControlTreeWidget::clearSubItem()
{
	for (auto iter = items.begin(); iter != items.end(); iter++)
	{
		auto childrens = iter->second->takeChildren();
		for (auto children = childrens.begin(); children != childrens.end();)
		{
			auto ptr = *children;
			children = childrens.erase(children);
			delete ptr;
		}
	}
	update();
}

void ControlTreeWidget::clear()
{
	clearSubItem();
	if (tempHdf5IO == nullptr)
		return;
	delete tempHdf5IO;
	tempHdf5IO = nullptr;
}


bool ControlTreeWidget::addContourItem(const std::string& str)
{
	QString typeName, name, rank;
	typeName = QString::fromStdString("Contour");
	if (!analysisType(str, typeName, name, rank))
		return false;

	QTreeWidgetItem* childItem = new QTreeWidgetItem;
	childItem->setText(0,name);
	auto item = items[CONTOUR];
	item->addChild(childItem);
	return true;
}

bool ControlTreeWidget::addPhaseSpaceItem(const std::string& str)
{
	QString typeName, name, rank;
	typeName = QString::fromStdString("PhaseSpace");
	if (!analysisType(str, typeName, name, rank))
		return false;

	QTreeWidgetItem* childItem = new QTreeWidgetItem;
	childItem->setText(0, name);
	auto item = items[PHASE_SPACE];
	item->addChild(childItem);
	return true;
}

bool ControlTreeWidget::addObserveItem(const std::string& str)
{
	QString typeName, name, rank;
	typeName = QString::fromStdString("Observe");
	if (!analysisType(str, typeName, name, rank))
		return false;

	QTreeWidgetItem* childItem = new QTreeWidgetItem;
	childItem->setText(0, name);
	auto item = items[OBSERVE];
	item->addChild(childItem);
	return true;
}

bool ControlTreeWidget::addRangeItem(const std::string& str)
{
	QString typeName, name, rank;
	typeName = QString::fromStdString("Range");
	if (!analysisType(str, typeName, name, rank))
		return false;

	QTreeWidgetItem* childItem = new QTreeWidgetItem;
	childItem->setText(0, name);
	auto item = items[RANGE];
	item->addChild(childItem);
	return true;
}

bool ControlTreeWidget::addVectorItem(const std::string& str)
{
	QString typeName, name, rank;
	typeName = QString::fromStdString("Vector");
	if (!analysisType(str, typeName, name, rank))
		return false;

	QTreeWidgetItem* childItem = new QTreeWidgetItem;
	childItem->setText(0, name);
	auto item = items[VECTOR];
	item->addChild(childItem);
	return true;
}

bool ControlTreeWidget::addContour3DItem(const std::string& str)
{
	QString typeName, name, rank;
	typeName = QString::fromStdString("CONTOUR3D");
	if (!analysisType(str, typeName, name, rank))
		return false;

	QTreeWidgetItem* childItem = new QTreeWidgetItem;
	childItem->setText(0, name);
	auto item = items[CONTOUR_3D];
	item->addChild(childItem);
	return true;
}

bool ControlTreeWidget::addParticle3DItem(const std::string& str)
{
	QString typeName, name, rank;
	typeName = QString::fromStdString("PHASESPACE3D");
	if (!analysisType(str, typeName, name, rank))
		return false;

	QTreeWidgetItem* childItem = new QTreeWidgetItem;
	childItem->setText(0, name);
	auto item = items[PARTICLE_3D];
	item->addChild(childItem);
	return true;
}

bool ControlTreeWidget::addVector3DItem(const std::string& str)
{
	QString typeName, name, rank;
	typeName = QString::fromStdString("VECTOR3D");
	if (!analysisType(str, typeName, name, rank))
		return false;

	QTreeWidgetItem* childItem = new QTreeWidgetItem;
	childItem->setText(0, name);
	auto item = items[VECTOR_3D];
	item->addChild(childItem);
	return true;
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
	QString qstr = DV::GetEncodingstr(str.c_str(), ENCODING_GB2312);
	auto lists = qstr.split(QString::fromStdString("="));

	if (lists.size() != 2)
		return false;

	qstr = lists.at(0);
	//获取名称和观测排序
	if (qstr.indexOf(typeName) == -1)
		return false;
	rank = qstr.remove(typeName);
	name = lists.at(1);
	name = name.simplified();
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

	QString m3dFileName = name;
	QString path = fileInfo.absolutePath();

	//获取线程数，因为并行时输出文件的路径不一样
	int threadCount = control->getChipicThreadCount(threadID);
	if (threadCount < 1)
		return QString::fromStdString("");
	QString tempFilePath;
	if (threadCount > 1)
		tempFilePath = path + QString::fromStdString("/1/") + m3dFileName + QString::fromStdString("_Temp.h5");
	else
		tempFilePath = path + QString::fromStdString("/") + m3dFileName + QString::fromStdString("_Temp.h5");

	//生成新的临时文件路径
	QString newTempPath = path + QString::fromStdString("/") + m3dFileName + QString::fromStdString("_gather.h5");

	this->tempFilePath = newTempPath;

	return tempFilePath;
}

void ControlTreeWidget::initParticle3DItem()
{
	auto item = items[PARTICLE_3D];

	auto subItem = new QTreeWidgetItem();
	subItem->setText(0,QString::fromLocal8Bit("Particle3D"));
	item->addChild(subItem);
}

void ControlTreeWidget::initContour3DItem()
{
	//观测名称
	std::vector<std::string> names;
	names.reserve(9);
	names.push_back("E1");
	names.push_back("E2");
	names.push_back("E3");
	names.push_back("B1");
	names.push_back("B2");
	names.push_back("B3"); 
	names.push_back("J1"); 
	names.push_back("J2");
	names.push_back("J3");

	auto item = items[CONTOUR_3D];

	for each ( std::string name in names)
	{
		auto subItem = new  QTreeWidgetItem();
		subItem->setText(0,QString::fromStdString(name));
		item->addChild(subItem);
	}

}

void ControlTreeWidget::itemDouble_clicke(QTreeWidgetItem* item, int column)
{
	if ((item->flags() & Qt::ItemIsEnabled) != Qt::ItemIsEnabled)
		return;
	sendControlMsg(item);
}


void ControlTreeWidget::outputStructFile(unsigned long threadID)
{
	auto control = ContorlInterface::GetInstance();
	if (!control->hasManualChipicRuning())
		return;

	QString filePath = makeFilePath(threadID);
	if (filePath == QString::fromStdString(""))
		return;

	//打开结构图文件 获取结构图对象
	Hdf5IO tempIO;
	tempIO.setFilePath(filePath.toStdString());
	tempIO.initHdf5Data();
	if (tempIO.hdf5DataList.size() < 1)
		return;

	//创建一个新的h5文件 存储临时的数据
	if (tempHdf5IO != nullptr)
		delete tempHdf5IO;
	tempHdf5IO = new Hdf5IO();
	tempHdf5IO->setFilePath(this->tempFilePath.toStdString(),Hdf5IO::CREAT_NEW_FILE);
	auto structData = tempIO.hdf5DataList.begin();
	auto newStructData = Hdf5IO::copyToHdf5IO(*tempHdf5IO, *structData);
	init(newStructData);
	
	auto mainWindow = Gui::MainWindow::getInstance();

	mainWindow->ClearVisualizationTree();
	mainWindow->showVisualizationTree();
	mainWindow->dataVisualizationTree->addHdf5Data(newStructData);
 
	
}

void ControlTreeWidget::outputTempFile(unsigned long threadID)
{
	setTreeUseable();

	if (tempHdf5IO == nullptr)
		return;

	QString filePath = makeFilePath(threadID);
	if (filePath == QString::fromStdString(""))
		return;
	//打开结构图文件 获取结构图对象
	Hdf5IO tempIO;
	tempIO.setFilePath(filePath.toStdString());
	tempIO.initHdf5Data();
	if (tempIO.hdf5DataList.size() < 1)
		return;
	auto data= tempIO.hdf5DataList.begin();
	auto newData = Hdf5IO::copyToHdf5IO(*tempHdf5IO, *data);
	
	Gui::MainWindow::getInstance()->dataVisualizationTree->addHdf5DataToShow(newData);
}

/**
* @brief ControlTreeWidget::treeDoubleClickTimeOut 定时器超时
* @return void
*/
void ControlTreeWidget::treeDoubleClickTimeOut()
{
	setTreeUseable();
}

void ControlTreeWidget::openResultFile(std::string path)
{
	auto control = ContorlInterface::GetInstance();
	if (control->chipicRunModIsAuto())
		return;
	auto mw = Gui::MainWindow::getInstance();
	mw->hideContorlUI();

	//读取hdf5数据
	Hdf5IO hdf5IO(path);
	hdf5IO.initHdf5Data();
	

	//清空临时文件窗口
	mw->ClearVisualizationTree();
	mw->dataVisualizationTree->loadHdf5Datas(hdf5IO.hdf5DataList);
	mw->showVisualizationTree();
}


/**
* @brief ControlTreeWidget::setTreeUnuseable 设置树控件的状态为不可用
* @return void
*/
void ControlTreeWidget::setTreeUnuseable()
{
	return;
// 	for(auto iter = items.begin();iter != items.end();iter++)
// 		(*iter)->setFlags(contourItem->flags() & (~Qt::ItemIsEnabled));
// 	timer.start(timeOutCount);
}

/**
* @brief ControlTreeWidget::setTreeUseable 设置树控件为可用状态
* @return void
*/
void ControlTreeWidget::setTreeUseable()
{
	return;
// 	for (auto iter = items.begin(); iter != items.end(); iter++)
// 		(*iter)->setFlags(contourItem->flags() | Qt::ItemIsEnabled);
// 	Gui::MainWindow::getInstance()->setFocus();
// 	this->setEnabled(true);
// 	timer.stop();
}

