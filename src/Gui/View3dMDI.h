#pragma once
#include "View3DInventor.h"
#include "Document.h"
#include <QWidget>
class View3dMDI:public Gui::View3DInventor{
public:
	View3dMDI(Gui::Document* pcDocument, QWidget* parent, const QtGLWidget* sharewidget = 0, Qt::WindowFlags wflags = 0);
	~View3dMDI();

public:
	virtual bool onMsg(const char* pMsg, const char** ppReturn);
	virtual bool onHasMsg(const char* pMsg) const;

	//处理运行与停止消息
	static bool onMsgChipic(const char* pMsg, const char** ppReturn,Gui::Document* doc);
	static bool onHasMsgChipic(const char* pMsg);
};