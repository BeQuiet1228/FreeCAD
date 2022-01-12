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

bool DocumentManager::loadFile(const QString& filePath)
{
	std::string _filePath = filePath.toStdString();
	loadFile(_filePath);
	return true;
}


/**
* @time	2021/12/02
* @brief DocumentManager::loadFile 读取文件，并保存数据
* @param const std::string & FilePath
* @return bool
*/
bool DocumentManager::loadFile(const std::string& FilePath)
{
	Hdf5IO io(FilePath);
	io.initHdf5Data();
	hdf5dataList = io.hdf5DataList;
	return true;
}
DocumentManager::DocumentManager(){
	//构造数据管理
	DV::CanvasItem::registerMetaTye();
	classID = 5;
}
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

std::vector<Hdf5Data> DocumentManager::gethdf5dataList()
{
	return hdf5dataList;
}

/**
* @time	2021/12/02
* @brief DocumentManager::saveHdf5Data 直接传入数据时，保存数据。
* @param Hdf5Data data
* @return int
*/
int DocumentManager::saveHdf5Data(Hdf5Data data)
{
	hdf5dataList.push_back(data);
	return hdf5dataList.size() - 1;
}