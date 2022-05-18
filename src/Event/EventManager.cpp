#include "EventManager.h"
#include <QApplication>

EV::EventManager::EventManager()
{
	connect(QApplication::instance(), SIGNAL(aboutToQuit()), this, SLOT(appQuit()));
}

void EV::EventManager::registerRecevier(EventRecevier* recevier)
{
	if (recevier->isRegister)
		return;
	recevier->isRegister = true;
	receviers.push_back(recevier);
}

void EV::EventManager::removeRecevier(EventRecevier* recevier)
{
	if (!recevier->isRegister)
		return;
	for (auto iter = receviers.begin(); iter != receviers.end(); iter++)
	{
		if(*iter != recevier)
			continue;
		receviers.erase(iter);
		break;
	}
	recevier->isRegister = false;
}

std::shared_ptr<EV::EventManager> EV::EventManager::instance;

void EV::EventManager::appQuit()
{
	instance.reset();
}

EV::EventManager::~EventManager()
{

}

std::shared_ptr<EV::EventManager> EV::EventManager::GetInstance()
{
	static std::once_flag flag;

	std::call_once(flag, [&](){
		instance.reset(new EventManager());
		});
	return instance;
}

void EV::EventManager::postEvent(Event* event)
{
	auto manager = GetInstance();
	for (auto s : manager->receviers)
	{
		if(!s->hasEvent(event))
			continue;
		s->postEvent(event);
	}
}

EV::EventRecevier::EventRecevier()
{
	EventManager::GetInstance()->registerRecevier(this);
}

EV::EventRecevier::~EventRecevier()
{
	EventManager::GetInstance()->removeRecevier(this);
}

EV::Event::Event()
{

}

EV::Event::~Event()
{

}
