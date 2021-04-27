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
class UndoRedoStack;
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
	const unsigned int SUB_RENDER_START_RANK = 10;
	const unsigned int FIND_POINT_RENDER_RANK = SUB_RENDER_START_RANK + 20;
	//颜色图例
	QwtScaleWidget *scaleWIdget;
	QwtScaleEngine *scaleEngine;
	//图例是否可用
	bool axisRightEnabled;
	//撤销恢复栈
	std::shared_ptr<UndoRedoStack> URStack;
	//图表网格线渲染器
	std::shared_ptr<Renderer> gridRender;
	//坐标轴网格等级
	unsigned int xAxisLevel, yAxisLevel;
	//是否显示网格线
	bool gridLineEnabled;
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
	//清理取点提示图层
	void clearFindPoint();
	//撤销恢复
	void undo();
	void redo();
	//刷新网格线
	void updateGridLine();
	//清理从渲染器
	void clearSubRenderer(){
		subRenderers.clear();
	}
	//设置是否显示网格线
	void setGridLineEnabled(const bool& e) {
		gridLineEnabled = e;
		updateGridLine();
	};
	bool getGridLineEnabled() {
		return gridLineEnabled;
	}
private:
	//初始化界面
	void initGUI();
	//初始化数据
	void initData();
	//点渲染
	void findPointRender(const float& x, const float& y);
	//设置渲染范围
	void setRenderRange(const float& xMin, const float xMax, const float& yMin, const float& yMax);
	//渲染网格
	void creatGridRenderTask();
public Q_SLOTS:
	//渲染完成
	void renderFinished();
	//画布框选
	void canvasSelectRect(QRect rect);
	//画布取点
	void canvasSelectPoint(QPoint point);
	//
	void reRendererEvent(const std::list<std::shared_ptr<Renderer>>& listRender);
protected:
	void resizeEvent(QResizeEvent *event) override;
protected:
	void keyReleaseEvent(QKeyEvent *event);
};