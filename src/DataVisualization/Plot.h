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
#include <QLabel>
#include <QToolBar>
#include "qwt/qwt_scale_widget.h"
#include <QHBoxLayout>
class Canvas;
class Renderer;
class RenderThreadManager;
class Axis;
class QwtScaleEngine;
//class QwtScaleWidget;
class ColorMapWidget;
//class ScaleWidget;
class rightScaleWidget;
class UndoRedoStack;
class PlotAdapter;
class DATA_VISUALIZATION_EXPORT Plot:public QWidget{
	Q_OBJECT
public:
	Plot(QWidget* parent = 0);
	~Plot();
	friend class ContourRenderStateGetter;
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
	//图表信息label
	QLabel* informationLabel;
	//适配器
	std::shared_ptr<PlotAdapter> adapter;
	//QwtScaleWidget *scaleWIdget;
	//ColorMapWidget* scaleWIdget;
	//ScaleWidget* scaleWIdget;
	rightScaleWidget* scaleWIdget;
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
	//按钮条
	QWidget* toolbar;
	QHBoxLayout *toolbarLayout;
public:
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
	//以默认大小渲染
	void autoMaxRender();
	//刷新label显示
	void updateInformationLabel();
	//读取配置
	void loadconfig();
	//Equal scale display
	void EqualScaleDisplay();
	//设置适配器
	void setAdapter(const std::shared_ptr < PlotAdapter>& adapter);
	//保存主渲染器中的数据
	void MainRendererDataSaveAs(const std::string& path);
	//设置是否显示网格线
	void setGridLineEnabled(const bool& e) {
		gridLineEnabled = e;
		updateGridLine();
	};
	bool getGridLineEnabled() {
		return gridLineEnabled;
	}
	//根据横纵比例显示
	void setRatioDisplay(double& horizonal,double& vertical);
	void SaveAs(std::string);
private:
	//初始化界面
	void initGUI();
	//初始化数据
	void initData();
	//点渲染
	void findPointRender(const float& x, const float& y);
	//渲染网格
	void creatGridRenderTask();
	//初始化信息框字体
	void initInformationLabelFont();
	//更新按钮条
	void updateToolbar();
public Q_SLOTS:
	//重渲染
	void reRender();
	//渲染完成
	void renderFinished();
	//画布框选
	void canvasSelectRect(QRect rect);
	//画布取点
	void canvasSelectPoint(QPoint point);
	void reRendererEvent(std::shared_ptr<PlotAdapter>);
	void reRendererXRang(const float& min, const float& max);
	void reRendererYRang(const float& min, const float& max);
	void ScaleWidgetRightRange(const float& min, const float& max);
	//画布改变大小
	void canvasResize(QSize size);
	//设置应用事件
	void setappEvent();
	
protected:
	void resizeEvent(QResizeEvent *event) override;
protected:
	void keyReleaseEvent(QKeyEvent *event);
};