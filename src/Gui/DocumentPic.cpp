#include "PreCompiled.h"
#include "DocumentPic.h"
#include <iostream>
#include "MDIEditView.h"
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
#include "app/DocumentM3dText.h"
#include <FileDialog.h>
#include "MDIView.h"
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
		MDIEditView* edit = new MDIM3dOr2dEditorView(this);
		auto mainWindow = Gui::MainWindow::getInstance();
		mainWindow->addWindow(edit);
	}
	else if (appDoc->classID == 5) {
		Gui::PlotMDIView* plot = new Gui::PlotMDIView(this);
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
	auto mw = Gui::MainWindow::getInstance();
	auto view = mw->windows();

	for (auto iter = view.begin(); iter != view.end(); iter++)
	{
		auto plot = dynamic_cast<Gui::PlotMDIView*>(*iter);
		if (plot)
		{
			mw->removeWindow(plot);
		}
			
	}

	auto doc = getAppDocument();
	if (doc == nullptr)
		return;

	auto dataDoc = dynamic_cast<DocumentManager*>(doc);
	if (!dataDoc)
		return;


	dataDoc->dataclear();
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
	Gui::TreeViewCtrl* mlisttreewidget =(Gui::MainWindow::getInstance()->mTreeWidget);
	if (!mlisttreewidget)
	{
		std::cerr << "ListTreeWidget is nullptr from Gui void DocumentPic::openH5File(const std::string& path)" << std::endl;
		return;
	}
	docm->loadFile(path);
	mlisttreewidget->loadHdflist(docm->gethdf5dataList());
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
	if (!control->hasChipicRuning())
	{
		//设置主界面上的ui
		mw->setContorlUI();
		//设置运行路
		control->setM3dPath(getTextPath());
		//清空h5文件对象
		this->releaseH5Object();
	}
	else {
		//设置主界面上的ui
		mw->hideContorlUI();
		this->releaseH5Object();
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
	this->releaseH5Object();
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
	auto views = this->getMDIViews();
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

void DocumentPic::showProcessingBatchView()
{
	auto mw = Gui::MainWindow::getInstance();
	auto views = this->getMDIViews();
	for (auto iter = views.begin(); iter != views.end(); iter++)
	{
		auto psoView = dynamic_cast<ProcessingBatchView*> (*iter);
		if (!psoView)
			continue;
		mw->setActiveWindow(psoView);
		return;
	}
	ProcessingBatchView* mdi = new ProcessingBatchView(this);
	mdi->init(getTextPath());
	mw->addWindow(mdi);
}

void DocumentPic::save()
{
	Document::save();
}

void DocumentPic::saveAs()
{
	Document::saveAs();
}

bool DocumentPic::onMsg(const char* pMsg, const char** ppReturn)
{
	if (strcmp("Save", pMsg) == 0) {
		this->save();
		return true;
	}
	else if (strcmp("SaveAs", pMsg) == 0) {
		this->saveAs();
		return true;
	}else if (strcmp("RunChipic", pMsg) == 0) {
		this->runChipic();
		return true;
	}
	else if (strcmp("StopChipic", pMsg) == 0) {
		this->stopChipic();
		return true;
	}
	else if (strcmp("ParalleRunChipic", pMsg) == 0) {
		this->paralleRunChipic();
		return true;
	}
	else if (strcmp("showPSOView", pMsg) == 0) {
		this->showParticleSwarmOptimizationView();
		return true;
	}
	else if (strcmp("showProcessingBatchView", pMsg) == 0) {
		this->showProcessingBatchView();
		return true;
	}

	return false;
}

bool DocumentPic::onHasMsg(const char* pMsg) const
{
	if (strcmp("Save", pMsg) == 0) {
		return true;
	}
	else if (strcmp("SaveAs", pMsg) == 0) {
		return true;
	}else if (strcmp("RunChipic", pMsg) == 0) {
		auto control = ContorlInterface::GetInstance();
		if (control->hasAutoChipicRuning())
			return false;
		return true;
	}
	else if (strcmp("ParalleRunChipic", pMsg) == 0) {
		auto control = ContorlInterface::GetInstance();
		if (control->hasChipicRuning())
			return false;
		return true;
	}
	else if (strcmp("showPSOView", pMsg) == 0) {
		auto control = ContorlInterface::GetInstance();
		if (control->hasChipicRuning())
			return false;
		return true;
	}
	else if (strcmp("showProcessingBatchView", pMsg) == 0) {
		auto control = ContorlInterface::GetInstance();
		if (control->hasChipicRuning())
			return false;
		return true;
	}
	return false;
}

DocumentText::DocumentText(App::Document* pcDocument, Gui::Application* app)
	:DocumentPic(pcDocument,app)
{

}

void DocumentText::save()
{
	auto doc = this->getAppDocument();
	DocumentM3dText* doct = dynamic_cast<DocumentM3dText*>(doc);
	if (!doct)
		return;

	if (doct->isSaved())
	{
		doct->save();
	}else {
		saveAs();
	}
	Gui::Application::Instance->ToSubItemTree();
}

void DocumentText::saveAs()
{
	auto doc = this->getAppDocument();
	QString path = QString::fromUtf8(doc->FileName.getValue());
	DocumentM3dText* doct = dynamic_cast<DocumentM3dText*>(doc);
	if (!doct)
		return;

	std::string format = doct->getFileFormat();

	QString fn = Gui::FileDialog::getSaveFileName(Gui::MainWindow::getInstance(), QObject::tr("Save  Document"),
		QString(), QString::fromLatin1("(*.%1)").arg(QString::fromStdString(format)));
	if (fn.isEmpty())
		return;
	Base::FileInfo fi(fn.toStdString());
	doc->FileName.setValue(fn.toUtf8());
	doc->Label.setValue(fi.fileNamePure());
	doc->Uid.touch();
	
	//修改所有窗口的标题
	auto views = getMDIViews();
	for (auto iter = views.begin(); iter != views.end(); iter++)
	{
		(*iter)->setWindowTitle(QString::fromStdString(fi.fileNamePure()));
	}

	doc->save();
}

void DocumentText::initMDIView()
{

	MDIEditView* edit = new MDIM3dOr2dEditorView(this);
	auto mainWindow = Gui::MainWindow::getInstance();
	mainWindow->addWindow(edit);
}

DocumentPic* CreatePICDocument(App::Document* doc, Gui::Application* app)
{
	//判断是否为文本编辑器工程，如果是那么不显示3D视窗
	if (doc->classID == 1 || doc->classID == 4 )
	{
		return new DocumentText(doc,app);
	}else if (doc->classID == 5) {
		return new DocumentH5File(doc, app);
	}else {
		return new DocumentPic(doc, app);
	}
}

DocumentH5File::DocumentH5File(App::Document* pcDocument, Gui::Application* app)
	:DocumentPic(pcDocument,app)
{

}

bool DocumentH5File::onHasMsg(const char* pMsg) const
{
	return false;
}
