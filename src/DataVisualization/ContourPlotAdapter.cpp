#include "ContourPlotAdapter.h"
#include <QAction>
#include "ContourRender.h"
#include <QIcon>
#include "C_encoding.h"
#include "realTimewidget.h"
namespace DV {
	ContourPlotAdapter::ContourPlotAdapter(const std::list<std::shared_ptr<Renderer>>& listRender)
	{
		addRenderer(listRender);
		initAciton();
	}

	ContourPlotAdapter::~ContourPlotAdapter()
	{

	}

	/**
	* @brief ContourPlotAdapter::initAciton 初始化action
	* @return void
	*/
	void ContourPlotAdapter::initAciton()
	{
		switchShader = new QAction(this);
		switchContour = new QAction(this);
		adjuLevel = new QAction(this);
		connect(adjuLevel, SIGNAL(triggered(bool)), this, SLOT(adjuLevelTrigger(bool)));
		connect(switchShader, SIGNAL(triggered(bool)), this, SLOT(switchShaderTrigger(bool)));
		connect(switchContour, SIGNAL(triggered(bool)), this, SLOT(switchContourTrigger(bool)));

		updateAcitonState();
	}

	/**
	* @brief ContourPlotAdapter::updateAcitonState 更新action的图标状态
	* @return void
	*/
	void ContourPlotAdapter::updateAcitonState()
	{
		if (!mainRenderer)
			return;

		auto contourRd = std::dynamic_pointer_cast<ContourRender>(mainRenderer);
		if (!contourRd)
			return;

		if (contourRd->testDisplayMode(QwtPlotSpectrogram::ImageMode))
		{
			switchShader->setIcon(QIcon(":/ActionIcon/contour_image_on.svg"));
			switchShader->setText(GetEncodingstr("着色(开)", ENCODING_GB2312));
		}
		else {
			switchShader->setIcon(QIcon(":/ActionIcon/contour_image_off.svg"));
			switchShader->setText(GetEncodingstr("着色(关)", ENCODING_GB2312));
		}

		if (contourRd->testDisplayMode(QwtPlotSpectrogram::ContourMode)) {
			switchContour->setIcon(QIcon(":/ActionIcon/contour_line_on.svg"));
			switchContour->setText(GetEncodingstr("等值线(开)", ENCODING_GB2312));
		}
		else {
			switchContour->setIcon(QIcon(":/ActionIcon/contour_line_off.svg"));
			switchContour->setText(GetEncodingstr("等值线(关)", ENCODING_GB2312));
		}

		adjuLevel->setIcon(QIcon(":/ActionIcon/contour_line_on.svg"));
		adjuLevel->setText(GetEncodingstr("调整等值线等级", ENCODING_GB2312));
	}

	std::shared_ptr<ContourRender> ContourPlotAdapter::getContourRender()
	{
		if (!mainRenderer)
			throw "ContourPlotAdapter::getContourRender() not have main render!";

		auto contourRd = std::dynamic_pointer_cast<ContourRender>(mainRenderer);
		if (!contourRd)
			throw "ContourPlotAdapter::getContourRender() cast contour render failed!";
		return contourRd;
	}

	void ContourPlotAdapter::switchShaderTrigger(bool)
	{
		auto contourRd = getContourRender();

		//着色和等值线必须存在一个
		bool ok = !contourRd->testDisplayMode(QwtPlotSpectrogram::ImageMode);
		if (!(ok || contourRd->testDisplayMode(QwtPlotSpectrogram::ContourMode)))
			return;

		//如果只开启等值线，那么需要给等值线一个空的画笔，这样等值线才会显示颜色
		QPen pen;
		if (!ok)
		{
			pen.setStyle(Qt::NoPen);
		}
		else {
			pen.setStyle(Qt::SolidLine);
		}
		contourRd->setDefaultContourPen(pen);

		contourRd->setDisplayMode(QwtPlotSpectrogram::ImageMode, ok);
		updateAcitonState();
		Q_EMIT updatePlot();
	}

