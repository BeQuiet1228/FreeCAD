#pragma once
#include <QTreeWidget>
#include <HDF5Reader/hdf5io.h>
class ControlTreeWidget :public QTreeWidget {
public:
	~ControlTreeWidget();
	ControlTreeWidget();

public:
	void init(const Hdf5Data& data);
};