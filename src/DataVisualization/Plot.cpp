#include "Plot.h"
#include <QPainter>
#include "Canvas.h"
#include "Axis.h"
#include "RenderThreadManager.h"
#include "RenderTask.h"
#include "Renderer.h"
#include "qwt/qwt_scale_engine.h"
#include "ContourRender.h"
#include <stack>
#include "RenderGrid.h"
#include <QFont>
#include "C_encoding.h"
#include"ConfigWidget.h"
#include "PlotAdapter.h"
#include "CustomConfig.h"
#include "QToolButton"
#include <QList>
#include <QPaintEvent>
#include "rightScaleWidget.h"
#include "ContourPlotAdapter.h"
#include "TLabel.h"
#include"CombAxis.h"
namespace DV {
	Plot::Plot(QWidget* parent /*= 0*/)
		:QWidget(parent)
	{
		CanvasItem::registerMetaTye();
		setObjectName("visualizationPlot");
		initData();
		initGUI();
		setAxisRightEnabled(true);
		loadconfig();
	}

	Plot::~Plot()
	{
		delete canvas;
		delete AxisB;
		delete AxisL;
		delete scaleWIdget;
		delete scaleEngine;
		delete informationLabel;
	}


	/**
	* @brief Plot::reRender 重新渲染
	* @return void
	*/
	void Plot::reRender()
	{
		if (!adapter)
			return;
		//清理寻点的画布
		clearFindPoint();
		//创建坐标轴网格渲染任务
		creatGridRenderTask();
		//更新信息显示label
		updateInformationLabel();
		adapter->reRender(this->canvas->size());
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
		if (!adapter)
			return;

		Data::Rang xr, yr;
		xr = adapter->getAxisBottomRange();
		yr = adapter->getAxisLeftRange();

		AxisL->setAxisRange(yr.min, yr.max);
		AxisB->setAxisRange(xr.min, xr.max);


		//设置横纵坐标单位

		//AxisL->setAxisText(QString::fromStdString(adapter->getYTag()));
		//AxisB->setAxisText(QString::fromStdString(adapter->getXTag()));

		AxisB->_update();
		AxisL->_update();



		//显示图例
		if (adapter->axisRightIsHide())
		{
			setAxisRightEnabled(false);
			return;
		}
		else
			setAxisRightEnabled(true);

		Data::Rang vr = adapter->getAxisRightRange();
		if (/*(vr.max - vr.min) > -0.0000001 && (vr.max - vr.min) < 0.0000001*/
			vr.min == vr.max)
		{
			scaleWIdget->hide();
			return;
		}
		QwtInterval interval(vr.min, vr.max);
		scaleWIdget->setColorMap(interval, ConfigWidget::getQwtLinearColorMap());
		scaleWIdget->setAxisRange(vr.min, vr.max);
		scaleWIdget->_update();
		scaleWIdget->show();

	}

	/**
	* @brief Plot::clearFindPoint 清理取点图层
	* @return void
	*/
	void Plot::clearFindPoint()
	{
		canvas->removeItem(Canvas::FIND_POINT_RENDER_RANK);
	}

	/**
	* @brief Plot::undo
	* @return void
	*/
	void Plot::undo()
	{
		if (!adapter->undo())
			return;
		updateAxis();
		reRender();
	}

	void Plot::redo()
	{
		if (!adapter->redo())
			return;
		updateAxis();
		reRender();
	}

	/**
	* @brief Plot::updateGridLine 刷新网格线显示
	* @return void
	*/
	void Plot::updateGridLine()
	{
		// 	creatGridRenderTask();
		// 	renderManager->start();
	}

	/**
	* @brief Plot::autoMaxRender 自动调整渲染范围 以最大范围渲染
	* @return void
	*/
	void Plot::autoMaxRender()
	{
		if (!adapter)
			return;

		adapter->autoMaxRender();
		updateAxis();
		reRender();

		//清空撤销恢复栈，将新的操作压入
		auto URStack = adapter->getUndoRedoStack();
		URStack->clear();
		UndoRedoStack::DataPtr URData(adapter->CreateUndoRedoData(adapter->getAxisBottomRange(), adapter->getAxisLeftRange()));
		URStack->push(URData);
	}

