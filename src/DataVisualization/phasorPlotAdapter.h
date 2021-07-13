#pragma once
#ifndef PHASORPLOTADAPTER_H_ 
#define PHASORPLOTADAPTER_H_
#include "PlotAdapter.h"
#include <QObject>
#include "phasorRenderer.h"
#include <memory>

class PhasorPlotAdapter :public PlotAdapter
{
	Q_OBJECT
public:
	PhasorPlotAdapter() = delete;
	PhasorPlotAdapter(const std::list<std::shared_ptr<Renderer>>& listRender);
	~PhasorPlotAdapter();
public:
	bool axisRightIsHide() override;
	Data::Rang getAxisRightRange() override;
};
#endif 
