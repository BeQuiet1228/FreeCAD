#pragma once
#include "ControlerAction.h"
#include <Contour3dActorPipeline.h>
#include "Contour3dControlerWidget.h"
#include <QObject>
namespace DV3D
{
	class ControlerContourSurface :public ControlerAction
	{
	public:
		ControlerContourSurface();

		void active(std::shared_ptr<Controler> controler) override;
		virtual void initState(std::shared_ptr<Controler> controler) override;
	private:
		bool showWidget(std::shared_ptr<Controler> controler);
	};
};