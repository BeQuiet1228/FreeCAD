#pragma once
#include "OptimizeCurse.h"
#include <vector>

class GeneticAlgorithm :public OptimizeCurseLua {
public:
	GeneticAlgorithm();
	~GeneticAlgorithm();

private:
	//随机抽取个体索引
	std::vector<int> getIndexsForRular(std::vector<float> rular);
	//获取交叉池
	std::vector<int> getCrossPool(SmartContorl* smartControl);
	std::vector<float> getVariate(QString str);
	float getRandom0To1();
	double getExcpectF();
	int getExcpectMod();
	double getBeta();
 	std::vector<float> getCurrentFs(SmartContorl* smartControl);
	std::vector<float> generatRular(std::vector<float> targetValues);
public:
 	virtual void optimize(SmartContorl* smartControl);

public:
	void test();

};