#include "../basicmath.h"
//#include <algorithm>

namespace PM3
{

double trunc(double a) {
        return (a >= 0) ? floor(a) : ceil(a);
}

double round(double a) {
        return a < 0 ? ceil(a - 0.5f) : floor(a + 0.5f);
}

float fmin(float a, float b) {
        return a < b ? a : b;
}

double fmax(double a, double b) {
        return a > b ? a : b;
}
////////////////define function:double (*FunctionPtr)(const double*);
double atan2(const double *in)
{
    double y,x;
    y = in[0];
    x = in[1];
    //THIS SUB DELETE THE BLANK CHAR IN STRING.
        float a,t;
        float PI= 3.141592f;
        if(x!=0.f)
        {
                a=abs(y)/abs(x);
                t=atan(a);
                if(x>0.f)
                {
                        if(y>=0.f)
                                return a;
                        else
                                return -a;
                }
                else
                {
                        if(y>=0.f)
                                return PI-a;
                        else
                                return -PI+a;
                }
        }
        else
        {
                if(y>=0.f)
                        return PI/2.f;
                else
                        return -PI/2.f;
        }
}
double nint(const double *x)
{
    double b;
    if(*x>=0.f)
            b=*x+0.5;
    else
            b=*x-0.5;
    return int(b);
}
double sign(const double *x)
{
        if(*x>0.f)
                return 1.f;
        else
                return -1.f;
}

double negtive(const double *x)
{
	if (*x>0.f)
		return 0.f;
	else
		return 1.f;
}
//float CCvtExpress:: GAUSSIAN(float x,float y)
//{
//	return 0.;
//}
//float CCvtExpress:: RANDOM()
//{
//	return 0.;
//}
double step(const double *x/*,double y*/)
{
    if(x[0]>x[1])
                return 1.f;
    else if(x[0]==x[1])
                return 0.5f;
        else
                return 0.f;
}
double theta(const double *x)
{
        if(*x>0.f)
                return 1.f;
        else
                return 0.f;
}

double ramp(const double *x)
{
    return(fmax(0.,fmin(1.,*x)));
}
double smooth_ramp(const double *x)
{
    double a,b;
    double PI= 3.141592f;
    b=ramp(x);
    a=sin(PI/(2.f)*b);
    a=a*a;

    return a;
}
double fsqrt(const double *a)
{
    return sqrt(*a);
}
}
