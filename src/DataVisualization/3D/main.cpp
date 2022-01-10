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
#include "controlerItemFactor.h"
#include "DataVisualization/ContourData.h"
#include "ContourDataSetConstructor.h"
#include "vtkOutputWindow.h"
#ifndef INIT_VTK_OPENGL_AND_FRNT	//防止多次初始化模块
#define INIT_VTK_OPENGL_AND_FRNT
#include <vtkAutoInit.h>
VTK_MODULE_INIT(vtkRenderingOpenGL2)   //初始化opengl渲染器
VTK_MODULE_INIT(vtkRenderingFreeType)   //初始化字体渲染器
VTK_MODULE_INIT(vtkInteractionStyle)
#endif //INIT_VTK_OPENGL_AND_FRNT
#include "Vector3dConfigWidget.h"
#include "Contour3dConfigWidget.h"
using namespace DV3D;

int main(int argc, char* argv[])
{
	//vtkOutputWindow::SetGlobalWarningDisplay(0);
	QApplication a(argc, argv);
#if 0
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
#if 1
	if (datalist.size() == 0)
		return 0;
	auto iter = datalist.begin();
	for (; iter != datalist.end(); iter++)
	{
		if(iter->name=="struct")
			break;
	}
	Widget3D* w3d = new Widget3D();
	ControlerFactory controlerFactor;
	//auto controler = controlerFactor.CreatParticle3dControler(paticle3d);
	auto structControler = controlerFactor.CreatStrucControler(*iter);
	//auto contourControler = controlerFactor.CreatContourControler(*iter);
	//auto contour3dContrler = controlerFactor.CreatContour3dControler(*(iter));
	//w3d->binding(controler.get());
	w3d->binding(structControler.get());
	//w3d->binding(contourControler.get());
	//w3d->binding(contour3dContrler.get());
	w3d->show();

	auto item = ControlerItemFactor::CreatContour3dControlerItem();
	item->setControler(structControler);
	item->show();
#endif
#if 0
	auto iter = datalist.begin();
	ControlerFactory controlerFactory;
	auto vector3dContrler = controlerFactory.CreatVector3dControler(*(iter+1));
	auto structControler = controlerFactory.CreatStrucControler(*datalist.begin());
	Widget3D* w3d = new Widget3D();
	w3d->binding(vector3dContrler.get());
	w3d->binding(structControler.get());
	w3d->show();
	auto item = ControlerItemFactor::CreatContour3dControlerItem();
	item->setControler(structControler);
	item->show();
#endif
#endif
	//Vector3dConfigWidget* vector3dconfigwidget = new Vector3dConfigWidget();
	//vector3dconfigwidget->show();
	//Contour3dConfigWidget* contour3dconfigwidget = new Contour3dConfigWidget();
	//contour3dconfigwidget->show();
	return a.exec();
}
