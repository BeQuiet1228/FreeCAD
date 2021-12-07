#pragma once
#include"DataVisualization/RendererFactory.h"
#include"FCConfig.h"
namespace App
{
	class AppExport PlotAdapterBase
	{
	public:
		enum DataType
		{
			PLOT_2D = 0x01,
			PLOT_3D = 0x02,
			PLOT_NULL
		};
		PlotAdapterBase(DataType datatype);
		~PlotAdapterBase()=default;
	public:
		virtual DV::PlotAdapterPtr creatPlotAdapter(Hdf5Data h5d,std::string name) = 0;
		virtual void setStructData(Hdf5Data& data) = 0;
		bool getIsStructData();
	protected:
		DataType mdatatype;
		bool haveStructData;
	};

	class AppExport PlotAdapter2D :public PlotAdapterBase
	{
	public:
		PlotAdapter2D(const Hdf5Data& structData);
		PlotAdapter2D();
		~PlotAdapter2D();
	public:
		virtual DV::PlotAdapterPtr creatPlotAdapter(Hdf5Data h5d, std::string name) override;
		void setStructData(Hdf5Data& data);
	private:
		std::shared_ptr<DV::RendererFactory> factoryPtr;
		
	};
};