#include <qwidget.h>
#include <QApplication>
#include <QVTKWidget.h>
#include <vtkRenderWindow.h>
#include <vtkRenderWidget.h>
#include <vtkRenderer.h>
#include <vtkNew.h>
#include <vtkActor.h>
#include <vtkPolyDataMapper.h>
#include <vtkSmartPointer.h>
#include "CartesianStructActorPipeline.h"
#include "CartesianStructDataSetConstructor.h"
#include "widget3D.h"
#include "controler.h"
#include <QFileDialog>
#include <HDF5Reader/hdf5io.h>
#include "CartesianStructDataSetConstructor.h"
#include"PolarStructDataSetConstructor.h"
#include"vtkDataSetMapper.h"
#include <vtkCellData.h>
#include"vtkUnstructuredGridGeometryFilter.h"
#include"CylinderStructDataSetConstructor.h"
#include"CylinderPlanConstruct.h"
#include"PolarPlanConstruct.h"
#include"vtkDataSet.h"
#include"vtkProperty.h"
#include"vtkCamera.h"
#include "ControlerItem.h"
#include "ControlerAction.h"
#include "dataSetConstructorFactory.h"
#include "ControlerFactory.h"
#ifndef INIT_VTK_OPENGL_AND_FRNT	//防止多次初始化模块
#define INIT_VTK_OPENGL_AND_FRNT
#include <vtkAutoInit.h>
VTK_MODULE_INIT(vtkRenderingOpenGL2)   //初始化opengl渲染器
VTK_MODULE_INIT(vtkRenderingFreeType)   //初始化字体渲染器
VTK_MODULE_INIT(vtkInteractionStyle)
#endif //INIT_VTK_OPENGL_AND_FRNT

using namespace DV3D;

int main(int argc, char* argv[])
{
	QApplication a(argc, argv);

	QFileDialog* fileDialog = new QFileDialog();
	fileDialog->setWindowTitle("OpenFile");
	fileDialog->setDirectory("D:/test");
	fileDialog->setFilter(("H5 Files(*.h5 *.H5)"));
	if (fileDialog->exec() != QDialog::Accepted)
		return 0;
	QString h5fFilePath = fileDialog->selectedFiles()[0];
	Hdf5IO io(h5fFilePath.toStdString());
	io.initHdf5Data();

	auto datalist = io.hdf5DataList;
	if (datalist.size() == 0)
		return 0;
	auto iter = datalist.begin();
	for (; iter != datalist.end(); iter++)
	{
		if(iter->name =="struct")
			break;
	}
	if (iter == datalist.end())
		return 0;

	
#if 0
	vtkSmartPointer<vtkUnstructuredGridGeometryFilter> filter = vtkSmartPointer<vtkUnstructuredGridGeometryFilter>::New();
	filter->SetInputData(dataset);
	filter->MergingOn();
	filter->Update();
	vtkSmartPointer<vtkDataSetMapper> ugridMapper = vtkSmartPointer<vtkDataSetMapper>::New();
//	ugridMapper->SetInputConnection(filter->GetOutputPort());
	ugridMapper->SetInputData(filter->GetOutput());
	ugridMapper->ScalarVisibilityOff();
	ugridMapper->Update();
	vtkSmartPointer<vtkActor> ugridActor = vtkSmartPointer<vtkActor>::New();
	ugridActor->SetMapper(ugridMapper);
	ugridActor->GetProperty()->EdgeVisibilityOn();
	vtkSmartPointer<vtkRenderer> renderer = vtkSmartPointer<vtkRenderer>::New();
	renderer->AddActor(ugridActor.Get());
	renderer->ResetCamera();
	renderer->GetActiveCamera()->Elevation(60.0);
	renderer->GetActiveCamera()->Azimuth(30.0);
	renderer->GetActiveCamera()->Dolly(1.2);
	vtkSmartPointer<vtkRenderWindow>renWin = vtkSmartPointer<vtkRenderWindow>::New();
	vtkSmartPointer<vtkRenderWindowInteractor>iren = vtkSmartPointer<vtkRenderWindowInteractor>::New();
	renWin->AddRenderer(renderer);
	renWin->SetSize(640, 480);
	renWin->SetWindowName("UGrid)");
	iren->SetRenderWindow(renWin);
	// interact with data
	renWin->Render();
	iren->Start();
	return a.exec();
#endif

	Widget3D* w3d = new Widget3D();

	ControlerFactory controlerFactor;
	auto controler = controlerFactor.CreatControler(*iter);



	w3d->binding(controler.get());
	w3d->show();

	return a.exec();
}
