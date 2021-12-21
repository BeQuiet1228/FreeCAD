#pragma once
#include "ControlerAction.h"
#include <Contour3dActorPipeline.h>
#include "../realTimewidget.h"
#include <QWidget>
namespace DV3D
{
	class ControlerContourSurface :public ControlerAction
	{
	public:
		void active(std::shared_ptr<Controler> controler) override;
	private:
		void showWidget(std::shared_ptr<Controler> controler);
	};

	class Contour3dControlerWidget :public DV::realTimewidget
	{
		Q_OBJECT
	public:
		Contour3dControlerWidget(QWidget* parent=nullptr);
		~Contour3dControlerWidget();
	public:
		void init(std::vector<ContourValue>& values);
		void setControler(std::shared_ptr<Controler> controler);
	public Q_SLOTS:
		void getContourValues(std::list<double>&);
	private:
		std::shared_ptr<Controler> controlerptr;
	};
};