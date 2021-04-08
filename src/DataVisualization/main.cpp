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
#include "InterSpaceData.h"
#include "InterspaceRender.h"
#include <qwt/qwt_plot.h>
#include "ContourData.h"
#include <qwt/qwt_plot_spectrogram.h>
#include <qwt/qwt_color_map.h>
#include "qwt/qwt_scale_widget.h"
#include "ContourRender.h"

int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	CanvasItem::registerMetaTye();

	//std::string path = "E:/lingshiwenjianjia/MILO_C/MILO_C.h5";
	std::string path = "D:\RBWO_CY.h5";
	//std::string path = "D:\MILO_P.h5";
	//std::string path = "E:/tt/TEST.h5";
	Hdf5IO io(path);
	
	io.initHdf5Data();
	auto data = io.hdf5DataList.begin();
	data +=35;
	//data += 99;
	Hdf5Data d = *data;

#if 0



	ContourData *contour = new ContourData(d);
	contour->loadPoint();

	QwtPlotSpectrogram *spec = new QwtPlotSpectrogram;
	auto rasterData = contour->getQwtMatrixRasterData();
	spec->setData(rasterData);
	rasterData->setResampleMode(QwtMatrixRasterData::BilinearInterpolation);

	spec->setRenderThreadCount(0);
	spec->setColorMap(new ColorMap);
	spec->setDisplayMode(QwtPlotSpectrogram::ContourMode,true);

	QwtPlot plot;
	spec->attach(&plot);


	const QwtInterval zInterval = rasterData->interval(Qt::ZAxis);
	// A color bar on the right axis
	QwtScaleWidget *rightAxis = plot.axisWidget(QwtPlot::yRight);
	rightAxis->setColorBarEnabled(true);
	rightAxis->setColorBarWidth(40);
	rightAxis->setColorMap(zInterval, new ColorMap());

	plot.setAxisScale(QwtPlot::yRight, zInterval.minValue(), zInterval.maxValue());
	plot.enableAxis(QwtPlot::yRight);

	plot.show();

#endif // DEBUG
	


	std::shared_ptr<ContourData> particleData(new ContourData(d));


	ContourRender *timeRenderer = new ContourRender(particleData);
	timeRenderer->dataInit();
	timeRenderer->setDefaultRang();
	//timeRenderer->setDisplayMode(QwtPlotSpectrogram::ContourMode,true);
	Plot p;
	std::shared_ptr<Renderer> rd(timeRenderer);
	p.setMainRenderer(rd);
	//p.resize(800,600);
	p.showMaximized(); 



	////测试单线程渲染
	//std::shared_ptr<Renderer> re(timeRenderer);
	//RenderTask task(re);
	//
	//RenderThreadManager ma;
	//ma.addTask(task);
	//task.rank = 3;
	//ma.addTask(task);
	//task.rank = 2;
	//ma.addTask(task);
	//ma.start();

	//刻度组件测试
	//Axis w;
	//以下都为省却，有初始化参数
	//m.setAxixStyle(Axisleft);
	//m.setAxisRange(20, 700);
	//m.SetAxisNumber(10);
	//m.setAxisText("XX(s)", 20);
	//w.show();
	
	//Axis m;
	//m.setAxixStyle(Axisleft);
	
	
	//m.AxisCanvans(QSizeF(500, 500));
	
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
