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
	auto data = io.hdf5DataList.end();
	data--;
	Hdf5Data d = *data;
	std::shared_ptr<TimeData> timeData(new TimeData(d));
	TimeRenderer *timeRenderer = new TimeRenderer(timeData);
	timeData->loadSourceData();
	timeData->loadPoint();
	timeRenderer->setSize(500, 500);
	timeRenderer->setXRang(timeData->getXRang());
	timeRenderer->setYRang(timeData->getYRang());
	timeRenderer->drawPixmap();

	Plot p;
	CanvasItem item;
	item.setPixmap(timeRenderer->getPixmap(),QPoint(0,0));
	p.addCanvasItem(item);
	p.show();

	//≤‚ ‘µ•œﬂ≥Ã‰÷»æ
	std::shared_ptr<Renderer> re(timeRenderer);
	RenderTask task(re);
	
	RenderThreadManager ma;
	ma.addTask(task);
	task.rank = 3;
	ma.addTask(task);
	task.rank = 2;
	ma.addTask(task);
	ma.start();

	return a.exec();
}
