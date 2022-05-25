#pragma once
#include "TimePlotAdapter.h"
namespace DV {
	class TimeMultiplePlotAdapter:public TimePlotAdapter{
	public:
		TimeMultiplePlotAdapter(std::list<std::shared_ptr<Renderer>> renders);
		void findPointRender(const float& x, const float& y) override;
	};
}