#include "PreCompiled.h"
#include "FileFormatH5.h"
#include "Application.h"
#include "App/DocumentH5.h"
#include <FileDialog.h>
#include"PlotMDIView.h"
#include "CombiView.h"
#include "DockWindowManager.h"
#include "MainWindow.h"
#include "DataVisualization/Canvas.h"
#include"DataVisualization/ListTreeWidget.h"
#include "Gui/MainWindow.h"
#include"TreeViewctrl.h"



#include "DataVisualizationTree.h"
#include "hdf5DataItemFactory.h"
#include "Hdf5DataItemEventHandler.h"
#include "HDF5DataItem2DFactory.h"
#include "HDF5DataItem2DDoubleClickEventHander.h"
/**
* @brief FileFormatH5::open 打开h5文件并进行处理
* @param const QStringList& fileList 文件路径列表
* @return void
*/
void FileFormatH5::open(const QStringList& fileList)
{
	for (auto i = fileList.begin();i!=fileList.end(); i++)
	{
		QDir dir(*i);
		QString filename = dir.dirName();
		App::Document* doc = App::GetApplication().newDocumentH5(i->toUtf8().data(),filename.toUtf8(), "");
		this->openOnce(*i,doc);
		Gui::FileDialog::setWorkingDirectory(QString(*i).remove(filename));
	}
}
/**
* @brief FileFormatH5::openOnce 打开一次
* @param const QString& fileList
* @param App::Document* doc
* @return void
*/
void FileFormatH5::openOnce(const QString& fileList, App::Document* doc)
{
	doc->FileName.setValue(fileList.toUtf8());
	App::DocumentH5* docH5 = static_cast<App::DocumentH5*> (doc);
	if (!docH5)
		return;
	docH5->loadHdf5File(fileList.toStdString());
	auto mw = Gui::MainWindow::getInstance();
	mw->ClearVisualizationTree();
	mw->showVisualizationTree();

	auto hdf5Datas = docH5->getHdf5IO()->hdf5DataList;

	Gui::DataVisualizationTree* tree = mw->dataVisualizationTree;
	tree->loadHdf5Datas(hdf5Datas);
}
