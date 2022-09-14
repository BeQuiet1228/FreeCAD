#include "Function.h"
#include <math.h>
#define M_PI       3.14159265358979323846
#define M_PI_2     1.57079632679489661923
FS::FunctionString::FunctionString()
	:x(0),y(0),z(0)
{

}

void FS::FunctionString::setFunctionString(const std::string& func)
{
	symbol_table.add_variable("x", x);
	symbol_table.add_variable("y", y);
	symbol_table.add_variable("z", z);

	symbol_table.add_constants();

	expression.register_symbol_table(symbol_table);
	parser.compile(func, expression);
}

double FS::FunctionString::EvaluateFunction(double d[3])
{
	x = d[0];
	y = d[1];
	z = d[2];
	return expression.value();
}

void FS::FunctionString::EvaluateGradient(double x[3], double g[3])
{

}

FS::FunctionStringClinder::FunctionStringClinder()
	:r(0),t(0),z(0)
{
	rMax = 0.01;
	rMin = -0.01;
	tMax = 360;
	tMin = 0;
	zMax = 0.01;
	zMin = -0.01;
}

FS::FunctionStringClinder::~FunctionStringClinder()
{

}

void FS::FunctionStringClinder::setFunctionString(const std::string& func)
{
	symbol_table.add_variable("r", r);
	symbol_table.add_variable("t", t);
	symbol_table.add_variable("z", z);

	symbol_table.add_constants();

	expression.register_symbol_table(symbol_table);
	parser.compile(func, expression);
}

double  FS::FunctionStringClinder::FastAtan(double x)
{
	if (x < -1.0)
		return -M_PI_2 - x / (x * x + 0.28);

	if (x > 1.0)
		return M_PI_2 - x / (x * x + 0.28);

	return x / (1.0 + x * x * 0.28);
}

double  FS::FunctionStringClinder::FastAtan2(double y, double x)
{
	if (x > 0)
		return FastAtan(y / x);

	if (x < 0)
	{
		const double d = FastAtan(y / x);
		return (y >= 0) ? d + M_PI : d - M_PI;
	}

	if (y < 0.0)
		return -M_PI_2;

	if (y > 0.0)
		return M_PI_2;

	return 0.0;
}

bool FS::FunctionStringClinder::inCylinder()
{
	if (r < rMin)
		return false;
	if (r > rMax)
		return false;
	if (t > tMax)
		return false;
	if (t < tMin)
		return false;
	if (z < zMin)
		return false;
	if (z > zMax)
		return false;
	return true;
}

double FS::FunctionStringClinder::EvaluateFunction(double d[3])
{
	r = sqrt(pow(d[0], 2) + pow(d[1], 2));
	t= FastAtan2(d[1], d[0]);
	t = t > 0 ? t : 2*M_PI + t;
	t = t / (2*M_PI) * 360;
	z = d[2];
	if (!inCylinder())
		return 0.1;
	return expression.value();
}
