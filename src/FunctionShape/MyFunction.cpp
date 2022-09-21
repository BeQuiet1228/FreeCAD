#include "MyFunction.h"
#include <vtkMath.h>
MyFuntion::MyFuntion()
{

}

double MyFuntion::EvaluateFunction(double d[3])
{
	double x = d[0];
	double y = d[1];
	double z = d[2];

// 	double x2C[3];
// 	x2C[0] = x ;
// 	x2C[1] = y ;
// 	x2C[2] = z ;
// 
// 	double Axis[3] = {1,0,0};
// 
// 	// projection onto cylinder axis
// 	double proj = vtkMath::Dot(Axis, x2C);
// 
// 	// return distance^2 - R^2
// 	return ((vtkMath::Dot(x2C, x2C) - proj * proj) - 2);
// 
// 
// 
// 
// 	//return x*x*2+y*y+z*z - 2;

	return pow(x*x + (9.0 / 4.0)*y*y + z*z- 1.0,3) - x*x*pow(z,3) - (9.0 / 80.0)*y*y * pow(z,3);
}

void MyFuntion::EvaluateGradient(double x[3], double g[3])
{

}

MyFuntion1::MyFuntion1()
{

}

double MyFuntion1::EvaluateFunction(double d[3])
{
	double x = d[0];
	double y = d[1];
	double z = d[2];

	 	double x2C[3];
	 	x2C[0] = x ;
	 	x2C[1] = y ;
	 	x2C[2] = z ;
	 
	 	double Axis[3] = {1,0,0};
	 
	 	// projection onto cylinder axis
	 	double proj = vtkMath::Dot(Axis, x2C);
	 
	 	// return distance^2 - R^2
	 	return ((vtkMath::Dot(x2C, x2C) - proj * proj) - 1);

}

void MyFuntion1::EvaluateGradient(double x[3], double g[3])
{

}

double MyFuntion2::EvaluateFunction(double d[3])
{
	double x = d[0];
	double y = d[1];
	double z = d[2];

	return x * x + y * y + z * z - 1;
}

void MyFuntion2::EvaluateGradient(double x[3], double g[3])
{

}

double MyFuntion3::EvaluateFunction(double d[3])
{
	double x = d[0];
	double y = d[1];
	double z = d[2];

	if (abs(x) == 1.0)
		return 0;
	if (abs(y) == 1.0)
		return 0;
	if (abs(z) == 1.0)
		return 0;
	return 1;

}

void MyFuntion3::EvaluateGradient(double x[3], double g[3])
{

}



MyFuntion4::MyFuntion4()
{

	symbol_table.add_variable("x", x);
	symbol_table.add_variable("y", y);
	symbol_table.add_variable("z", z);

	symbol_table.add_constants();

	std::string expression_string =
		"x*x + y*y + z*z -1";
	
	expression.register_symbol_table(symbol_table);
	parser.compile(expression_string, expression);
}

double MyFuntion4::EvaluateFunction(double d[3])
{
	x = d[0];
	y = d[1];
	z = d[2];
	return expression.value();
}

void MyFuntion4::EvaluateGradient(double x[3], double g[3])
{

}
