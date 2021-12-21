#include "controlerItemFactor.h"
#include "ControlerAction.h"
#include "Contour3dControlerAction.h"

DV3D::ControlerItem* DV3D::ControlerItemFactor::CreatControlerItem()
{
	ControlerItem *item = new ControlerItem();

	std::shared_ptr<ControlerClipEnable> clip(new ControlerClipEnable());
	std::shared_ptr<ControlerEdgeVisible> edge(new ControlerEdgeVisible());

	item->addAction(clip);
	item->addAction(edge);
	
	return item;
}

DV3D::ControlerItem* DV3D::ControlerItemFactor::CreatContour3dControlerItem()
{
	ControlerItem* item = new ControlerItem();
	std::shared_ptr<ControlerClipEnable> clip(new ControlerClipEnable());
	std::shared_ptr<ControlerEdgeVisible> edge(new ControlerEdgeVisible());
	std::shared_ptr<ControlerContourSurface> contourSurface(new ControlerContourSurface());
	item->addAction(clip);
	item->addAction(edge);
	item->addAction(contourSurface);
	return item;
}

