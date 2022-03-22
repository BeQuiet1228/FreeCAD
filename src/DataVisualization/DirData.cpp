#include "DirData.h"
namespace DV {
	DirData::DirData(Hdf5Data& hedata, const RunMod& mod) :XYData(hedata, mod)
	{
	}
	/**
	* @brief  DirData::isTruedir 判断方向是否正确
	* @return bool
	*/
	bool DirData::isTruedir()
	{
		auto xtag = getXTag();
		auto ytag = getYTag();
		switch (directionTyp)
		{
		case X_Y:
		{
			if (xtag.find("X1") != std::string::npos || xtag.find("X") != std::string::npos)
				return true;
		}break;
		case X_Z:
		{
			if (xtag.find("X1") != std::string::npos || xtag.find("X") != std::string::npos)
				return true;
		}break;
		case Y_Z:
		{
			if (xtag.find("Y") != std::string::npos || xtag.find("X2") != std::string::npos)
				return true;
		}break;
		case R_Z:
		{
			if (xtag.find("Z") != std::string::npos && ytag.find("R") != std::string::npos)
				return true;
		}break;
		case R_THETA:
		{
			return true;
		}break;
		case NONE:
			return true;
			break;
		}
		return false;
	}
};
