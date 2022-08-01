#pragma once
#include "MDIView.h"
#include <qaction.h>
#include <QIcon>
#include "Document.h"
#include "Editor/M3dEditor.h"
#include <QObject>
#include "DocumentPic.h"
//为mdiview添加一个获取documentpic对象的接口

class MDIViewPIC :public Gui::MDIView{
public:
	MDIViewPIC(DocumentPic* doc, QWidget* parent = 0)
		:MDIView(doc, parent) {
	};
	~MDIViewPIC() = default;

public:
	DocumentPic* getDocumengPic() const{
		auto doc = getGuiDocument();
		auto docPic = dynamic_cast<DocumentPic*>(doc);
		if (!docPic)
			return nullptr;
		return docPic;
	};
};

class MDIEditView :public MDIViewPIC{
public:
	MDIEditView(DocumentPic* doc,QWidget* parent = 0);
	MDIEditView(DocumentPic* doc, CodeEditor* editor,QWidget* parent = 0);
	~MDIEditView() {}; //这里qobject会自动释放掉指针 可以不管(仅对继承qobject且设置parent的对象有效)
	
	void setText(const QString& text);

	//接收窗口消息
	bool onMsg(const char* pMsg, const char** ppReturn) override;
	bool onHasMsg(const char* pMsg) const override;

	void windowStateChanged(MDIView* mdiVew);
	//设置编辑器只读
	void setReadOnly(const bool& b);

protected:
	CodeEditor* codeEditor;
};

class MDIM3dOr2dEditorView :public MDIEditView {
	Q_OBJECT
public:
	MDIM3dOr2dEditorView(DocumentPic* doc, QWidget* parent = 0);
	~MDIM3dOr2dEditorView() {};

public Q_SLOTS:
	void textChange();

public:
	//获取编辑器中的命令
	Cmds getM3dCmds();
	//跳转到指定行
	void gotoLine(const int& mun);
private:
	M3dEditor* m3dEditor;
};

class LogView :public MDIEditView {
public:
	LogView(DocumentPic* doc, QWidget* parent = 0);
	~LogView();

public:
	void setText(const QString& text);

};