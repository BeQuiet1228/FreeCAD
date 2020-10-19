#pragma once
#include "MDIView.h"
#include <qaction.h>
#include <QIcon>
class CodeEditor;
class LuaEditView :public Gui::MDIView{
public:
	LuaEditView(QWidget* parent = 0);
	~LuaEditView(){};

private:
	CodeEditor *codeEditor;
};
struct SmartContorlAction
{
	QAction *actionShowEdit = nullptr;
	QAction *actionRun = nullptr;
	QAction *actionStop = nullptr;
	
	void setIcon(){
		if (actionRun == nullptr
			|| actionRun == nullptr
			|| actionStop == nullptr)
			return;
		{
			QIcon icon(QString::fromStdString(":/icons/ClassBrowser/property.png"));
			actionRun->setIcon(icon);
			actionRun->setToolTip(QString::fromStdString("samrtContorl run"));
		}
		{
			QIcon icon(QString::fromStdString(":/icons/ClassBrowser/property.png"));
			actionStop->setIcon(icon);
			actionStop->setToolTip(QString::fromStdString("samrtContorl stop"));
		}
		{
			QIcon icon(QString::fromStdString(":/icons/ClassBrowser/property.png"));
			actionShowEdit->setIcon(icon);
			actionShowEdit->setToolTip(QString::fromStdString("samrtContorl show edit"));
		}
	}
};