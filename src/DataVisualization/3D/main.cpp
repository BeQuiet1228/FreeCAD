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
#include <vtkCellData.h>

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
	auto data = datalist.begin();

	CartesianStructDataSetConstructor constructor;
	constructor.setHdf5Data(*data);

	std::shared_ptr<CartesianStructActorPipeline> pipeLine(new CartesianStructActorPipeline);
	pipeLine->setDataSet(constructor.creatDataset());
	pipeLine->connect();

	Widget3D* w3d = new Widget3D();
	Controler* controler = new Controler();
	controler->setActorPipeline(pipeLine);
	controler->setVisible(true);
	w3d->binding(controler);
	w3d->show();

	return a.exec();
}
