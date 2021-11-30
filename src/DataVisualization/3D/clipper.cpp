#include "clipper.h"

DV3D::Clipper::Clipper()
{
	clipperPlane = vtkSmartPointer<vtkPlane>::New();
	clipperPlane->SetOrigin(0, 0, 0);
	clipperPlane->SetNormal(-1, 0, 0);

	vtkClipper = vtkSmartPointer<vtkTableBasedClipDataSet>::New();
	vtkClipper->SetClipFunction(clipperPlane);
	vtkClipper->SetValue(0.0);
	vtkClipper->GenerateClippedOutputOn();
}

vtkAlgorithmOutput* DV3D::Clipper::getOutpuPort()
{
	return vtkClipper->GetOutputPort();
}

void DV3D::Clipper::setInputConnection(vtkAlgorithmOutput* input)
{
	vtkClipper->SetInputConnection(input);
}

void DV3D::Clipper::setInputData(vtkDataObject* data)
{
	vtkClipper->SetInputData(data);
}


void DV3D::Clipper::setClipPlane(vtkSmartPointer<vtkPlane> plane)
{
	this->clipperPlane = plane;
	this->vtkClipper->SetClipFunction(plane);
}

