#pragma once
#include "ControlerItemListWidget.h"
#include <memory>
namespace DV3D {
	class ControlerItem;
	class Controler;
}
namespace Gui {
	class HDF5DataItem;
	class HDF5DataItemEventHander {
	public:
		HDF5DataItemEventHander() =default;
		virtual ~HDF5DataItemEventHander() {};

	public:
		virtual void trigger(HDF5DataItem* item) = 0;
	};

	class HDF5DataItem3DDoubleClickEventHander :public HDF5DataItemEventHander{
	public:
		void trigger(HDF5DataItem* item) override;
	private:
		std::shared_ptr<DV3D::Controler> creatStructControler(HDF5DataItem* item);
		void showView3D(DV3D::ControlerItem* controlerItem);
	};
}