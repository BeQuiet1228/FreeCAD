#pragma once
#include <iostream>
#include <boost/bind.hpp>
#include <boost/shared_ptr.hpp>
#include <boost/enable_shared_from_this.hpp>
#include <boost/asio.hpp>
#include <queue>
#include <boost/thread/mutex.hpp>
#include <boost/lockfree/queue.hpp>
#include <set>
#include <direct.h>
#include<io.h>
#include "NetMsg.hpp"


namespace PicNet
{
	using boost::asio::ip::tcp;

	class SessionGroup;
	class Session;

	typedef boost::shared_ptr<Session> SessionPtr;
	typedef boost::weak_ptr<Session> SessionWeakPtr;

	class SessionGroup
	{
	public:
		void Add(SessionPtr session)
		{
			//线程锁
			boost::unique_lock<boost::mutex> lock(_mutex);
			_sessionSet.insert(session);
		}

		void Remove(SessionPtr session)
		{
			//线程锁
			boost::unique_lock<boost::mutex> lock(_mutex);
			_sessionSet.erase(session);
		}

		SessionPtr Top()
		{
			return *(_sessionSet.begin());
		}

		size_t Count()
		{
			return _sessionSet.size();
		}

		void Clear()
		{
			_sessionSet.clear();
		}

	private:
		std::set<SessionPtr> _sessionSet;
		boost::mutex _mutex;
	};

