#pragma once
#ifndef DATARESOURCE_H_
#define DATARESOURCE_H_
#include <QWidget>
#include "HDF5Reader/hdf5io.h"
#include "Renderer.h"
#include<map>
#include "Plot.h"
#include "RendererFactory.h"
#include "ListTreeWidget.h"
class DataSourceManage:public QObject
{
	Q_OBJECT
public:
	explicit DataSourceManage();
	DataSourceManage& operator =(const DataSourceManage& that){}
public:
	~DataSourceManage(){
		RendererManger.clear();
	}
	static DataSourceManage* Getinstance()
	{
		static DataSourceManage instance;
		return &instance;
	}
public:
	void init(ListTreeWidget* ptr);
signals:
	void _loadhdflist(std::vector<Hdf5Data>& Hdf5Data);
public slots:
	void tranfromRenderer(std::string name, int index);
	void clearMap();
	void loadhdffile(std::string filepath);
private:
	RendererPtr CreateRendererList(Hdf5Data data);
private:
	std::map<std::string,RendererPtr> RendererManger;
	std::vector<Hdf5Data> hdfDatelist;
	Plot p;
};
#endif