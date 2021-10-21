#include "Widget3DFactory.h"
#include <QWidget>
#include "DataProcess.h"
Widget3DFactory::Widget3DFactory() {
	structWidget = nullptr;
}
Widget3DFactory::~Widget3DFactory() {
}

/**
* @brief Widget3DFactory::creat3DWidget 创建窗口指针
* @param Hdf5Data & data h5数据
* @return std::shared_ptr<QT_NAMESPACE::QWidget>
*/
QWidget* Widget3DFactory::creat3DWidget(Hdf5Data& data)
{
	if (nullptr != structWidget)
		return structWidget;
	DataProcess mDataProcess;
	bool ok = mDataProcess.initData(data);
	if (!ok)
	{
		return nullptr;
	}
	structWidget = mDataProcess.getWidget();
	return structWidget;
}