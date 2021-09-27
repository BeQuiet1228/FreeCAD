#include"DataProcess.h"
#include<list>
#include "HDF5Reader/hdf5io.h"
#include"algorithm"
#include"vtk-7.0/vtkSmartPointer.h"
#include"vtk-7.0/vtkPoints.h"
#include"vtk-7.0/vtkFloatArray.h"
#include"vtk-7.0/vtkCellArray.h"
#include"vtk-7.0/vtkPolyData.h"
#include"vtk-7.0/vtkPointData.h"
#include"vtk-7.0/vtkAppendPolyData.h"
#include"vtk-7.0/vtkCleanPolyData.h"
void processCirSingle(std::map<double, PlanData::PlanInfo>&cirPlan,
	std::map<double, std::map<PlanData::ValSolf, std::vector<PlanData::ValSolf>>>::iterator& it1,
	std::map<PlanData::ValSolf, std::vector<PlanData::ValSolf>>::iterator& it2,
	double& val_1,
	double& val_2);
void processVerSingle(PlanData::PlanInfo& pf,
	std::map<double, std::map<PlanData::ValSolf, std::vector<PlanData::ValSolf>>>::iterator& it1,
	std::map<PlanData::ValSolf, std::vector<PlanData::ValSolf>>::iterator& it2,
	std::vector<PlanData::ValSolf>::iterator& it3);
