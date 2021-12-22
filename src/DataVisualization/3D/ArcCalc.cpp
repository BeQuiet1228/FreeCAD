#include "ArcCalc.h"
#include "vtkMath.h"
#include "math.h"
DV3D::ArcCalc::ArcCalc()
{
	init();
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
	double r1 = vtkMath::Distance2BetweenPoints(mPoint1,mCenter);
	double r2 = vtkMath::Distance2BetweenPoints(mPoint2,mCenter);
	if (abs(r1 - r2) < 0.00001f)
	{
		printf("The two points are not on the same arc\n");
		return;
	}
	double v1[3];
	double v2[3];
	vtkMath::Subtract(mPoint1, mCenter, v1);
	vtkMath::Subtract(mPoint2, mCenter, v2);
	auto rad=vtkMath::AngleBetweenVectors(v1,v2);
	//获取弧度的间距
	auto intervalRad = vtkMath::RadiansFromDegrees(360.0) / mResolution;

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

