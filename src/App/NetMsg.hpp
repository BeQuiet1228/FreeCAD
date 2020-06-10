#pragma once

#include <boost/property_tree/ptree.hpp>  
#include <boost/property_tree/json_parser.hpp>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <io.h>


#define BLOCK_SIZE 66000
#define FILE_BLOCK_SIZE 1024*64
#define HEADER_LENGTH 32 
#define MAX_BODY_LENGTH 65535 
#define FILE_NAME_MAX_LENGTH 64

//userid名称
#define JSONUSERID    "UserId"
#define JSONPASSWORD  "Password"

namespace PicNet
{
	typedef long long FileSizeType;

	struct FileInfo {
		FileSizeType FileSize;
		char Name[FILE_NAME_MAX_LENGTH];
		FileInfo() : FileSize(0) {}
	};

	struct WinMsgInfo {

		int wParam;
		int lParam;
	};
	/*fubiao*/
	class UserInfo {
	public:
		UserInfo() {};
		UserInfo(int userid, std::string password) {
			_userId = userid;
			_password = password;
		}
		~UserInfo() {};
		//将json字符串转化为对象
		bool InstanceByjsonStr(std::string jsonStr) {
			std::stringstream stream(jsonStr);
			boost::property_tree::ptree strTree;
			try {
				boost::property_tree::read_json<boost::property_tree::ptree>(stream, strTree);
			}
			catch (boost::property_tree::ptree_error &e) {
				std::cout << e.what() << std::endl;
				return false;
			}
			try {
				_userId = strTree.get<int>(JSONUSERID);
				_password = strTree.get<std::string>(JSONPASSWORD);
			}
			catch (boost::property_tree::ptree_error &e) {
				std::cout << e.what() << std::endl;
				std::cout << "json parse failed!\n" << std::endl;
				return false;
			}
			return true;
		}
		//将对象转化为jsonStr
		std::string ToJsonStr() {
			std::string jsonStr = "";
			boost::property_tree::ptree strTree;
			strTree.put(JSONUSERID, _userId);
			strTree.put(JSONPASSWORD, _password);
			std::stringstream s;
			try {
				boost::property_tree::write_json(s, strTree);
			}
			catch (boost::property_tree::ptree_error &e) {
				std::cout << e.what() << std::endl;
				std::cout << "user to json failed!\n" << std::endl;
			}
			jsonStr = s.str();
			return jsonStr;
		}

		inline int getUserId() {
			return _userId;
		}
		inline std::string getPassward() {
			return _password;
		}
		inline void setUserId(int id) {
			_userId = id;
		}
		inline void setPassword(std::string password) {
			_password = password;
		}

	private:
		int _userId;
		std::string _password;
	};

	typedef boost::shared_ptr<UserInfo> UserInfoPtr;

	//消息头
	class NetMsgHeader{

	public:
		enum MsgType{
			ID_COMMAD = 1,
			MSG_COMMAD,
			STRING,
			FILE_CONENT
		};
		//用于检查数据是否有误


		//消息长度
		//size_t Length;
		int Length;

		//消息类型
		MsgType Type;

		//消息Id
		int Id;

		//用户验证码
		int UserCode;
	};



	//定义消息本体
	class NetMsg {
	public:
		//根据指针和长度初始化该消息
		NetMsg(char* allData, size_t length){
			NetMsgHeader* h = reinterpret_cast<NetMsgHeader*>(allData);
			_length = length;
			_header = *h;
			_data = new char[_length];
			memcpy(_data, allData, _length);
		}

		NetMsg(NetMsgHeader header, const char* exdata)
		{
			_header = header;
			_length = _header.Length;
			_data = new char[_length];
			memcpy(_data, &_header, HEADER_LENGTH);
			if (_length > HEADER_LENGTH && exdata != nullptr)
			{
				memcpy(_data + HEADER_LENGTH, exdata, _length - HEADER_LENGTH);
			}
		}

		char* Data()
		{
			return _data;
		}

		size_t Length()
		{
			return _length;
		}

		NetMsgHeader::MsgType GetType()
		{
			return _header.Type;
		}

		int GetId(){
			return _header.Id;
		}
		int GetRealUserCode(){
			return _header.UserCode & 0x000FFFFF;
		}


		template <typename T>
		T CastBody()
		{
			return reinterpret_cast<T>(_data + HEADER_LENGTH);
		}

