#include <qwidget.h>
#include <QApplication>
#include "Plot.h"
#include <HDF5Reader/hdf5io.h>
#include <memory>
#include "TimeData.h"
#include "structureData.h"
#include "TimeRenderer.h"
#include "StructRenderer.h"
#include <Canvas.h>
#include "RenderTask.h"
#include "RenderThreadManager.h"
#include"Axis.h"
int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    CanvasItem::registerMetaTye();
    std::string path = "F:\wdtproject\PICGUI\MILO_C_2.h5";
    Hdf5IO io(path);
	
	io.initHdf5Data();
	auto data = io.hdf5DataList.begin();
	Hdf5Data d = *data;
	
	std::shared_ptr<structureData> _structData(new structureData(d));
	
	StructureRenderer* structureRenderer = new StructureRenderer(_structData);
	structureRenderer->dataInit();
	structureRenderer->setDefaultRang();

    Plot p;
	std::shared_ptr<Renderer> rd(structureRenderer);
    p.setMainRenderer(rd);
    p.show();

    return a.exec();
}
