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
#include"PolarStructActorPipeline.h"
#include"CylinderPlanConstruct.h"
#include"PolarPlanConstruct.h"
#include"vtkDataSet.h"
#include"vtkProperty.h"
#include"vtkCamera.h"
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
	//打开只有k矩阵的h5文件
	//auto data = datalist.begin();
	__int32 index = -1;
	for (auto i = 0; i < datalist.size(); i++)
	{
		if (datalist[i].name.find("struct") != std::string::npos)
		{
			index = i;
			break;
		}
	}
	if (-1 == index)
		return 0;
	auto data = datalist.begin() + index;

	//CylinderStructDataSetConstructor constructor;
	//constructor.setHdf5Data(*data);
	DataSetConstructorH5* constructor;
	//测试
	switch (data->coordinateSystem)
	{
	case Hdf5Data::CoordinateSystem::POLAR:
	{
		if (data->headList[1].find("X2=2") != std::string::npos ||
			data->headList[1].find("X2=3") != std::string::npos)
			constructor = new  PolarPlanConstruct();
		else
			constructor = new PolarStructDaraSetConstruct();
	}
	break;
	case Hdf5Data::CoordinateSystem::CARTESIAN:
	{
		constructor = new CartesianStructDataSetConstructor();
	}
	break;
	case Hdf5Data::CoordinateSystem::CYLINDER:
	{
		if (data->headList[2].find("X3=2") != std::string::npos ||
			data->headList[2].find("X3=3") != std::string::npos)
			constructor = new  CylinderPlanConstruct();
		else
			constructor = new CylinderStructDataSetConstructor();
	}
	break;
	}
	constructor->setHdf5Data(*data);
	std::shared_ptr<PolarStructActorPipeline> pipeLine(new PolarStructActorPipeline);
	pipeLine->setDataSet(constructor->creatDataset());
	pipeLine->connect();

	Widget3D* w3d = new Widget3D();
	Controler* controler = new Controler();
	controler->setActorPipeline(pipeLine);
	w3d->binding(controler);
	w3d->show();

	return a.exec();
}
