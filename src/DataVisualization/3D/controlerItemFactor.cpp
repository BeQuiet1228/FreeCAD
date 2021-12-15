#include "controlerItemFactor.h"
#include "ControlerAction.h"

DV3D::ControlerItem* DV3D::ControlerItemFactor::CreatControlerItem()
{
	ControlerItem *item = new ControlerItem();

	std::shared_ptr<ControlerClipEnable> clip(new ControlerClipEnable());
	std::shared_ptr<ControlerEdgeVisible> edge(new ControlerEdgeVisible());

	item->addAction(clip);
	item->addAction(edge);
	
	return item;
}

