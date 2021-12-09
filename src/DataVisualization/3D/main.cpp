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
#include "DataVisualization/ContourData.h"
#include "ContourDataSetConstructor.h"
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
#if 0
	auto iter = datalist.begin();
	//结构图 
	for (; iter != datalist.end(); iter++)
	{
		if (iter->name == "struct")
			break;
	}
	if (iter == datalist.end())
		return 0;
#endif
#if 1
	//等位图
	std::vector<Hdf5Data> contourlist;
	for (auto i : datalist)
	{
		if (i.name.find("CONTOUR") != std::string::npos)
		{
			contourlist.push_back(i);
		}
	}
	auto iter = contourlist.begin();
#endif
	Widget3D* w3d = new Widget3D();

	ControlerFactory controlerFactor;
	auto controler = controlerFactor.CreatControler(*iter);



	w3d->binding(controler.get());
	w3d->show();

	return a.exec();
}
