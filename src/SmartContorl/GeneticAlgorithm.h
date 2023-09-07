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
	std::vector<float> getVariate(QString str);
	float getRandom0To1();
	double getExcpectF();
	int getExcpectMod();
	double getBeta();
 	std::vector<float> getCurrentFs(SmartContorl* smartControl);
	std::vector<float> generatRular(std::vector<float> targetValues);
	void printBestF(SmartContorl* smartControl);
public:
 	virtual void optimize(SmartContorl* smartControl);

	//get set
	void setMutationProbability(const double& probability);
	double getMutationProbability();
	void setMutationProbabilityRange(const double& range);
	double getMutationProbabilityRange();
protected:
	//获取交叉池
	virtual std::vector<int> getCrossPool(SmartContorl* smartControl);

protected:
	ChipicRunDatas bestRunData;
	//结果最优的数据
	ChipicRunDataPtr resutData;
private:
	double mutationProbability;
	double mutationProbabilityRange;
public:
	void test();

};