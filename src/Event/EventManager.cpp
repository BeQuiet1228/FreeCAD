#include "EventManager.h"
#include <QApplication>

EV::EventManager::EventManager()
{
	connect(QApplication::instance(), SIGNAL(aboutToQuit()), this, SLOT(appQuit()));
}

void EV::EventManager::registerSender(EventSender* sender)
{
	if (sender->isRegister)
		return;
	sender->isRegister = true;
	senders.push_back(sender);
}

void EV::EventManager::removeSender(EventSender* sender)
{
	if (!sender->isRegister)
		return;
	for (auto iter = senders.begin(); iter != senders.end(); iter++)
	{
		if(*iter != sender)
			continue;
		senders.erase(iter);
		break;
	}
	sender->isRegister = false;
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

void EV::EventManager::postEvent(QEvent* event)
{
	auto manager = GetInstance();
	for (auto s : manager->senders)
	{
		if(!s->hasEvent(event->type()))
			continue;
		s->postEvent(event);
	}
}

EV::EventSender::EventSender()
{
	EventManager::GetInstance()->registerSender(this);
}

EV::EventSender::~EventSender()
{
	EventManager::GetInstance()->removeSender(this);
}
