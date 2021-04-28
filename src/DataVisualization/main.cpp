#include <qwidget.h>
#include <QApplication>
#include "Canvas.h"
#include "HDF5Reader/hdf5io.h"
#include "Plot.h"
#include "StructRender.h"
#include "StructData.h"
#include "Dataresource.h"
#include "ListTreeWidget.h"
#include "ConfigWidget.h"
int main(int argc, char *argv[])
{
	QApplication a(argc, argv);
	CanvasItem::registerMetaTye();
#if 1
	std::string path = "D:/MILO_P.h5";
	Plot p;
	DataSourceManage manager;
	ListTreeWidget treectrl;
	manager.init(&treectrl, &p);
	manager.loadhdffile(path);
	p.show();
	treectrl.show();
	ConfigWidget m_configwidget;
	m_configwidget.show();
#endif
	return a.exec();
}
