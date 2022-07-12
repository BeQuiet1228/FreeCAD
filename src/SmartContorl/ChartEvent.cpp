#include "ChartEvent.h"

std::shared_ptr<DV::PlotAdapter> ChartEvent::getAdaopter()
{
	return adapter;
}

void ChartEvent::setAdapter(std::shared_ptr<DV::PlotAdapter> adapter)
{
	this->adapter = adapter;
}

std::string ChartEvent::getType()
{
	return "ChartEvent";
}

