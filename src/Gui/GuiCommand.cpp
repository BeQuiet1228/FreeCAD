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
	sPixmap = "help-supertube";
	eType = 0;
}

void GuiCmdPlotDataExport::activated(int iMsg) {
	QString fn = Gui::FileDialog::getSaveFileName(Gui::MainWindow::getInstance(), QObject::tr("Export data"),
		QString(), QString::fromLatin1("(*.png *.h5)"));
	if (fn.isEmpty())
		return;
	auto view = Gui::MainWindow::getInstance()->activeWindow();
	auto plotView = dynamic_cast<Gui::PlotMDIView*>(view);
	if (!plotView)
		return;
	//plotView->getPlot()->MainRendererDataSaveAs(fn.toStdString());
	plotView->getPlot()->SaveAs(fn.toUtf8().data());
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
	sPixmap = "help-supertube";
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


DEF_STD_CMD_A(StdCmdMultipleTargetGeneticAlgorithmG);

StdCmdMultipleTargetGeneticAlgorithmG::StdCmdMultipleTargetGeneticAlgorithmG()
	: Command("Std_Multiple_TargetGenetic_Algorithm_G")
{
	// setting the
	sGroup = QT_TR_NOOP("File");
	sMenuText = QT_TR_NOOP("MultipleTargetGeneticAlgorithmG");
	sToolTipText = QT_TR_NOOP("MultipleTargetGeneticAlgorithmG");
	sWhatsThis = "Std_Paralle_Run";
	sStatusTip = QT_TR_NOOP("SmartContorl");
	sPixmap = "smartContorl";
}

void StdCmdMultipleTargetGeneticAlgorithmG::activated(int iMsg)
{
	Q_UNUSED(iMsg);
	doCommand(Command::Gui, "Gui.SendMsgToActiveView(\"Save\")");
	getGuiApplication()->sendMsgToActiveView("showMultipleTargetGeneticAlgorithmG");
}
bool StdCmdMultipleTargetGeneticAlgorithmG::isActive(void)
{
	return getGuiApplication()->sendHasMsgToActiveView("showMultipleTargetGeneticAlgorithmG");
}


void creatGuiCommand()
{
	Gui::CommandManager& rcCmdMgr = Gui::Application::Instance->commandManager();
	rcCmdMgr.addCommand(new GuiCmdPlotDataExport);
	rcCmdMgr.addCommand(new GuiCmdPlotEqualProportion);
	rcCmdMgr.addCommand(new StdCmdMultipleTargetGeneticAlgorithmG);
}
