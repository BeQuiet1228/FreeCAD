#pragma  once
#include "PlotAdapter.h"
#include <QObject>
#include "ContourRender.h"
#include <memory>
class ContourPlotAdapter :public PlotAdapter{
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
	QAction *switchShader,
			*switchContour;

public Q_SLOTS:
	void switchShaderTrigger(bool);
	void switchContourTrigger(bool);

public:
	std::list<QAction*> getActions() override;

	bool axisRightIsHide() override;

	Data::Rang getAxisRightRange() override;

	void setAxisRightRange(const float& min, const float& max);
};
