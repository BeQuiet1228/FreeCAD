#include "PreCompiled.h"
#include "HDF5DataItem2DDoubleClickEventHander.h"
#include <cassert>
#include "Hdf5DataItem.h"
#include "App/DocumentDataManager.h"
#include "PlotMDIView.h"
#include "MainWindow.h"
namespace Gui
{
	struct structDirectType {
		std::string str;
		DV::DirectionType mDirectionType;
	};
	const structDirectType structDirectTypelist[]
	{
		{
			"Phi-Z",
			DV::DirectionType::R_Z
		},
		{
			"Z-R",
			DV::DirectionType::R_Z,
		},
		{
			"R*cos(Phi)-R*sin(Phi)",
			DV::DirectionType::R_THETA
		},
		{
			"X_Y",
			DV::DirectionType::X_Y
		},
		{
			"Y_Z",
			DV::DirectionType::Y_Z
		},
		{
			"X_Z",
			DV::DirectionType::X_Z
		}
	};
}
Gui::HDF5DataItem2DDoubleClickEventHander::HDF5DataItem2DDoubleClickEventHander():ishaveStruct(false)
{

}

void Gui::HDF5DataItem2DDoubleClickEventHander::trigger(HDF5DataItem* item)
{
	assert(item && "item is nullptr");
	auto h5data = item->getHdf5Data();
	std::string name = item->text().toStdString();
	//获取适配器
	auto plotAdapter = creatPlotAdapter(h5data, name);
	//获取Plot
	auto guidoc = dynamic_cast<DocumentPic*>(Gui::Application::Instance->activeDocument());
	std::list<Gui::MDIView*> list = guidoc->getMDIViews();
	Gui::PlotMDIView* ptr = nullptr;
	for each (Gui::MDIView * var in list)
	{
		ptr = dynamic_cast<Gui::PlotMDIView*>(var);
		if (ptr) break;
	}
	if (nullptr == ptr)
	{
		ptr = new Gui::PlotMDIView(guidoc);
		Gui::MainWindow::getInstance()->addWindow(ptr);
	}
	Gui::MainWindow::getInstance()->setActiveWindow(ptr);
	ptr->setAdapter(plotAdapter);
}


/**
* @time	2021/12/20
* @brief Gui::HDF5DataItem2DDoubleClickEventHander::setStructData
* @param Hdf5Data data
* @return void
*/
void Gui::HDF5DataItem2DDoubleClickEventHander::setStructData(Hdf5Data data)
{
	structData = data;
}


/**
* @time	2021/12/20
* @brief Gui::HDF5DataItem2DDoubleClickEventHander::creatPlotAdapter 创建适配器
* @param Hdf5Data h5d
* @param std::string name
* @return DV::PlotAdapterPtr
*/
DV::PlotAdapterPtr Gui::HDF5DataItem2DDoubleClickEventHander::creatPlotAdapter(Hdf5Data h5d, std::string name)
{
	std::shared_ptr<DV::RendererFactory> factoryPtr;
	factoryPtr.reset(new DV::RendererFactory());
	if (ishaveStruct)
		factoryPtr->setStructData(structData);
	if (h5d.name != "struct")
		return factoryPtr->creatPlotAdapter(h5d);
	DV::DirectionType type = DV::X_Y;
	for (auto& it : structDirectTypelist)
	{
		if(name!=it.str)
			continue;
		type = it.mDirectionType;
		break;
	}
	return factoryPtr->creatPlotAdapter(h5d, type);
}

