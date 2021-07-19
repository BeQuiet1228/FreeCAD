#include "phasorPlotAdapter.h"

PhasorPlotAdapter::PhasorPlotAdapter(const std::list<std::shared_ptr<Renderer>>& listRender)
{
	addRenderer(listRender);
}
PhasorPlotAdapter::~PhasorPlotAdapter()
{

}
bool PhasorPlotAdapter::axisRightIsHide()
{
	auto phasorrenderer = std::dynamic_pointer_cast<phasorRenderer>(mainRenderer);
	if (!phasorrenderer)
		return true;
	if (1 == phasorrenderer->getMode())
		return false;
	else
		return true;
}
Data::Rang PhasorPlotAdapter::getAxisRightRange()
{
	Data::Rang r;
	r.max = 1.0;
	r.min = 0.0;
	return r;
}
#include "moc_phasorPlotAdapter.cpp"