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
#include <stack>
#include "RenderGrid.h"
struct UndoRedoData
{
	UndoRedoData(const Data::Rang& xr, const Data::Rang& yr)
		:xr(xr), yr(yr) {};
	UndoRedoData() = default;
	Data::Rang xr, yr;
};
class UndoRedoStack {
public:
	UndoRedoStack() = default;
	~UndoRedoStack() = default;

	/**
	* @brief UndoRedoStack::undo 撤销之前的操作
	* @param UndoRedoData & data 返回渲染范围
	* @return bool false 代表操作失败
	*/
	bool undo(UndoRedoData& data) {
		if (undoStack.size() < 2)
			return false;
		redoStack.push(undoStack.top());
		undoStack.pop();
		data = undoStack.top();
		
	};
	/**
	* @brief UndoRedoStack::redo 恢复之前的撤销
	* @param UndoRedoData & data 返回渲染数据
	* @return bool false 代表操作失败
	*/
	bool redo(UndoRedoData& data) {
		if (redoStack.empty())
			return false;
		data = redoStack.top();
		undoStack.push(data);
		redoStack.pop();
	};
	/**
	* @brief UndoRedoStack::push 压入操作，如放大缩小操作的数据
	* @param const UndoRedoData & data
	* @return void
	*/
	void push(const UndoRedoData& data) {
		undoStack.push(data);
		clearStack(redoStack);
	};
	/**
	* @brief UndoRedoStack::clear 清空数据
	* @return void
	*/
	void clear() {
		clearStack(redoStack);
		clearStack(undoStack);
	}
private:
	std::stack<UndoRedoData> undoStack, redoStack;
private:
	void clearStack(std::stack<UndoRedoData>& stack) {
		while (!stack.empty())
		{
			stack.pop();
		}
	}
};

Plot::Plot(QWidget* parent /*= 0*/)
	:QWidget(parent),URStack(new UndoRedoStack)
{
	initData();
	setAxisRightEnabled(true);
	initGUI();
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
	//清理寻点的画布
	clearFindPoint();
	//创建坐标轴网格渲染任务
	creatGridRenderTask();


	if (mainRenderer)
	{
		std::cerr << "reRender" << std::endl;
		mainRenderer->setSize(canvas->size());
		RenderTask task(mainRenderer);
		renderManager->addTask(task);
	}
	unsigned int rank = SUB_RENDER_START_RANK;
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
	rd->loadconfig();

	if (mainRenderer)
	{
		Data::Rang xr, yr;
		xr = mainRenderer->getXRang();
		yr = mainRenderer->getYRang();
		rd->setXRang(xr);
		rd->setYRang(yr);
	}else {
		rd->setDefaultRang();
	}

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
	rd->loadconfig();
	this->mainRenderer = rd;
	auto xr = mainRenderer->getXRang();
	auto yr = mainRenderer->getYRang();
	setRenderRange(xr.min, xr.max, yr.min, yr.max);
	//清空撤销恢复栈，将新的操作压入
	URStack->clear();
	UndoRedoData URData(xr, yr);
	URStack->push(URData);
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

	AxisL->setAxisRange(yr.min, yr.max);
	AxisB->setAxisRange(xr.min, xr.max);
	

	//设置横纵坐标单位
		//获取横纵坐标单位
	auto d = std::dynamic_pointer_cast<XYData>(mainRenderer->data);
	if (d)
	{
		AxisL->setAxisText(QString::fromStdString(d->getYTag()));
		AxisB->setAxisText(QString::fromStdString(d->getXTag()));
	}
	AxisB->_update();
	AxisL->_update();



	//显示图例
	if (!axisRightEnabled)
		return;
	auto contourRender = std::dynamic_pointer_cast<ContourRender>(mainRenderer);
	if (!contourRender)
	{
		scaleWIdget->hide();
		return;
	}

	Data::Rang vr = contourRender->getValueRange();
	QwtInterval interval(vr.min, vr.max);
	scaleWIdget->setColorMap(interval, new ColorMap);
	scaleWIdget->setScaleDiv(scaleEngine->divideScale(vr.min, vr.max, 6, 8, 0));
	scaleWIdget->show();
}

/**
* @brief Plot::clearFindPoint 清理取点图层
* @return void
*/
void Plot::clearFindPoint()
{
	canvas->removeItem(FIND_POINT_RENDER_RANK);
}

/**
* @brief Plot::undo
* @return void
*/
void Plot::undo()
{
	UndoRedoData data;
	if (!URStack->undo(data))
		return;
	Data::Rang& xr = data.xr;
	Data::Rang& yr = data.yr;
	setRenderRange(xr.min, xr.max, yr.min, yr.max);
	updateAxis();
	reRender();
}

void Plot::redo()
{
	UndoRedoData data;
	if (!URStack->redo(data))
		return;
	Data::Rang& xr = data.xr;
	Data::Rang& yr = data.yr;
	setRenderRange(xr.min, xr.max, yr.min, yr.max);
	updateAxis();
	reRender();
}

