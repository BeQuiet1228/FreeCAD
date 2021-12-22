#pragma once
#include "ControlerAction.h"
#include "Contour3dActorPipeline.h"
#include "DataVisualization/realTimewidget.h"
namespace DV3D
{
	class Contour3dControlerWidget :public DV::realTimewidget
	{
		Q_OBJECT
	public:
		explicit Contour3dControlerWidget(QWidget* parent = nullptr);
		~Contour3dControlerWidget();
	public:
		void init(std::vector<ContourValue>& values);
		void setControler(std::shared_ptr<Controler> controler);
	public Q_SLOTS:
		void slotGetContourValues(std::list<double>&);
	private:
		std::shared_ptr<Controler> controlerptr;
	};
};