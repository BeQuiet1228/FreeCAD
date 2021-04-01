#include <qwidget.h>
#include <QApplication>
#include "Plot.h"
#include <HDF5Reader/hdf5io.h>
#include <memory>
#include "TimeData.h"
#include "TimeRenderer.h"
#include <Canvas.h>
#include "RenderTask.h"
#include "RenderThreadManager.h"
#include"Axis.h"
#include "ParticleData.h"
#include <ParticleRenderer.h>
#include "StructRenderer.h"
#include "structureData.h"
int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	CanvasItem::registerMetaTye();
	//std::string path = "E:/lingshiwenjianjia/MILO_C/MILO_C.h5";
	std::string path = "F:/wdtproject/PICGUI/TEMP(1).H5";
	Hdf5IO io(path);
	io.initHdf5Data();
	auto data = io.hdf5DataList.begin();
	//data += 9;
	Hdf5Data d = *data;
	std::shared_ptr<structureData> _structData(new structureData(d));
	StructureRenderer *_structRenderer = new StructureRenderer(_structData);
	_structRenderer->dataInit();
	_structRenderer->SetCoordinateDir(Coordinate_Dir::Z_R_coordinater);
	Plot p;
	std::shared_ptr<Renderer> rd(_structRenderer);
	p.setMainRenderer(rd);
	p.setFixedSize(600*3, 400*3);
	p.show();
	return a.exec();
}
