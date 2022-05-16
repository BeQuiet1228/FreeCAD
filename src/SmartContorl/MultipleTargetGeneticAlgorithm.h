#pragma  once

#include "OptimizeCurse.h"
#include "target.h"
#include "GeneticAlgorithm.h"
#include <vector>


class MultipleTargetGeneticAlgorithm :public GeneticAlgorithm{
public:
	struct TargetList
	{
		int rank = 0;	//个体序号
		std::vector<double> TargetValues;
		int parentCount = 0;//被支配的数量
	};
public:
	MultipleTargetGeneticAlgorithm();
	~MultipleTargetGeneticAlgorithm();

public:
	virtual bool resultDataFilter(SmartContorl* smarControl) override;
	virtual bool resultExpcet(SmartContorl* smartControl)override;

protected:
	virtual std::vector<int> getCrossPool(SmartContorl* smartControl) override;

private:
	using TargetLayer = std::map<int, std::list<TargetList>>;
	//生成支配关系层级
	TargetLayer generateTargetListLayer(std::list<TargetList> targetLists);
private:
	//所有的目标类型
	std::vector<Target*> targets;
	//当前次所有个体的目标值信息
	std::list<TargetList> currentTargetLists;
	//历史所有个体的目标值信息
	std::list<std::list<TargetList>> historyTargetList;
};
