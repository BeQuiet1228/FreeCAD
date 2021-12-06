#pragma once
#include <memory>
#include <string>
class Hdf5Data;
namespace DV3D {
	class Controler;
	class ControlerFactory {

	public:
		ControlerFactory() = default;
		~ControlerFactory() = default;

	public:
		static std::shared_ptr<Controler> CreatControler(Hdf5Data& h5data);
		//创建结构图控制器
		static std::shared_ptr<Controler> CreatStrucControler(Hdf5Data& h5data);
		//寻找字符串中的长度信息
		static int findStringAttribute(const std::string& str);
	};
}