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
#include "CustomConfig.h"
#include "StructData.h"
#include "StructRender.h"
int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	CanvasItem::registerMetaTye();
	std::string path = "D:/MILO_P.h5";
	Hdf5IO io(path);
	io.initHdf5Data();
	Hdf5Data data = *(io.hdf5DataList.begin());
	std::shared_ptr<StructData> _StructData(new StructData(data,R_Z));
	StructRender* _StructRender = new StructRender(_StructData);
	std::shared_ptr<StructRender> rd(_StructRender);
	Plot p;
	p.setMainRenderer(rd);
	p.show();
	return a.exec();
}
