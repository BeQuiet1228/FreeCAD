#pragma once
#include <QTreeWidget>
#include <HDF5Reader/hdf5io.h>
#include <QTreeWidgetItem>
#include <vector>
#include <QTimer>
class ControlTreeWidget :public QTreeWidget {
	enum MsgType {
		NONE = 0,
		CONTOUR = 1,
		PHASE_SPACE,
		OBSERVE,
		VECTOR = 5,
		RANGE,
	};
	Q_OBJECT
public:
	~ControlTreeWidget();
	ControlTreeWidget(QWidget* parent = 0);

public:
	void init(const Hdf5Data& data);
	void initItem();
	//根据被点击的item，发送消息
	void sendControlMsg(QTreeWidgetItem* item);
	//根据item，获取类型，和图索引
	bool getTypeAndIndex(QTreeWidgetItem* item, MsgType& type, int& index);
	void clearSubItem();
	//清除数据
	void clear();
private:
	QTreeWidgetItem* contourItem,*phaseSpaceItem,*observeItem,*rangeItem,*vectorItem;
	const unsigned int itemCount = 5;
	std::vector<QTreeWidgetItem*> items;

private:
	bool addContourItem(const std::string& str);
	bool addPhaseSpaceItem(const std::string& str);
	bool addObserveItem(const std::string& str);
	bool addRangeItem(const std::string& str);
	bool addVectorItem(const std::string& str);
	bool analysisType(const std::string& str,const QString& typeName ,QString& name, QString& rank);
	//生成临时文件路径
	QString makeFilePath(unsigned long threadID);
public Q_SLOTS :
	void itemDouble_clicke(QTreeWidgetItem* item, int column);
	//控制模块解析完成
	void outputStructFile(unsigned long threadID);
	//输出临时文件
	void outputTempFile(unsigned long threadID);
	//点击定时器超时
	void treeDoubleClickTimeOut();
	//计算完成槽
	void openResultFile(std::string path);
private:
	//存储临时文件路径
	QString tempFilePath;
	//存储临时h5文件
	Hdf5IO *tempHdf5IO;
	//点击超时定时器
	QTimer timer;
	//超时时间
	const unsigned int timeOutCount = 10*1000;
private:
	//设置树控件为不可用
	void setTreeUnuseable();
	void setTreeUseable();
};