#pragma once
#include "MDIView.h"
class CodeEditor;
class LuaEditView :public Gui::MDIView{
public:
	LuaEditView(QWidget* parent = 0);
	~LuaEditView(){};

private:
	CodeEditor *codeEditor;
};
