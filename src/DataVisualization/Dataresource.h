#pragma once
#ifndef DATARESOURCE_H_
#define DATARESOURCE_H_
#include "HDF5Reader/hdf5io.h"
#include "Renderer.h"
#include<map>
#include "Plot.h"
class DataSourceManage
{
private:
	DataSourceManage(){
		RendererManger.clear();
	}
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
	void tranfromRenderer(std::string name,Hdf5Data data);
	void clearMap();
	void loadhdffile(std::string filepath);
private:
	Renderer* CreateRendererList(Hdf5Data data);
private:
	std::map<std::string, std::shared_ptr<Renderer>> RendererManger;
	std::vector<Hdf5Data> hdfDatelist;
	Plot p;
};
#endif