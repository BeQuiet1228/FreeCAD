#pragma  once
#include "PlotAdapterNeedStruct.h"
#include <QObject>
#include "ContourRender.h"
#include <memory>
class ContourPlotAdapter :public PlotAdapterNeedStruct{
	Q_OBJECT
public:
	ContourPlotAdapter()  = delete;
	ContourPlotAdapter(const std::list<std::shared_ptr<Renderer>>& listRender);
	~ContourPlotAdapter();

private:
	void initAciton();
	void updateAcitonState();

	std::shared_ptr<ContourRender> getContourRender();
private:
	QAction* switchShader,
		* switchContour,
		* adjuLevel;

public Q_SLOTS:
	void switchShaderTrigger(bool);
	void switchContourTrigger(bool);
	void adjuLevelTrigger(bool);
	void Getlevels(std::list<double>&);
public:
	std::list<QAction*> getActions() override;

	bool axisRightIsHide() override;

	Data::Rang getAxisRightRange() override;

	void setAxisRightRange(const float& min, const float& max);
};
