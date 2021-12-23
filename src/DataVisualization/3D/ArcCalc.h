#pragma once
#include <vector>
#include <QVector3D>
namespace DV3D
{
	//用于计算弧度相关
	class ArcCalc
	{
	public:
		ArcCalc();
		ArcCalc(int res);
		~ArcCalc();
		using ArcPoint = QVector3D;
		using ArcScalar = double;
		struct ArcTextInfo
		{
			ArcPoint point;
			ArcScalar scalar;
		};
	public:
		void init();
		//center
		void setCenter(double* center);
		void setCenter(double x, double y, double z);
		double* getCenter();
		//Normal
		void setNormal(double* normal);
		void setNormal(double x, double y, double z);
		double* getNormal();
		//PolarVector
		void setPolarVector(double*);
		void setPolarVector(double x, double y, double z);
		double* getPolarVector();
		//Resolution
		void setResolution(int);
		int getResolution();
		void Update();
		//Point1 and 2
		void setPoint1(double*);
		void setPoint1(double x, double y, double z);
		void setPoint2(double*);
		void setPoint2(double x, double y, double z);
		double* getPoint1();
		double* getPoint2();
		//scalar1and2
		void setScalar1(double);
		void setScalar2(double);
		double getScalar1();
		double getScalar2();
		//
		std::vector<ArcTextInfo>& getOutputArc();
	protected:
		void notMalkArcText();
		void insertPoint1();
		void insertPoint2();
	private:
		double mPoint1[3];//端点1
		double mPoint2[3];//端点2
		double mCenter[3];//中心点
		double mNormal[3];//法线
		double mPolarVector[3];//极坐标方向
		int mResolution;//分辨率
		double scalar1;
		double scalar2;
		std::vector<ArcTextInfo>  outputArc;
	};
}