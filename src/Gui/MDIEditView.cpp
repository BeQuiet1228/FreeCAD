#include "MDIEditView.h"
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
MDIEditView::MDIEditView(DocumentPic* doc, QWidget* parent /*= 0*/)
	: MDIViewPIC(doc, parent)
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

void MDIEditView::setText(const QString& text)
{
	codeEditor->setPlainText(text);
}

bool MDIEditView::onMsg(const char* pMsg, const char** ppReturn)
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

bool MDIEditView::onHasMsg(const char* pMsg) const
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

void MDIEditView::windowStateChanged(MDIView* mdiVew)
{
	
}

bool MDIEditView::save()
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

bool MDIEditView::saveAs()
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
* @brief MDIEditView::setReadOnly ÉèÖÃ±à¼­Æ÷Ö»¶Á
* @param const bool & b
* @return void
*/
void MDIEditView::setReadOnly(const bool& b)
{
	codeEditor->setReadOnly(b);
}

Cmds MDIM3dOr2dEditorView::getM3dCmds()
{
	return codeEditor->getCmds();
}

void MDIM3dOr2dEditorView::gotoLine(const int& mun)
{
	codeEditor->gotoLine(mun);
}

MDIM3dOr2dEditorView::MDIM3dOr2dEditorView(DocumentPic* doc, QWidget* parent /*= 0*/)
	: MDIEditView(doc, parent)
{
	connect(codeEditor, SIGNAL(textChanged()), this, SLOT(textChange()));
}

void MDIM3dOr2dEditorView::textChange()
{
	auto doc = this->getAppDocument();
	QString path = QString::fromUtf8(doc->FileName.getValue());
	DocumentM3dText* doct = dynamic_cast<DocumentM3dText*>(doc);
	if (!doct)
		return;
	doct->setContent(codeEditor->toPlainText());
}

#include "moc_MDIEditView.cpp"