#pragma once
#include <QTreeWidget>
#include <HDF5Reader/hdf5io.h>
#include <QTreeWidgetItem>
#include <vector>
class ControlTreeWidget :public QTreeWidget {
public:
	~ControlTreeWidget();
	ControlTreeWidget(QWidget* parent = 0);

public:
	void init(const Hdf5Data& data);
	void initItem();
private:
	QTreeWidgetItem* contourItem,*phaseSpaceItem,*observeItem,*rangeItem,*vectorItem;
	const unsigned int itemCount = 5;
	std::vector<QTreeWidgetItem*> items;

private:
	bool addContourItem(const std::string& str);
	bool addPhaseSpaceItem()
};