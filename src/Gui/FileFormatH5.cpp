#include "PreCompiled.h"
#include "FileFormatH5.h"
#include "Application.h"
#include "App/DocumentDataManager.h"
#include <FileDialog.h>
#include"PlotMDIView.h"
#include "CombiView.h"
#include "DockWindowManager.h"
#include "MainWindow.h"
#include "DataVisualization/Canvas.h"
#include"DataVisualization/ListTreeWidget.h"
#include "Gui/MainWindow.h"
#include"TreeViewctrl.h"
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
		App::Document* doc = App::GetApplication().newDocumentH5(filename.toUtf8(), "");
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
	DocumentManager* docManager = static_cast<DocumentManager*> (doc);
	if (!docManager)
		return;
	auto mw = Gui::MainWindow::getInstance();
	mw->ClearVisualizationTree();
	Gui::TreeViewCtrl* m_lisTreeWidget = Gui::MainWindow::getInstance()->mTreeWidget;
	docManager->loadFile(fileList);
	m_lisTreeWidget->loadHdflist(docManager->gethdf5dataList());
	mw->showVisualizationTree();

}