/**
* @brief Plot::updateGridLine 刷新网格线显示
* @return void
*/
void Plot::updateGridLine()
{
	creatGridRenderTask();
	renderManager->start();
}

/**
* @brief Plot::autoMaxRender 自动调整渲染范围 以最大范围渲染
* @return void
*/
void Plot::autoMaxRender()
{
	if (!mainRenderer)
		return;
	mainRenderer->setDefaultRang();
	auto xr = mainRenderer->getXRang();
	auto yr = mainRenderer->getYRang();

	setRenderRange(xr.min, xr.max, yr.min, yr.max);

	updateAxis();

	reRender();
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
	AxisL->SetAxisNumber(yAxisLevel);
	
	AxisB = new Axis();
	AxisB->setAxixStyle(AxisBottom);
	AxisB->SetAxisNumber(xAxisLevel);
	connect(AxisL, SIGNAL(sendAxisRang(const float&, const float&)), this, SLOT(setRenderYRange(const float&, const float&)));
	connect(AxisB, SIGNAL(sendAxisRang(const float&, const float&)), this, SLOT(setRenderXRange(const float&, const float&)));
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
/**
* @brief Plot::initData 初始化数据
* @return void 
*/
void Plot::initData()
{
	renderManager.reset(new RenderThreadManager);
	connect(renderManager.get(), SIGNAL(allWorkFinished()), this, SLOT(renderFinished()));

	scaleEngine = new QwtLinearScaleEngine;
	axisRightEnabled = false;

	xAxisLevel = 7;
	yAxisLevel = 7;
	RenderGrid* r = new RenderGrid(xAxisLevel, yAxisLevel);
	gridRender.reset(r);

	gridLineEnabled = false;
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
	RenderTask task(mainRenderer,RenderTask::FIND_POINT, FIND_POINT_RENDER_RANK);
	renderManager->addTask(task);
	renderManager->start();
}

/**
* @brief Plot::setRenderRange 设置所有渲染器的渲染范围
* @param const float & xMin
* @param const float xMax
* @param const float & yMin
* @param const float & yMax
* @return void
*/
void Plot::setRenderRange(const float& xMin, const float xMax, const float& yMin, const float& yMax)
{
	Data::Rang xr(xMin, xMax), yr(yMin, yMax);
	mainRenderer->setXRang(xr);
	mainRenderer->setYRang(yr);
	//设置其他渲染器的范围
	for (auto iter = subRenderers.begin(); iter != subRenderers.end(); iter++)
	{
		(*iter)->setYRang(yr);
		(*iter)->setXRang(xr);
	}


	//设置坐标轴刻度
	AxisL->setAxisRange(yr.min, yr.max);
	AxisB->setAxisRange(xr.min, xr.max);
	updateAxis();
	reRender();
}

void Plot::setRenderXRange(const float& min, const float& max)
{
	if (!mainRenderer)
		return;
	auto yr = mainRenderer->getYRang();
	setRenderRange(min, max, yr.min, yr.max);
}

void Plot::setRenderYRange(const float& min, const float& max)
{
	if (!mainRenderer)
		return;
	auto xr = mainRenderer->getXRang();
	setRenderRange(xr.min, xr.max, min, max);
}

void Plot::creatGridRenderTask()
{
	const unsigned int GRID_RENDER_RANK = FIND_POINT_RENDER_RANK - 1;

	canvas->removeItem(GRID_RENDER_RANK);

	if (!gridLineEnabled)
		return;

	std::shared_ptr<RenderGrid> gr = std::dynamic_pointer_cast<RenderGrid>(gridRender);
	gr->setXLevel(xAxisLevel);
	gr->setYLevel(yAxisLevel);

	gridRender->setSize(canvas->size());
	RenderTask task(gridRender);
	task.rank = GRID_RENDER_RANK;
	renderManager->addTask(task);
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

	//将操作压入栈
	UndoRedoData unData(xr, yr);
	URStack->push(unData);

	//设置渲染范围
	setRenderRange(xr.min, xr.max, yr.min, yr.max);
	//重绘
	reRender(); 
	//跟新坐标轴
	updateAxis();
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
		autoMaxRender();
/**************测试撤销恢复的代码 ****************/
	}
	else if (event->key() == Qt::Key_Left) {
		this->undo();
	}else if (event->key() == Qt::Key_Right) {
		this->redo();
	}
	
}
/**
* @brief Plot::reRendererEvent 重绘槽函数
* @param const std::list<std::shared_ptr<Renderer>>& listRender 渲染器列表
* @return void  
*/
void Plot::reRendererEvent(const std::list<std::shared_ptr<Renderer>>& listRender)
{
	addRenderer(listRender);
	reRender();
}
#include "moc_Plot.cpp"
