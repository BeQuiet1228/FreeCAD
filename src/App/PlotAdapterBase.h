#pragma once
#include"DataVisualization/RendererFactory.h"
#include"FCConfig.h"
namespace PI
{
	class GuiExport PlotAdapterBase
	{
	public:
		enum DataType
		{
			PLOT_2D = 0x01,
			PLOT_3D = 0x02,
			PLOT_NULL
		};
		PlotAdapterBase(DataType datatype) :mdatatype(datatype) {};
		~PlotAdapterBase() = default;
	public:
		//virtual PlotAdapterPtr creatPlotAdapter(Hdf5Data h5d, DirectionType type = X_Y) = 0;
	protected:
		DataType mdatatype;
	};

	class GuiExport PlotAdapter2D :public PlotAdapterBase
	{
	public:
		PlotAdapter2D(const Hdf5Data& structData);
		~PlotAdapter2D();
	public:
		//PlotAdapterPtr creatPlotAdapter(Hdf5Data h5d, DirectionType type = X_Y);
	private:
		std::shared_ptr<RendererFactory> factoryPtr;
	};
};