	/**
	* @brief Plot::updateInformationLabel 刷新图表信息显示
	* @return void
	*/
	void Plot::updateInformationLabel()
	{
		//添加单位信息
		AxisL->setAxisText(QString::fromStdString(adapter->getYTag()));
		AxisB->setAxisText(QString::fromStdString(adapter->getXTag()));
		if (!informationLabel)
			return;
		informationLabel->setTextstr(adapter->getInformationTitile());
	}

	/**
	* @brief Plot::MainRendererDataSaveAs 将主渲染器中的数据保存到指定路径，如果文件已存在则将数据添加到最后
	* @param const std::string & path
	* @return void
	*/
	void Plot::MainRendererDataSaveAs(const std::string& path)
	{
		if (!adapter)
			return;
		adapter->MainRendererDataSaveAs(path);
	}

	/**
	* @brief Plot::initGUI 初始化布局
	* @return void
	*/
	void Plot::initGUI()
	{
		gridLayout = new QGridLayout;
		//调整画布与坐标轴的间距
		gridLayout->setSpacing(0);
		gridLayout->setContentsMargins(1, 20, 1, 1);
		this->setLayout(gridLayout);

		canvas = new Canvas();
		connect(canvas, SIGNAL(emitSelectRect(QRect)), this, SLOT(canvasSelectRect(QRect)));
		connect(canvas, SIGNAL(emitSelectPoint(QPoint)), this, SLOT(canvasSelectPoint(QPoint)));
		connect(canvas, SIGNAL(emitResize(QSize)), this, SLOT(canvasResize(QSize)));

		AxisL = new CombAxis();
		AxisL->setAxixStyle(Axisleft);
		AxisL->SetAxisNumber(yAxisLevel);
		AxisL->setColorBarEnabled(false);
		AxisL->setMargin(1);
		AxisL->setSpacing(1);
		AxisL->setBorderDist(0, 0);
		AxisB = new CombAxis();
		AxisB->setAxixStyle(AxisBottom);
		AxisB->SetAxisNumber(xAxisLevel);
		AxisB->setColorBarEnabled(false);
		AxisB->setMargin(1);
		AxisB->setSpacing(1);
		AxisB->setBorderDist(0, 0);
		connect(AxisL->mAxis, SIGNAL(sendAxisRang(const float&, const float&)), this, SLOT(reRendererYRang(const float&, const float&)));
		connect(AxisB->mAxis, SIGNAL(sendAxisRang(const float&, const float&)), this, SLOT(reRendererXRang(const float&, const float&)));
		//	scaleWIdget = new rightScaleWidget(QwtScaleDraw::RightScale, this);
		scaleWIdget = new Axis(this);
		scaleWIdget->setAxixStyle(Axisstyle::AxisRight);
		scaleWIdget->setColorBarEnabled(true);
		scaleWIdget->setColorBarWidth(20);
		scaleWIdget->setMargin(10);
		scaleWIdget->setBorderDist(0.0, 0.0);
		connect(scaleWIdget, SIGNAL(sendAxisRang(const float&, const float&)), this, SLOT(ScaleWidgetRightRange(const float&, const float&)));
		informationLabel = new TLabel();
		informationLabel->setAlignment(Qt::AlignCenter);
		informationLabel->setContentsMargins(0, 10, 0, 0);
		initInformationLabelFont();

		//初始化按钮条
		toolbar = new QWidget();
		toolbarLayout = new QHBoxLayout;
		toolbarLayout->setAlignment(Qt::AlignLeft);
		toolbarLayout->setContentsMargins(0, 20, 0, 0);
		toolbar->setLayout(toolbarLayout);
		toolbar->setObjectName("PlotToolbar");

		//增加右边距
		QWidget* space = new QWidget(this);
		space->setMinimumWidth(20);

		gridLayout->addWidget(canvas, 0, 1, 1, 1);
		gridLayout->addWidget(space, 0, 3, 1, 1);
		gridLayout->addWidget(AxisL, 0, 0, 1, 1);
		gridLayout->addWidget(AxisB, 1, 1, 1, 1);
		gridLayout->addWidget(scaleWIdget, 0, 2, 1, 1);
		gridLayout->addWidget(informationLabel, 2, 0, 1, 4);
		gridLayout->addWidget(toolbar, 3, 0, 1, 4);

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
		if (!adapter)
			return;
		adapter->findPointRender(x, y);
	}


