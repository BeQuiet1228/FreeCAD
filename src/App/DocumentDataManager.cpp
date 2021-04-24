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
	//构造数据管理
	CanvasItem::registerMetaTye();
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

	m_DataSourceManage->DisPlayPlot(data, _type);
	/*std::list<Gui::MDIView*> list=Gui::Application().activeDocument()->getMDIViews();
	Gui::PlotMDIView* ptr=nullptr;
	for each (Gui::MDIView* var in list)
	{
	ptr=dynamic_cast<Gui::PlotMDIView*> (var);
	if (ptr)break;
	}
	if (ptr!=nullptr)
	{
	if (m_DataSourceManage)
	m_DataSourceManage->DisPlayPlot(data, _type);
	}
	else
	{
	Gui::PlotMDIView* plot = new Gui::PlotMDIView(Gui::Application().activeDocument()->getDocument());
	Gui::MainWindow::getInstance()->addWindow(plot);
	bindTreeContrue(nullptr, (Plot*)plot->GetViewPtr());
	m_DataSourceManage->DisPlayPlot(data, _type);
	}*/
	
}

void DocumentManager::_ToRenderer(std::string name, int index)
{
	if (m_DataSourceManage)
		m_DataSourceManage->tranfromRenderer(name,index);
}