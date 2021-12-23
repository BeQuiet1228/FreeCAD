#include "ArcCalc.h"
#include "vtkMath.h"
#include "math.h"
#include "../ContourDataPolar.h"
DV3D::ArcCalc::ArcCalc()
{
	init();
}

DV3D::ArcCalc::~ArcCalc()
{

}

DV3D::ArcCalc::ArcCalc(int res)
{
	init();
	this->mResolution = (res < 1 ? 1 : res);
}

void DV3D::ArcCalc::init()
{
	//point1
	this->mPoint1[0] = 0.0;
	this->mPoint1[1] = 0.5;
	this->mPoint1[2] = 0.0;
	//point2
	this->mPoint2[0] = 0.5;
	this->mPoint2[1] = 0.0;
	this->mPoint2[2] = 0.0;
	//center
	this->mCenter[0] = 0.0;
	this->mCenter[1] = 0.0;
	this->mCenter[2] = 0.0;
	//normal
	this->mNormal[0] = 0.0;
	this->mNormal[0] = 0.0;
	this->mNormal[0] = 1.0;
	//Resolution
	this->mResolution = 1;
	scalar1 = 0.0;
	scalar2 = 1.0;
}

void DV3D::ArcCalc::setCenter(double* center)
{
	mCenter[0] = center[0];
	mCenter[1] = center[1];
	mCenter[2] = center[2];
}

double* DV3D::ArcCalc::getCenter()
{
	return mCenter;
}

void DV3D::ArcCalc::setNormal(double* normal)
{
	mNormal[0] = normal[0];
	mNormal[1] = normal[1];
	mNormal[2] = normal[2];
}

double* DV3D::ArcCalc::getNormal()
{
	return mNormal;
}

void DV3D::ArcCalc::setPolarVector(double* polarvector)
{
	mPolarVector[0] = polarvector[0];
	mPolarVector[1] = polarvector[1];
	mPolarVector[2] = polarvector[2];
}

double* DV3D::ArcCalc::getPolarVector()
{
	return mPolarVector;
}

void DV3D::ArcCalc::setResolution(int m)
{
	if (m < 1)
		return;
	mResolution = m;
}

int DV3D::ArcCalc::getResolution()
{
	return mResolution;
}
void DV3D::ArcCalc::Update()
{
	//获取两点之间的夹角
	double r1 = vtkMath::Distance2BetweenPoints(mPoint1, mCenter);
	double r2 = vtkMath::Distance2BetweenPoints(mPoint2, mCenter);
	double subVal = abs(r1 - r2);
	if (subVal > 0.00001f)
	{
		printf("The two points are not on the same arc\n");
		return;
	}
	double v1[3];
	double v2[3];
	vtkMath::Subtract(mPoint1, mCenter, v1);
	vtkMath::Subtract(mPoint2, mCenter, v2);
	auto rad = vtkMath::AngleBetweenVectors(v1, v2);
	//获取弧度的间距
	auto intervalRad = vtkMath::RadiansFromDegrees(360.0) / mResolution;
	if (intervalRad >= rad)
	{
		notMalkArcText();
		return;
	}
	//做处理
	double perpendicular[3];//垂直向量
	double normal[3];
	vtkMath::Cross(this->mNormal, this->mPolarVector, perpendicular);
	/*double dotprod =
		vtkMath::Dot(v1, v2) / vtkMath::Norm(v1) * vtkMath::Norm(v2);
	double angle = acos(dotprod);*/
	vtkMath::Normalize(perpendicular);
	auto radius = vtkMath::Normalize(v1);
	double theta = intervalRad;
	insertPoint1();
	for (int i = 0; i <= this->mResolution; ++i, theta += intervalRad)
	{
		if (theta >= rad)
			break;
		const double cosine = cos(theta);
		const double sine = sin(theta);
		ArcTextInfo p;
		p.point.setX(this->mCenter[0] + cosine * radius * v1[0] + sine * radius * perpendicular[0]);
		p.point.setY(this->mCenter[1] + cosine * radius * v1[1] + sine * radius * perpendicular[1]);
		p.point.setZ(this->mCenter[2] + cosine * radius * v1[2] + sine * radius * perpendicular[2]);
		p.scalar = (scalar2 - scalar1) * (theta / rad) + scalar1;
		outputArc.push_back(p);
	}
	insertPoint2();
}

void DV3D::ArcCalc::setPoint1(double* p)
{
	mPoint1[0] = p[0];
	mPoint1[1] = p[1];
	mPoint1[2] = p[2];
}

void DV3D::ArcCalc::setPoint2(double* p)
{
	mPoint2[0] = p[0];
	mPoint2[1] = p[1];
	mPoint2[2] = p[2];
}

double* DV3D::ArcCalc::getPoint1()
{
	return mPoint1;
}

double* DV3D::ArcCalc::getPoint2()
{
	return mPoint2;
}

void DV3D::ArcCalc::setScalar1(double s1)
{
	scalar1 = s1;
}

void DV3D::ArcCalc::setScalar2(double s2)
{
	scalar2 = s2;
}

double DV3D::ArcCalc::getScalar1()
{
	return scalar1;
}

double DV3D::ArcCalc::getScalar2()
{
	return scalar2;
}

std::vector<DV3D::ArcCalc::ArcTextInfo>& DV3D::ArcCalc::getOutputArc()
{
	return outputArc;
}


/**
* @time	2021/12/23
* @brief DV3D::ArcCalc::notMalkArcText 不做处理
* @return void
*/
void DV3D::ArcCalc::notMalkArcText()
{
	insertPoint1();
	insertPoint2();
}

void DV3D::ArcCalc::insertPoint1()
{
	outputArc.clear();
	ArcTextInfo port1;
	port1.point.setX(mPoint1[0]);
	port1.point.setY(mPoint1[1]);
	port1.point.setZ(mPoint1[2]);
	port1.scalar = scalar1;
	outputArc.push_back(port1);
}

void DV3D::ArcCalc::insertPoint2()
{
	ArcTextInfo port2;
	port2.point.setX(mPoint2[0]);
	port2.point.setY(mPoint2[1]);
	port2.point.setZ(mPoint2[2]);
	port2.scalar = scalar2;
	outputArc.push_back(port2);
}

void DV3D::ArcCalc::setPoint2(double x, double y, double z)
{
	mPoint2[0] = x;
	mPoint2[1] = y;
	mPoint2[2] = z;
}

void DV3D::ArcCalc::setPoint1(double x, double y, double z)
{
	mPoint1[0] = x;
	mPoint1[1] = y;
	mPoint1[2] = z;
}

void DV3D::ArcCalc::setPolarVector(double x, double y, double z)
{
	mPolarVector[0] = x;
	mPolarVector[1] = y;
	mPolarVector[2] = z;
}
void DV3D::ArcCalc::setNormal(double x, double y, double z)
{
	mNormal[0] = x;
	mNormal[1] = y;
	mNormal[2] = z;
}
void DV3D::ArcCalc::setCenter(double x, double y, double z)
{
	mCenter[0] = x;
	mCenter[1] = y;
	mCenter[2] = z;
}

DV::ContourDataPolar* DV3D::polarInterVal(Hdf5Data& h5)
{

}

