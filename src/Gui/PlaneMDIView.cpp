#include"PreCompiled.h"
#include"PlaneMDIView.h"
TYPESYSTEM_SOURCE_ABSTRACT(Gui::PlanMDIView, Gui::MDIView);
namespace Gui {
	PlanMDIView::PlanMDIView(DocumentPic* _doc, QWidget* parent):MDIView(_doc,parent)
	{
		lastptr = 0;
		mwidget3D = nullptr;
	}
	PlanMDIView::~PlanMDIView()
	{

	}
	void PlanMDIView::setWidget(std::shared_ptr<QWidget>& wid3D)
	{
		unsigned __int64 curPtr =reinterpret_cast<unsigned __int64>(wid3D.get());
		if (lastptr != curPtr)
		{
			if (nullptr != mwidget3D)
			{
				mwidget3D->setParent(nullptr);
				mwidget3D->hide();
			}
			wid3D->setParent(this);
			mwidget3D = wid3D;
			setCentralWidget(mwidget3D.get());
			/*mwidget3D = wid3D;
			mwidget3D->resize(this->size());
			mwidget3D->move(QPoint(0, 0));
			mwidget3D->show();*/
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