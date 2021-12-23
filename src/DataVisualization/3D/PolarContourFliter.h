#pragma once
#include "HDF5Reader/hdf5io.h"
namespace DV3D
{
	class PolarContourFilter
	{
	public:
		PolarContourFilter();
		~PolarContourFilter();
		bool loadPoint(Hdf5Data& h5,int resolution);
		std::vector<double>& getRGridData();
		std::vector<double>& getThetaGridData();
		std::vector<double>& getZGridData();
		std::vector<double>& getVallist();
	protected:
		bool loadPoint3d(Hdf5Data& h5, int resolution);
		bool loadPoint2d(Hdf5Data& h5, int resolution);
		void eraseRedundant(std::vector<double>&);
	private:
		//int mResolution;//Æ½»¬¶È
		std::vector<double> rGridData;
		std::vector<double> thetaGridData;
		std::vector<double> zGridData;
		std::vector<double> vallist;
	};
};