#pragma once
#include <vtkImplicitFunction.h>

class MyFuntion :public vtkImplicitFunction {
public:
	MyFuntion();
	~MyFuntion() = default;

	virtual double EvaluateFunction(double d[3]);
	virtual void EvaluateGradient(double x[3], double g[3]);
};

class MyFuntion1 :public MyFuntion {
public:
	MyFuntion1();
	~MyFuntion1() = default;

	virtual double EvaluateFunction(double d[3]);
	virtual void EvaluateGradient(double x[3], double g[3]);
};

class MyFuntion2 :public MyFuntion {
public:
	MyFuntion2() =default;
	~MyFuntion2() = default;

	virtual double EvaluateFunction(double d[3]);
	virtual void EvaluateGradient(double x[3], double g[3]);
};

class MyFuntion3 :public MyFuntion {
public:
	MyFuntion3() = default;
	~MyFuntion3() = default;

	virtual double EvaluateFunction(double d[3]);
	virtual void EvaluateGradient(double x[3], double g[3]);
};