#include "ParticleData.h"

ParticleData::ParticleData(Hdf5Data& h5Data, const RunMod& mod /*= SINGLE_THREAD*/)
	:XYData(h5Data,mod)
{

}

ParticleData::~ParticleData()
{

}

/**
* @brief ParticleData::findIndexFromXValueL 根据x的值返回左边的边界索引
* @param const float & x
* @return unsigned int
*/
unsigned int ParticleData::findIndexFromXValueL(const float& x)
{
	unsigned int index = particles.size()/2;
	
	Particle p;
	unsigned int add = 0;
	for (; index > 0 && index < particles.size();)
	{
		p = particles.at(index + add);
		if (p.x < x)
		{
			add += index;
		}		
		index = index / 2;
	}	

	return add;
}

/**
* @brief ParticleData::loadPoint 载入点数据
* @return bool
*/
bool ParticleData::loadPoint()
{
	Data::ListValuesPtr listValues;
	bool ok = autoModGetSourceData(listValues);

	if (!ok || !listValues || listValues->size() == 0)
		return false;
	particles.clear();
	
	particles.reserve(listValues->size() / 3 + 10);
	
	Particle p;
	Data::ValuesPtr values = *(listValues->begin());
	for (unsigned int i = 2; i < values->size(); i = i+3)
	{
		p.x = values->at(i - 2);
		p.y = values->at(i - 1);
		p.type = values->at(i);
		particles.push_back(p);
	}
	setPointSize(particles.size());
	initXYRang();
	Data::clearSourceData();

	return true;
}

/**
* @brief ParticleData::initXYRang 初始化xy的范围
* @return bool
*/
bool ParticleData::initXYRang()
{
	if (particles.size() <= 0)
		return false;
	//粒子的数据是x坐标的位置进行排序的
	Rang xr, yr;
	auto iter = particles.begin();
	xr.min = iter->x;
	iter = particles.end();
	iter--;
	xr.max = iter->x;

	iter = particles.begin();
	yr.min = yr.max = particles.begin()->y;
	for (; iter != particles.end(); iter++)
	{
		if (yr.min > iter->y)
			yr.min = iter->y;
		else if (yr.max < iter->y)
			yr.max = iter->y;
	}

	setXRang(xr);
	setYRang(yr);

	return true;
}

