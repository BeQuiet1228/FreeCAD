#include"PlotAdapterBase.h"
namespace App
{
	struct structDirectType {
		std::string str;
		DV::DirectionType mDirectionType;
	};
	static structDirectType structDirectTypelist[]
	{
		{
			"Phi-Z",
			DV::DirectionType::R_Z
		},
		{
			"Z-R",
			DV::DirectionType::R_Z,
		},
		{
			"R*cos(Phi)-R*sin(Phi)",
			DV::DirectionType::R_THETA
		},
		{
			"X_Y",
			DV::DirectionType::X_Y
		},
		{
			"Y_Z",
			DV::DirectionType::Y_Z
		},
		{
			"X_Z",
			DV::DirectionType::X_Z
		}
	};
	PlotAdapterBase::PlotAdapterBase(DataType datatype) :mdatatype(datatype) {
		haveStructData = false;
	};
	PlotAdapter2D::PlotAdapter2D(const Hdf5Data& structData) :PlotAdapterBase(PLOT_2D)
	{
		factoryPtr = std::shared_ptr<DV::RendererFactory>(new DV::RendererFactory(structData));
		haveStructData = true;
	}
	PlotAdapter2D::PlotAdapter2D():PlotAdapterBase(PLOT_2D)
	{
		factoryPtr = std::shared_ptr<DV::RendererFactory>(new DV::RendererFactory());
		haveStructData = false;
	}
	PlotAdapter2D::~PlotAdapter2D() {

	}
	void PlotAdapter2D::setStructData(Hdf5Data& data)
	{
		factoryPtr->setStructData(data);
		haveStructData = true;
	}
	
	/**
	* @time	2021/12/02
	* @brief App::PlotAdapter2D::creatPlotAdapter ´´½¨ÊÊÅäÆ÷
	* @param Hdf5Data h5d
	* @param std::string name
	* @return DV::PlotAdapterPtr
	*/
	DV::PlotAdapterPtr PlotAdapter2D::creatPlotAdapter(Hdf5Data h5d, std::string name)
	{
		if (h5d.name.find("struct") != std::string::npos)
		{
			DV::DirectionType type;
			for (auto& it : structDirectTypelist)
			{
				if (name.find(it.str) != std::string::npos)
				{
					type = it.mDirectionType;
					break;
				}
			}
			return factoryPtr->creatPlotAdapter(h5d, type);
		}
		return factoryPtr->creatPlotAdapter(h5d);
	}
	bool PlotAdapterBase::getIsStructData()
	{
		return haveStructData;
	}
};
