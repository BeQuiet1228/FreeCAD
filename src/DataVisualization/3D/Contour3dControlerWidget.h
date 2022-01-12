#pragma once
#include "ControlerAction.h"
#include "Contour3dActorPipeline.h"
#include "../realTimewidget.h"
namespace DV3D
{
	class Contour3dControlerWidget :public DV::realTimewidget
	{
	public:
		explicit Contour3dControlerWidget(QWidget* parent = nullptr);
		~Contour3dControlerWidget();
	public:
		void init(std::vector<ContourValue>& values);
		void setControler(std::shared_ptr<Controler> controler);
		void slotGetContourValues(std::list<double>&);
	protected:
		//ÖØÐ´±£´æº¯Êý
		virtual void saveClicked() override;
	private:
		std::shared_ptr<Controler> controlerptr;
	};
};