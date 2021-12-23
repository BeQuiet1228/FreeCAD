#pragma once
#include "ControlerItemListWidget.h"
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
	};


	//¶ÔÐü¸¡´°¿Ú²Ù×÷
	ControlerItemListWidget* getControlerListWidget();
	ControlerItemListWidget* CreatControlerListWidget();
	void hideControlerListWidget();
	void showControlerListWidget();
}