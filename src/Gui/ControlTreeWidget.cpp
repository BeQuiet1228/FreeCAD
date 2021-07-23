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
ControlTreeWidget::ControlTreeWidget(QWidget* parent)
	:QTreeWidget(parent),tempHdf5IO(nullptr)
{
	QTreeWidget::setHeaderLabel(GetEncodingstr(" ", ENCODING_GB2312));
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
	for each (QTreeWidgetItem * item in items)
	{
		delete item;
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
	contourItem->setText(0,GetEncodingstr("等位图", ENCODING_GB2312));

	phaseSpaceItem = items.at(1);
	phaseSpaceItem->setText(0, GetEncodingstr("相空间图", ENCODING_GB2312));

	observeItem = items.at(2);
	observeItem->setText(0,GetEncodingstr("时间观测图", ENCODING_GB2312));

	rangeItem = items.at(3);
	rangeItem->setText(0, GetEncodingstr("空间观测图", ENCODING_GB2312));

	vectorItem = items.at(4);
	vectorItem->setText(0, GetEncodingstr("矢量图", ENCODING_GB2312));

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
		index = vectorItem->indexOfChild(item);
		type = VECTOR;
	}else if (phaseSpaceItem->indexOfChild(item) >= 0) {
		index = phaseSpaceItem->indexOfChild(item);
		type = PHASE_SPACE;
	}else if (rangeItem->indexOfChild(item) >= 0) {
		index = rangeItem->indexOfChild(item);
		type = RANGE;
	}
	if (type == NONE)
		return false;
	return true;
}

void ControlTreeWidget::clearSubItem()
{
	for each (QTreeWidgetItem * item in items)
	{
		auto childs = item->takeChildren();
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
	contourItem->addChild(childItem);
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
	phaseSpaceItem->addChild(childItem);
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
	observeItem->addChild(childItem);
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
	rangeItem->addChild(childItem);
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
	vectorItem->addChild(childItem);
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
	QString qstr = GetEncodingstr(str.c_str(), ENCODING_GB2312);
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
	
	Gui::MainWindow::getInstance()->ClearVisualizationTree();
	Gui::MainWindow::getInstance()->showVisualizationTree();
 
	Gui::Application::ToStruct(newStructData);
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
	auto structData = tempIO.hdf5DataList.begin();
	auto newStructData = Hdf5IO::copyToHdf5IO(*tempHdf5IO, *structData);
	Gui::Application::DisplatPlot(newStructData);
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
	auto mw = Gui::MainWindow::getInstance();
	mw->hideContorlUI();

	//清空h5文件对象
	auto doc = Gui::Application::Instance->activeDocument();
	auto picDoc = dynamic_cast<DocumentPic*>(doc);
	if (picDoc)
		picDoc->releaseH5Object();
	picDoc->openH5File(path);
	//显示树控件
	mw->showVisualizationTree();
}


/**
* @brief ControlTreeWidget::setTreeUnuseable 设置树控件的状态为不可用
* @return void
*/
void ControlTreeWidget::setTreeUnuseable()
{
	return;
	for(auto iter = items.begin();iter != items.end();iter++)
		(*iter)->setFlags(contourItem->flags() & (~Qt::ItemIsEnabled));
	timer.start(timeOutCount);
}

/**
* @brief ControlTreeWidget::setTreeUseable 设置树控件为可用状态
* @return void
*/
void ControlTreeWidget::setTreeUseable()
{
	return;
	for (auto iter = items.begin(); iter != items.end(); iter++)
		(*iter)->setFlags(contourItem->flags() | Qt::ItemIsEnabled);
	Gui::MainWindow::getInstance()->setFocus();
	this->setEnabled(true);
	timer.stop();
}

