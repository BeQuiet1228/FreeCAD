#include "PlotAdapterNeedStruct.h"
#include "C_encoding.h"
#include "PlotAdapter.h"
#include "Renderer.h"
#include "RenderTask.h"
#include "RenderThreadManager.h"
#include "Plot.h"
namespace DV {
	PlotAdapterNeedStruct::PlotAdapterNeedStruct()
		:displayStruct(true)
	{
		switchStruct = new QAction(this);
		switchStruct->setIcon(QIcon(":/ActionIcon/contour_image_on.svg"));
		switchStruct->setText(GetEncodingstr("结构图(开)", ENCODING_GB2312));
		connect(switchStruct, SIGNAL(triggered(bool)), this, SLOT(switcStructTrigger(bool)));
	}

	PlotAdapterNeedStruct::~PlotAdapterNeedStruct()
	{
		delete switchStruct;
	}

	void PlotAdapterNeedStruct::switcStructTrigger(bool)
	{
		if (displayStruct) {
			displayStruct = false;
			removeCanvasItem(Canvas::SUB_RENDER_START_RANK);
			switchStruct->setIcon(QIcon(":/ActionIcon/contour_image_off.svg"));
			switchStruct->setText(GetEncodingstr("结构图(关)", ENCODING_GB2312));
		}
		else {
			switchStruct->setIcon(QIcon(":/ActionIcon/contour_image_on.svg"));
			switchStruct->setText(GetEncodingstr("结构图(开)", ENCODING_GB2312));
			displayStruct = true;
			reRender(mainRenderer->getSize());
		}
	}

	std::list<QAction*> PlotAdapterNeedStruct::getActions()
	{
		std::list<QAction*> actions;

		actions.push_back(switchStruct);
		return actions;
	}

	void PlotAdapterNeedStruct::initPlot(Plot& plot)
	{
		PlotAdapter::initPlot(plot);
		connect(this, SIGNAL(removeCanvasItem(unsigned int)), &plot, SLOT(rmoveCanvasItem(unsigned int)));
	}


	void PlotAdapterNeedStruct::reRender(const QSize& size)
	{
		if (mainRenderer)
		{
			mainRenderer->setSize(size);
			RenderTask task(mainRenderer);
			renderManager->addTask(task);
		}
		unsigned int rank = Canvas::SUB_RENDER_START_RANK;
		for (auto rdIter = subRenderers.begin(); rdIter != subRenderers.end(); rdIter++)
		{
			if (rank == Canvas::SUB_RENDER_START_RANK && (!displayStruct))
				continue;
			(*rdIter)->setSize(size);
			RenderTask task(*rdIter, RenderTask::MAP, rank);
			renderManager->addTask(task);
			rank++;
		}

		renderManager->start();
	}
};

#include "moc_PlotAdapterNeedStruct.cpp"