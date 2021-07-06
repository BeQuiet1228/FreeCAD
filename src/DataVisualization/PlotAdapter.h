#pragma once
#include <memory>
#include <QSize>
#include <list>
#include "Data.h"
#include "Canvas.h"
#include <QAction>
#include <QObject>
class Renderer;
class RenderThreadManager;
class Plot;
class PlotAdapter :public QObject{
	Q_OBJECT
public:
	PlotAdapter();
	~PlotAdapter();

public:

protected:
	//渲染管理器
	std::shared_ptr<RenderThreadManager> renderManager;
	//从渲染器
	std::list<std::shared_ptr<Renderer>> subRenderers;
	//主渲染器
	std::shared_ptr<Renderer> mainRenderer;

//修改框架时从plot中移动过来的函数
public:
	//重渲染
	void reRender(const QSize& size);
	//添加从渲染器
	void addSubRenderer(const std::shared_ptr<Renderer>& rd);
	//设置主渲染器
	void setMainRenderer(const std::shared_ptr<Renderer>& rd);
	//添加渲染器
	void addRenderer(const std::list<std::shared_ptr<Renderer>>& listRender);
	//以默认大小渲染
	void autoMaxRender();
	//刷新网格线
	void updateGridLine();
	//取点渲染
	void findPointRender(const float& x, const float& y);
	//设置渲染范围
	void setRenderRange(const float& xMin, const float xMax, const float& yMin, const float& yMax);
	void setRenderXRange(const float& min, const float& max);
	void setRenderYRange(const float& min, const float& max);
	//载入配置
	void loadConfig();
	//存储主渲染器的数据
	void MainRendererDataSaveAs(const std::string& path);

	//清理从渲染器
	void clearSubRenderer() {
		subRenderers.clear();
	}

public:
	//取走渲染结果
	std::list<CanvasItem> takeResut();
	//获取图表信息
	QString getInformationTitile();
	

	std::string getXTag();
	std::string getYTag();


//虚函数接口
public:
	//初始化与plot之间的关系
	virtual void initPlot(Plot& plot);
	virtual std::list<QAction*> getActions();
	//获取坐标轴显示状态
	virtual bool axisLeftIsHide();
	virtual bool axisRightIsHide();
	virtual bool axisTopIsHide();
	virtual bool axisBottomIsHide();
	//获取坐标轴范围
	virtual Data::Rang getAxisLeftRange();
	virtual Data::Rang getAxisRightRange();
	virtual Data::Rang getAxisTopRange();
	virtual Data::Rang getAxisBottomRange();

Q_SIGNALS:
	void updatePlot();
};