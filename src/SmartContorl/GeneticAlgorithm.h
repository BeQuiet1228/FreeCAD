#pragma once
#include "OptimizeCurse.h"

class GeneticAlgorithm :public OptimizeCurseLua {
public:
	GeneticAlgorithm();
	~GeneticAlgorithm();

private:
	//随机抽取个体索引
	std::vector<int> getIndexsForRular(std::vector<float> rular);
	std::vector<float> getVariate(QString str);
	float getRandom0To1();
public:
	virtual void optimize(SmartContorl* smartCOntrol);

public:
	void test();

};