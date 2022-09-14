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

		virtual void setFunctionString(const std::string& func);
		virtual double EvaluateFunction(double d[3]);
		virtual void EvaluateGradient(double x[3], double g[3]);
		
	protected:
		symbol_table_t symbol_table;
		expression_t expression;
		parser_t parser;
	private:
		double x, y, z;
	};

	class FunctionStringClinder :public FunctionString {
	public:
		FunctionStringClinder();
		~FunctionStringClinder();

		void setFunctionString(const std::string& func) override;
		virtual double EvaluateFunction(double d[3]) override;
	private:
		double FastAtan(double x);
		double FastAtan2(double y, double x);
		//判断当前的r t z 是否在函数设定的范围内
		bool inCylinder();
	private:
		double r, t, z;
		/*
			约束函数的取值范围，由于vtk处理范围时使用直角坐标系，
			及一个长方体来显示函数的范围。
			而极坐标系的范围应该是一个圆柱体，所以需要在函数中直接做处理
		*/
		double rMax, rMin, tMax, tMin, zMax, zMin;

	};

}