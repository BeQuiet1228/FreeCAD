#pragma once
#include "Session.hpp"

namespace PicNet
{
	class ISessionCreateListener
	{
	public:

		virtual ~ISessionCreateListener(){};
		void virtual OnSessionCreated(SessionWeakPtr) {};

	};

}
