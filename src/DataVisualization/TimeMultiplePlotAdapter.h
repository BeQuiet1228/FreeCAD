#pragma once
#include "TimePlotAdapter.h"
namespace DV {
	class TimeMultiplePlotAdapter:public TimePlotAdapter{
	public:
		void findPointRender(const float& x, const float& y) override;
	};
}