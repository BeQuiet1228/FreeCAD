#include <qwidget.h>
#include <QApplication>
#include "Canvas.h"
#include "HDF5Reader/hdf5io.h"
#include "Plot.h"
#include "StructRender.h"
#include "StructData.h"
//#include "DoubleSilder.h"
int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	CanvasItem::registerMetaTye();
#if 1
	std::string path = "D:/wandaotongProject/MILO_P.h5";
	Hdf5IO io(path);
	io.initHdf5Data();
	Hdf5Data data = *(io.hdf5DataList.begin());
	std::shared_ptr<StructData> _StructData(new StructData(data, R_Z));
	StructRender* _StructRender = new StructRender(_StructData);
	std::shared_ptr<StructRender> rd(_StructRender);
	Plot p;
	p.setMainRenderer(rd);
	p.show();
#endif
#if 0
	/*DoubleSilder b(DoubleSilder::DoubelSilderDir::HORIZONTAL);
	b.showMaximized();*/
#endif
	return a.exec();
}
