#pragma  once
#include <vtkImplicitFunction.h>
#include "exprtk.hpp"


namespace FS {
	typedef exprtk::symbol_table<double> symbol_table_t;
	typedef exprtk::expression<double>   expression_t;
	typedef exprtk::parser<double>       parser_t;
	class FunctionString :public vtkImplicitFunction{
	public:
		FunctionString();
		~FunctionString() {};

		void setFunctionString(const std::string& func);
		virtual double EvaluateFunction(double d[3]);
		virtual void EvaluateGradient(double x[3], double g[3]);

		double x, y, z;
		symbol_table_t symbol_table;
		expression_t expression;
		parser_t parser;
	};

}