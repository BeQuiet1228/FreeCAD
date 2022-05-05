extern "C" {
#include <lua/lua.h>
#include <lua/lualib.h>
#include <lua/lauxlib.h>
}
#include "GeneticAlgorithm.h"
#include <random>
#include <iostream>
#include <QString>
GeneticAlgorithm::GeneticAlgorithm()
{

}

GeneticAlgorithm::~GeneticAlgorithm()
{

}

/**
* 传入一个尺子。尺子从0开始，到1结束，中间刻度不需要均匀，随机抽取一些刻度的索引。
* 刻度越长，则抽取到的几率越大，抽取的刻度会有重复。
* @brief GeneticAlgorithm::getIndexsForRular 
* @param std::vector<float> rular
* @return std::vector<int>
*/
std::vector<int> GeneticAlgorithm::getIndexsForRular(std::vector<float> rular)
{
	int count = rular.size() / 2;

	std::vector<int> indexs;
	std::random_device rd;
	const float MaxRandom = 100000;
	std::uniform_int_distribution<int> distribution(0, MaxRandom);
	for (int i = 0; i<count;i++)
	{
		float randomF = distribution(rd)/MaxRandom;
		int j = 1;
		for (; j < rular.size(); j++)
		{
			if (randomF < rular.at(j))
				break;
		}
		//因为这里取尺子中间的索引。所以需要个数索引-1
		indexs.push_back(j - 1);
	}
	return indexs;
}

std::vector<float> GeneticAlgorithm::getVariate(QString str)
{
	std::vector<float> variates;
	auto vars = str.split(";\n");
	for (int i = 0; i < vars.size(); i++)
	{
		QString value = vars.at(i);
		if(value.isEmpty())
			continue;
		auto ls = value.split("=");
		if(ls.size() !=2)
			continue;
		auto s = ls.at(1);
		variates.push_back(s.toFloat());
	}
	return variates;
}

float GeneticAlgorithm::getRandom0To1()
{
	std::random_device rd;
	const float MaxRandom = 10000;
	std::uniform_int_distribution<int> distribution(0, MaxRandom);

	return distribution(rd) / MaxRandom;
}

