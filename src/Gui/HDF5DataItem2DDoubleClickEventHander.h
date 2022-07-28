#pragma once
#include "Hdf5DataItemEventHandler.h"
#include "HDF5Reader/hdf5io.h"
#include"DataVisualization/RendererFactory.h"
namespace Gui
{
	class HDF5DataItem2DDoubleClickEventHander:public HDF5DataItemEventHander{
	public:
		HDF5DataItem2DDoubleClickEventHander();
		void trigger(HDF5DataItem* item) override;
		void setStructData(Hdf5Data data);
	private:
		DV::PlotAdapterPtr creatPlotAdapter(Hdf5Data h5d, HDF5DataItem* item);
	private:
		std::shared_ptr<DV::RendererFactory> factoryPtr;
	};
}