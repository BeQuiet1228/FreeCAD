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

MDIEditView::MDIEditView(DocumentPic* doc, CodeEditor* editor, QWidget* parent /*= 0*/)
	: MDIViewPIC(doc, parent)
{
	auto frame = new QFrame(this);
	auto layout = new QHBoxLayout();
	codeEditor = editor;
	editor->setParent(this);
	layout->addWidget(editor);
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
	if (strcmp("Undo", pMsg) == 0) {
		codeEditor->undo();
		return true;
	}
	else  if (strcmp("Redo", pMsg) == 0) {
		codeEditor->redo();
		return true;
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

	return getDocumengPic()->onMsg(pMsg, ppReturn);
}

bool MDIEditView::onHasMsg(const char* pMsg) const
{
	if (strcmp("Undo", pMsg) == 0) {
		return true;
	}
	else  if (strcmp("Redo", pMsg) == 0) {
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
	return getDocumengPic()->onHasMsg(pMsg);
}

void MDIEditView::windowStateChanged(MDIView* mdiVew)
{
	
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
	return m3dEditor->getCmds();
}

void MDIM3dOr2dEditorView::gotoLine(const int& mun)
{
	m3dEditor->gotoLine(mun);
}

MDIM3dOr2dEditorView::MDIM3dOr2dEditorView(DocumentPic* doc, QWidget* parent /*= 0*/)
	: MDIEditView(doc, parent)
{
	connect(codeEditor, SIGNAL(textChanged()), this, SLOT(textChange()));
	m3dEditor = dynamic_cast<M3dEditor*>(codeEditor);
	assert(m3dEditor);
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

LogView::LogView(DocumentPic* doc, QWidget* parent /*= 0*/)
	:MDIEditView(doc, new LogEditor(),parent)
{
	setWindowTitle(QString::fromLocal8Bit("LOG"));
}

LogView::~LogView()
{

}


void LogView::setText(const QString& text)
{	
	codeEditor->setPlainText(text);
}

#include "moc_MDIEditView.cpp"


