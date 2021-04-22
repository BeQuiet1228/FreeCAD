#include "Plot.h"
#include <QPainter>
#include "Canvas.h"
#include "Axis.h"
#include "RenderThreadManager.h"
#include "RenderTask.h"
#include "Renderer.h"
#include "qwt/qwt_scale_widget.h"
#include "qwt/qwt_scale_engine.h"
#include "ContourRender.h"
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
	delete scaleWIdget;
	delete scaleEngine;
}


/**
* @brief Plot::reRender 重新渲染
* @return void
*/
void Plot::reRender()
{
	if (mainRenderer)
	{
		std::cerr << "reRender" << std::endl;
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
	rd->dataInit();
	rd->setDefaultRang();
	subRenderers.push_back(rd);
}

/**
* @brief Plot::setMainRenderer
* @param const std::shared_ptr<Renderer> & rd
* @return void
*/
void Plot::setMainRenderer(const std::shared_ptr<Renderer>& rd)
{
	//初始化数据
	rd->dataInit();
	rd->setDefaultRang();

	this->mainRenderer = rd;
	auto xr = mainRenderer->getXRang();
	auto yr = mainRenderer->getYRang();
	AxisL->setAxisRange(yr.min, yr.max);
	AxisB->setAxisRange(xr.min, xr.max);
}

/**
* @brief Plot::addRenderer 添加渲染器 这个操作会清空之前的渲染器，第一个渲染器默认为主渲染器。
* @param const std::list<std::shared_ptr<Renderer>> & listRender
* @return void
*/
void Plot::addRenderer(const std::list<std::shared_ptr<Renderer>>& listRender)
{
	if (listRender.size() < 1)
		return;
	clearSubRenderer();
	auto iter = listRender.begin();
	setMainRenderer(*iter);
	iter++;
	for (; iter != listRender.end(); iter++)
	{
		addSubRenderer(*iter); 
	}

	canvas->clearIteam();
}

/**
* @brief Plot::setAxisRightEnabled 设置是否显示图例
* @param const bool & e
* @return void
*/
void Plot::setAxisRightEnabled(const bool& e)
{
	if (axisRightEnabled == e)
		return;
	axisRightEnabled = e;
	if (axisRightEnabled)
		updateAxis();
	else
		scaleWIdget->hide();
}

void Plot::updateAxis()
{
	if (!mainRenderer)
		return;

	Data::Rang xr, yr;
	xr = mainRenderer->getXRang();
	yr = mainRenderer->getYRang();

//	AxisL->setAxisRange(yr.min, yr.max);
//	AxisL->_update();
//	AxisB->setAxisRange(xr.min, xr.max);
//	AxisB->_update();

	if (!axisRightEnabled)
		return;
	auto contourRender = std::dynamic_pointer_cast<ContourRender>(mainRenderer);
	if (!contourRender)
		return;
	Data::Rang vr = contourRender->getValueRange();
	QwtInterval interval(vr.min, vr.max);
	scaleWIdget->setColorMap(interval, new ColorMap);
	scaleWIdget->setScaleDiv(scaleEngine->divideScale(vr.min, vr.max, 6, 8, 0));
	scaleWIdget->show();
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
	connect(canvas, SIGNAL(emitSelectRect(QRect)), this, SLOT(canvasSelectRect(QRect)));
	connect(canvas, SIGNAL(emitSelectPoint(QPoint)), this, SLOT(canvasSelectPoint(QPoint)));

	AxisL = new Axis();
	AxisL->setAxixStyle(Axisleft);
	AxisL->SetAxisNumber(6);
	AxisL->setAxisRange(-100, 100);
	AxisB = new Axis();
	AxisB->setAxixStyle(AxisBottom);
	AxisB->SetAxisNumber(6);
	AxisB->setAxisRange(-100, 100);

	scaleWIdget = new QwtScaleWidget(QwtScaleDraw::RightScale, this);
	scaleWIdget->setColorBarEnabled(true);
	scaleWIdget->setColorBarWidth(20);

	gridLayout->addWidget(canvas, 0, 1, 1, 1);
	gridLayout->addWidget(AxisL, 0, 0, 1, 1);
	gridLayout->addWidget(AxisB, 1, 1, 1, 1);
	gridLayout->addWidget(scaleWIdget, 0, 2, 1, 1);

	gridLayout->setRowStretch(0, 9);
	gridLayout->setRowStretch(1, 1);
	gridLayout->setColumnStretch(0, 1);
	gridLayout->setColumnStretch(1, 9);
	gridLayout->setColumnStretch(2, 0);

	scaleWIdget->hide();
	
	
}

void Plot::initData()
{
	renderManager.reset(new RenderThreadManager);
	connect(renderManager.get(), SIGNAL(allWorkFinished()), this, SLOT(renderFinished()));

	scaleEngine = new QwtLinearScaleEngine;
	axisRightEnabled = false;
}

/**
* @brief Plot::findPointRender 开始取点渲染
* @param const float & x
* @param const float & y
* @return void
*/
void Plot::findPointRender(const float& x, const float& y)
{
	mainRenderer->setSize(canvas->size());
	mainRenderer->setFindPosition(QPointF(x, y));
	RenderTask task(mainRenderer,RenderTask::FIND_POINT,1);
	renderManager->addTask(task);
	renderManager->start();
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

/**
* @brief Plot::canvasSelectRect 处理画布框选时的放大缩小
* @param QRect rect
* @return void
*/
void Plot::canvasSelectRect(QRect rect)
{
	//如果选取框太小  不给予放大缩小操作
	if (rect.width() < 10 || rect.height() < 10)
		return;


	auto xr = mainRenderer->getXRang();
	auto yr = mainRenderer->getYRang();
	auto size = mainRenderer->getSize();

	//将矩形框转换为范围
	float xMax, xMin, yMax, yMin;
	xMax = rect.width() > 0 ? rect.x() + rect.width() : rect.x();
	xMin = xMax - rect.width();
	yMax = rect.height() > 0 ? rect.y() + rect.height() : rect.y();
	yMin = yMax - rect.height();
	//因为屏幕坐标系的原点在左上角，而实际坐标系的远点在左下角。所以这里的y范围需要做一下翻转
	float tempYMax = size.height() - yMin;
	yMin = size.height() - yMax;
	yMax = tempYMax;
	//获取数据到坐标的缩放比例
	float xScale, yScale;
	xScale = xr.length() / size.width();
	yScale = yr.length() / size.height();

	//获得数据范围
	//框选的起始刻度可能不是0，所以得加上起点的刻度才是渲染刻度
	xr.max = xMax*xScale + xr.min;
	xr.min = xMin*xScale + xr.min;
	yr.max = yMax*yScale + yr.min;
	yr.min = yMin*yScale + yr.min;

	mainRenderer->setXRang(xr);
	mainRenderer->setYRang(yr);
	AxisL->setAxisRange(yr.min, yr.max);
	AxisL->_update();
	AxisB->setAxisRange(xr.min, xr.max);
	AxisB->_update();
	//设置其他渲染器的范围
	for (auto iter = subRenderers.begin(); iter != subRenderers.end(); iter++)
	{
		(*iter)->setYRang(yr);
		(*iter)->setXRang(xr);
	}

	//重绘
	reRender(); 
}

void Plot::canvasSelectPoint(QPoint point)
{
	float x, y;
	x = point.x();
	//因为屏幕坐标系的原点在左上角，而实际坐标系的远点在左下角。所以这里的y范围需要做一下翻转
	auto size = mainRenderer->getSize();
	y = size.height() - point.y();

	findPointRender(x, y);
}

void Plot::resizeEvent(QResizeEvent *event)
{
	QWidget::resizeEvent(event);
	reRender();
}

/**
* @brief Plot::keyReleaseEvent 
* @param QKeyEvent * event
* @return void
*/
void Plot::keyReleaseEvent(QKeyEvent *event)
{
	//暂时使用空格回到主页  方便测试
	QWidget::keyReleaseEvent(event);
	if (event->key() == Qt::Key_Space)
	{
		if (!mainRenderer)
			return;
		mainRenderer->setDefaultRang();
		auto xr = mainRenderer->getXRang();
		auto yr = mainRenderer->getYRang();

		for (auto i = subRenderers.begin(); i != subRenderers.end(); i++)
		{
			(*i)->setXRang(xr);
			(*i)->setYRang(yr);
		}
		//改变坐标轴的范围
		AxisL->setAxisRange(yr.min, yr.max);
		AxisB->setAxisRange(xr.min, xr.max);
		AxisL->_update();
		AxisB->_update();

		//清理点取点图层
		canvas->removeItem(1);

		reRender();
	}
	
}
void Plot::reRendererEvent(const std::list<std::shared_ptr<Renderer>>& listRender)
{
	addRenderer(listRender);
	reRender();
}
#include "moc_Plot.cpp"
