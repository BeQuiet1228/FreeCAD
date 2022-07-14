#pragma once
#include <vtkImplicitFunction.h>
#include "exprtk.hpp"
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

typedef exprtk::symbol_table<double> symbol_table_t;
typedef exprtk::expression<double>   expression_t;
typedef exprtk::parser<double>       parser_t;
class MyFuntion4 :public MyFuntion {
public:
	MyFuntion4();
	~MyFuntion4() {};


	virtual double EvaluateFunction(double d[3]);
	virtual void EvaluateGradient(double x[3], double g[3]);

	double x, y, z;
	symbol_table_t symbol_table;
	expression_t expression;
	parser_t parser;
};