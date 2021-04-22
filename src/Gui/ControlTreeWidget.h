#pragma once
#include <QTreeWidget>
#include <HDF5Reader/hdf5io.h>
#include <QTreeWidgetItem>
#include <vector>
class ControlTreeWidget :public QTreeWidget {
	enum MsgType {
		NONE = 0,
		CONTOUR = 1,
		OBSERVE,
		VECTOR,
		PHASE_SPACE,
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

public Q_SLOTS :
	void itemDouble_clicke(QTreeWidgetItem* item, int column);
	//控制模块解析完成
	void controlAnalysis(unsigned long threadID);

private:
	//存储临时文件路径
	QString tempFilePath;
};