#include "PreCompiled.h"
#include "DataVisualizationWorkbench.h"
#include "MenuManager.h"
#include "ToolBarManager.h"
#include "DockWindowManager.h"

TYPESYSTEM_SOURCE(DataVisualizationWorkbench, Gui::Workbench)
DataVisualizationWorkbench::DataVisualizationWorkbench()
{
}

DataVisualizationWorkbench::~DataVisualizationWorkbench()
{

}

Gui::MenuItem* DataVisualizationWorkbench::setupMenuBar() const
{
	return new Gui::MenuItem;
}

Gui::ToolBarItem* DataVisualizationWorkbench::setupToolBars() const
{
	using namespace Gui;
	ToolBarItem* root = new ToolBarItem;

	ToolBarItem* visu = new ToolBarItem(root);
	visu->setCommand("DataVisualization");
	*visu << "Std_Open_Data_Visualization_Config" << "Std_Data_Visualization_Auto_Max" << "Std_Data_Visualization_Plot_Display_Grid_Mod"
		<< "gui_plot_data_export" << "gui_plot_equal_proportion";

	return root;
}

Gui::ToolBarItem* DataVisualizationWorkbench::setupCommandBars() const
{
	return new Gui::ToolBarItem;
}

Gui::DockWindowItems* DataVisualizationWorkbench::setupDockWindows() const
{
	return new Gui::DockWindowItems;
}

