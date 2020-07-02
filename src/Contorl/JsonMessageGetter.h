#pragma once
#include <memory>
#include <mutex>
#include <deque>
#include <QObject>
class JsonMessageGetter:public QObject{
	Q_OBJECT
private:
	JsonMessageGetter();
	static std::shared_ptr<JsonMessageGetter> _instance;
public:
	~JsonMessageGetter();
	static std::shared_ptr<JsonMessageGetter> GetInstance()
	{
		static std::once_flag flag;
		std::call_once(flag, [&](){
			_instance.reset(new JsonMessageGetter);
		});

		return _instance;
	}
	JsonMessageGetter(const JsonMessageGetter &) = delete;
	JsonMessageGetter operator=(const JsonMessageGetter&) = delete;
private:
	//消息队列
	std::deque<std::string> jsonDeque;
	//队列锁
	std::mutex jsonDequeMutex;

public:
	//判断是否有消息
	bool hasMessage();
	//取出一个消息
	bool getJsonMessage(std::string& json);
	//添加一个消息
	void addJsonMessage(const std::string& json);

signals:
	void hasNewMessage();
};