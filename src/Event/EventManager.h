#pragma  once
#include <mutex>
#include <memory>
#include <QObject>
#include <QEvent>
#include <vector>

#ifdef _EVENT_
#define EVENT_EXPORT __declspec(dllexport)
#else
#define EVENT_EXPORT   __declspec(dllimport)
#endif 

namespace EV {
	class EVENT_EXPORT EventSender {
		friend class EventManager;
	public:
		EventSender();
		~EventSender();
		
		virtual void postEvent(QEvent* event) = 0;
		virtual bool hasEvent(const QEvent::Type& type) = 0;
	private:
		bool isRegister;
	};


	class EVENT_EXPORT EventManager :QObject{
		friend class EventSender;
		Q_OBJECT
	public:
		~EventManager();
		EventManager(const EventManager&) = delete;
		EventManager operator=(const EventManager&) = delete;

		static std::shared_ptr<EventManager> GetInstance();
		static void postEvent(QEvent* event);
	private:
		EventManager();
		void registerSender(EventSender* sender);
		void removeSender(EventSender* sender);
	private:
		static std::shared_ptr<EventManager> instance;
		std::vector<EventSender*> senders;
	public Q_SLOTS:
		void appQuit();
	};

}