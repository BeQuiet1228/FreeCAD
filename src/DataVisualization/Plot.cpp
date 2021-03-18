#include "Plot.h"
#include <QPainter>
#include "Canvas.h"
#include "Axis.h"
#include "RenderThreadManager.h"
#include "RenderTask.h"
#include "Renderer.h"
Plot::Plot(QWidget* parent /*= 0*/)
	:QWidget(parent)
{
	initGUI();
	initData();
	
}

Plot::~Plot()
{
	delete canvas;
	delete AxisB;
	delete AxisL;
}


/**
* @brief Plot::reRender 重新渲染
* @return void
*/
void Plot::reRender()
{
	if (mainRenderer)
	{
		mainRenderer->setSize(canvas->size());
		RenderTask task(mainRenderer);
		renderManager->addTask(task);
	}
	unsigned int rank = subRenderStartRank;
	for (auto rdIter = subRenderers.begin(); rdIter != subRenderers.end(); rdIter++)
	{
		(*rdIter)->setSize(canvas->size());
		RenderTask task(*rdIter, RenderTask::MAP, rank);
		renderManager->addTask(task);
		rank++;
	}

	renderManager->start();

}

/**
* @brief Plot::addSubRenderer 添加附属渲染器 渲染一些附加内容，这些内容会自动覆盖到主渲染器渲染的内容之上（层级按照添加顺序覆盖）。
* @param const std::shared_ptr<Renderer> & rd
* @return void
*/
void Plot::addSubRenderer(const std::shared_ptr<Renderer>& rd)
{
	subRenderers.push_back(rd);
}

/**
* @brief Plot::initGUI 初始化布局
* @return void
*/
void Plot::initGUI()
{
	gridLayout = new QGridLayout;
	this->setLayout(gridLayout);
	canvas = new Canvas();
	AxisL = new Axis();
	AxisB = new Axis();

	gridLayout->addWidget(canvas, 0, 1, 1, 1);
	gridLayout->addWidget(AxisL, 0, 0, 1, 1);
	gridLayout->addWidget(AxisB, 1, 1, 1, 1);

	gridLayout->setRowStretch(0, 9);
	gridLayout->setRowStretch(1, 1);
	gridLayout->setColumnStretch(0, 1);
	gridLayout->setColumnStretch(1, 9);
}

void Plot::initData()
{
	renderManager.reset(new RenderThreadManager);
	connect(renderManager.get(), SIGNAL(allWorkFinished()), this, SLOT(renderFinished()));
}

/**
* @brief Plot::renderFinished 渲染完成槽
* @return void
*/
void Plot::renderFinished()
{
	auto result = renderManager->takeResut();
	for (auto i = result.begin(); i != result.end(); i++)
		canvas->addIteam(*i);
	canvas->update();
}

void Plot::resizeEvent(QResizeEvent *event)
{
	QWidget::resizeEvent(event);
	reRender();
}

#include "moc_Plot.cpp"
