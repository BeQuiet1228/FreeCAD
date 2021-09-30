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
#include"Widget3D.h"
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
/**
* @brief DataProcess::DataProcess
* @return 
*/
DataProcess::DataProcess()
{
	planePtr = std::shared_ptr<PlanData>(new PlanData());
}
/**
* @brief DataProcess::~DataProcess
* @return 
*/
DataProcess::~DataProcess()
{
	
}
/**
* @brief DataProcess::initData
* @param Hdf5Data & data
* @return bool
*/
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
/**
* @brief DataProcess::calcCartesian
* @param Hdf5Data & data
* @return bool
*/
bool DataProcess::calcCartesian(Hdf5Data& data) {

	Data::ListValuesPtr sourceData(new Data::ListValues);
	//处理数据
	bool ok = Hdf5IO::getValue(data.listDataSet,*(sourceData.get()));
	if (!ok)return false;
	auto it = sourceData->begin();
	Data::ValuesPtr COLOR = *it; it++;
	Data::ValuesPtr NAME = *it; it++;
	Data::ValuesPtr datasetPla = *it; it++;
	__int64 index = 0;
	//std::map<__int64, PlanD> mPland;
	//std::map<__int64, RPlan> mrPlan;
	for (auto iterdata=datasetPla->begin();iterdata!=datasetPla->end();index++)
	{
		PlanData::DInfo temp;
		temp.x1 = *iterdata; iterdata++;
		temp.y1 = *iterdata; iterdata++;
		temp.z1 = *iterdata; iterdata++;
		temp.x2 = *iterdata; iterdata++;
		temp.y2 = *iterdata; iterdata++;
		temp.z2 = *iterdata; iterdata++;
		temp.proPer = *(NAME->begin() + index);
		planePtr->statisticalD(temp);
	}
	planePtr->mergePolyDataD();
	return true;
}
/**
* @brief DataProcess::calcPolar
* @param Hdf5Data & data
* @return bool
*/
bool DataProcess::calcPolar(Hdf5Data& data) {
	//r-theta-z
	Data::ListValuesPtr sourceData(new Data::ListValues);
	//处理数据
	bool ok = Hdf5IO::getValue(data.listDataSet,*(sourceData.get()));
	if (!ok)return false;
	auto it = sourceData->begin();
	Data::ValuesPtr COLOR = *it; it++;
	Data::ValuesPtr NAME = *it; it++;
	Data::ValuesPtr datasetPla = *it;
	__int64 index = 0;
	for (auto iterval = datasetPla->begin(); iterval != datasetPla->end(); index++)
	{
		PlanData::CirInfo temp;
		temp.rI = *iterval; iterval++;
		temp.sA = *iterval; iterval++;
		temp.zU = *iterval; iterval++;
		temp.rE = *iterval; iterval++;
		temp.eA = *iterval; iterval++;
		temp.zD = *iterval; iterval++;
		temp.proPer = *(NAME->begin() + index);
		planePtr->statisticalC(temp);
	}
	//处理面
	planePtr->mergePolyDataC();
	return true;
}
/**
* @brief DataProcess::calcCylinder
* @param Hdf5Data & data
* @return bool
*/
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
/**
* @brief PlanData::PlanData
* @return 
*/
PlanData::PlanData() {
	cylinderS.clear();
	castersianS.clear();
	Polys.clear();
}
/**
* @brief PlanData::~PlanData
* @return 
*/
PlanData::~PlanData(){
	cylinderS.clear();
	castersianS.clear();
	Polys.clear();
}
/**
* @brief PlanData::setDataType
* @param DataType type
* @return void
*/
void PlanData::setDataType(DataType type)
{
	mDataType = type;
}
/**
* @brief PlanData::statisticalC
* @param CirInfo & info
* @return void
*/
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
/**
* @brief PlanData::statisticalD
* @param DInfo & info
* @return void
*/
void PlanData::statisticalD(DInfo& info)
{
	ValSolf xvsf(info.x1,info.x2);
	ValSolf yvsf(info.y1, info.y2);
	ValSolf zvsf(info.z1, info.z2);
	//castersianS
	if (info.z1 == info.z2)
	{
		castersianS[info.proPer][_Z_].pland[info.z1][yvsf].push_back(xvsf);
		castersianS[info.proPer][_Z_].planr[info.z1].push_back(yvsf);
	}
	else if (info.y1 == info.y2)
	{
		castersianS[info.proPer][_Y_].pland[info.y1][zvsf].push_back(xvsf);
		castersianS[info.proPer][_Y_].planr[info.y1].push_back(zvsf);
	}
	else if (info.x1 == info.x2)
	{
		castersianS[info.proPer][_X_].pland[info.x1][zvsf].push_back(yvsf);
		castersianS[info.proPer][_X_].planr[info.x1].push_back(zvsf);
	}
}
/**
* @brief PlanData::mergePolyDataC
* @return void
*/
void PlanData::mergePolyDataC()
{
	Polys.clear();
	for (auto iter = cylinderS.begin(); iter != cylinderS.end(); iter++)
	{
		auto v1=processCir(iter->second.plans);
		auto v2=processVer(iter->second.verPlans, iter->second.releZ);
		auto v3=processCirCut(iter->second.cirCutPlan);
		vtkSmartPointer<vtkAppendPolyData> AppendData = vtkSmartPointer<vtkAppendPolyData>::New();
		AppendData->AddInputData(v1);
		AppendData->AddInputData(v2);
		AppendData->AddInputData(v3);
		AppendData->Update();
		vtkSmartPointer<vtkCleanPolyData> cleanPolyData = vtkSmartPointer<vtkCleanPolyData>::New();
		cleanPolyData->SetInputConnection(AppendData->GetOutputPort());
		cleanPolyData->Update();
		Polys[iter->first] = PdPtr::New();
		Polys[iter->first]->ShallowCopy(cleanPolyData->GetOutput());
	}
	cylinderS.clear();
}
/**
* @brief PlanData::mergePolyDataD
* @return void
*/
void PlanData::mergePolyDataD()
{
	Polys.clear();
	for (auto iter = castersianS.begin(); iter != castersianS.end(); iter++)
	{
		for (auto iterCoord = iter->second.begin(); iterCoord != iter->second.end(); iterCoord++)
		{
			processVerD(iterCoord->second.pland,iterCoord->second.planr);
		}
		auto v1=calcCastersianX(iter->second[_X_].pland);
		auto v2=calcCastersianY(iter->second[_Y_].pland);
		auto v3=calcCastersianZ(iter->second[_Z_].pland);
		vtkSmartPointer<vtkAppendPolyData> AppendData = vtkSmartPointer<vtkAppendPolyData>::New();
		AppendData->AddInputData(v1);
		AppendData->AddInputData(v2);
		AppendData->AddInputData(v3);
		AppendData->Update();
		vtkSmartPointer<vtkCleanPolyData> cleanPolyData = vtkSmartPointer<vtkCleanPolyData>::New();
		cleanPolyData->SetInputConnection(AppendData->GetOutputPort());
		cleanPolyData->Update();
		Polys[iter->first] = PdPtr::New();
		Polys[iter->first]->ShallowCopy(cleanPolyData->GetOutput());
	}
	castersianS.clear();
}
/**
* @brief PlanData::processCir
* @param std::map<double
* @param std::map<ValSolf
* @param std::vector<ValSolf>>> & info
* @return vtkSmartPointer<vtkPolyData>
*/
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
		vtkSmartPointer<vtkCellArray> planCell = vtkSmartPointer<vtkCellArray>::New();
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
/**
* @brief PlanData::processVer
* @param std::map<double
* @param std::map<ValSolf
* @param std::vector<ValSolf>>> & pd
* @param std::map<double
* @param std::vector<ValSolf>> & pz
* @return vtkSmartPointer<vtkPolyData>
*/
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
/**
* @brief PlanData::processCirCut
* @param std::map<ValSolf
* @param std::map<double
* @param std::vector<ValSolf>>> & info
* @return vtkSmartPointer<vtkPolyData>
*/
vtkSmartPointer<vtkPolyData> PlanData::processCirCut(std::map<ValSolf, std::map<double, std::vector<ValSolf>>>&info)
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
	vtkSmartPointer<vtkPolyData> polyData = vtkSmartPointer<vtkPolyData>::New();
	vtkSmartPointer<vtkPoints> cirCutPoints = vtkSmartPointer<vtkPoints>::New();
	vtkSmartPointer<vtkCellArray> cirCutCell = vtkSmartPointer<vtkCellArray>::New();
	vtkSmartPointer<vtkFloatArray> cirCutScalaes = vtkSmartPointer<vtkFloatArray>::New();
	for (__int64 i=0;i<mPlanInfo.points.size();i++)
	{
		cirCutPoints->InsertPoint(i,mPlanInfo.points[i].data());
		cirCutScalaes->InsertTuple1(i,i);
	}
	for (auto&& i : mPlanInfo.faces)
		cirCutCell->InsertNextCell(vtkIdType(i.size()),i.data());
	polyData->SetPoints(cirCutPoints);
	polyData->SetPolys(cirCutCell);
	polyData->GetPointData()->SetScalars(cirCutScalaes);

	return polyData;
}
/**
* @brief PlanData::processVerD
* @param PlanD & ps
* @param RPlan & rps
* @return void
*/
void PlanData::processVerD(PlanD& ps, RPlan& rps)
{
	PlanD caclps;
	{
		//1
		for (auto iterplan = ps.begin(); iterplan != ps.end(); iterplan++)
		{
			//排序，删除重复元素
			std::sort(rps[iterplan->first].begin(), rps[iterplan->first].end());
			std::vector<ValSolf>::iterator posz;
			posz = std::unique(rps[iterplan->first].begin(), rps[iterplan->first].end());
			rps[iterplan->first].erase(posz, rps[iterplan->first].end());
			//2
			for (auto iter2 = iterplan->second.begin(); iter2 != iterplan->second.end(); iter2++)
			{
				//排序，删除重复元素
					//排序，删除重复元素
				std::sort(iter2->second.begin(), iter2->second.end());
				std::vector<ValSolf>::iterator pos;
				pos = std::unique(iter2->second.begin(), iter2->second.end());
				iter2->second.erase(pos, iter2->second.end());
				double val_1;
				double val_2;
				for (auto iter3 = iter2->second.begin(); iter3 != iter2->second.end(); iter3++)
				{
					if (iter3 == iter2->second.begin())
					{
						val_1 = iter3->val1;
						val_2 = iter3->val2;
					}
					else {
						if (iter3->val1 != (iter3 - 1)->val2) {
							val_2 = (iter3 - 1)->val2;
							ValSolf valsolf(val_1, val_2);
							caclps[iterplan->first][iter2->first].push_back(valsolf);
							val_1 = iter3->val1;
							val_2 = iter3->val2;
						}
					}
				}
				{
					val_2 = (iter2->second.end() - 1)->val2;
					ValSolf valsolf(val_1, val_2);
					caclps[iterplan->first][iter2->first].push_back(valsolf);
				}
			}
		}
	}
	//生成点位
	PlanD retalmap;
	{
		for (auto iter1 = rps.begin(); iter1 != rps.end(); iter1++)
		{
			for (auto iter2 = iter1->second.begin(); iter2 != iter1->second.end(); iter2++)
			{
				auto iterresole = caclps[iter1->first].find(*iter2);
				if (iterresole == caclps[iter1->first].end())
					continue;
				for (__int64 i = 0; i < iterresole->second.size(); i++)
				{
					double val_1 = iter2->val1;
					double val_2 = iter2->val2;
					auto iter2next = iter2 + 1;
					while (iter2next != iter1->second.end() &&
						caclps[iter1->first].find(*iter2next) != caclps[iter1->first].end())
					{
						if (iter2next->val1 != (iter2next - 1)->val2)
							break;
						auto vallist = caclps[iter1->first].find(*iter2next);
						__int64 indexj = -1;
						for (__int64 j = 0; j < vallist->second.size(); j++)
						{
							if (vallist->second[j] == iterresole->second[i])
							{
								indexj = j;
								break;
							}
						}
						if (-1 == indexj)break;
						//如果有相等的情况
						val_2 = iter2next->val2;
						vallist->second.erase(vallist->second.begin() + indexj);
						if (0 == vallist->second.size()) caclps[iter1->first].erase(vallist);
						iter2next++;
					}
					{
						ValSolf valsoltf(val_1, val_2);
						retalmap[iter1->first][valsoltf].push_back(iterresole->second[i]);
					}
				}
				caclps[iter1->first].erase(iterresole);
			}
		}
	}
	ps.swap(retalmap);
	return;
}
/**
* @brief PlanData::calcCastersianX
* @param PlanD & info
* @return vtkSmartPointer<vtkPolyData>
*/
vtkSmartPointer<vtkPolyData> PlanData::calcCastersianX(PlanD& info){
	//xplan-x-(z1-z2)-(y1-y2)
	PlanInfo xplan;
	for (auto iter1 = info.begin(); iter1 != info.end(); iter1++)
	{
		for (auto iter2 = iter1->second.begin(); iter2 != iter1->second.end(); iter2++)
		{
			for (auto iter3 = iter2->second.begin(); iter3 != iter2->second.end(); iter3++)
			{
				__int64 lastsize = xplan.points.size();
				Points p1 = { iter1->first,iter3->val1,iter2->first.val1 };
				Points p2 = { iter1->first,iter3->val2,iter2->first.val1 };
				Points p3 = { iter1->first,iter3->val1,iter2->first.val2 };
				Points p4 = { iter1->first,iter3->val2,iter2->first.val2 };
				FaceIndex f1 = { 0 + lastsize,1 + lastsize,2 + lastsize };
				FaceIndex f2 = { 1 + lastsize,2 + lastsize,3 + lastsize };
				xplan.points.push_back(p1);
				xplan.points.push_back(p2);
				xplan.points.push_back(p3);
				xplan.points.push_back(p4);
				xplan.faces.push_back(f1);
				xplan.faces.push_back(f2);
			}
		}
	}
	vtkSmartPointer<vtkPolyData> polyData = vtkSmartPointer<vtkPolyData>::New();
	vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New();
	vtkSmartPointer<vtkCellArray> pointcellarra = vtkSmartPointer<vtkCellArray>::New();
	vtkSmartPointer<vtkFloatArray> pointscalaes = vtkSmartPointer<vtkFloatArray>::New();
	for (__int64 i = 0; i < xplan.points.size(); i++)
	{
		points->InsertPoint(i, xplan.points[i].data());
		pointscalaes->InsertTuple1(i, i);
	}
	for (auto&& i : xplan.faces)
		pointcellarra->InsertNextCell(vtkIdType(i.size()), i.data());
	polyData->SetPoints(points);
	polyData->SetPolys(pointcellarra);
	polyData->GetPointData()->SetScalars(pointscalaes);
	return polyData;
}
/**
* @brief PlanData::calcCastersianY
* @param PlanD & info
* @return vtkSmartPointer<vtkPolyData>
*/
vtkSmartPointer<vtkPolyData> PlanData::calcCastersianY(PlanD& info){
	//yplan-y-(z1-z2)-(x1-x2)
	PlanInfo yplan;
	for (auto iter1 = info.begin(); iter1 != info.end(); iter1++)
	{
		for (auto iter2 = iter1->second.begin(); iter2 != iter1->second.end(); iter2++)
		{
			for (auto iter3 = iter2->second.begin(); iter3 != iter2->second.end(); iter3++)
			{
				__int64 lastsize = yplan.points.size();
				Points p1 = { iter3->val1,iter1->first,iter2->first.val1 };
				Points p2 = { iter3->val2,iter1->first,iter2->first.val1 };
				Points p3 = { iter3->val1,iter1->first,iter2->first.val2 };
				Points p4 = { iter3->val2,iter1->first,iter2->first.val2 };
				FaceIndex f1 = { 0 + lastsize,1 + lastsize,2 + lastsize };
				FaceIndex f2 = { 1 + lastsize,2 + lastsize,3 + lastsize };
				yplan.points.push_back(p1);
				yplan.points.push_back(p2);
				yplan.points.push_back(p3);
				yplan.points.push_back(p4);
				yplan.faces.push_back(f1);
				yplan.faces.push_back(f2);
			}
		}
	}
	vtkSmartPointer<vtkPolyData> polyData = vtkSmartPointer<vtkPolyData>::New();
	vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New();
	vtkSmartPointer<vtkCellArray> pointcellarra = vtkSmartPointer<vtkCellArray>::New();
	vtkSmartPointer<vtkFloatArray> pointscalaes = vtkSmartPointer<vtkFloatArray>::New();
	for (__int64 i = 0; i < yplan.points.size(); i++)
	{
		points->InsertPoint(i, yplan.points[i].data());
		pointscalaes->InsertTuple1(i, i);
	}
	for (auto&& i : yplan.faces)
		pointcellarra->InsertNextCell(vtkIdType(i.size()), i.data());
	polyData->SetPoints(points);
	polyData->SetPolys(pointcellarra);
	polyData->GetPointData()->SetScalars(pointscalaes);
	return polyData;
}
/**
* @brief PlanData::calcCastersianZ
* @param PlanD & info
* @return vtkSmartPointer<vtkPolyData>
*/
vtkSmartPointer<vtkPolyData> PlanData::calcCastersianZ(PlanD& info){
	//zplan-z-(y1-y2)-(x1-x2)
	PlanInfo zplan;
	for (auto iter1 = info.begin(); iter1 != info.end(); iter1++)
	{
		for (auto iter2 = iter1->second.begin(); iter2 != iter1->second.end(); iter2++)
		{
			for (auto iter3 = iter2->second.begin(); iter3 != iter2->second.end(); iter3++)
			{
				__int64 lastsize = zplan.points.size();
				Points p1 = { iter3->val1,iter2->first.val1,iter1->first };
				Points p2 = { iter3->val2,iter2->first.val1,iter1->first };
				Points p3 = { iter3->val1,iter2->first.val2,iter1->first };
				Points p4 = { iter3->val2,iter2->first.val2,iter1->first };
				FaceIndex f1 = { 0 + lastsize,1 + lastsize,2 + lastsize };
				FaceIndex f2 = { 1 + lastsize,2 + lastsize,3 + lastsize };
				zplan.points.push_back(p1);
				zplan.points.push_back(p2);
				zplan.points.push_back(p3);
				zplan.points.push_back(p4);
				zplan.faces.push_back(f1);
				zplan.faces.push_back(f2);
			}
		}
	}
	vtkSmartPointer<vtkPolyData> PolyData = vtkSmartPointer<vtkPolyData>::New();
	vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New();
	vtkSmartPointer<vtkCellArray> pointcellarra = vtkSmartPointer<vtkCellArray>::New();
	vtkSmartPointer<vtkFloatArray> pointscalaes = vtkSmartPointer<vtkFloatArray>::New();
	for (__int64 i = 0; i < zplan.points.size(); i++)
	{
		points->InsertPoint(i, zplan.points[i].data());
		pointscalaes->InsertTuple1(i, i);
	}
	for (auto&& i : zplan.faces)
		pointcellarra->InsertNextCell(vtkIdType(i.size()), i.data());
	PolyData->SetPoints(points);
	PolyData->SetPolys(pointcellarra);
	PolyData->GetPointData()->SetScalars(pointscalaes);
	return PolyData;
}
/****************************************************************************/
/**
* @brief processCirSingle
* @param std::map<double
* @param PlanData::PlanInfo> & cirPlan
* @param std::map<double
* @param std::map<PlanData::ValSolf
* @param std::vector<PlanData::ValSolf>>>::iterator & it1
* @param std::map<PlanData::ValSolf
* @param std::vector<PlanData::ValSolf>>::iterator & it2
* @param double & val_1
* @param double & val_2
* @return void
*/
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
/**
* @brief processVerSingle
* @param PlanData::PlanInfo & pf
* @param std::map<double
* @param std::map<PlanData::ValSolf
* @param std::vector<PlanData::ValSolf>>>::iterator & it1
* @param std::map<PlanData::ValSolf
* @param std::vector<PlanData::ValSolf>>::iterator & it2
* @param std::vector<PlanData::ValSolf>::iterator & it3
* @return void
*/
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
/**
* @brief processCirCutSingle
* @param PlanData::PlanInfo & info
* @param std::map<PlanData::ValSolf
* @param std::map<double
* @param std::vector<PlanData::ValSolf>>>::iterator & it1
* @param std::map<double
* @param std::vector<PlanData::ValSolf>>::iterator & it2
* @param std::vector<PlanData::ValSolf>::iterator & it3
* @return void
*/
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
std::shared_ptr<QWidget> DataProcess::getWidget()
{
	std::shared_ptr<Widget3D> widget3D(new Widget3D());
	auto polydatas = planePtr->getPro();
	for (auto iter = polydatas.begin(); iter != polydatas.end(); iter++)
	{
		widget3D->transfromPolyData(iter->first,iter->second);
	}
	//widget3D->update();
	widget3D->drawImage();
	return widget3D;
}