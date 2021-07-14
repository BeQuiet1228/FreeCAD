#include "LuaEditView.h"
#include <QFrame>
#include <QHBoxLayout>
#include "Editor/M3dEditor.h"
#include "app/Document.h"
#include "app/DocumentM3dText.h"
#include "MainWindow.h"
#include <QFileDialog>
#include <FileDialog.h>
#include <QFile>
#include <QMdiArea>
#include "Application.h"
#include "View3dMDI.h"
LuaEditView::LuaEditView(Gui::Document* doc, QWidget* parent /*= 0*/)
	: MDIView(doc, parent, 0)
{
	auto frame = new QFrame(this);
	auto layout = new QHBoxLayout();
	codeEditor = new M3dEditor();
	layout->addWidget(codeEditor);
	layout->setMargin(0);
	frame->setLayout(layout);
	layout->setSpacing(0);


	setCentralWidget(frame);
}

void LuaEditView::setText(const QString& text)
{
	codeEditor->setPlainText(text);
}

bool LuaEditView::onMsg(const char* pMsg, const char** ppReturn)
{
	if(View3dMDI::onMsgChipic(pMsg,ppReturn,getGuiDocument()))
		return true;

	if (strcmp("Undo", pMsg) == 0) {
		codeEditor->undo();
		return true;
	}
	else  if (strcmp("Redo", pMsg) == 0) {
		codeEditor->redo();
		return true;
	}
	else if (strcmp("Save", pMsg) == 0) {
		return save();
	}
	else if (strcmp("SaveAs", pMsg) == 0) {
		return saveAs();
	}else if (strcmp("SaveCopy", pMsg) == 0) {
		
		return true;
	}else if (strcmp("Copy", pMsg) == 0){
		this->codeEditor->copy();
		return true;
	}else if (strcmp("Cut", pMsg) == 0){
		this->codeEditor->cut();
		return true;
	}else if (strcmp("Paste", pMsg) == 0){
		this->codeEditor->paste();
		return true;
	}else  if (strcmp("Findm", pMsg) == 0){
		this->codeEditor->autoFindDialogPoint();
		this->codeEditor->showFindDialog();
		return true;
	}

	return false;
}

bool LuaEditView::onHasMsg(const char* pMsg) const
{
	if (View3dMDI::onHasMsgChipic(pMsg))
		return true;

	if (strcmp("Undo", pMsg) == 0) {
		return true;
	}
	else  if (strcmp("Redo", pMsg) == 0) {
		return true;
	}else if (strcmp("Save", pMsg) == 0) {
		return true;
	}else if (strcmp("SaveAs", pMsg) == 0) {
		return true;
	}else if (strcmp("SaveCopy", pMsg) == 0) {
		return true;
	}else if (strcmp("Copy", pMsg) == 0){
		return true;
	}else if (strcmp("Cut", pMsg) == 0){
		return true;
	}else if (strcmp("Paste", pMsg) == 0){
		return true;
	}else if (strcmp("Findm", pMsg) == 0){
		return true;
	}
	return false;
}

void LuaEditView::windowStateChanged(MDIView* mdiVew)
{
	
}

bool LuaEditView::save()
{
	auto doc = this->getAppDocument();
	DocumentM3dText *doct = dynamic_cast<DocumentM3dText*>(doc);
	if (!doct)
	{
		Gui::Application::Instance->activeDocument()->save();
		return true;
	}
	doct->setContent(this->codeEditor->toPlainText());
	if (doct->isSaved())
	{
		doct->save();
	}else{
		saveAs();
	}
	Gui::Application::Instance->ToSubItemTree();
	return true;
}

bool LuaEditView::saveAs()
{
	auto doc = this->getAppDocument();
	QString path = QString::fromUtf8(doc->FileName.getValue());
	DocumentM3dText *doct = dynamic_cast<DocumentM3dText*>(doc);
	if (!doct)
	{
		Gui:: Application::Instance->activeDocument()->saveAs();
		return false;
	}
		
	std::string format = doct->getFileFormat();

	QString fn = Gui::FileDialog::getSaveFileName(Gui::MainWindow::getInstance(), QObject::tr("Save  Document"),
		QString(), QString::fromLatin1("(*.%1)").arg(QString::fromStdString(format)));
	if (fn.isEmpty())
		return false;
	Base::FileInfo fi(fn.toStdString());
	doc->FileName.setValue(fn.toUtf8());
	doc->Label.setValue(fi.fileNamePure());
	doc->Uid.touch();
	setWindowTitle(QString::fromStdString(fi.fileNamePure()));
	doc->save();
	return true;
}

/**
* @brief LuaEditView::setReadOnly ÉèÖÃ±à¼­Æ÷Ö»¶Á
* @param const bool & b
* @return void
*/
void LuaEditView::setReadOnly(const bool& b)
{
	codeEditor->setReadOnly(b);
}

Cmds LuaEditView::getM3dCmds()
{
	return codeEditor->getCmds();
}

void LuaEditView::gotoLine(const int& mun)
{
	codeEditor->gotoLine(mun);
}
