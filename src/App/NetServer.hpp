#pragma once

#include"IRuntimeModule.hpp"
#include <iostream>
#include <cstdio>
#include <boost/bind.hpp>
#include <boost/function.hpp>
#include <boost/shared_ptr.hpp>
#include <boost/enable_shared_from_this.hpp>
#include <boost/thread.hpp>
#include "Session.hpp"
#include "ISessionCreateListener.hpp"


using boost::asio::ip::tcp;

namespace PicNet
{
	//定义一个智能指针的typedef,它指向socket对象，用来在回调函数中和传递。
	typedef boost::shared_ptr<tcp::socket> sock_ptr;
	typedef std::vector<char> buffer_type;
	typedef boost::system::error_code Error;



	class NetServer : IRuntimeModule
	{
	public:
		enum ConnectState{
			NON = 0,
			INIT,
			CONNECTING,
			CONNECT_FAIL,
			CONNECTED,
			CLOSE
		};
		
	private:
		boost::asio::io_service io_server;
#ifdef PICNET_SERVER
		//服务器用
		tcp::acceptor* _serverAcceptor;
#endif
		//客户端用
		tcp::endpoint* _clientEndpoint;
		;

		boost::thread* _netThread;

		SessionGroup _group;

		bool IsServer;
		
		//当前链接状态
		ConnectState _state;

		ISessionCreateListener* _sessionCreateListener;

		std::string _ip;
		int _port;
		std::string _workpath;
	public:

		//具体实现
		NetServer(bool server, std::string ip, int port, std::string workpath) :
			IsServer(server),
#ifdef PICNET_SERVER
			_serverAcceptor(nullptr),
#endif
			_clientEndpoint(nullptr),
			_sessionCreateListener(nullptr),
			_ip(ip),
			_port(port),
			_workpath(workpath),
			_state(ConnectState::NON){

		}

		//注册监听函数
		void SetSessionCreateListener(ISessionCreateListener* isner)
		{
			_sessionCreateListener = isner;
		}

		virtual int Initialize()
		{
			_state = ConnectState::INIT;
#ifdef PICNET_SERVER
			if (IsServer)
			{
				std::cout << "Net Server Init..." << std::endl;
				_serverAcceptor = new tcp::acceptor(io_server, tcp::endpoint(
					boost::asio::ip::address::from_string(_ip), _port));
				_clientEndpoint = nullptr;
			}
			else
			
#endif
			{
				std::cout << "Net Client Init..." << std::endl;
				_clientEndpoint = new  tcp::endpoint(
					boost::asio::ip::address::from_string(_ip), _port);
#ifdef PICNET_SERVER
				_serverAcceptor = nullptr;
#endif
			}

			RunThread();
			return 0;
		}


		void StartAsync()
		{
			_state = ConnectState::CONNECTING;
			SessionPtr newSession(new Session(io_server, &_group, _workpath));
#ifdef PICNET_SERVER
			if (IsServer)
			{
				_serverAcceptor->async_accept(newSession->Socket(),
					boost::bind(&NetServer::ConnecttHandler, this, boost::asio::placeholders::error, newSession));
			}
			else
#endif
			{
				newSession->Socket().async_connect(*_clientEndpoint,
					boost::bind(&NetServer::ConnecttHandler, this, boost::asio::placeholders::error, newSession));
			}
		}

		//当有TCP连接发生时，ConnecttHandler()函数将被调用，它使用socket对象发送数据
		void ConnecttHandler(const boost::system::error_code& ec, SessionPtr session)
		{		
			//检验错误码，并打印错误信息
			if (ec)
			{
				//客户端链接失败
				_state = ConnectState::CONNECT_FAIL;
				std::cout << boost::system::system_error(ec).what() << std::endl;
				return;
			}
			else{
				std::cout << "Connect Success" << std::endl;
				//客户端链接成功
				_state = ConnectState::CONNECTED;
				if (_sessionCreateListener != nullptr)
				{
					SessionWeakPtr wp = SessionWeakPtr(session);
					_sessionCreateListener->OnSessionCreated(wp);
				}
				session->Start();
			}


			if (IsServer)
			{
				StartAsync();
			}
			else{

			}
		}

		void NetThread()
		{
			StartAsync();
			io_server.run();
		}

		//删除线程
		virtual void Finalize()
		{
			_state = ConnectState::NON;
			io_server.stop();
			_netThread->interrupt();
			delete _netThread;
			_netThread = nullptr;
			_group.Clear();
		}

		virtual void Tick()
		{

		}

		//获取链接状态
		ConnectState GetConnectState(){
			if (_group.Count()==0
				&& _state == ConnectState::CONNECTED)
			{
				_state = ConnectState::CLOSE;
			}
			return _state;
		}

		void Stop()
		{

		}




		~NetServer(){
#ifdef PICNET_SERVER
			delete _serverAcceptor;
#endif
			if (_clientEndpoint != nullptr)
			{
				delete _clientEndpoint;
			}

		}

	private:
		//运行线程
		void RunThread()
		{
			_netThread = new boost::thread(boost::bind(&NetServer::NetThread, this));
		}
	};
}