#include "TimePlotAdapter.h"
#include "C_encoding.h"
#include "PlotAdapter.h"
#include "Renderer.h"
#include "RenderTask.h"
#include "RenderThreadManager.h"
#include "Plot.h"
#include "TimeRenderer.h"
#include <qcoreapplication.h>
#include <qmessagebox.h>

namespace DV {
	TimePlotAdapter::TimePlotAdapter(std::list<std::shared_ptr<Renderer>>& listRender)
	{
		addRenderer(listRender);
	}

	TimePlotAdapter::~TimePlotAdapter()
	{

	}
};

#include "moc_TimePlotAdapter.cpp"