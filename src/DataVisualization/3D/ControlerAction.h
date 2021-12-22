#pragma once
#include "action.h"
#include "ClipPlaneWidget.h"

namespace DV3D {
	class Controler;
	
	class ControlerAction :public ActionSwitch{
	public:
		void active() {};
		virtual void active(std::shared_ptr<Controler> controler) = 0;
	};

	class ControlerVisible :public ControlerAction {
	public:
		void active(std::shared_ptr<Controler> controler) override;
	};

	class ControlerEdgeVisible :public ControlerAction {

	public:
		void active(std::shared_ptr<Controler> controler) override;
	};

	class ControlerClipEnable :public ControlerAction {

	public:
		void active(std::shared_ptr<Controler> controler) override;
	};
	class ControlerClipPlan :public ControlerAction
	{
	public:
		void active(std::shared_ptr<Controler> controler) override;
	private:
		void showWidget(std::shared_ptr<Controler> controler);
		void hideWidget();
	private:
		ClipPlaneWidget clipPlaneWidget;
	};
}