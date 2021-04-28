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
<<<<<<< .mine












=======
	auto cg = Config::GetInstance();
	auto group = cg->getRootGroup();
	group.setSetting("value", "test3");
	auto group1 = group.getGroup("group");
	group1.addSetting("config", "ttt");
#endif
	
#if 0
	//std::string path = "E:/lingshiwenjianjia/MILO_C/MILO_C.h5";
	//std::string path = "D:\RBWO_CY.h5";
	//std::string path = "D:\MILO_P.h5";
	//std::string path = "E:/tt/TEST.h5";
>>>>>>> .theirs
	std::string path = "D:/MILO_P.h5";
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
