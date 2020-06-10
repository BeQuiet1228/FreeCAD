#pragma once
#include "IRuntimeModule.hpp"
#include "ISessionCreateListener.hpp"
#include "Controller.hpp"

namespace PicNet
{
	class ControllerManager :public ISessionCreateListener, public IRuntimeModule
	{
	public:

		virtual int Initialize(){
			return 0;
		}


		virtual void Finalize(){

		}

		virtual void Tick() {

		}

		virtual void OnSessionCreated(SessionWeakPtr ptr){
			ControllerPtr controllerPtr(new Controller(ptr, &_group));
			controllerPtr->Start();
		}

		virtual ~ControllerManager(){

		}

	private:
		ControllerGroup _group;
	};
}