#pragma  once
#include "Data.h"
#include <mutex>
#include <memory>
#include <vector>
#include "DirData.h"
class ParticleData :public DirData{
public:
	struct Particle{
		Particle():x(0.0), y(0.0), type(0),d1(0.0),d2(0.0){};
		float x, y;		//直角坐标系下的数据
		unsigned int type;

		float d1, d2;	//原始数据

		bool operator >(const Particle& part){
			return this->x > part.x;
		}
		bool operator <(const Particle& part){
			return this->x < part.x;
		}
		bool operator ==(const Particle& part){
			return this->x == part.x;
		}
	};

	//图表的类型
	enum Type{
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
protected:
	bool initXYRang() override;
	virtual void restorDeriveData(){};
public:
	std::vector<Particle> particles;

private:
	//是否已经载入点数据
	bool isLoadPoint;

private:
	//数据转换
	void transitionData();
	//排序
	void particleSort();
};


	
