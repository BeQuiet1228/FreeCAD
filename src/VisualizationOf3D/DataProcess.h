#pragma once
#ifndef DATA_PROCESS_H_
#define DATA_PROCESS_H_
//#include"hdf5io.h"
#include<map>
#include<vector>
#include<memory>
class PlanData;
class Hdf5Data;
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
public:
	void setDataType(DataType type);
	void statisticalC(CirInfo&);
	//void statisticalD();
	void mergePolyDataC();
protected:
	void processCir(std::map<double,std::map<ValSolf,std::vector<ValSolf>>>&);
	void processVer(std::map<double, std::map<ValSolf, std::vector<ValSolf>>>&,
		std::map<double, std::vector<ValSolf>>&);
	void processCirCut(std::map<ValSolf,std::map<double,std::vector<ValSolf>>>&);
protected:
	std::map<int, CylinderInfo> cylinderS;
	DataType mDataType;
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