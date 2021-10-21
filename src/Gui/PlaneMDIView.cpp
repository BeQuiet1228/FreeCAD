#include"PreCompiled.h"
#include"PlaneMDIView.h"
//#include"VisualizationOf3D/Widget3D.h"
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
	}
	PlanMDIView::~PlanMDIView()
	{
	}
	/**
	* @brief Gui::PlanMDIView::setWidget 设置子窗口
	* @param QWidget * wid3D
	* @return void
	*/
	void PlanMDIView::setWidget(QWidget* wid3D)
	{
		if (nullptr == wid3D)
			return;
		//使用__int64类型来存储当前的指针地址。
		unsigned __int64 curPtr = reinterpret_cast<unsigned __int64>(wid3D);
		//与之前的地址进行对比,如果不同，则是新的窗口传了进来。
		if (lastptr != curPtr)
		{
			if (0 != lastptr)
			{
				//执行析构之前的窗口的操作。
				QWidget* lastWidget = reinterpret_cast<QWidget*>(lastWidget);
				lastWidget->setParent(nullptr);
				delete lastWidget;
			}
			//执行当前窗口操作为子窗口
			wid3D->setParent(this);
			setCentralWidget(wid3D);
			//记录当前指针的地址
			lastptr = curPtr;
		}
	}
};
#include"moc_PlaneMDIView.cpp"