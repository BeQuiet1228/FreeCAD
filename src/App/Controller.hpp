#pragma once

#include <boost\thread.hpp>
#include "Session.hpp"
#include"Distributer.hpp"

namespace PicNet
{
	class Controller;
	class ControllerGroup;

	typedef boost::shared_ptr<Controller> ControllerPtr;

	//控制器组，用来收集控制器的
	class ControllerGroup {

	public:
		void Add(ControllerPtr session)
		{
			//线程锁
			boost::unique_lock<boost::mutex> lock(_mutex);
			_sessionSet.insert(session);
		}

		void Remove(ControllerPtr session)
		{
			//线程锁
			boost::unique_lock<boost::mutex> lock(_mutex);
			_sessionSet.erase(session);
		}

		ControllerPtr Top()
		{
			return *(_sessionSet.begin());
		}
	private:
		std::set<ControllerPtr> _sessionSet;
		boost::mutex _mutex;

	};

	//控制器类
	class Controller :public boost::enable_shared_from_this<Controller>
	{
	public:

		//构造函数需要一个会话
		Controller(SessionWeakPtr session, ControllerGroup* group) :_loopThread(nullptr)
		{
			_session = session;
			_group = group;
		}


		void Start(){
			_group->Add(shared_from_this());
			if (_loopThread != nullptr)
			{
				delete _loopThread;
			}
			_loopThread = new boost::thread(boost::bind(&Controller::ThreadLoop, this));
		}

		void ThreadLoop()
		{
			while (true)
			{
				Sleep(1);
				if (_session.expired())
				{
					Finalize();
					return;
				}
				auto s = _session.lock();

				while (s->ExistReceiveMsg())
				{

					_distributer.InputNet(s->Get());
				}
				std::vector<MsgPtr> outputs;
				std::vector<FILE*> outputFiles;
				//刷新
				_distributer.Update(outputs, outputFiles);

				//遍历发送消息
				for (auto msg : outputs)
				{
					//判断发送文件还是发送消息，区分
					if (msg->GetType() == NetMsgHeader::MsgType::FILE_CONENT)
					{
						s->SendFile(msg, outputFiles.front());
						outputFiles.erase(outputFiles.begin());
					}
					else{
						s->Send(msg);
					}
				}
			}
		}

		void Finalize(){
			_distributer.Finalize();
			_group->Remove(shared_from_this());

		}

		virtual ~Controller()
		{
			if (_loopThread != nullptr)
			{
				delete _loopThread;
			}
			_loopThread = nullptr;
			std::cout << "Exit A Controlller" << std::endl;
		}
	private:

		boost::weak_ptr<Session> _session;
		ControllerGroup* _group;
		boost::thread* _loopThread;
		//分发对象
		Distributer _distributer;
	};
}