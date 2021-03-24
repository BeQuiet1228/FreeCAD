#pragma  once
#include "Data.h"
#include <mutex>
#include <memory>
#include <vector>
class ParticleData :public XYData{
public:
	struct Particle{
	Particle():x(0.0), y(0.0), type(0){};
		float x, y;
		unsigned int type;
	};
public: 
	ParticleData(Hdf5Data& h5Data, const RunMod& mod = SINGLE_THREAD);
	~ParticleData();
public:
	unsigned int findIndexFromXValueL(const float& x) override;
	virtual bool loadPoint() override;
	//获取一个点的数据
protected:
	bool initXYRang() override;
	virtual void restorDeriveData(){};
public:
	std::vector<Particle> particles;
};


	
