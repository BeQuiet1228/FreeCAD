#pragma once

#define BOOST_SPIRIT_THREADSAFE
#include <boost/property_tree/ptree.hpp>  
#include <boost/property_tree/json_parser.hpp>  
#include <boost/thread.hpp>
#include <boost/thread/lock_guard.hpp>
#include <boost/thread/mutex.hpp>
#include <boost/thread/thread.hpp>

#include<string>

#include"NetMsg.hpp"

//json 文件的根节点名称
#define JSONROOT      "user"
//userid名称
#define JSONUSERID    "UserId"
#define JSONPASSWORD  "Password"
namespace PicNet {
	class UserJson
	{
	public:
		UserJson() {}
		~UserJson() {
		}
		UserJson(const UserJson&) = delete;
		UserJson &operator=(const UserJson) = delete;

		//验证一个user是否登录成功
		bool vaildLogin(UserInfoPtr userptr) {
			//int userId = userptr->getUserId();
			//std::string password = userptr->getPassward();

			boost::property_tree::ptree root;
			boost::property_tree::ptree items;
			boost::property_tree::read_json<boost::property_tree::ptree>(_userJsonFile, root);


			items = root.get_child(JSONROOT);
			for (boost::property_tree::ptree::iterator it = items.begin(); it != items.end(); ++it)
			{
				//遍历读出数据  
				//string key = it->first;//key ID 
				try {
					int userid = it->second.get<int>(JSONUSERID);
					std::string password = it->second.get<std::string>(JSONPASSWORD);
					if (userid == userptr->getUserId() && password == userptr->getPassward()) {
						return true;
					}
				}
				catch (boost::property_tree::ptree_error &e) {
					std::cout << "valid user failed!" << std::endl;
					return false;

				}

			}
			return false;
		}
	private:



	private:
		//向json中添加一个user信息
		//bool addUserInfo() {};
	private:
		std::string _userJsonFile = "UsersInfo.json";
	};

	typedef Singleton<UserJson> UserJsonSingleton;
}

//
//#pragma once
//
//#define BOOST_SPIRIT_THREADSAFE
//#include <boost/property_tree/ptree.hpp>  
//#include <boost/property_tree/json_parser.hpp>  
//#include <boost/thread.hpp>
//#include <boost/thread/lock_guard.hpp>
//#include <boost/thread/mutex.hpp>
//#include <boost/thread/thread.hpp>
//
//#include<string>
//#include<iostream>
//#include"NetMsg.hpp"
//
////json 文件的根节点名称
//#define JSONROOT      "user"
////userid名称
//#define JSONUSERID    "UserId"
//#define JSONPASSWORD  "Password"
//namespace PicNet {
//	class UserJsonSingleton
//	{
//	public:
//		typedef boost::shared_ptr<UserJsonSingleton> userJsonPtr;
//		~UserJsonSingleton() {
//		}
//		UserJsonSingleton(const UserJsonSingleton&) = delete;
//		UserJsonSingleton &operator=(const UserJsonSingleton) = delete;
//
//		static userJsonPtr get_instance() {
//			if (m_instance_ptr == nullptr) {
//				boost::lock_guard<boost::mutex> lk(m_mutex);
//				if (m_instance_ptr == nullptr) {
//					m_instance_ptr = boost::shared_ptr<UserJsonSingleton>(new UserJsonSingleton);
//				}
//				return m_instance_ptr;
//			}
//		}
//
//		//验证一个user是否登录成功
//		bool vaildLogin(UserInfoPtr userptr) {
//			//int userId = userptr->getUserId();
//			//std::string password = userptr->getPassward();
//
//			boost::property_tree::ptree root;
//			boost::property_tree::ptree items;
//			boost::property_tree::read_json<boost::property_tree::ptree>(_userJsonFile, root);
//
//
//			items = root.get_child(JSONROOT);
//			for (boost::property_tree::ptree::iterator it = items.begin(); it != items.end(); ++it)
//			{
//				//遍历读出数据  
//				//string key = it->first;//key ID 
//				try {
//					int userid = it->second.get<int>(JSONUSERID);
//					std::string password = it->second.get<std::string>(JSONPASSWORD);
//					if (userid == userptr->getUserId() && password == userptr->getPassward()) {
//						return true;
//					}
//				}
//				catch (boost::property_tree::ptree_error &e) {
//					std::cout << "valid user failed!" << std::endl;
//					return false;
//
//				}
//
//			}
//			return false;
//		}
//	private:
//		UserJsonSingleton() {}
//		static userJsonPtr m_instance_ptr;
//		static boost::mutex m_mutex;
//
//	private:
//		//向json中添加一个user信息
//		//bool addUserInfo() {};
//	private:
//		std::string _userJsonFile = "UsersInfo.json";
//	};
//
//	UserJsonSingleton::userJsonPtr UserJsonSingleton::m_instance_ptr = nullptr;
//	boost::mutex UserJsonSingleton::m_mutex;
//}
