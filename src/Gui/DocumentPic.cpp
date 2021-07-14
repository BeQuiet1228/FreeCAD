#include "PreCompiled.h"
#include "DocumentPic.h"
#include <iostream>
#include "LuaEditView.h"
#include "PlotMDIView.h"
#include "MainWindow.h"
#include "View3DInventor.h"
#include "app/DocumentDataManager.h"
#include "TreeViewctrl.h"
#include "Contorl/ContorlInterface.h"
#include "ParticleSwarmOptimizationMDI.h"
#include "MDIView.h"
#include "View3DInventor.h"
#include "View3dMDI.h"
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
	//此处增加树控件和documentManager的绑定
	ListTreeWidget* mlisttreewidget = dynamic_cast<ListTreeWidget*>(Gui::MainWindow::getInstance()->mTreeWidget);
	if (!mlisttreewidget)
	{
		std::cerr << "ListTreeWidget is nullptr from Gui void DocumentPic::openH5File(const std::string& path)" << std::endl;
		return;
	}
	docm->bindTreeContrue(mlisttreewidget, nullptr);
	docm->loadFile(path);
}

void DocumentPic::runChipic()
{
	//设置主界面上的ui
	auto control = ContorlInterface::GetInstance();
	auto mw = Gui::MainWindow::getInstance();
	/*
		如果有仿真程序正在运行，那么实现停止功能。
		如果没有仿真程序运行，那么实现开始功能
	*/
	if (!control->hasChipicRuning()){
		mw->setContorlUI();
		std::string path = this->getTextPath();
		control->setM3dPath(path);

		//清空h5文件对象
		this->releaseH5Object();
	}else
	{
		mw->hideContorlUI();
	}
	

	control->buttonClicked(0);
}

void DocumentPic::stopChipic()
{
	auto control = ContorlInterface::GetInstance();
	control->buttonClicked(0);
}

void DocumentPic::paralleRunChipic()
{
	auto mw = Gui::MainWindow::getInstance();
	mw->setContorlUI();
	auto contorl = ContorlInterface::GetInstance();
	contorl->setM3dPath(getTextPath());
	contorl->buttonClicked(1);
}

void DocumentPic::showParticleSwarmOptimizationView()
{
	/*
	*	判断主窗口中是否已经含有优化算法窗口。
	*	如果已经含有则将窗口置为活动。
	*	如果不含有则增加。
	*/
	auto mw = Gui::MainWindow::getInstance();
	auto views = mw->windows();
	for (auto iter = views.begin(); iter != views.end(); iter++)
	{
		auto psoView = dynamic_cast<ParticleSwarmOptimizationMDI*> (*iter);
		if (!psoView)
			continue;
		mw->setActiveWindow(psoView);
		return;
	}
	ParticleSwarmOptimizationMDI* mdi = new ParticleSwarmOptimizationMDI(this);
	mdi->init(getTextPath());
	mw->addWindow(mdi);
}

