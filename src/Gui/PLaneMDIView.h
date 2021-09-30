#pragma once
#ifndef _PLANMDIVIEW_H_
#define _PLANMDIVIEW_H_
#include"PreCompiled.h"
#include"MDIEditView.h"
#include<boost/shared_ptr.hpp>
#include<boost/signal.hpp>
#include <boost/signals2.hpp>
class QWidget;
namespace Gui {
	class GuiExport PlanMDIView :public MDIView
	{
		Q_OBJECT
			TYPESYSTEM_HEADER();
	public:
		PlanMDIView(DocumentPic *_doc,QWidget* parent=0);
		~PlanMDIView();
		void setWidget(std::shared_ptr<QWidget>&);
	protected:
		void resizeEvent(QResizeEvent*);
	private:
		__int64 lastptr;
		std::shared_ptr<QWidget> mwidget3D;
	};
}
#endif