void processCirCutSingle(PlanData::PlanInfo& info,
	std::map<PlanData::ValSolf, std::map<double, std::vector<PlanData::ValSolf>>>::iterator& it1,
	std::map<double, std::vector<PlanData::ValSolf>>::iterator& it2,
	std::vector<PlanData::ValSolf>::iterator& it3);
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
vtkSmartPointer<vtkPolyData> PlanData::processCir(std::map<double, std::map<ValSolf, std::vector<ValSolf>>>& info){
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
	vtkSmartPointer<vtkAppendPolyData> appendData = vtkSmartPointer<vtkAppendPolyData>::New();
	for (auto iter = cirPlan.begin(); iter != cirPlan.end(); iter++)
	{
		vtkSmartPointer<vtkPoints> planPoints = vtkSmartPointer<vtkPoints>::New();
		vtkSmartPointer<vtkCellArray> planCell = vtkSmartPointer<vtkCellData>::New();
		vtkSmartPointer<vtkFloatArray> planscalaes = vtkSmartPointer<vtkFloatArray>::New();
		for (__int64 i=0;i<iter->second.points.size();i++)
		{
			planPoints->InsertPoint(i,iter->second.points[i].data());
			planscalaes->InsertTuple1(i, i);
		}
		for (auto &&i:iter->second.faces)
		{
			planCell->InsertNextCell(vtkIdType(i.size()),i.data());
		}
		vtkSmartPointer<vtkPolyData> planPolydata = vtkSmartPointer<vtkPolyData>::New();
		planPolydata->SetPoints(planPoints);
		planPolydata->SetPolys(planCell);
		planPolydata->GetPointData()->SetScalars(planscalaes);
		appendData->AddInputData(planPolydata);
	}
	appendData->Update();
	vtkSmartPointer<vtkCleanPolyData> cleanPolyData = vtkSmartPointer<vtkCleanPolyData>::New();
	cleanPolyData->SetInputConnection(appendData->GetOutputPort());
	cleanPolyData->Update();
	vtkSmartPointer<vtkPolyData> newdata = vtkSmartPointer<vtkPolyData>::New();
	newdata->ShallowCopy(cleanPolyData->GetOutput());
	return newdata;
}
vtkSmartPointer<vtkPolyData> PlanData::processVer(std::map<double, std::map<ValSolf, std::vector<ValSolf>>>& pd, 
	std::map<double, std::vector<ValSolf>>& pz)
{
	//确认顶点
	std::map<double, std::map<ValSolf, std::vector<ValSolf>>>calcVerPlans;
	for (auto iter1=pd.begin();iter1!=pd.end();iter1++)
	{
		std::sort(pz[iter1->first].begin(),pz[iter1->first].end());
		std::vector<ValSolf>::iterator posz;
		posz = std::unique(pz[iter1->first].begin(), pz[iter1->first].end());
		pz[iter1->first].erase(posz,pz[iter1->first].end());
		//z
		for (auto iter2 = iter1->second.begin(); iter2 != iter1->second.end(); iter2++)
		{
			//排序，删除元素
			std::sort(iter2->second.begin(),iter2->second.end());
			std::vector<ValSolf>::iterator pos;
			pos = std::unique(iter2->second.begin(),iter2->second.end());
			iter2->second.erase(pos,iter2->second.end());
			double val_1;
			double val_2;
			for (auto iter3 = iter2->second.begin(); iter3 != iter2->second.end(); iter3++)
			{
				if (iter3 == iter2->second.begin())
				{
					val_1 = iter3->val1;
					val_2 = iter3->val2;
				}
				else if (iter3->val1!=(iter3-1)->val2)
				{
					val_2 = (iter3 - 1)->val2;
					ValSolf valSolf(val_1,val_2);
					calcVerPlans[iter1->first][iter2->first].push_back(valSolf);
					val_1 = iter3->val1;
					val_2 = iter3->val2;
				}
			}
			val_2 = (iter2->second.end() - 1)->val2;
			ValSolf valSolf(val_1, val_2);
			calcVerPlans[iter1->first][iter2->first].push_back(valSolf);
		}
	}
	//生成点位
	std::map<double, std::map<ValSolf, std::vector<ValSolf>>> retalmap;
	for (auto iter1 = pz.begin(); iter1 != pz.end(); iter1++)
	{
		for (auto iter2 = iter1->second.begin(); iter2 != iter1->second.end(); iter2++)
		{
			auto iter3 = calcVerPlans[iter1->first].find(*iter2);
			if (iter3 == calcVerPlans[iter1->first].end())
				continue;
			for (__int64 i = 0; i < iter3->second.size(); i++)
			{
				double zU = iter2->val1;
				double zD = iter2->val2;
				double rI = iter3->second[i].val1;
				double rE = iter3->second[i].val2;
				auto iter2Next = iter2 + 1;
				while (iter2Next!=iter1->second.end()&& calcVerPlans[iter1->first].find(*iter2Next)!=
					calcVerPlans[iter1->first].end())
				{
					if (iter2Next->val1 != (iter2Next - 1)->val2)
						break;
					auto rlist = calcVerPlans[iter1->first].find(*iter2Next);
					__int64 indexj = -1;
					for (__int64 j = 0; j < rlist->second.size(); j++)
					{
						if (rlist->second[j] == iter3->second[i])
						{
							indexj = j;
							break;
						}
					}
					if (-1 == indexj)break;
					zD = iter2Next->val2;
					rlist->second.erase(rlist->second.begin()+indexj);
					if (0 == rlist->second.size()) {
						calcVerPlans[iter1->first].erase(rlist);
						iter2Next++;
					}
				}
				ValSolf	zvalSolf(zU, zD);
				ValSolf	rvalSolf(rI,rE);
				retalmap[iter1->first][zvalSolf].push_back(rvalSolf);
			}
			calcVerPlans[iter1->first].erase(iter3);
		}
	}
	//处理垂直面
	PlanInfo mPlanInfo;
	for (auto iter1 = retalmap.begin(); iter1 != retalmap.end(); iter1++){
		for (auto iter2 = iter1->second.begin(); iter2 != iter1->second.end(); iter2++){
			for (auto iter3 = iter2->second.begin(); iter3 != iter2->second.end(); iter3++){
				processVerSingle(mPlanInfo,iter1,iter2,iter3);
			}
		}
	}
	vtkSmartPointer<vtkPolyData> polydata = vtkSmartPointer<vtkPolyData>::New();
	vtkSmartPointer<vtkPoints> verPlanPoints = vtkSmartPointer<vtkPoints>::New();
	vtkSmartPointer<vtkCellArray> verCell = vtkSmartPointer<vtkCellArray>::New();
	vtkSmartPointer<vtkFloatArray> verScalaes = vtkSmartPointer<vtkFloatArray>::New();
	for (__int64 i=0;i<mPlanInfo.points.size();i++)
	{
		verPlanPoints->InsertPoint(i, mPlanInfo.points[i].data());
		verScalaes->InsertTuple1(i, i);
	}
	for (auto&& i : mPlanInfo.faces)
		verCell->InsertNextCell(vtkIdType(i.size()),i.data());
	polydata->SetPoints(verPlanPoints);
	polydata->SetPolys(verCell);
	polydata->GetPointData()->SetScalars(verScalaes);
	return polydata;
}
void PlanData::processCirCut(std::map<ValSolf, std::map<double, std::vector<ValSolf>>>&info)
{
	std::map<ValSolf, std::map<double, std::vector<ValSolf>>>calcCirCutPlan;
	for (auto iter1 = info.begin(); iter1 != info.end(); iter1++)
	{
		for (auto iter2 = iter1->second.begin(); iter2 != iter1->second.end(); iter2++)
		{
			//排序，删除重复元素
			std::sort(iter2->second.begin(),iter2->second.end());
			std::vector<ValSolf>::iterator posz;
			posz = std::unique(iter2->second.begin(), iter2->second.end());
			iter2->second.erase(posz,iter2->second.end());
			double zU, zD;
			for (auto iter3 = iter2->second.begin(); iter3 != iter2->second.end(); iter3++)
			{
				if (iter3 == iter2->second.begin())
				{
					zU = iter3->val1;
					zD = iter3->val2;
				}
				else if (iter3->val1!=(iter3-1)->val2)
				{
					zD = (iter3 - 1)->val2;
					ValSolf valSolf(zU,zD);
					calcCirCutPlan[iter1->first][iter2->first].push_back(valSolf);
					zU = iter3->val1;
					zD = iter3->val2;
				}
			}
			zD = (iter2->second.end() - 1)->val2;
			ValSolf valSolf(zU, zD);
			calcCirCutPlan[iter1->first][iter2->first].push_back(valSolf);
		}
	}
	//处理点
	PlanInfo mPlanInfo;
	for (auto iter1=calcCirCutPlan.begin();iter1!=calcCirCutPlan.end();iter1++)
	{
		for (auto iter2 = iter1->second.begin(); iter2 != iter1->second.end(); iter2++)
		{
			for (auto iter3 = iter2->second.begin(); iter3 != iter2->second.end(); iter3++)
			{
				processCirCutSingle(mPlanInfo,iter1,iter2,iter3);
			}
		}
	}
}
/****************************************************************************/
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
void processVerSingle(PlanData::PlanInfo& pf,
	std::map<double,std::map<PlanData::ValSolf,std::vector<PlanData::ValSolf>>>::iterator &it1,
	std::map<PlanData::ValSolf,std::vector<PlanData::ValSolf>>::iterator &it2,
	std::vector<PlanData::ValSolf>::iterator &it3
	)
{
	PlanData::Points p1 = { it3->val1 * cos(it1->first),it3->val1 * sin(it1->first),it2->first.val1 };
	PlanData::Points p2 = { it3->val2 * cos(it1->first),it3->val2 * sin(it1->first),it2->first.val1 };
	PlanData::Points p3 = { it3->val1 * cos(it1->first),it3->val1 * sin(it1->first),it2->first.val2 };
	PlanData::Points p4 = { it3->val2 * cos(it1->first),it3->val2 * sin(it1->first),it2->first.val2 };
	__int64 lastsize = pf.points.size();
	PlanData::FaceIndex f1 = { 0 + lastsize,1 + lastsize,2 + lastsize };
	PlanData::FaceIndex f2 = { 1 + lastsize,2 + lastsize,3 + lastsize };
	pf.points.push_back(p1);
	pf.points.push_back(p2);
	pf.points.push_back(p3);
	pf.points.push_back(p4);
	pf.faces.push_back(f1);
	pf.faces.push_back(f2);
}
void processCirCutSingle(PlanData::PlanInfo& info,
	std::map<PlanData::ValSolf,std::map<double,std::vector<PlanData::ValSolf>>>::iterator& it1,
	std::map<double,std::vector<PlanData::ValSolf>>::iterator& it2,
	std::vector<PlanData::ValSolf>::iterator& it3)
{
	PlanData::Points p1 = { it2->first * cos(it1->first.val1),it2->first * sin(it1->first.val1),it3->val1 };
	PlanData::Points p2 = { it2->first * cos(it1->first.val2),it2->first * sin(it1->first.val2),it3->val1 };
	PlanData::Points p3 = { it2->first * cos(it1->first.val1),it2->first * sin(it1->first.val1),it3->val2 };
	PlanData::Points p4 = { it2->first * cos(it1->first.val2),it2->first * sin(it1->first.val2),it3->val2 };
	__int64 lastsize = info.points.size();
	PlanData::FaceIndex f1 = { 0 + lastsize,1 + lastsize,2 + lastsize };
	PlanData::FaceIndex f2 = { 1 + lastsize,2 + lastsize,3 + lastsize };
	info.points.push_back(p1);
	info.points.push_back(p2);
	info.points.push_back(p3);
	info.points.push_back(p4);
	info.faces.push_back(f1);
	info.faces.push_back(f2);
}