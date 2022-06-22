#pragma  once
#include <mutex>
#include <memory>
#include <QObject>
#include <vector>

#ifdef _EVENT_
#define EVENT_EXPORT __declspec(dllexport)
#else
#define EVENT_EXPORT   __declspec(dllimport)
#endif 

namespace EV {
	class EVENT_EXPORT Event {
	public:
		Event();
		virtual ~Event();
	public:
		virtual std::string getType() = 0;
	};

	class EVENT_EXPORT EventRecevier {
		friend class EventManager;
	public:
		EventRecevier();
		virtual ~EventRecevier();
		
		virtual void postEvent(Event* event) = 0;
		virtual bool hasEvent(Event* event) = 0;
	private:
		bool isRegister;
	};


	class EVENT_EXPORT EventManager :QObject{
		friend class EventRecevier;
		Q_OBJECT
	public:
		~EventManager();
		EventManager(const EventManager&) = delete;
		EventManager operator=(const EventManager&) = delete;

		static std::shared_ptr<EventManager> GetInstance();
		static void postEvent(Event* event);
	private:
		EventManager();
		void registerRecevier(EventRecevier* recevier);
		void removeRecevier(EventRecevier* recevier);
	private:
		static std::shared_ptr<EventManager> instance;
		std::vector<EventRecevier*> receviers;
	public Q_SLOTS:
		void appQuit();
	};

}