	void Plot::creatGridRenderTask()
	{
		// 	const unsigned int GRID_RENDER_RANK = FIND_POINT_RENDER_RANK - 1;
		// 
		// 	canvas->removeItem(GRID_RENDER_RANK);
		// 
		// 	if (!gridLineEnabled)
		// 		return;
		// 
		// 	std::shared_ptr<RenderGrid> gr = std::dynamic_pointer_cast<RenderGrid>(gridRender);
		// 	gr->setXLevel(xAxisLevel);
		// 	gr->setYLevel(yAxisLevel);
		// 
		// 	gridRender->setSize(canvas->size());
		// 	RenderTask task(gridRender);
		// 	task.rank = GRID_RENDER_RANK;
		// 	renderManager->addTask(task);
	}


	/**
	* @brief Plot::initInformationLabelFont 设置信息框的字体
	* @return void
	*/
	void Plot::initInformationLabelFont()
	{
		QFont font;
		font.setPointSize(12);
		informationLabel->setFont(font);
	}

	void Plot::updateToolbar()
	{
		//先清空之前的按钮
		QList<QToolButton*> btns = toolbar->findChildren<QToolButton*>();
		for (auto iter = btns.begin(); iter != btns.end(); iter++)
		{
			delete* iter;
		}


		if (!adapter)
			return;
		auto actions = adapter->getActions();

		for (auto iter = actions.begin(); iter != actions.end(); iter++)
		{
			QToolButton* button = new QToolButton();
			button->setDefaultAction(*iter);
			button->setMinimumSize(32, 32);
			button->setAutoRaise(true);
			button->setIconSize(QSize(20, 20));
			button->setToolButtonStyle(Qt::ToolButtonTextBesideIcon);
			toolbar->layout()->addWidget(button);
		}
	}

	/**
	* @brief Plot::renderFinished 渲染完成槽
	* @return void
	*/
	void Plot::renderFinished()
	{
		auto result = adapter->takeResut();
		for (auto i = result.begin(); i != result.end(); i++)
		{
			canvas->addIteam(*i);

		}

		canvas->update();
		updateAxis();
	}

	/**
	* @brief Plot::canvasSelectRect 处理画布框选时的放大缩小
	* @param QRect rect
	* @return void
	*/
	void Plot::canvasSelectRect(QRect rect)
	{
		//如果选取框太小  不给予放大缩小操作
		//这里取绝对值是因为反向选取的框，宽度和高度都是负值。
		if (std::abs(rect.width()) < 10 || std::abs(rect.height()) < 10)
			return;


		auto xr = adapter->getAxisBottomRange();
		auto yr = adapter->getAxisLeftRange();
		auto size = canvas->size();

		//将矩形框转换为范围
		float xMax, xMin, yMax, yMin;
		xMax = rect.width() > 0 ? rect.x() + rect.width() : rect.x();
		xMin = rect.width() > 0 ? xMax - rect.width() : xMax + rect.width();
		yMax = rect.height() > 0 ? rect.y() + rect.height() : rect.y();
		yMin = rect.height() > 0 ? yMax - rect.height() : yMax + rect.height();
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
		xr.max = xMax * xScale + xr.min;
		xr.min = xMin * xScale + xr.min;
		yr.max = yMax * yScale + yr.min;
		yr.min = yMin * yScale + yr.min;

		//将操作压入栈
		auto URStack = adapter->getUndoRedoStack();
		UndoRedoStack::DataPtr unData(adapter->CreateUndoRedoData(xr, yr));
		URStack->push(unData);

		//设置渲染范围
		adapter->setRenderRange(xr.min, xr.max, yr.min, yr.max);
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
		auto size = canvas->size();
		y = size.height() - point.y();

		findPointRender(x, y);
	}

	/**
	* @brief  Plot::resizeEvent 大小变化
	* @param  QResizeEvent * event
	* @return void
	*/
	void Plot::resizeEvent(QResizeEvent* event)
	{
		QWidget::resizeEvent(event);
		//reRender();
	}

