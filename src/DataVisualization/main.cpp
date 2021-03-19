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
int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	CanvasItem::registerMetaTye();

	std::string path = "E:/lingshiwenjianjia/MILO_C_2.h5";
	Hdf5IO io(path);
	
	io.initHdf5Data();
	auto data = io.hdf5DataList.begin();
	data +=22;
	Hdf5Data d = *data;
	std::shared_ptr<TimeData> timeData(new TimeData(d));
	TimeRenderer *timeRenderer = new TimeRenderer(timeData);
	timeRenderer->dataInit();
	timeRenderer->setDefaultRang();
	Plot p;
	std::shared_ptr<Renderer> rd(timeRenderer);
	p.setMainRenderer(rd);
	p.show();

	return a.exec();
}
