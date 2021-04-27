#pragma once
#include <QWidget>
#include <QPaintEvent>
#include <QImage>
#include <QGridLayout>
#include <memory>
#include <list>
#include <QResizeEvent>
#include <QKeyEvent>
#include "exportConfig.hpp"
#include "Canvas.h"
class Canvas;
class Renderer;
class RenderThreadManager;
class Axis;
class QwtScaleEngine;
class QwtScaleWidget;
class DATA_VISUALIZATION_EXPORT Plot:public QWidget{
	Q_OBJECT
public:
	Plot(QWidget* parent = 0);
	~Plot();
public:
	void addCanvasItem(const CanvasItem& item){
		canvas->addIteam(item);
	};
private:
	//布局
	QGridLayout * gridLayout;
	//画布
	Canvas *canvas;
	//坐标轴
	Axis *AxisL, *AxisB;
	//渲染管理器
	std::shared_ptr<RenderThreadManager> renderManager;
	//从渲染器
	std::list<std::shared_ptr<Renderer>> subRenderers;
	//主渲染器
	std::shared_ptr<Renderer> mainRenderer;
	//从渲染器起始层级
	const unsigned int subRenderStartRank = 10;
	//颜色图例
	QwtScaleWidget *scaleWIdget;
	QwtScaleEngine *scaleEngine;
	//图例是否可用
	bool axisRightEnabled;
public:
	//重渲染
	void reRender();
	//添加从渲染器
	void addSubRenderer(const std::shared_ptr<Renderer>& rd);
	//设置主渲染器
	void setMainRenderer(const std::shared_ptr<Renderer>& rd);
	//添加渲染器
	void addRenderer(const std::list<std::shared_ptr<Renderer>>& listRender);
	//设置图例是否可用
	void setAxisRightEnabled(const bool& e);
	//更新坐标轴
	void updateAxis();
	//清理从渲染器
	void clearSubRenderer(){
		subRenderers.clear();
	}
private:
	//初始化界面
	void initGUI();
	//初始化数据
	void initData();
	//点渲染
	void findPointRender(const float& x, const float& y);
public Q_SLOTS:
	//渲染完成
	void renderFinished();
	//画布框选
	void canvasSelectRect(QRect rect);
	//画布取点
	void canvasSelectPoint(QPoint point);
	void reRendererEvent(const std::list<std::shared_ptr<Renderer>>& listRender);
protected:
	void resizeEvent(QResizeEvent *event) override;
protected:
	void keyReleaseEvent(QKeyEvent *event);
};