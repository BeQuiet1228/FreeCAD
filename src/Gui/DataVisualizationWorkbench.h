#pragma once
#include "Workbench.h"
namespace Gui {
	class MenuItem;
	class ToolBarItem;
	class DockWindowItems;
	class WorkbenchManager;
}
class DataVisualizationWorkbench:public Gui::Workbench {
	TYPESYSTEM_HEADER();
public:
	DataVisualizationWorkbench();
	~DataVisualizationWorkbench();


protected:
	/** Returns a MenuItem tree structure of menus for this workbench. */
	virtual Gui::MenuItem* setupMenuBar() const override;
	/** Returns a ToolBarItem tree structure of toolbars for this workbench. */
	virtual Gui::ToolBarItem* setupToolBars() const override;
	/** Returns a ToolBarItem tree structure of command bars for this workbench. */
	virtual Gui::ToolBarItem* setupCommandBars() const override;
	/** Returns a DockWindowItems structure of dock windows this workbench. */
	virtual Gui::DockWindowItems* setupDockWindows() const override;
};