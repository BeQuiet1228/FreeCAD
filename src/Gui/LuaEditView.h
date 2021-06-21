#pragma once
#include "MDIView.h"
#include <qaction.h>
#include <QIcon>
#include "Document.h"
#include "Editor/M3dEditor.h"
class LuaEditView :public Gui::MDIView{
public:
	LuaEditView(Gui::Document* doc,QWidget* parent = 0);
	~LuaEditView(){};
	
	void setText(const QString& text);

	//接收窗口消息
	bool onMsg(const char* pMsg, const char** ppReturn) override;
	bool onHasMsg(const char* pMsg) const override;

	void windowStateChanged(MDIView* mdiVew);

	//响应保存函数
	bool save();
	bool saveAs();

	//设置编辑器只读
	void setReadOnly(const bool& b);

	//获取编辑器中的命令
	Cmds getM3dCmds();
	//跳转到指定行
	void gotoLine(const int& mun);
private:
	M3dEditor*codeEditor;
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