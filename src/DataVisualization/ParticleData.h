#pragma  once
#include "Data.h"
#include <mutex>
#include <memory>
#include <vector>
#include "DirData.h"
#include"exportConfig.hpp"
namespace DV {
	class DATA_VISUALIZATION_EXPORT ParticleData :public DirData {
	public:
		struct Particle {
			Particle();
			float x, y;		//直角坐标系下的数据
			unsigned int type;

			float d1, d2;	//原始数据

			bool operator >(const Particle& part);
			bool operator <(const Particle& part);
			bool operator ==(const Particle& part);
		};

		//图表的类型
		enum Type {
			NEED_STRUCT = 0,
			NEEDLESS_STRUCT
		};
	public:
		ParticleData(Hdf5Data& h5Data, const RunMod& mod = SINGLE_THREAD);
		~ParticleData();
	public:
		unsigned int findIndexFromXValueL(const float& x) override;
		//载入点
		virtual bool loadPoint() override;
		bool loadPointHard();
		//根据索引获取一个粒子数据
		Particle getParticle(const unsigned int& index);
		Particle getParticleHard(const unsigned int& index);
		//获取图表信息
		std::string getInformationTitle() override;
		//设置粒子显示与否
		void setDisplayParticle(const int& index,const bool& b = true);
		bool getDisplayParticle(const int& index);
	protected:
		bool initXYRang() override;
		virtual void restorDeriveData() {};
	public:
		std::vector<Particle> particles;
		//粒子种类数量
		int typeSize;
		//粒子颜色
		std::vector<std::string> typeColors;
	private:
		//是否已经载入点数据
		bool isLoadPoint;
		//粒子显示开关
		std::vector<bool> particleDisplaySwitch;
	private:
		//数据转换
		void transitionData();
		//排序
		void particleSort();
	};
};



	
