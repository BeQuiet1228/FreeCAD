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
	int initStructData(Hdf5Data& data);
	void DisPlayPlot(Hdf5Data data,int _type=0);
	void DataClear();
	//bool isbind();
Q_SIGNALS:
	void _loadhdflist(std::vector<Hdf5Data>& Hdf5Data);
	void _reRendererEvent(const std::list<std::shared_ptr<Renderer>>& listRender);
	void toTreeNewData(Hdf5Data& data,int index);
public Q_SLOTS :
	void tranfromRenderer(std::string name, int index);
	void clearMap();
	void loadhdffile(std::string filepath);
private:
	Renderers CreateRendererList(Hdf5Data& data);
	Renderers CreateRenderer(Hdf5Data& data, int _type);
private:
	std::map<std::string,Renderers> RendererManger;
	std::vector<Hdf5Data> hdfDatelist;
	Hdf5Data structData;
	int structindex;
	//工厂类
	std::shared_ptr<RendererFactory> factoryptr;
	//用于保存Plot和ListTreeWidget的地址,仅用于校验使用
	unsigned long long treePtrsite;
	unsigned long long plotPtrsite;
	Hdf5IO _hdf5io;
};
#endif