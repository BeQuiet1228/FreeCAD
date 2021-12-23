#pragma once
#include "HDF5Reader/hdf5io.h"
namespace DV3D
{
	class PolarContourFilter
	{
	public:
		PolarContourFilter();
		~PolarContourFilter();
		bool loadPoint(Hdf5Data& h5);
	private:
		int mResolution;//Æ½»¬¶È
		std::vector<double> rGridData;
		std::vector<double> thetaGridData;
		std::vector<double> zGridData;
		std::vector<double> vallist;
	};
};