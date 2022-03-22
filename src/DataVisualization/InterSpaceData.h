#pragma once
#include "TimeData.h"
#include"exportConfig.hpp"
namespace DV {
	class DATA_VISUALIZATION_EXPORT InterspaceData :public TimeData {
	public:
		InterspaceData(Hdf5Data& h5Data, const RunMod& mod = SINGLE_THREAD);
		~InterspaceData() = default;

	public:
		virtual unsigned int findIndexFromXValueL(const float& x) override;
		void dataToFFT(Data::Rang xr) override;
		bool addNewGroup() override;

	private:
		std::string getNewXTag();
	};
};
