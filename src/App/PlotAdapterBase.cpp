#include"PlotAdapterBase.h"
namespace PI
{
	PlotAdapter2D::PlotAdapter2D(const Hdf5Data& structData) :PlotAdapterBase(PLOT_2D)
	{
		factoryPtr = std::shared_ptr<RendererFactory>(new RendererFactory(structData));
	}
	PlotAdapter2D::~PlotAdapter2D() {
		
	}
	PlotAdapterPtr PlotAdapter2D::creatPlotAdapter(Hdf5Data h5d, DirectionType type)
	{
		return creatPlotAdapter(h5d,type);
	}
}
