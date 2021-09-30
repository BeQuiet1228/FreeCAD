#include "Widget3DFactory.h"
#include <QWidget>
#include "DataProcess.h"
Widget3DFactory::Widget3DFactory() {
}
Widget3DFactory::~Widget3DFactory() {
}
std::shared_ptr<QWidget> Widget3DFactory::creat3DWidget(Hdf5Data& data)
{
	DataProcess mDataProcess;
	bool ok = mDataProcess.initData(data);
	if (!ok)
	{
		return nullptr;
	}
	return mDataProcess.getWidget();
}