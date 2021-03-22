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

	//测试单线程渲染
	std::shared_ptr<Renderer> re(timeRenderer);
	RenderTask task(re);
	
	RenderThreadManager ma;
	ma.addTask(task);
	task.rank = 3;
	ma.addTask(task);
	task.rank = 2;
	ma.addTask(task);
	ma.start();

	//刻度组件测试
	//Axis w;
	//w.setAxixStyle(AxisRight);
	//w.setAxisRange(20, 700);
	//w.SetAxisNumber(10);
	//w.AxisCanvans(QSizeF(500, 500));
	//w.setAxisText("XX(s)", 20);
	//w.AxisResize(true);
	//w._update();
	//w.show();

	//Axis m;
	//m.setAxixStyle(Axisleft);
	//m.setAxisRange(20, 700);
	//m.SetAxisNumber(10);
	//m.AxisCanvans(QSizeF(500, 500));
	//m.setAxisText("XX(s)", 20);
	//m.AxisResize(true);
	//m._update();
	//m.show();

	//Axis n;
	//n.setAxixStyle(AxisTop);
	//n.setAxisRange(20, 700);
	//n.SetAxisNumber(10);
	//n.AxisCanvans(QSizeF(500, 500));
	//n.setAxisText("XX(s)", 20);
	//n.AxisResize(true);
	//n._update();
	//n.show();

	//Axis s;
	//s.setAxixStyle(AxisBottom);
	//s.setAxisRange(20, 700);
	//s.SetAxisNumber(10);
	//s.AxisCanvans(QSizeF(500, 500));
	//s.setAxisText("XX(s)", 20);
	//s.AxisResize(true);
	//s._update();
	//s.show();
	return a.exec();
}
