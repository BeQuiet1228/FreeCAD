#pragma once
#include <memory>
#include <QSize>
#include <list>
#include "Data.h"
class Renderer;
class RenderThreadManager;

class PlotAdapter {
public:
	PlotAdapter();
	~PlotAdapter();

public:

public:
	//渲染管理器
	std::shared_ptr<RenderThreadManager> renderManager;
	//从渲染器
	std::list<std::shared_ptr<Renderer>> subRenderers;
	//主渲染器
	std::shared_ptr<Renderer> mainRenderer;
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
	//设置渲染范围
	void setRenderRange(const float& xMin, const float xMax, const float& yMin, const float& yMax);
	void setRenderXRange(const float& min, const float& max);
	void setRenderYRange(const float& min, const float& max);
	//获取渲染范围 暂时使用
	Data::Rang getXRange();
	Data::Rang getYRange();
	//清理从渲染器
	void clearSubRenderer() {
		subRenderers.clear();
	}

};