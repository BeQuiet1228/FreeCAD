#include"DataProcess.h"
#include<list>
#include "HDF5Reader/hdf5io.h"
#include"algorithm"
#include"vtk-7.0/vtkSmartPointer.h"
#include"vtk-7.0/vtkPoints.h"
void processCirSingle(std::map<double, PlanData::PlanInfo>&cirPlan,
	std::map<double, std::map<PlanData::ValSolf, std::vector<PlanData::ValSolf>>>::iterator& it1,
	std::map<PlanData::ValSolf, std::vector<PlanData::ValSolf>>::iterator& it2,
	double& val_1,
	double& val_2);
namespace Data {
	using Value = std::vector<float>;
	using ValuesPtr = std::shared_ptr<Value>;
	using ListValues = std::list<ValuesPtr>;
	using ListValuesPtr = std::shared_ptr<ListValues>;
};
DataProcess::DataProcess()
{
	planePtr = std::shared_ptr<PlanData>(new PlanData());
}
DataProcess::~DataProcess()
{

}

bool DataProcess::initData(Hdf5Data& data)
{
	if (data.headList[3].find("PLANE") == std::string::npos)
		return false;
	//开始处理
	switch (data.coordinateSystem)
	{
	case Hdf5Data::CoordinateSystem::CARTESIAN:
	{
		planePtr->setDataType(PlanData::CASTESIAN);
		calcCartesian(data);
	}
	break;
	case Hdf5Data::CoordinateSystem::POLAR:
	{
		planePtr->setDataType(PlanData::POLAR);
		calcPolar(data);
	}
	break;
	case Hdf5Data::CoordinateSystem::CYLINDER:
	{
		planePtr->setDataType(PlanData::CYLINDER);
		calcCylinder(data);
	}
	break;
	}
	return true;
}

bool DataProcess::calcCartesian(Hdf5Data& data) {

	return true;
}
bool DataProcess::calcPolar(Hdf5Data& data) {
	return true;
}
bool DataProcess::calcCylinder(Hdf5Data& data) {
	//z-r-theta
	Data::ListValuesPtr sourceData(new Data::ListValues);
	//处理数据
	bool ok = Hdf5IO::getValue(data.listDataSet,*(sourceData.get()));
	if (!ok) return false;
	auto it = sourceData->begin();
	Data::ValuesPtr COLOR = *it; it++;
	Data::ValuesPtr NAME = *it; it++;
	Data::ValuesPtr datasetPla = *it;
	__int64 index = 0;
	for (auto iterval=datasetPla->begin();iterval!=datasetPla->end();index++)
	{
		PlanData::CirInfo temp;
		temp.zU = *iterval; iterval++;
		temp.rI = *iterval; iterval++;
		temp.sA= *iterval; iterval++;
		temp.zD= *iterval; iterval++;
		temp.rE = *iterval; iterval++;
		temp.eA = *iterval; iterval++;
		temp.proPer = *(NAME->begin() + index);
		planePtr->statisticalC(temp);
	}
	//处理面
	planePtr->mergePolyDataC();
	return true;
}

/****************************************************************************/
void PlanData::setDataType(DataType type)
{
	mDataType = type;
}
void PlanData::statisticalC(CirInfo& info) {
	//根据法线方向进行判断
	ValSolf angle(info.sA, info.eA);
	ValSolf rSolf(info.rI, info.rE);
	ValSolf zSolf(info.zU,info.zD);
	if (info.zU == info.zD)	{
		cylinderS[info.proPer].plans[info.zU][angle].push_back(rSolf);
	}
	else if (info.sA==info.eA) {
		cylinderS[info.proPer].verPlans[info.sA][zSolf].push_back(rSolf);
		cylinderS[info.proPer].releZ[info.sA].push_back(zSolf);
	}
	else if (info.rI==info.rE) {
		cylinderS[info.proPer].cirCutPlan[angle][info.rI].push_back(zSolf);
	}
}

void PlanData::mergePolyDataC()
{
	for (auto iter = cylinderS.begin(); iter != cylinderS.end(); iter++)
	{
		processCir(iter->second.plans);
		processVer(iter->second.verPlans, iter->second.releZ);
		processCirCut(iter->second.cirCutPlan);
	}
}
void PlanData::processCir(std::map<double, std::map<ValSolf, std::vector<ValSolf>>>& info){
	std::map<double, PlanInfo>cirPlan;
	//处理正投影面
	//z
	for (auto iter1=info.begin();iter1!=info.end();iter1++)
	{
		auto val1 = iter1->first;
		//angle
		for (auto iter2 = iter1->second.begin(); iter2 != iter1->second.end(); iter2++)
		{
			//排序,删除重复元素
			std::sort(iter2->second.begin(),iter2->second.end());
			std::vector<ValSolf>::iterator pos;
			pos = std::unique(iter2->second.begin(),iter2->second.end());
			iter2->second.erase(pos,iter2->second.end());
			double val_1, val_2;
			for (auto iter3 = iter2->second.begin(); iter3 != iter2->second.end(); iter3++)
			{
				if (iter3 == iter2->second.begin())
				{
					val_1 = iter3->val1;
					val_2 = iter3->val2;
				}
				else if(iter3->val1!=(iter3-1)->val2)
				{
					val_2 = (iter3 - 1)->val2;
					processCirSingle(cirPlan, iter1, iter2, val_1, val_2);
					val_1 = iter3->val1;
					val_2 = iter3->val2;
				}
			}
			val_2 = (iter2->second.end() - 1)->val2;
			processCirSingle(cirPlan, iter1, iter2, val_1, val_2);
		}
	}
	//装入
	for (auto iter = cirPlan.begin(); iter != cirPlan.end(); iter++)
	{
		vtkSmartPointer<vtkPoints> planPoints = vtkSmartPointer<vtkPoints>::New();
	}
}
void PlanData::processVer(std::map<double, std::map<ValSolf, std::vector<ValSolf>>>& pd, std::map<double, std::vector<ValSolf>>& pz)
{

}
void PlanData::processCirCut(std::map<ValSolf, std::map<double, std::vector<ValSolf>>>&info)
{

}
void processCirSingle(std::map<double, PlanData::PlanInfo>&cirPlan,
	std::map<double, std::map<PlanData::ValSolf, std::vector<PlanData::ValSolf>>>::iterator& it1,
	std::map<PlanData::ValSolf, std::vector<PlanData::ValSolf>>::iterator& it2,
	double& val_1,
	double& val_2)
{
	PlanData::Points p1 = { val_1 * cos(it2->first.val1),val_1 * sin(it2->first.val1),it1->first };
	PlanData::Points p2 = { val_1 * cos(it2->first.val2),val_1 * sin(it2->first.val2),it1->first };
	PlanData::Points p3 = { val_2 * cos(it2->first.val2),val_2 * sin(it2->first.val2),it1->first };
	PlanData::Points p4 = { val_2 * cos(it2->first.val1),val_2 * sin(it2->first.val1),it1->first };
	__int64 lastSize = cirPlan[it1->first].points.size();
	PlanData::FaceIndex f1 = {0+lastSize,1+lastSize,2+lastSize};
	PlanData::FaceIndex f2 = {0+lastSize,2+lastSize,3+lastSize};
	cirPlan[it1->first].points.push_back(p1);
	cirPlan[it1->first].points.push_back(p2);
	cirPlan[it1->first].points.push_back(p3);
	cirPlan[it1->first].points.push_back(p4);
	cirPlan[it1->first].faces.push_back(f1);
	cirPlan[it1->first].faces.push_back(f2);
}