#include"PreCompiled.h"
#include"PlaneMDIView.h"
#include"VisualizationOf3D/Widget3D.h"
TYPESYSTEM_SOURCE_ABSTRACT(Gui::PlanMDIView, Gui::MDIView);
namespace Gui {
	/**
	* @brief Gui::PlanMDIView::PlanMDIView
	* @param DocumentPic * _doc
	* @param QWidget * parent
	* @return 
	*/
	
	PlanMDIView::PlanMDIView(DocumentPic* _doc, QWidget* parent):MDIView(_doc,parent)
	{
		lastptr = 0;
		mwidget3D = nullptr;
	}
	PlanMDIView::~PlanMDIView()
	{
		/*if (nullptr != mwidget3D)
		{
			Widget3D* newWidget = dynamic_cast<Widget3D*>(mwidget3D);
			auto items = newWidget->GetTreeItems();
			auto iter = items.begin();
			auto parentItem = (*iter)->parent();
			if (nullptr != parentItem && parentItem->hasChildren() > 0)
			{
				parentItem->removeRows(0, parentItem->rowCount());
			}
		}*/
	}
	void PlanMDIView::setWidget(QWidget* wid3D)
	{
		unsigned __int64 curPtr =reinterpret_cast<unsigned __int64>(wid3D);
		if (lastptr != curPtr)
		{
			if (nullptr != mwidget3D)
			{
				mwidget3D->setParent(nullptr);
				mwidget3D->hide();
			}
			wid3D->setParent(this);
			mwidget3D = wid3D;
			setCentralWidget(mwidget3D);
			lastptr = curPtr;
		}
	}
	void PlanMDIView::resizeEvent(QResizeEvent*e)
	{
		QWidget::resizeEvent(e);
		/*if (nullptr != mwidget3D)
		{
			mwidget3D->resize(this->size());
			mwidget3D->move(QPoint(0, 0));
		}*/
	}
	//__int64 lastptr;
};
#include"moc_PlaneMDIView.cpp"