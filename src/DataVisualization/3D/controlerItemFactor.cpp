#include "controlerItemFactor.h"
#include "ControlerAction.h"
#include "Contour3dControlerAction.h"

DV3D::ControlerItem* DV3D::ControlerItemFactor::CreatControlerItem()
{
	ControlerItem *item = new ControlerItem();

	std::shared_ptr<ControlerClipEnable> clip(new ControlerClipEnable());
	std::shared_ptr<ControlerEdgeVisible> edge(new ControlerEdgeVisible());
	//std::shared_ptr<ControlerClipPlan> controlerClipPlan(new ControlerClipPlan());
	item->addAction(clip);
	item->addAction(edge);
	//item->addAction(controlerClipPlan);
	
	return item;
}

DV3D::ControlerItem* DV3D::ControlerItemFactor::CreatContour3dControlerItem()
{
	ControlerItem* item = CreatControlerItem();
	std::shared_ptr<ControlerContourSurface> contourSurface(new ControlerContourSurface());
	std::shared_ptr<ControlerClipPlan> controlerClipPlan(new ControlerClipPlan());
	item->addAction(contourSurface);
	item->addAction(controlerClipPlan);
	return item;
}

/**
* @brief DV3D::ControlerItemFactor::AddSaveAction 为item添加一个保存按钮
* @param ControlerItem * item item
* @param Hdf5Data & data 要保存的HDF5数据
* @param const QString & path 保存时文件浏览器打开的路径
* @return DV3D::ControlerItem* 
*/
DV3D::ControlerItem* DV3D::ControlerItemFactor::AddSaveAction(ControlerItem* item, Hdf5Data& data, const QString& path /*=""*/)
{
	return item;
	auto saveAction = std::make_shared<ControlerSave>();
	saveAction->setHdf5Data(data);
	saveAction->setPath(path);
	item->addAction(saveAction);

	return item;
}

