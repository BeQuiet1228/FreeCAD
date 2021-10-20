#pragma once
#ifndef _WIDGET_3D_H_
#define _WIDGET_3D_H_
#include"qwidget.h"
#include"map"
//include"vtk-7.0/vtkActor.h"
#include"vtk-7.0/vtkSmartPointer.h"
#include "exPortConfig.hpp"
#include "Utility.h"
class vtkActor;
class vtkPolyData;
class vtkRenderer;
class QVTKWidget;
class QCheckBox;
class QGridLayout;
class QStandardItem;
//定义函数指针
typedef void(*fLp)(void*, bool);
class VISUALZATION3D_EXPORT Widget3D :public BaseWidget
{
	Q_OBJECT
public :
	explicit Widget3D(QWidget* parent=nullptr);
	~Widget3D();
	void transfromPolyData(__int64,vtkPolyData*);
	void setRenderProper();
	void setFunction(void*lp, fLp);
	void clearItem(TreeItem* lp);
protected:
	void initUi();
	virtual void resizeEvent(QResizeEvent*);
public slots:
	void slotitemStateChange(QStandardItem*);
private:
	std::map<QStandardItem*, vtkSmartPointer<vtkActor>>actorS;
	vtkSmartPointer<vtkRenderer> render;
	QVTKWidget* mVtkWidget;
	fLp mflp;
	void* dataMPtr;
};
#endif