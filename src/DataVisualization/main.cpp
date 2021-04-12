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
#include"phasorData.h"
#include "phasorRenderer.h"
#include "ContourRender.h"
#include "structureData.h"
#include "StructRenderer.h"
#include "Struct2dData.h"
#include"Struct2DRenderer.h"

int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	CanvasItem::registerMetaTye();
	//std::string path = "D:\\MILO_C_2.h5";
	std::string path = "D:\\wandaotongProject\\TEMP2.H5";
	Hdf5IO io(path);
	
	io.initHdf5Data();
	auto data = io.hdf5DataList.begin();
	//data +=816;
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
	


	//std::shared_ptr<ContourData> particleData(new ContourData(d));
	//ContourRender *timeRenderer = new ContourRender(particleData);
	//timeRenderer->dataInit();
	//timeRenderer->setDefaultRang();
	////timeRenderer->setDisplayMode(QwtPlotSpectrogram::ContourMode,true);
	//Plot p;
	//std::shared_ptr<Renderer> rd(timeRenderer);
	//p.setMainRenderer(rd);
	////p.resize(800,600);
	//p.showMaximized(); 
	
	//矢量图测试
	//std::shared_ptr<phasorData> _phasorData(new phasorData(d));
	//phasorRenderer *_phasorRenderer = new phasorRenderer(_phasorData);
	//_phasorRenderer->dataInit();
	//_phasorRenderer->setDefaultRang();
	//Plot p;
	//std::shared_ptr<Renderer> rd(_phasorRenderer);
	//p.setMainRenderer(rd);
	//p.showMaximized();

	//结构图测试
	//std::shared_ptr<structureData> _structdata(new structureData(d));
	//StructureRenderer* _StructureRenderer = new StructureRenderer(_structdata);
	//_StructureRenderer->dataInit();
	//_StructureRenderer->SetCoordinateDir(Coordinate_Dir::cylindrical_coordinate);
	//_StructureRenderer->setDefaultRang();
	//
	//Plot p;
	//std::shared_ptr<Renderer> rd(_StructureRenderer);
	//p.setMainRenderer(rd);
	//p.showMaximized();

	//2维结构图测试
	std::shared_ptr<Struct2dData> _Struct2dData(new Struct2dData(d));
	Struct2DRenderer* _Struct2DRenderer = new Struct2DRenderer(_Struct2dData);
	_Struct2DRenderer->dataInit();
	_Struct2DRenderer->setDefaultRang();

	Plot p;
	std::shared_ptr<Renderer> rd(_Struct2DRenderer);
	p.setMainRenderer(rd);
	p.showMaximized();

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