	void Plot::paintEvent(QPaintEvent* event)
	{
		QWidget::paintEvent(event);
		QPainter painter(this);
		QPen pen;
		pen.setWidth(1);
		pen.setColor(QColor(125, 125, 125));
		painter.setPen(pen);
		painter.drawRect(1, 1, this->size().width() - 2, this->size().height() - 2);
	}

	/**
	* @brief Plot::keyReleaseEvent
	* @param QKeyEvent * event
	* @return void
	*/
	void Plot::keyReleaseEvent(QKeyEvent* event)
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
		}
		else if (event->key() == Qt::Key_Right) {
			this->redo();
		}

	}

	void Plot::reRendererEvent(std::shared_ptr<PlotAdapter> ad)
	{
		setAdapter(ad);
	}

	void Plot::reRendererXRang(const float& min, const float& max) {
		if (!adapter)
			return;
		adapter->setRenderXRange(min, max);
		reRender();

	}
	void Plot::reRendererYRang(const float& min, const float& max) {
		if (!adapter)
			return;
		adapter->setRenderYRange(min, max);
		reRender();
	}

	void Plot::canvasResize(QSize size)
	{
		if (!adapter)
			return;
		adapter->reRender(size);
	}
	void Plot::loadconfig()
	{
		AxisL->loadconfig();
		AxisB->loadconfig();
		scaleWIdget->loadconfig();
		informationLabel->loadconfig();
		reRender();

		if (!adapter)
			return;
		adapter->loadConfig();
	}
	void Plot::setappEvent()
	{
		loadconfig();
		updateAxis();
		reRender();
	}

	void Plot::rmoveCanvasItem(unsigned int rank)
	{
		canvas->removeItem(rank);
	}

	/**
	* @brief  Plot::EqualScaleDisplay 按等比例显示
	* @return void
	*/
	void Plot::EqualScaleDisplay()
	{
		setRatioDisplay(1, 1);
	}

	void Plot::setAdapter(const std::shared_ptr < PlotAdapter>& adapter)
	{
		this->adapter = adapter;
		adapter->initPlot(*this);

		canvas->clearIteam();
		autoMaxRender();
		updateToolbar();
		updateInformationLabel();
	}

	/**
	* @brief Plot::setRatioDisplay 根据横纵比例显示内容
	* @param double & horizonal
	* @param double & vertical
	* @return void
	* @Time 2021/6/28
	*/
	void Plot::setRatioDisplay(const double& horizonal, const double& vertical)
	{
		if (!adapter)
			return;
		adapter->setRatioDisplay(horizonal, vertical);

		Data::Rang xr = adapter->getAxisBottomRange();
		Data::Rang yr = adapter->getAxisLeftRange();
		AxisL->setAxisRange(yr.min, yr.max);
		AxisB->setAxisRange(xr.min, xr.max);
		updateAxis();
		reRender();
	}

	/**
	* @brief Plot::SaveAs 保存h5数据
	* @param std::string filename
	* @return void
	* @Time 2021/7/6
	*/
	void Plot::SaveAs(std::string filename)
	{
		int filenamelen = filename.length();
		std::string fileFormat = filename.substr(filenamelen - 4);
		//转大写
		//transform(fileFormat.begin(), fileFormat.end(), fileFormat.begin(), toupper);
		//转小写
		transform(fileFormat.begin(), fileFormat.end(), fileFormat.begin(), tolower);
		if (fileFormat.find("png") != std::string::npos)
		{
			//保存图片
			bool isvisible = toolbar->isVisible();
			if (isvisible)
				toolbar->hide();
			QPixmap pixmap(this->size());
			this->render(&pixmap);
			//保存
			pixmap.save(QString::fromStdString(filename));
			if (isvisible)
				toolbar->show();
		}
		else if (fileFormat.find("h5") != std::string::npos)
		{
			//保存为*.h5
			MainRendererDataSaveAs(filename);
		}

	}
	void Plot::ScaleWidgetRightRange(const float& min, const float& max)
	{
		if (!adapter)
			return;
		adapter->setAxisRightRange(min, max);
		reRender();
	}
};

#include "moc_Plot.cpp"
