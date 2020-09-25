#ifndef _PM3_BASIC_MATCH_H
#define _PM3_BASIC_MATCH_H
//#include <algorithm>
#include <cmath>
#include <math.h>
namespace PM3
{

double trunc(double a);
double round(double a);
float fmin(float a, float b);
double fmax(double a, double b);
double fsqrt(const double *a);

/// Pi
inline double pi()
{
	return 3.1415926535897932384626433832795;
}

/// Pi divided-by two
inline double pi_over_2()
{
	return pi() * 0.5;
}

/// Pi times two
inline double pi_times_2()
{
	return pi() * 2.0;
}

/// Converts degrees to radians
inline double radians(const double degrees)
{
	return degrees * 0.01745329252;
}

/// Converts radians to degrees
inline double degrees(const double radians)
{
	return radians * 57.2957795131;
}

/// Computes N!
inline double factorial(double N)
{
	double result = 1;
	for(double i = 2; i <= N; ++i)
		result *= i;

	return result;
}

/// Computes an integer power of a base via successive squaring
template <typename Type>
Type fast_pow(Type base, int exponent)
{
	bool invert = exponent < 0;
	if (invert)
		exponent = -exponent;

	// loop invariant: prod * base^exponent
	Type prod = Type(1);
	while (exponent > 0) {
		if (exponent % 2 == 0) {
			base *= base;
			exponent /= 2;
		}
		else {
			prod *= base;
			--exponent;
		}
	}

	if (invert)
		prod = Type(1) / prod;

	return prod;
}

/// Returns the sign of an argument: -1 if negative, 0 if zero, +1 if positive
template<class type> double sign(const type& Arg)
{
	if(Arg > 0.0) return 1.0;
	if(Arg < 0.0) return -1.0;

	return 0.0;
}

///// Rounds a value to the closest integer
//inline double round(const double Value)
//{
//	return (Value - std::floor(Value)) < 0.5 ? std::floor(Value) : std::ceil(Value);
//}

/// Clamps a value within the specified range (conforms to SL usage)
template<class type>
type clamp(const type& x, const type& minval, const type& maxval)
{
	return fmin(fmax(x, minval), maxval);
}

/// Returns the linear interpolation of two values
template<class type>
type mix(const type& x, const type& y, const double alpha)
{
	return x * (1 - alpha) + y * (alpha);
}

/// Returns the ratio of two values (handles type-casting to a floating-point value)
template<typename type>
double ratio(const type& x, const type& y)
{
	return static_cast<double>(x) / static_cast<double>(y);
}

////////////////define function:double (*FunctionPtr)(const double*);
double atan2(const double *in);
double nint(const double *x);
double sign(const double *x);
double negtive(const double *x);
double step(const double *x/*,double y*/);
double theta(const double *x);
double ramp(const double *x);
double smooth_ramp(const double *x);
double Max(double d1, double d2);


}

#endif
