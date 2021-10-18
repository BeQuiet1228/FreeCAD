#include<QWidget>
#include"DataProcess.h"
#include<QApplication>
#include"QFileDialog"
#include"HDF5Reader/hdf5io.h"
#include"qtextcodec.h"
//#include"vtk-7.0/vtkNew.h"
//#include"vtk-7.0/vtkNamedColors.h"
//#include"vtk-7.0/vtkRenderer.h"
//#include"vtk-7.0/vtkRenderWindow.h"
//#include"vtk-7.0/vtkCubeSource.h"
//#include"vtk-7.0/vtkPolyDataMapper.h"
//#include"vtk-7.0/vtkRenderWindowInteractor.h"
//#include"vtk-7.0/vtkActor.h"
//#include"vtk-7.0/vtkProperty.h"
//#include"vtk-7.0/vtkCamera.h"
int main(int argc, char* argv[])
{
#if 1
	QApplication a(argc, argv);
	DataProcess dataprocess;
	QFileDialog* fileDialog = new QFileDialog();
	fileDialog->setWindowTitle("OpenFile");
	fileDialog->setDirectory(".");
	fileDialog->setFilter(("H5 Files(*.h5 *.H5)"));
	if (fileDialog->exec() == QDialog::Accepted)
	{
		QString h5fFilePath = fileDialog->selectedFiles()[0];
		
		Hdf5IO io(h5fFilePath.toStdString());
		io.initHdf5Data();
		auto datalist = io.hdf5DataList;
		for (auto iter = datalist.begin(); iter != datalist.end(); iter++)
		{
			if (iter->headList.size() >= 4 && iter->headList[3].find("PLANE") != std::string::npos)
			{
				dataprocess.initData(*iter);
				break;
			}
		}
	}
	auto widget=dataprocess.getWidget();
	widget->showMaximized();
	return a.exec();
#endif

#if 0
    vtkNew<vtkNamedColors> colors;

    // Create a rendering window and renderer.
    vtkNew<vtkRenderer> ren;
    vtkNew<vtkRenderWindow> renWin;
    renWin->SetWindowName("Cube");
    renWin->AddRenderer(ren.Get());
    // Create a renderwindowinteractor
    vtkNew<vtkRenderWindowInteractor> iren;
    iren->SetRenderWindow(renWin.Get());

    // Create a cube.
    vtkNew<vtkCubeSource> cube;
    cube->Update();

    // mapper
    vtkNew<vtkPolyDataMapper> cubeMapper;
    cubeMapper->SetInputData(cube->GetOutput());

    // Actor.
    vtkNew<vtkActor> cubeActor;
    cubeActor->SetMapper(cubeMapper.Get());
    cubeActor->GetProperty()->SetColor(1.0,0.5,0.5);

    // Assign actor to the renderer.
    ren->AddActor(cubeActor.Get());

    ren->ResetCamera();
    ren->GetActiveCamera()->Azimuth(30);
    ren->GetActiveCamera()->Elevation(30);
    ren->ResetCameraClippingRange();
    ren->SetBackground(1.0,1.0,1.0);

    renWin->SetSize(300, 300);
    renWin->SetWindowName("Cube1");

    // Enable user interface interactor.
    iren->Initialize();
    renWin->Render();
    iren->Start();

#endif
}