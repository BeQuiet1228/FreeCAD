#include  "MultipleTargetGeneticAlgorithm.h"

MultipleTargetGeneticAlgorithm::MultipleTargetGeneticAlgorithm()
{

}

MultipleTargetGeneticAlgorithm::~MultipleTargetGeneticAlgorithm()
{
	for (auto iter = targets.begin(); iter != targets.end(); iter++)
	{
		delete *iter;
	}
}

bool MultipleTargetGeneticAlgorithm::resultDataFilter(SmartContorl* smarControl)
{
	//清理数据 并将数据保存到历史
	smarControl->clearFinishData();
	//生成目标值
	std::vector<SmartContorl::HistoryData> historyDatas = smarControl->getHistoryDatas();
	if (historyDatas.size() < 1)
		return false;
	auto historyData = *historyDatas.rbegin();
	ChipicRunDatas runDatas = historyData.datas;
	std::list<TargetList> targetLists;
	for each (auto runData in runDatas) {
		TargetList targetList;
		targetList.rank = runData->rank;
	 	std::string hdf5Path = runData->h5FilePath.toStdString();
		for each (auto  target in targets)
		{
			double v = target->getTagetValue(hdf5Path);
#if 1 // 兼容之前的数据格式，临时实现查看目标趋势的功能
			runData->resultData->addValue(v);
#endif
			targetList.TargetValues.push_back(v);
		}
		targetLists.push_back(targetList);
	}
	currentTargetLists = targetLists;
	historyTargetList.push_back(currentTargetLists);
}


bool MultipleTargetGeneticAlgorithm::resultExpcet(SmartContorl* smartControl)
{
	
	for each (auto list in currentTargetLists) {
		bool ok = true;
		for (int i = 0;i < targets.size(); i++)
		{
			ok = ok && targets[i]->comparison(list.TargetValues[i], targets[i]->value);
		}
		if (ok)
			return ok;
	}

	return false;

}

void MultipleTargetGeneticAlgorithm::addTarget(Target* target)
{
	targets.push_back(target);
}

std::vector<int> MultipleTargetGeneticAlgorithm::getCrossPool(SmartContorl* smartControl)
{
	auto tempLists = currentTargetLists;
	TargetLayer layer;
	std::vector<int> indexs;

	while (indexs.size() < currentTargetLists.size() / 2)
	{
		layer = generateTargetListLayer(tempLists);

		if (layer.size() == 0)
			return indexs;
		auto list = layer.begin()->second;

		for each (auto t in list)
		{
			for (auto iter = tempLists.begin(); iter != tempLists.end();)
			{
				if (iter->rank == t.rank)
					iter = tempLists.erase(iter);
				else
					iter++;
			}
			indexs.push_back(t.rank);
			if (indexs.size() >= currentTargetLists.size() / 2)
				break;
		}

	}

	return indexs;
}

MultipleTargetGeneticAlgorithm::TargetLayer MultipleTargetGeneticAlgorithm::generateTargetListLayer(std::list<TargetList> targetLists)
{
	//清除之前的支配关系
	for each (auto t in targetLists)
	{
		t.parentCount = 0;
	}

	//建立目标之间的支配关系
	//支配 A个体中的所有目标都优于B个体中的目标，那么A支配B
	//需要计算出每个个体被支配的个数，以作为优劣排序的依据
	for each (auto list in targetLists) {

		for each (auto tempList in targetLists) {
			//不与自己相比
			if (list.rank == tempList.rank)
				continue;
			//对比所有参数
			bool ok = false;
			for (int i = 0; i < targets.size(); i++)
			{
				ok = ok || targets[i]->comparison(list.TargetValues[i], tempList.TargetValues[i]);
			}
			//如果没有一项目标值优于tempList，那么增加被支配数量
			if (!ok)
				list.parentCount++;

		}
	}

	//根据被支配次数划分层级
	TargetLayer layer;
	for each (auto list in targetLists)
	{
		auto iter = layer.find(list.parentCount);
		if (iter == layer.end())
		{
			std::list<TargetList> tl;
			tl.push_back(list);
			layer.insert(TargetLayer::value_type(list.parentCount, tl));
		}else{
			iter->second.push_back(list);
		}		
	}

	return layer;
}

