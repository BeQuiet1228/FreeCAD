#include "LuaEditView.h"
#include <QFrame>
#include <QHBoxLayout>
#include "SmartContorl/codeEdit/codeeditor.h"
#include "app/Document.h"
#include "app/DocumentM3dText.h"
#include "MainWindow.h"
#include <QFileDialog>
#include <FileDialog.h>
#include <QFile>
LuaEditView::LuaEditView(Gui::Document* doc, QWidget* parent /*= 0*/)
	: MDIView(doc, parent, 0)
{
	auto frame = new QFrame(this);
	auto layout = new QHBoxLayout();
	codeEditor = new CodeEditor();
	layout->addWidget(codeEditor);
	frame->setLayout(layout);
	setCentralWidget(frame);
}

void LuaEditView::setText(const QString& text)
{
	codeEditor->setPlainText(text);
}

bool LuaEditView::onMsg(const char* pMsg, const char** ppReturn)
{
	if (strcmp("Undo", pMsg) == 0) {
		codeEditor->undo();
		return true;
	}
	else  if (strcmp("Redo", pMsg) == 0) {
		codeEditor->redo();
		return true;
	}
	else if (strcmp("Save", pMsg) == 0) {
		auto doc = this->getAppDocument();
		DocumentM3dText *doct = static_cast<DocumentM3dText*>(doc);
		if (!doct)
			return false;
		doct->setContent(this->codeEditor->toPlainText());
		doct->save();
		return true;
	}
	else if (strcmp("SaveAs", pMsg) == 0) {
		auto doc = this->getAppDocument();
		QString path = QString::fromUtf8(doc->FileName.getValue());
		auto format = path;
		format = format.right(3);
		QString fn = Gui::FileDialog::getSaveFileName(Gui::MainWindow::getInstance(), QObject::tr("Save  Document"),
			QString(), QString::fromLatin1("M3D (*.%1)").arg(format));
		doc->FileName.setValue(fn.toLocal8Bit());
		doc->save();
		return true;
	}
	else if (strcmp("SaveCopy", pMsg) == 0) {
		
		return true;
	}
	return false;
}

bool LuaEditView::onHasMsg(const char* pMsg) const
{
	return true;
}
