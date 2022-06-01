#include "ParticleData.h"
#include "DataInformationGetter.h"
namespace DV {
	ParticleData::ParticleData(Hdf5Data& h5Data, const RunMod& mod /*= SINGLE_THREAD*/)
		:DirData(h5Data, mod), isLoadPoint(false),typeSize(0)
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
		unsigned int index = particles.size() / 2;

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
		if (isLoadPoint)
			return false;
		return loadPointHard();
	}

	/**
	* @brief ParticleData::loadPointHard 无论是否已经载入了，都重新载入
	* @return bool
	*/
	bool ParticleData::loadPointHard()
	{
		//载入原始数据
		Data::ListValuesPtr listValues;
		bool ok = autoModGetSourceData(listValues);

		if (!ok || !listValues || listValues->size() == 0)
			return false;
		particles.clear();
		//预分配vector的空间
		particles.reserve(listValues->size() / 3 + 10);

		//判断数据方向与结构图方向是否一致、不一致对数据位置进行一定调整
		unsigned int xIndex, yIndex;
		if (isTruedir())
		{
			xIndex = 1;
			yIndex = 2;
		}
		else {
			xIndex = 2;
			yIndex = 1;

			//跟换横纵标签
			auto xtag = getYTag();
			auto ytag = getXTag();
			setXTag(xtag);
			setYTag(ytag);
		}
		//获取粒子数据
		Particle p;
		Data::ValuesPtr values = *(listValues->begin());
		for (unsigned int i = 2; i < values->size(); i = i + 3)
		{
			p.d2 = values->at(i - yIndex);
			p.d1 = values->at(i - xIndex);
			p.type = values->at(i);
			particles.push_back(p);
		}

		//转换数据 并对数据进行排序
		transitionData();
		particleSort();

		//初始化范围
		setPointSize(particles.size());
		initXYRang();

		//清理掉原始数据
		Data::clearSourceData();

		isLoadPoint = true;

		//载入粒子颜色信息
		 std::vector<std::string> headList =  this->h5Data.headList;
		 if (headList.size() < 5)
			 return true;
		 QString str(headList[4].c_str());
		 str = str.split("=").at(1);
		 auto list = str.split(" ");
		 if (list.size() < 2)
			 return true;
		 typeSize = list.at(0).toInt();
		 for (int i = 1; i < list.size(); i++)
			 typeColors.push_back(list[i].toStdString());
		return true;
	}

	/**
	* @brief ParticleData::getParticle 获取数据 无越界风险
	* @param const unsigned int & index
	* @return ParticleData::Particle
	*/
	ParticleData::Particle ParticleData::getParticle(const unsigned int& index)
	{
		if (index >= particles.size())
		{
			Particle part;
			return part;
		}
		return getParticleHard(index);
	}

	/**
	* @brief ParticleData::getParticleHard 获取数据 不判断索引范围 又越界风险
	* @param const unsigned int & index
	* @return ParticleData::Particle
	*/
	ParticleData::Particle ParticleData::getParticleHard(const unsigned int& index)
	{
		return particles.at(index);
	}

	std::string ParticleData::getInformationTitle()
	{
		std::string title;
		const std::string end = "  ";
		title += "观察时间:";
		title += DataInformationGetter::getObserveTime(headList.at(11)) + end;
		title += "观察分量:";
		title += DataInformationGetter::getObserveObejct(headList.at(2)) + end;

		return title;
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
	/**
	* @brief ParticleData::transitionData 这里主要针对R-Theta方向的图进行一个数据转换
	* @return void
	*/
	void ParticleData::transitionData()
	{
		if (directionTyp == R_THETA)
		{
			for (auto part = particles.begin(); part != particles.end(); part++)
			{
				part->x = part->d1 * cos(part->d2);
				part->y = part->d1 * sin(part->d2);
			}
		}
		else {
			for (auto part = particles.begin(); part != particles.end(); part++)
			{
				part->y = part->d1;
				part->x = part->d2;
			}
		}

	}

	/**
	* @brief ParticleData::particleSort 给数据排序 增加找点、重绘操作的效率
	* @return void
	*/
	void ParticleData::particleSort()
	{
		//if (directionTyp == R_THETA)
		std::sort(particles.begin(), particles.end());
	}

	/*****************************************************/
	ParticleData::Particle::Particle() :x(0.0), y(0.0), type(0), d1(0.0), d2(0.0) {};
	bool ParticleData::Particle::operator >(const Particle& part) {
		return this->x > part.x;
	}
	bool ParticleData::Particle::operator <(const Particle& part) {
		return this->x < part.x;
	}
	bool ParticleData::Particle::operator ==(const Particle& part) {
		return this->x == part.x;
	}
};
