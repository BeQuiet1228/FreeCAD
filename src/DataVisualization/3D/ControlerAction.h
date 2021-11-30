#pragma once
#include "action.h"

namespace DV3D {
	class Controler;
	
	class ControlerAction :public ActionSwitch{
	public:
		virtual void active(std::shared_ptr<Controler> controler) = 0;
	};

	class ControlerVisible :public ControlerAction {

	public:
		void active() {};
		void active(std::shared_ptr<Controler> controler) override;
	};

	class ControlerEdgeVisible :public ControlerAction {

	public:
		void active() {};
		void active(std::shared_ptr<Controler> controler) override;
	};

	class ControlerClipEnable :public ControlerAction {

	public:
		void active() {};
		void active(std::shared_ptr<Controler> controler) override;
	};
}