#pragma once
#ifndef _WIDGET_3D_H_
#define _WIDGET_3D_H_
#include"qwidget.h"
#include"map"
//include"vtk-7.0/vtkActor.h"
#include"vtk-7.0/vtkSmartPointer.h"
#include "exPortConfig.hpp"
class vtkActor;
class vtkPolyData;
class vtkRenderer;
class QVTKWidget;
class QCheckBox;
class QGridLayout;
//定义函数指针
typedef void(*fLp)(void*, bool);
class VISUALZATION3D_EXPORT Widget3D :public QWidget
{
	Q_OBJECT
public :
	explicit Widget3D(QWidget* parent=nullptr);
	~Widget3D();
	void transfromPolyData(__int64,vtkPolyData*);
	void Updata();
	void drawImage();
	void setFunction(void*lp, fLp);
protected:
	void initUi();
	virtual void resizeEvent(QResizeEvent*);
protected slots:
	void slotStateChanged(int);
private:
	std::map<__int64, vtkSmartPointer<vtkActor>>actorS;
	vtkSmartPointer<vtkRenderer> render;
	std::map<__int64, QCheckBox*> checks;
	QVTKWidget* mVtkWidget;
	QWidget* subwidget;
	QGridLayout* layout;
	fLp mflp;
	void* dataMPtr;
};
#endif