#include "LuaEditView.h"
#include <QFrame>
#include <QHBoxLayout>
#include "SmartContorl/codeEdit/codeeditor.h"
LuaEditView::LuaEditView(QWidget* parent)
	: MDIView(0, parent, 0)
{
	auto frame = new QFrame(this);
	auto layout = new QHBoxLayout();
	codeEditor = new CodeEditor();
	layout->addWidget(codeEditor);
	frame->setLayout(layout);
	setCentralWidget(frame);
}
