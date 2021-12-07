#pragma once
#include "PlotAdapterBase.h"
namespace Gui {
	class Item3DDoubleClickEvent:public PlotAdapterBase{
	public:
		Item3DDoubleClickEvent() = default;
		~Item3DDoubleClickEvent() = default;

	public:
		void doubleEvent(Hdf5Data h5d, std::string name) override;
	};

}