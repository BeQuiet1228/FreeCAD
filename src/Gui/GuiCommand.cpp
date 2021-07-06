#include "PreCompiled.h"

#include "GuiCommand.h"
#include "command.h"
#include "Application.h"
#include "FileDialog.h"
#include "MainWindow.h"
#include "PlotMDIView.h"
#include "DataVisualization/Plot.h"
DEF_STD_CMD_A(GuiCmdPlotDataExport);
GuiCmdPlotDataExport::GuiCmdPlotDataExport() 
	:Command("gui_plot_data_export"){
	sGroup = QT_TR_NOOP("Vislization");
	sMenuText = QT_TR_NOOP("Plot data export...");
	sToolTipText = QT_TR_NOOP("export plot data under a new file name");
	sWhatsThis = "gui_plot_data_export";
	sStatusTip = QT_TR_NOOP("export plot data under a new file name");
	eType = 0;
}

void GuiCmdPlotDataExport::activated(int iMsg) {
	QString fn = Gui::FileDialog::getSaveFileName(Gui::MainWindow::getInstance(), QObject::tr("Export data"),
		QString(), QString::fromLatin1("(*.h5 *.png)"));
	if (fn.isEmpty())
		return;
	auto view = Gui::MainWindow::getInstance()->activeWindow();
	auto plotView = dynamic_cast<Gui::PlotMDIView*>(view);
	if (!plotView)
		return;
	plotView->getPlot()->MainRendererDataSaveAs(fn.toStdString());
}
bool GuiCmdPlotDataExport::isActive() {
	return getGuiApplication()->sendHasMsgToActiveView("PlotDataExport");
}

DEF_STD_CMD_A(GuiCmdPlotEqualProportion);
GuiCmdPlotEqualProportion::GuiCmdPlotEqualProportion()
	:Command("gui_plot_equal_proportion") {
	sGroup = QT_TR_NOOP("Vislization");
	sMenuText = QT_TR_NOOP("Plot proportion...");
	sToolTipText = QT_TR_NOOP("set plot proportion 1:1");
	sWhatsThis = "gui_plot_equal_proportion";
	sStatusTip = QT_TR_NOOP("set plot proportion 1:1");
	eType = 0;
}

void GuiCmdPlotEqualProportion::activated(int iMsg) {
	auto view = Gui::MainWindow::getInstance()->activeWindow();
	auto plotView = dynamic_cast<Gui::PlotMDIView*>(view);
	if (!plotView)
		return;
	plotView->getPlot()->EqualScaleDisplay();
}
bool GuiCmdPlotEqualProportion::isActive() {
	return getGuiApplication()->sendHasMsgToActiveView("PlotEqualProportion");
}


void creatGuiCommand()
{
	Gui::CommandManager& rcCmdMgr = Gui::Application::Instance->commandManager();
	rcCmdMgr.addCommand(new GuiCmdPlotDataExport);
	rcCmdMgr.addCommand(new GuiCmdPlotEqualProportion);
}
