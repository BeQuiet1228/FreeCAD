#pragma once 
#include "Event/EventManager.h"
#include "SmartContorlConfig.hpp"
#include <memory>
namespace DV {
	class PlotAdapter;
}
class SMARTCONTORL_EXPORT ChartEvent :public EV::Event {
public:
	std::shared_ptr<DV::PlotAdapter> getAdaopter();
	void setAdapter(std::shared_ptr<DV::PlotAdapter> adapter);
	std::string  getType() override;
private:
	std::shared_ptr<DV::PlotAdapter> adapter;
};