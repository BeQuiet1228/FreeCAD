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
* @brief DocumentManager::loadfile 加载h5文件
* @param const QString& filePath 传入路径
* @return bool
*/
bool DocumentManager::loadfile(const QString& filePath)
{
	std::string _filePath = filePath.toStdString();
	m_DataSourceManage->loadhdffile(_filePath);
	return true;
}
/**
* @brief DocumentManager::bindTreeContrue 绑定控制控件
* @param ListTreeWidget* ptr
* @param Plot* plotptr
* @return bool
*/
bool DocumentManager::bindTreeContrue(ListTreeWidget* ptr,Plot* plotptr)
{
	if (ptr||plotptr)
	{
		m_DataSourceManage->init(ptr,plotptr);
		return true;
	}
	return false;
}
/**
* @brief DocumentManager::DocumentManager 构造函数
*/
DocumentManager::DocumentManager(){
	//构造数据管理
	CanvasItem::registerMetaTye();
	m_DataSourceManage = new DataSourceManage();
	classID = 5;
}
/**
* @brief DocumentManager::~DocumentManager 析构函数
*/
DocumentManager::~DocumentManager(){
	if (m_DataSourceManage)
	{
		delete m_DataSourceManage;
		m_DataSourceManage = nullptr;
	}
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
* @brief DocumentManager::ToStructHdf5 传入结构图数据
* @param Hdf5Data data
* @return int
*/
int DocumentManager::ToStructHdf5(Hdf5Data data){
	if (m_DataSourceManage)
		return m_DataSourceManage->initStructData(data);
	else
		return -1;
}
/**
* @brief DocumentManager::DisplatPlot 送显
* @param Hdf5Data data
* @param int _type
* @return void
*/
void DocumentManager::DisplatPlot(Hdf5Data data, int _type)
{ 
	m_DataSourceManage->DisPlayPlot(data, _type);
}
/**
* @brief DocumentManager::_ToRenderer 送显
* @param std::string name
* @param int index
* @return void 
*/
void DocumentManager::_ToRenderer(std::string name, int index)
{
	if (m_DataSourceManage)
		m_DataSourceManage->tranfromRenderer(name,index);
}
/**
* @brief  DocumentManager::dataclear 删除数据
* @return void  
*/
void DocumentManager::dataclear()
{
	if (m_DataSourceManage)
		m_DataSourceManage->DataClear();
}
/**
* @brief  DocumentManager::iSbind 是否绑定
* @return bool  
*/
bool DocumentManager::iSbind()
{
	if (m_DataSourceManage)
	{
		return m_DataSourceManage->isbind();
	}
	return false;
}