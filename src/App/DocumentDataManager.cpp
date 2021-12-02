#include "PreCompiled.h"
#include "DocumentDataManager.h"
#include <string>
#include <QWidget>
#include "DataVisualization/Dataresource.h"
#include "DataVisualization/Plot.h"
#include "Gui/Document.h"
#include "Gui/MDIView.h"
#include "Gui/PlotMDIView.h"
#include "Gui/MainWindow.h"
#include "Gui/Application.h"
/**
* @brief DocumentManager::loadFile 加载h5文件
* @param const QString& filePath 传入路径
* @return bool
*/
bool DocumentManager::loadFile(const QString& filePath)
{
	std::string _filePath = filePath.toStdString();
	loadFile(_filePath);
	return true;
}

bool DocumentManager::loadFile(const std::string& FilePath)
{
	//m_DataSourceManage->loadhdffile(FilePath);
	Hdf5IO io(FilePath);
	io.initHdf5Data();
	hdf5dataList = io.hdf5DataList;
	return true;
}

/**
* @brief DocumentManager::DocumentManager 构造函数
*/
DocumentManager::DocumentManager(){
	//构造数据管理
	DV::CanvasItem::registerMetaTye();
	classID = 5;
}
/**
* @brief DocumentManager::~DocumentManager 析构函数
*/
DocumentManager::~DocumentManager(){
	hdf5dataList.clear();
}
/**
* @brief DocumentManager::Save
* @param Base::Writer &write
* @return void
*/
void DocumentManager::Save(Base::Writer &write) const
{

}
/**
* @brief DocumentManager::save 保存
* @return bool
*/
bool DocumentManager::save(){
	return true;
}

/**
* @brief  DocumentManager::dataclear 删除数据
* @return void  
*/
void DocumentManager::dataclear()
{
	hdf5dataList.clear();
}

std::vector<Hdf5Data>& DocumentManager::gethdf5dataList()
{
	return hdf5dataList;
}
int DocumentManager::saveHdf5Data(Hdf5Data data)
{
	hdf5dataList.push_back(data);
	return hdf5dataList.size() - 1;
}