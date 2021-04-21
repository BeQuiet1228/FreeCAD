#pragma once
#ifndef DATARESOURCE_H_
#define DATARESOURCE_H_
//#include <QWidget>
#include "HDF5Reader/hdf5io.h"
#include<map>
#include "ListTreeWidget.h"
#include "exportConfig.hpp"
//#include "RendererFactory.h"
class Plot;
class RendererFactory;
class Renderer;
using RendererPtr = std::shared_ptr < Renderer > ;
using Renderers = std::list < RendererPtr > ;
class ListTreeWidget;
class DATA_VISUALIZATION_EXPORT DataSourceManage:public QObject
{
	Q_OBJECT
public:
	explicit DataSourceManage();
	DataSourceManage& operator =(const DataSourceManage& that){
		return *this;
	}
public:
	~DataSourceManage();
public:
	void init(ListTreeWidget* ptr,Plot* p);
Q_SIGNALS:
	void _loadhdflist(std::vector<Hdf5Data>& Hdf5Data);
	void _reRendererEvent(const std::list<std::shared_ptr<Renderer>>& listRender);
public Q_SLOTS :
	void tranfromRenderer(std::string name, int index);
	void clearMap();
	void loadhdffile(std::string filepath);
private:
	Renderers CreateRendererList(Hdf5Data data);
	Renderers CreateRenderer(Hdf5Data data, int _type);
private:
	std::map<std::string,Renderers> RendererManger;
	std::vector<Hdf5Data> hdfDatelist;
	Plot* p;
	RendererFactory* factoryptr;
	Hdf5IO _hdf5io;
};
#endif