#pragma once 
#ifndef _DOCUMENTMANAGER_H_
#define _DOCUMENTMANAGER_H_
#include "Document.h"
#include <QString>
#include "DataVisualization/Dataresource.h"
//class DataSourceManage;
class AppExport DocumentManager :public App::Document
{
public:
	DocumentManager();
	~DocumentManager();
public:
	void Save(Base::Writer &write) const override;
	//快捷调用的save函数，这个会在命令里被调用
	bool save() override;
	//撤销与恢复 这里暂时用不到，所以在这里继承后不做操作
	bool undo() override{ return true; }
	bool redo() override { return true; }
	virtual std::string getFileFormat()
	{
		return "hdf5";
	}
	void dataclear();
public:
	//载入文本
	bool loadFile(const QString& filePath);
	bool loadFile(const std::string& FilePath);
	std::vector<Hdf5Data>& gethdf5dataList();
protected:
	std::vector<Hdf5Data> hdf5dataList;
};
#endif