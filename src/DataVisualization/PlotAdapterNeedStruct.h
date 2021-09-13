#pragma once
#include "PlotAdapter.h"
#include <QAction>
#include <QSize>
class PlotAdapterNeedStruct :public PlotAdapter {
	Q_OBJECT
public:
	PlotAdapterNeedStruct();
	~PlotAdapterNeedStruct();

public Q_SLOTS:
	void switcStructTrigger(bool);

public:
	std::list<QAction*> getActions() override;
	void initPlot(Plot& plot) override;
	void reRender(const QSize& size) override;
private:
	QAction* switchStruct;
	//是否显示结构图
	bool displayStruct;

Q_SIGNALS:
	void removeCanvasItem(unsigned int);
};