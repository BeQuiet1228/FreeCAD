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
#include "qwt/qwt_scale_widget.h"
#include "qwt/qwt_scale_engine.h"
#include "ContourRenderPolar.h"
#include "ContourDataPolar.h"
#include "RendererFactory.h"
#include "Dataresource.h"
#include "ListTreeWidget.h"
int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	CanvasItem::registerMetaTye();
	ListTreeWidget m_tree;
	DataSourceManage dataMannage;
	a.connect(&dataMannage, SIGNAL(_loadhdflist(std::vector<Hdf5Data>)), &m_tree, SLOT(loadHdflist(std::vector<Hdf5Data>)));
	a.connect(&m_tree, SIGNAL(_transfromRenderer(std::string, Hdf5Data)), &dataMannage, SLOT(tranfromRenderer(std::string, Hdf5Data)));
	std::string path = "D:/MILO_P.h5";
	dataMannage.init();
	dataMannage.loadhdffile(path);
	m_tree.resize(400,300);
	m_tree.show();
	//std::string path = "E:/lingshiwenjianjia/MILO_C/MILO_C.h5";
	//std::string path = "D:\RBWO_CY.h5";
	//std::string path = "D:\MILO_P.h5";
	//std::string path = "E:/tt/TEST.h5";
	//std::string path = "D:/MILO_P.h5";
	//Hdf5IO io(path);
	//
	//io.initHdf5Data();
	//auto data = io.hdf5DataList.begin();
	////data +=35;
	////data += 752;
	//Hdf5Data d = *data;

	//Hdf5Data d = *data;
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

	//RendererPtr rd = RendererFactory::creatStructRender(d,R_Z);
	//
	//rd->dataInit();
	//rd->setDefaultRang();
	//Plot p;
	//p.setMainRenderer(rd);
	////p.setAxisRightEnabled(true);
	//p.resize(800, 600);
	////p.showMaximized();
	////p.renderFinished();
	//p.show();
	return a.exec();
}
