#include "PreCompiled.h"
#include "DocumentPic.h"
#include <iostream>
#include "LuaEditView.h"
#include "PlotMDIView.h"
#include "MainWindow.h"
#include "View3DInventor.h"
#include "app/DocumentDataManager.h"
DocumentPic::DocumentPic(App::Document* pcDocument, Gui::Application* app)
	:Gui::Document(pcDocument,app)
{

}

/**
* @brief DocumentPic::initMDIView 初始化mdi窗口
* @return void
*/
void DocumentPic::initMDIView()
{
	auto appDoc = getAppDocument();
	if (appDoc == nullptr)
		return ;

	//判断是否为文本编辑器工程，如果是那么不显示3D视窗
	if (appDoc->classID == 1 || appDoc->classID == 4)
	{
		LuaEditView* edit = new LuaEditView(this);
		auto mainWindow = Gui::MainWindow::getInstance();
		mainWindow->addWindow(edit);
	}
	else if (appDoc->classID == 5) {
		Gui::PlotMDIView* plot = new Gui::PlotMDIView(*this);
		auto mainWindow = Gui::MainWindow::getInstance();
		mainWindow->addWindow(plot);
	}
	else {
		createView(Gui::View3DInventor::getClassTypeId());
	}
}

/**
* @brief DocumentPic::getAppDocument 获取app doc
* @return App::Document* 获取失败 返回 nullptr
*/
App::Document* DocumentPic::getAppDocument()
{
	//document中只是保存了appDocument的指针，并不负责管理
	//所以在appDocument被释放了之后，再调用会抛出异常
	App::Document* doc = nullptr;
	try {
		doc = getDocument();
	}catch (...) {
		std::cerr << "DocumentPic::getAppDocument() get document failed!" << std::endl;
	}

	return doc;
}

/**
* @brief DocumentPic::releaseH5Object 释放app doc 中的h5对象
* @return void
*/
void DocumentPic::releaseH5Object()
{
	auto doc = getAppDocument();
	if (doc == nullptr)
		return;

	auto dataDoc = dynamic_cast<DocumentManager*>(doc);
	if (!dataDoc)
		return;

	dataDoc->restoreH5Data();
}

/**
* @brief DocumentPic::getTextPath 获取文本路径
* @return std::string
*/
std::string DocumentPic::getTextPath()
{
	//设置运行路
	auto appDoc = getAppDocument();
	if (appDoc == nullptr)
		return "";
	std::string path = appDoc->FileName.getValue();
	if (appDoc->classID == 2)
	{
		QString temp = QString::fromUtf8(path.c_str());
		temp = temp.left(temp.length() - 6) + QString::fromLocal8Bit(".m3d");
		path = temp.toStdString();
	}
	else if (appDoc->classID == 3) {
		QString temp = QString::fromUtf8(path.c_str());
		temp = temp.left(temp.length() - 9) + QString::fromLocal8Bit(".m2d");
		path = temp.toStdString();
	}

	return path;
}

void DocumentPic::openH5File(const std::string& path)
{
	auto appDoc = getAppDocument();
	if (appDoc == nullptr)
		return ;
	DocumentManager* docm = dynamic_cast<DocumentManager*>(appDoc);
	if (!docm)
		return;

	docm->loadFile(path);
}

