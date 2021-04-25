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
void FileFormatH5::openOnce(const QString& fileList, App::Document* doc)
{
	doc->FileName.setValue(fileList.toUtf8());
	DocumentManager* docManager = static_cast<DocumentManager*> (doc);
	if (!docManager)
		return;
	
	//创建树控件，和plot窗口
	//Gui::PlotMDIView* plot = new Gui::PlotMDIView(*doc);
	//Gui::MainWindow::getInstance()->addWindow(plot);
	//Gui::Application::Instance->attachView(plot);
	//在MainWindow里面创建
	/*Gui::DockWnd::CombiView* pcCombiView = qobject_cast<Gui::DockWnd::CombiView*>(Gui::DockWindowManager::instance()->getDockWindow("Combo View"));
	QTabWidget* _tabwidget = pcCombiView->getTabPanel();
	ListTreeWidget* m_lisTreeWidget = new ListTreeWidget();
	_tabwidget->insertTab(3, m_lisTreeWidget,GetEncodingstr("获取结果",ENCODING_GB2312));*/
	//ListTreeWidget* m_lisTreeWidget = new ListTreeWidget();
	Gui::TreeViewCtrl* m_lisTreeWidget = Gui::MainWindow::getInstance()->mTreeWidget;
	docManager->bindTreeContrue((ListTreeWidget*)m_lisTreeWidget,/*(Plot*)plot->GetViewPtr()*/nullptr);
	docManager->loadfile(fileList);
	//auto guiDoc = Gui::Application::Instance->getDocument(doc);
	//auto view = guiDoc->getActiveView();
}
