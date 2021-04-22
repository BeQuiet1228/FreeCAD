#include <QApplication>
#include "Canvas.h"
#include "StructData.h"
#include "StructRender.h"
#include "HDF5Reader/hdf5io.h"
#include "Plot.h"
int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	CanvasItem::registerMetaTye();
	std::string path = "D:/MILO_D(1).h5";
	//std::string path = "D:/MILO_P.h5";
	Hdf5IO io(path);
	io.initHdf5Data();
	auto hdfdata = *(io.hdf5DataList.begin());
	std::shared_ptr<StructData> _StructData(new StructData(hdfdata, X_Z));
	StructRender* _StructRender = new StructRender(_StructData);
	//_StructRender->dataInit();
	//_StructRender->setDefaultRang();
	std::shared_ptr<Renderer> rd(_StructRender);
	Plot p;
	p.setMainRenderer(rd);
	p.resize(400, 300);
	p.show();
	return a.exec();
}
