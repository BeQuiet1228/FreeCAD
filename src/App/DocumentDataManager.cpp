#include "PreCompiled.h"
#include "DocumentDataManager.h"
#include <string>
#include <QWidget>
#include "DataVisualization/Dataresource.h"
bool DocumentManager::loadfile(const QString& filePath)
{
	std::string _filePath = filePath.toStdString();
	m_DataSourceManage->loadhdffile(_filePath);
	return true;
}
bool DocumentManager::bindTreeContrue(ListTreeWidget* ptr,Plot* plotptr)
{
	if (ptr||plotptr)
	{
		m_DataSourceManage->init(ptr,plotptr);
		return true;
	}
	return false;
}
DocumentManager::DocumentManager(){
	m_DataSourceManage = new DataSourceManage();
}
DocumentManager::~DocumentManager(){
	if (m_DataSourceManage)
	{
		delete m_DataSourceManage;
		m_DataSourceManage = nullptr;
	}
}
void DocumentManager::Save(Base::Writer &write) const
{

}
bool DocumentManager::save(){
	return true;
}
void DocumentManager::ToStructHdf5(Hdf5Data data){
	if (m_DataSourceManage)
		m_DataSourceManage->initStructData(data);
}
void DocumentManager::DisplatPlot(Hdf5Data data, int _type)
{
	if (m_DataSourceManage)
		m_DataSourceManage->DisPlayPlot(data, _type);
}