		//生成一个
		static boost::shared_ptr<NetMsg> Create(NetMsgHeader::MsgType type, int id, size_t bodyLength, const char* body, int usercode)
		{
			NetMsgHeader header;
			header.Type = type;
			header.Id = id;
			header.Length = bodyLength + HEADER_LENGTH;
			header.UserCode = 712 << 20 | usercode;
			boost::shared_ptr<NetMsg> msg(new NetMsg(header, body));
			return msg;
		}
		//生成一个文件传送消息
		static boost::shared_ptr<NetMsg> CreateByFile(int id,
			std::string fileName, int usercode, FILE* fp)
		{
			FileInfo info;
			memcpy(info.Name, fileName.c_str(), fileName.length() + 1);

			//获取大小
			//auto size = _filelength(_fileno(fp));
			auto size = filesize(fileName.c_str());
			info.FileSize = size;
			NetMsgHeader header;
			header.Type = NetMsgHeader::FILE_CONENT;
			header.Id = id;
			header.Length = sizeof(info) + HEADER_LENGTH;
			header.UserCode = 712 << 20 | usercode;


			boost::shared_ptr<NetMsg> msg(new NetMsg(header, (char*)&info));
			return msg;
		}
		//获取一个文件的字节数，可以超过2G
		static __int64 filesize(const char *   path)

		{
			_finddatai64_t filefind;
			int   done = 0;
			long long  handle;
			__int64 fs = -1;
			if ((handle = _findfirsti64(path, &filefind)) == -1) return -1;


			if (!(_A_SUBDIR == (_A_SUBDIR & filefind.attrib)))
			{
				fs = filefind.size;

			}
			_findclose(handle);
			return fs;

		}
		//@伏彪,
		//生成一个文件传送消息
		static boost::shared_ptr<NetMsg> CreateByFileAndSize(int id,
			std::string fileName, int usercode, FileSizeType size)
		{
			FileInfo info;
			memcpy(info.Name, fileName.c_str(), fileName.length() + 1);

			//获取大小
			//auto size = _filelength(_fileno(fp));
			info.FileSize = size;
			NetMsgHeader header;
			header.Type = NetMsgHeader::FILE_CONENT;
			header.Id = id;
			header.Length = sizeof(info) + HEADER_LENGTH;
			header.UserCode = 712 << 20 | usercode;


			boost::shared_ptr<NetMsg> msg(new NetMsg(header, (char*)&info));
			return msg;
		}

		~NetMsg()
		{
			delete[] _data;
		}

	private:
		NetMsgHeader _header;

		size_t _length;
		char* _data;

	};
	typedef boost::shared_ptr<NetMsg> MsgPtr;

	//定义消息缓冲
	class NetMsgBuffer{
	private:
		char _fileBuffer[FILE_BLOCK_SIZE];
		char _sendFileBuffer[FILE_BLOCK_SIZE];
		char _readBuffer[BLOCK_SIZE];
		char _writeBuffer[BLOCK_SIZE];
		size_t _currentMsgBodyLength;
	public:
		//获取Buffer
		char* ReadBuffer(){
			return _readBuffer;
		}
		//获取Buffer
		char* WriteBuffer(){
			return _writeBuffer;
		}


		char* ReadBodyBuffer(){
			return _readBuffer + HeadLength();
		}

		size_t HeadLength(){
			return HEADER_LENGTH;
		}
		size_t CurrentMsgBodyLength(){
			return _currentMsgBodyLength;
		}

		char* ReceiveFileBuffer()
		{
			return _fileBuffer;
		}

		char* SendFileBuffer()
		{
			return _sendFileBuffer;
		}
		size_t FileBlockSize()
		{
			return FILE_BLOCK_SIZE;
		}

		//读写的缓冲大小
		size_t RWBufferSize()
		{
			return BLOCK_SIZE;
		}

		//
		bool DecodeHeader(){
			int* size = reinterpret_cast<int*>(_readBuffer);

			if (*size > MAX_BODY_LENGTH || *size < HEADER_LENGTH)
			{
				return false;
			}

			NetMsgHeader* h = reinterpret_cast<NetMsgHeader*>(_readBuffer);
			//检查消息头是否正确
			if (((h->UserCode) & 0xFFF00000) >> 20
				!= 712)
			{
				return false;
			}

			_currentMsgBodyLength = *size - HEADER_LENGTH;
			return true;
		}

		//
		MsgPtr GetMsgFromRead()
		{
			//这里转移给NetMsg控制
			auto p = MsgPtr(new NetMsg(_readBuffer, _currentMsgBodyLength + HEADER_LENGTH));

			return p;
		}
	};

}