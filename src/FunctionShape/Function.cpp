#include "Function.h"

FS::FunctionString::FunctionString()
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

