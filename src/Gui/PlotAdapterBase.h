#pragma once
#include"DataVisualization/RendererFactory.h"
#include"FCConfig.h"
namespace Gui
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
		PlotAdapterBase(DataType datatype);
		~PlotAdapterBase() = default;
	public:
		virtual void doubleEvent(Hdf5Data h5d, std::string name) = 0;
		virtual void setStructData(Hdf5Data& data) {};
		bool getIsStructData();
	protected:
		DataType mdatatype;
		bool haveStructData;
	};

	class GuiExport PlotAdapter2D :public PlotAdapterBase
	{
	public:
		PlotAdapter2D(const Hdf5Data& structData);
		PlotAdapter2D();
		~PlotAdapter2D();
	public:
		virtual void doubleEvent(Hdf5Data h5d, std::string name);
		void setStructData(Hdf5Data& data);
	protected:
		DV::PlotAdapterPtr creatPlotAdapter(Hdf5Data h5d, std::string name);
	private:
		std::shared_ptr<DV::RendererFactory> factoryPtr;

	};
};