void GeneticAlgorithm::optimize(SmartContorl* smartCOntrol)
{
	//获取目标F值，以及目标类型
	lua_getglobal(lua_state, "excpectF");
	double excpectF = lua_tonumber(lua_state,-1);
	lua_getglobal(lua_state, "excpectMod");
	int excpectFMod = lua_tointeger(lua_state, -1);
	
	auto historyDatas = smartCOntrol->getHistoryDatas();
	if (historyDatas.size() <= 0)
		return;
	SmartContorl::HistoryData  history = *historyDatas.rbegin();
	
	std::vector<float> functionValue;

	for (auto iter = history.datas.begin(); iter != history.datas.end(); iter++)
	{
		 float f = (*iter)->resultData->getValue(0);

		 //如果为接近目标，则修改f的值为越大越好
		 if (excpectFMod == 0)
		 {
			 f = abs(excpectF - f);
			 f = excpectF - f;
		 }

		 functionValue.push_back(f);
	}
	int count = functionValue.size();
	std::vector<float> rular;
	rular.push_back(0);
	double addValue = 0;
	for (auto iter = functionValue.begin(); iter != functionValue.end(); iter++)
	{
		addValue += *iter;
	}
	for (auto iter = functionValue.begin(); iter != functionValue.end(); iter++)
	{
		rular.push_back(*iter / addValue +(*rular.rbegin()));
	}

	auto indexs = getIndexsForRular(rular);

	
	std::vector<Variate> Variates = history.variates;
	for (auto iter = Variates.begin(); iter != Variates.end(); iter++) {
		iter->values.clear();
	}
	std::vector<int> pool1,pool2;
	//随机挑选两个个体进行交叉
	std::random_device rd;
	const int MaxRandom = indexs.size() - 1;
	std::uniform_int_distribution<int> distribution(0, MaxRandom);
	while(Variates.begin()->values.size()< count){

		int p1 = indexs[distribution(rd)];
		int p2 = indexs[distribution(rd)];

		//跳过重复抽取的
// 		if(p1 == p2)
// 			continue;
// 		bool ok = true;
// 		for (auto i = 0; i < pool1.size(); i++)
// 		{
// 			if (pool1[i] == p1 && pool2[i] == p2) {
// 				ok = false;
// 				break;
// 			}
// 			if (pool1[i] == p2 && pool2[i] == p1) {
// 				ok = false;
// 				break;
// 			}
// 
// 		}
// 		if(!ok)
// 			continue;
		pool1.push_back(p1);
		pool2.push_back(p2);

		QString variate1 = history.datas[p1]->variate;
		QString variate2 = history.datas[p2]->variate;

		auto vars1 = getVariate(variate1);
		auto vars2 = getVariate(variate2);

		//使用随机数生成一个β值
		float beta;
		{
			float r = getRandom0To1();
			if (r <= 0.5) {
				beta = pow((2 * r), 0.5);
			}else {
				beta = pow((2 - 2 * r), -0.5);
			}
		}

		if (vars1.size() != vars2.size())
		{
			std::cerr << "variate size not equal" << std::endl;
		}
		//将vars 覆盖为交叉之后变量
		std::vector<float> newVars1,newVars2;
		{
			int varCount = vars1.size();
			for (int i = 0; i < varCount; i++)
			{
				float var1 = ((1 - beta) * vars1[i] + (1 + beta) * vars2[i]) / 2;
				float var2 = ((1 + beta) * vars1[i] + (1 - beta) * vars2[i]) / 2;
				newVars1.push_back(var1);
				newVars2.push_back(var2);
			}
		}
		
		for (auto i = 0; i < Variates.size(); i++)
		{
			Variates[i].values.push_back(newVars1[i]);
			Variates[i].values.push_back(newVars2[i]);
		}

	}

	//变异
	{
		const double hitRata = 0.5;

		for (int i = 0;i < Variates.size();i++)
		{
			OPtimizeVariate var = optimizeVariates[i];
			for (int j = 0; j < Variates[i].values.size(); j++)
			{
				if (getRandom0To1() < hitRata)
				{
					double u = getRandom0To1();
					double n = 0.2;
					double temp;
					if (u <= 0.5) {
						temp = pow(2 * u + (1-2*u)*(1-(Variates[i].values[j] - var.min)/(var.max - var.min)), n) - 1;
					}else {
						temp = 1 - pow(2 * (1 - u) + 2 * (u - 0.5) * (1 - (var.max - Variates[i].values[j]) / (var.max - var.min)),n);
					}
					Variates[i].values[j] = Variates[i].values[j] + temp * (var.max - var.min);
				}
			}
		}
	}

	for each (auto  v in Variates)
	{
		smartCOntrol->addVariate(v);
	}

}

//完成所有的单元测试
void GeneticAlgorithm::test()
{
	/*
		样本抽取测试
	*/
	{
		std::vector<float> rular;
		rular.push_back(0);
		rular.push_back(0.1);
		rular.push_back(0.3);
		rular.push_back(0.5);
		rular.push_back(0.6);
		rular.push_back(0.9); 
		rular.push_back(1.0);
		
		std::cerr << "random indexs----" << std::endl;
		std::cerr << "rular: ";
		for each (float r in rular)
		{
			std::cerr << r << " ";
		}
		std::cerr << std::endl;

		auto indexs = getIndexsForRular(rular);
		std::cerr << "indexs: ";
		for each (int index in indexs)
		{
			std::cerr << index << " ";
		}
		std::cerr << std::endl;
	}
	//测试m3d解析
	{
		std::cerr << "Variate Analysis-----------" << std::endl;
		auto m3d = QString::fromLocal8Bit("a=2;\nb=3;\n");
		auto vars = getVariate(m3d);
		
		std::cerr << m3d.toStdString() << std::endl;
		std::cerr << "variate : ";
		for each(auto v in vars) {
			std::cerr << v << " ";
		}
		std::cerr <<  std::endl;
	}
}

