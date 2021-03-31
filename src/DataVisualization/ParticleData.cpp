#include "ParticleData.h"

ParticleData::ParticleData(Hdf5Data& h5Data, const RunMod& mod /*= SINGLE_THREAD*/)
	:XYData(h5Data, mod), directionTyp(NONE), mapType(NEEDLESS_STRUCT), isLoadPoint(false)
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
	//初始化图信息 
	initInformation();
	initDiretion();

	//载入原始数据
	Data::ListValuesPtr listValues;
	bool ok = autoModGetSourceData(listValues);

	if (!ok || !listValues || listValues->size() == 0)
		return false;
	particles.clear();

	particles.reserve(listValues->size() / 3 + 10);

	Particle p;
	Data::ValuesPtr values = *(listValues->begin());
	for (unsigned int i = 2; i < values->size(); i = i + 3)
	{
		p.d2 = values->at(i - 2);
		p.d1 = values->at(i - 1);
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

	return true;
}

/**
* @brief ParticleData::initDiretion 根据坐标轴tag，初始化图的方向
* @return void
*/
void ParticleData::initDiretion()
{
	QString xt = QString::fromStdString(getXTag());
	QString yt = QString::fromStdString(getYTag());
	
	if (xt.indexOf('(') < 0 || yt.indexOf('(') < 0)
		return;
	QString xd = xt.split('(').at(0);
	QString yd = yt.split('(').at(0);

	directionTyp = DirectionType(QStringToDirection(xd.toStdString()) | QStringToDirection(yd.toStdString()));
	if (directionTyp == NONE)
		mapType = NEEDLESS_STRUCT;
	else
		mapType = NEED_STRUCT;

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
* @brief ParticleData::QStringToDirection 将字符串转换为坐标类型
* @param const QString & str
* @return DirectionType
*/
DirectionType ParticleData::QStringToDirection(const std::string& str)
{
	DirectionType direction;

	if (str == "X ")
		direction = X;
	else if (str == "Y ")
		direction = Y;
	else if (str == "Z ")
		direction = Z;
	else if (str == "R ")
		direction = R;
	else if (str == "R*cos")
		direction = R;
	else if (str == "R*sin")
		direction = THETA;
	else
		direction = NONE;

	return direction;
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
			part->x = part->d1*sin(part->d2);
			part->y = part->d1*cos(part->d2);
		}
	}else{
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
		std::sort(particles.begin(),particles.end());
}