	class Session
		: public boost::enable_shared_from_this<Session>
	{
	private:

		tcp::socket _socket;
		SessionGroup* _group;
		NetMsgBuffer _buffer;

		//文件接收
		FileInfo _receiveFileInfo;
		FILE * _receiveFp;
		MsgPtr _receiveFileMsgPtr;

		//文件发送
		FILE * _sendFp;

		//接收消息的队列
		std::queue<MsgPtr> _receiveQueue;
		boost::mutex _receiveQueueMutex;

		//发送消息的队列
		std::queue<MsgPtr> _sendQueue;
		boost::mutex _sendQueueMutex;
		std::queue<FILE*> _sendFilePtr;

		//工作目录
		std::string _workpath;

		//用户目录
		std::string _userpath;

		//表明当前状态
		enum SessionReceiveState{ NON = 0, WAIT_HEAHDER, WAIT_BODY, WAIT_FILE, FINISH } ReceiveState;

		enum SessionSendState{ FREE = 0, SENDING_MSG, SENDING_FILE_MSG, SENDING_FILE } SendState;

		//传输进度比例
		float _transmissionRate;
	
		FileSizeType _sendFileSize;
	public:
		Session(boost::asio::io_service& io_service, SessionGroup* group, std::string workpath)
			: _socket(io_service),
			_group(group), _receiveFp(NULL), _workpath(workpath)
		{
			ReceiveState = NON;
			SendState = FREE;
		}

		~Session(){
			if (_receiveFp != NULL)
			{
				fclose(_receiveFp);
			}
			_socket.close();

			while (!_sendFilePtr.empty())
			{
				fclose(_sendFilePtr.front());
				_sendFilePtr.pop();
			}

			std::cout << "User Exit" << std::endl;
		}

		tcp::socket& Socket()
		{
			return _socket;
		}

		//每生成一个新的chat_session都会调用
		void Start()
		{
			_group->Add(shared_from_this());
			RestartReceiveHeader();
		}

		//异步接收消息头
		void HandleReadHeader(const boost::system::error_code& error)
		{
			if (!error && _buffer.DecodeHeader())
			{
				if (_buffer.CurrentMsgBodyLength() > 0)
				{
					StartReceiveBody();
				}
				else{
					InputReceive(_buffer.GetMsgFromRead());

					RestartReceiveHeader();
				}
			}
			else
			{
				time_t now = time(0);
				std::cout << "Error Header, Remove" <<" time:" <<now << std::endl;
				FinishSession();
			}
		}

		//异步接收消息体
		void HandleReadBody(const boost::system::error_code& error)
		{
			if (!error)
			{
				auto nm = _buffer.GetMsgFromRead();
				if (nm->GetType() == NetMsgHeader::MsgType::FILE_CONENT)
				{
					//取出对象
					_receiveFileInfo = *(nm->CastBody<FileInfo*>());

					if (_receiveFileInfo.FileSize == 0)
					{
						std::cout << "Error FILE_CONENT, Remove" << std::endl;
						FinishSession();
						return;
					}

					//暂存消息
					_receiveFileMsgPtr = MsgPtr(nm);

					//生成用户文件夹
					_userpath = _workpath + std::to_string(nm->GetRealUserCode()) + "\\";
					_mkdir(_userpath.c_str());

					_transmissionRate = 0;

					CreateReceiveFile();
					std::cout << "receive file size" << _receiveFileInfo.FileSize << std::endl;
					StartReceiveFile(_receiveFileInfo.FileSize);
				}
				else{
					//接收完毕
					InputReceive(_buffer.GetMsgFromRead());
					RestartReceiveHeader();
				}
			}
			else
			{
				std::cout << "Error Body, Remove" << std::endl;
				FinishSession();
			}
		}

		//异步接收文件内容的回调函数
		void HandleReceiveFile(const boost::system::error_code& error, size_t bytes_transferred, FileSizeType remaining)
		{
			//std::cout << "bytes_transferred: " << bytes_transferred << std::endl;
			//std::cout << "remaining: " << remaining << std::endl;
			if (error) {
				if (error != boost::asio::error::eof) {
					std::cerr << error.message() << "\n";
					FinishSession();
					return;
				}

				//总的大小不等于文件大小
				if (bytes_transferred > remaining)
					std::cerr << "file size dismach! " << bytes_transferred
					<< "/" << remaining << "\n";
				return;
			}
			if (!_receiveFp)
			{
				std::cerr << "write failed" << "\n";
				return;
			}

			remaining -= bytes_transferred;
			//得到传输比例
			_transmissionRate = static_cast<float>(_receiveFileInfo.FileSize - remaining) / _receiveFileInfo.FileSize;
			//写入文件
			fwrite(_buffer.ReceiveFileBuffer(), 1, bytes_transferred, _receiveFp);
			//std::cout << bytes_transferred / 1024<<"剩余：%lu\n"<< remaining / 1024<<std::endl;
			//反复调用receive_file_content函数，直到整个文件被接收完毕
			if (remaining > 0)
			{
				StartReceiveFile(remaining);
			}
			else{
				std::cout << "接收文件完成" << std::endl;

				_transmissionRate = 0;

				//完成接收文件，关闭句柄
				CompleteReceiveFile();

				//分发消息
				InputReceive(_receiveFileMsgPtr);

				//重置指针
				_receiveFileMsgPtr.reset();

				//重开接收消息头
				RestartReceiveHeader();

		
			}
		}

		void HandleSendNormalMsg(const boost::system::error_code& error)
		{
			if (!error)
			{
				boost::unique_lock<boost::mutex> lock(_sendQueueMutex);

				_sendQueue.pop();
				if (!_sendQueue.empty())
				{
					StartSendMsg();
				}
				else{
					//这个变量也要考虑同步问题
					SendState = FREE;
				}
			}
			else
			{
				_group->Remove(shared_from_this());
			}
		}
		void HandleSendFileMsg(const boost::system::error_code& error)
		{
			if (!error)
			{
				boost::unique_lock<boost::mutex> lock(_sendQueueMutex);
				_sendFp = _sendFilePtr.front();
				fseek(_sendFp, 0, SEEK_END);
				auto size = ftell(_sendFp);
				_transmissionRate = 0;
				_sendFileSize = size;
				StartSendFile(size);
			}
			else
			{
				_group->Remove(shared_from_this());
			}
		}

		//异步发送文件内容的回调函数
		void HandleSendFile(const boost::system::error_code& error, size_t bytes_transferred, FileSizeType remaining)
		{
			/*std::cout << "bytes_transferred: " << bytes_transferred << std::endl;
			std::cout << "remaining: " << remaining << std::endl;*/

			if (error) {
				if (error != boost::asio::error::eof) {
					std::cerr << error.message() << "\n";
					FinishSession();
					return;
				}

				//总的大小不等于文件大小
				if (bytes_transferred > remaining)
					std::cerr << "file size dismach " << bytes_transferred
					<< "/" << remaining << "\n";
				return;
			}
			remaining -= bytes_transferred;
			//得到传输比例
			_transmissionRate = static_cast<float>(_sendFileSize - remaining) / _sendFileSize;

			//反复调用receive_file_content函数，直到整个文件被接收完毕
			if (remaining > 0)
			{
				StartSendFile(remaining);
			}
			else{
				//完成接收文件，关闭句柄
				CompleteSendFile();
				boost::unique_lock<boost::mutex> lock(_sendQueueMutex);
				_sendFilePtr.pop();
				_sendQueue.pop();
				_transmissionRate = 0;
				if (!_sendQueue.empty())
				{
					StartSendMsg();
				}
				else{
					//这个变量也要考虑同步问题
					SendState = FREE;
				}
			}
		}

		//存在未取出的消息
		bool  ExistReceiveMsg()
		{
			boost::unique_lock<boost::mutex> lock(_receiveQueueMutex);
			return !_receiveQueue.empty();
		}

		//取出
		MsgPtr Get()
		{
			boost::unique_lock<boost::mutex> lock(_receiveQueueMutex);

			auto m = _receiveQueue.front();
			_receiveQueue.pop();
			return m;
		}

		//发送消息
		void Send(MsgPtr netMsg)
		{
			boost::unique_lock<boost::mutex> lock(_sendQueueMutex);

			_sendQueue.push(netMsg);

			if (SendState == FREE)
			{
				StartSendMsg();
			}
		}

		//发文件
		void SendFile(MsgPtr netMsg, FILE* fp)
		{
			boost::unique_lock<boost::mutex> lock(_sendQueueMutex);

			_sendQueue.push(netMsg);
			_sendFilePtr.push(fp);
			if (SendState == FREE)
			{
				StartSendMsg();
			}
		}

		//获取进度条
		float GetTransmissionRate()
		{
			return _transmissionRate;
		}

	private:
		//输入
		void InputReceive(MsgPtr netMsg)
		{
			boost::unique_lock<boost::mutex> lock(_receiveQueueMutex);
			_receiveQueue.push(netMsg);

		}

		//开始接收消息体
		void StartReceiveBody()
		{
			ReceiveState = WAIT_BODY;
			boost::asio::async_read(_socket,
				boost::asio::buffer(_buffer.ReadBodyBuffer(), _buffer.CurrentMsgBodyLength()),
				boost::bind(&Session::HandleReadBody, shared_from_this(),
				boost::asio::placeholders::error));
		}

		//重置到开始接收消息头
		void RestartReceiveHeader(){
			ReceiveState = WAIT_HEAHDER;
			boost::asio::async_read(_socket,
				boost::asio::buffer(_buffer.ReadBuffer(), _buffer.HeadLength()),
				boost::bind(
				&Session::HandleReadHeader, shared_from_this(),
				boost::asio::placeholders::error)); //异步读客户端发来的消息
		}

		//开始接收文件
		void StartReceiveFile(FileSizeType remaining)
		{
			ReceiveState = WAIT_FILE;

			if (remaining > _buffer.FileBlockSize())
			{
				//异步接收文件内容
				_socket.async_read_some(boost::asio::buffer(_buffer.ReceiveFileBuffer(), _buffer.FileBlockSize()),
					boost::bind(&Session::HandleReceiveFile, shared_from_this(), boost::asio::placeholders::error,
					boost::asio::placeholders::bytes_transferred, remaining));
			}
			else{
				size_t r = (size_t)remaining;
				//异步接收文件内容
				_socket.async_read_some(boost::asio::buffer(_buffer.ReceiveFileBuffer(), r),
					boost::bind(&Session::HandleReceiveFile, shared_from_this(), boost::asio::placeholders::error,
					boost::asio::placeholders::bytes_transferred, remaining));
			}
		}
		//开始发送文件
		void StartSendFile(FileSizeType remaining)
		{
			SendState = SENDING_FILE;
			long r = remaining;
			fseek(_sendFp, -r, SEEK_END);
			//写入文件
			auto wsize = fread(_buffer.SendFileBuffer(), 1, _buffer.FileBlockSize(), _sendFp);

			//异步接收文件内容
			_socket.async_write_some(boost::asio::buffer(_buffer.SendFileBuffer(), wsize),
				boost::bind(&Session::HandleSendFile, shared_from_this(), boost::asio::placeholders::error,
				boost::asio::placeholders::bytes_transferred, remaining));
		}

		//开始发送
		void StartSendMsg()
		{
			if (_sendQueue.front()->GetType() == NetMsgHeader::MsgType::FILE_CONENT)
			{
				SendState = SENDING_FILE_MSG;
				boost::asio::async_write(_socket,
					boost::asio::buffer(_sendQueue.front()->Data(),
					_sendQueue.front()->Length()),
					boost::bind(&Session::HandleSendFileMsg, shared_from_this(),
					boost::asio::placeholders::error));
			}
			else{
				SendState = SENDING_MSG;
				boost::asio::async_write(_socket,
					boost::asio::buffer(_sendQueue.front()->Data(),
					_sendQueue.front()->Length()),
					boost::bind(&Session::HandleSendNormalMsg, shared_from_this(),
					boost::asio::placeholders::error));
			}

		}

		//开始发送文件
		void StartSendFile(){
			SendState = SENDING_FILE;
		}

		//为了接收文件就创建一下
		void CreateReceiveFile()
		{
			//防止溢出
			_receiveFileInfo.Name[FILE_NAME_MAX_LENGTH - 1] = '\n';
			// 使用临时string代替Name
			std::string tempName = _receiveFileInfo.Name;
			std::string pathSub = "";
			//先判断_receiveFileInfo.Name中是否有其他路径
			int index = tempName.find_last_of("\\");
			//存在则提取路径
			if (index != -1){
				pathSub = tempName.substr(0, index);
				_userpath = _userpath + pathSub + "\\";

				tempName = tempName.substr(index + 1, strlen(tempName.c_str()));
			}
			//判断路径是否存在
			if (_access(_userpath.c_str(), 0) == -1){
				//创建路径
				_mkdir(_userpath.c_str());
			}
			auto e = fopen_s(&_receiveFp, (_userpath + tempName).c_str(), "wb+");
			while (e != NULL)
			{
				std::string timeName = changeFileName(tempName);
				e = fopen_s(&_receiveFp, (_userpath + timeName).c_str(), "wb+");
				std::cerr << "Can't write " << _receiveFileInfo.Name << " try:" << _userpath + timeName << "\n";
				//_receiveFileInfo.Name = (pathSub + "\\" + timeName).c_str();
				std::strcpy(_receiveFileInfo.Name, (pathSub + "\\" + timeName).c_str());

				auto m=_buffer.GetMsgFromRead();
				FileInfo file = *(m->CastBody<FileInfo*>());

				MsgPtr msg = NetMsg::CreateByFileAndSize(m->GetId(), _receiveFileInfo.Name, m->GetRealUserCode(), file.FileSize);
				_receiveFileMsgPtr = msg;
			}
			//if (e != NULL) {
			//	std::cerr << "Can't write " << _receiveFileInfo.Name << "\n";
			//	return;
			//}

		}
		//当文件被占用时，改一下文件名，在文件后面加上时间的秒
		std::string changeFileName(std::string fileName)
		{
			int seconds = time((time_t*)NULL);
			int index = fileName.find_last_of(".");
			std::string finalName = fileName.substr(0, index) + std::to_string(seconds) + fileName.substr(index, strlen(fileName.c_str()));
			return finalName;
		}
		//完成文件
		void CompleteReceiveFile()
		{
			if (_receiveFp != NULL)
			{
				fclose(_receiveFp);
			}
			_receiveFp = NULL;
		}
		//完成文件
		void CompleteSendFile()
		{
			if (_sendFp != NULL)
			{
				fclose(_sendFp);
			}
			_sendFp = NULL;
		}

		//结束本次会话
		void FinishSession()
		{
			ReceiveState = FINISH;

			_group->Remove(shared_from_this());
		}
	};
}