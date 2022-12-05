#pragma once
#include "PlotAdapter.h"
#include <QSize>
#include "TimeData.h"
#include <QTextEdit>

namespace DV {
	class TimePlotAdapter :public PlotAdapter {
		Q_OBJECT
	public:
		TimePlotAdapter(std::list<std::shared_ptr<Renderer>>& listRender);
		~TimePlotAdapter();
	};
};