	void ContourPlotAdapter::switchContourTrigger(bool)
	{

		auto contourRd = getContourRender();

		//着色和等值线必须存在一个
		bool ok = !contourRd->testDisplayMode(QwtPlotSpectrogram::ContourMode);
		if (!(ok || contourRd->testDisplayMode(QwtPlotSpectrogram::ImageMode)))
			return;

		contourRd->setDisplayMode(QwtPlotSpectrogram::ContourMode, ok);
		//如果只开启等值线，那么需要给等值线一个空的画笔，这样等值线才会显示颜色
		QPen pen;
		if (!contourRd->testDisplayMode(QwtPlotSpectrogram::ImageMode))
		{
			pen.setStyle(Qt::NoPen);
		}
		else {
			pen.setStyle(Qt::SolidLine);
		}
		contourRd->setDefaultContourPen(pen);
		updateAcitonState();
		Q_EMIT updatePlot();
	}

	std::list<QAction*> ContourPlotAdapter::getActions()
	{
		std::list<QAction*> actions = PlotAdapterNeedStruct::getActions();
		actions.push_back(switchShader);
		actions.push_back(switchContour);
		actions.push_back(adjuLevel);

		return actions;
	}

	bool ContourPlotAdapter::axisRightIsHide()
	{
		return false;
	}

	/**
	* @brief ContourPlotAdapter::getAxisRightRange 获取左边坐标轴的范围
	* @return Data::Rang
	*/
	Data::Rang ContourPlotAdapter::getAxisRightRange()
	{
		auto contourRd = getContourRender();
		return contourRd->getValueRange();
	}

	void ContourPlotAdapter::setAxisRightRange(const float& min, const float& max)
	{
		auto contourRd = getContourRender();
		contourRd->setValueRange(min, max);
	}

	std::string ContourPlotAdapter::getXTag()
	{
		if (!mainRenderer)
			return "";
		auto data = mainRenderer->getData();
		auto xd = std::dynamic_pointer_cast<DirData>(data);
		if (!xd)
			return "";
		if (xd->isTruedir())
			return xd->getXTag();
		else
			return xd->getYTag();
	}

	std::string ContourPlotAdapter::getYTag()
	{
		if (!mainRenderer)
			return "";
		auto data = mainRenderer->getData();
		auto xd = std::dynamic_pointer_cast<DirData>(data);
		if (!xd)
			return "";
		if (xd->isTruedir())
			return xd->getYTag();
		else
			return xd->getXTag();
	}

	/**
	* @brief ContourPlotAdapter::adjuLevelTrigger 调整等值线等级
	* @param bool
	* @return void
	* @Time 2021/7/7
	*/
	void ContourPlotAdapter::adjuLevelTrigger(bool)
	{
		auto contourRd = getContourRender();
		std::list<double> leves = contourRd->contourLevels().toStdList();
		//打开窗口
		if (leves.empty())
			return;
		realTimewidget* mrealTimewidget = new realTimewidget();
		mrealTimewidget->setModal(true);
		mrealTimewidget->loadConfigLevels(leves);
		mrealTimewidget->resize(500, 300);
		mrealTimewidget->show();
		connect(mrealTimewidget, SIGNAL(GetListDouble(std::list<double>&)), this, SLOT(Getlevels(std::list<double>&)));
	}
	void ContourPlotAdapter::Getlevels(std::list<double>& levels)
	{
		auto contourRd = getContourRender();
		QList<double> listlevel = QList<double>::fromStdList(levels);
		contourRd->setContourLevels(listlevel);
		emit updatePlot();
	}
	void ContourPlotAdapter::autoMaxRender()
	{
		if (!mainRenderer)
		{
			return;
		}
		//先设置主渲染器的默认大小
		mainRenderer->setDefaultRang();
		auto xr = mainRenderer->getXRang();
		auto yr = mainRenderer->getYRang();
		setRenderRange(xr.min, xr.max, yr.min, yr.max);
	}
};

#include "moc_ContourPlotAdapter.cpp"