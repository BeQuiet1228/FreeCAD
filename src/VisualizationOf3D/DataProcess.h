#pragma once
#ifndef DATA_PROCESS_H_
#define DATA_PROCESS_H_
#include"vtk-7.0/vtkSmartPointer.h"
#include<map>
#include<vector>
#include<memory>
class PlanData;
class Hdf5Data;
class vtkPolyData;
using PdPtr = vtkSmartPointer<vtkPolyData>;

class PlanData
{
public:
	using Points = std::vector<double>;
	using FaceIndex = std::vector<__int64>;
	enum DataType
	{
		CYLINDER=0,
		POLAR,
		CASTESIAN,
	};
	enum CoordData
	{
		_X_=0,
		_Y_=1,
		_Z_=2
	};
	struct ValSolf {
		double val1;
		double val2;
		double valCenter;
		ValSolf(double v1, double v2) :
			val1(v1), val2(v2), valCenter((v1 + v2) / 2) 
		{}
		ValSolf(const ValSolf& that) :
			val1(that.val1), val2(that.val2), valCenter(that.valCenter)
		{}
		bool operator <(const ValSolf& that)const
		{
			if (this->valCenter < that.valCenter)
			{
				return true;
			}
			return false;
		}
		bool operator ==(const ValSolf& that)const
		{
			if (this->valCenter == that.valCenter &&
				this->val1 == that.val1)
				return true;
			return false;
		}
	};
	struct CirInfo {
		double rI;
		double rE;
		double zU;
		double zD;
		double sA;
		double eA;
		int proPer;
	};
	struct  DInfo
	{
		double x1;
		double x2;
		double y1;
		double y2;
		double z1;
		double z2;
		int proPer;
	};
	struct CylinderInfo {
		std::map<double, std::map<ValSolf, std::vector<ValSolf>>> plans;
		std::map<double, std::map<ValSolf, std::vector<ValSolf>>> verPlans;
		std::map<ValSolf, std::map<double, std::vector<ValSolf>>> cirCutPlan;
		std::map<double, std::vector<ValSolf>> releZ;
		void clear()
		{
			releZ.clear();
			cirCutPlan.clear();
			verPlans.clear();
			plans.clear();
		}
	};
	struct PlanInfo {
		std::vector<Points> points;
		std::vector<FaceIndex> faces;
	};
	using PlanD = std::map<double, std::map<ValSolf, std::vector<ValSolf>>>;
	using RPlan = std::map<double, std::vector<ValSolf>>;
	struct CastersianInfo
	{
		PlanD pland;
		RPlan planr;
	};
public:
	PlanData();
	~PlanData();
	void setDataType(DataType type);
	void statisticalC(CirInfo&);
	void statisticalD(DInfo&);
	void mergePolyDataC();
	void mergePolyDataD();
protected:
	vtkSmartPointer<vtkPolyData> processCir(std::map<double,std::map<ValSolf,std::vector<ValSolf>>>&);
	vtkSmartPointer<vtkPolyData> processVer(std::map<double, std::map<ValSolf, std::vector<ValSolf>>>&,std::map<double, std::vector<ValSolf>>&);
	vtkSmartPointer<vtkPolyData> processCirCut(std::map<ValSolf,std::map<double,std::vector<ValSolf>>>&);
	vtkSmartPointer<vtkPolyData> calcCastersianX(PlanD&);
	vtkSmartPointer<vtkPolyData> calcCastersianY(PlanD&);
	vtkSmartPointer<vtkPolyData> calcCastersianZ(PlanD&);
	void processVerD(PlanD& ps, RPlan& rps);
protected:
	DataType mDataType;
	std::map<int, CylinderInfo> cylinderS;
	std::map<int, std::map<CoordData, CastersianInfo>> castersianS;
private:
	std::map<__int64, PdPtr> Polys;
};

class DataProcess
{
public:
	DataProcess();
	~DataProcess();
	bool initData(Hdf5Data& data);
protected:
	bool calcCartesian(Hdf5Data& data);
	bool calcPolar(Hdf5Data& data);
	bool calcCylinder(Hdf5Data& data);
private:
	std::shared_ptr<PlanData> planePtr;
};

#endif