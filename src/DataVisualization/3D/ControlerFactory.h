#pragma once
#include <memory>
#include <string>
#include "DataVisualization3DExport.hpp"
class Hdf5Data;
namespace DV3D {
	class Controler;
	class DATA_VISUALIZATION_3D_EXPORT ControlerFactory {

	public:
		ControlerFactory() = default;
		~ControlerFactory() = default;

	public:
		static std::shared_ptr<Controler> CreatControler(Hdf5Data& h5data);
		//创建结构图控制器
		static std::shared_ptr<Controler> CreatStrucControler(Hdf5Data& h5data);
		//创建3d粒子图控制器
		static std::shared_ptr<Controler> CreatParticle3dControler(Hdf5Data& h5data);
		//创建等位图控制器
		static std::shared_ptr<Controler> CreatContourControler(Hdf5Data& h5data);
		//创建3d等位图
		static std::shared_ptr<Controler> CreatContour3dControler(Hdf5Data& h5data);
		//寻找字符串中的长度信息
		static int findStringAttribute(const std::string& str);
	};
}