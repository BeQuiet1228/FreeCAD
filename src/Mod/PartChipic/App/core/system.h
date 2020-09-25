#ifndef _MYSYSTEM_H
#define _MYSYSTEM_H

#include <string>
#include <vcg/complex/complex.h>
#include "basicmath.h"

namespace PM3 {


const int SYSTEM_COUNT = 4;
enum SYSTEM {SYSCARTESIAN, //( x,  y,  z )
             SYSCYLINDRICAL,//(r(>=0),theta(0-360),z)
             SYSMYCC,       //圆柱坐标系
             SYSPOLAR,SYSANY};//( r,  f,  z )
const std::string SYSTEM_NAMES[SYSTEM_COUNT] = {"CARTESIAN","POLAR","CYLINDRICAL", "ANY"};
//{"CARTESIAN","CYLINDRICAL","POLAR", "ANY"};

template <class T>
vcg::Point3<T> car2cyl(vcg::Point3<T> in)
{
    vcg::Point3<T> out;
    out[0] = std::sqrt(in[0]*in[0]+in[1]*in[1]);
    out[1] =std::atan2(in[1],in[0]);//PM3::degrees(PM3::pi()+std::atan2(in[1],in[0])); PM3::pi()+
    out[2] = in[2];
    return out;
}

template <class T>
vcg::Point3<T> cyl2car(vcg::Point3<T> in)
{
    vcg::Point3<T> out;
    out[0] = in[0]*std::cos(in[1]);//out[0] = in[0]*std::cos(PM3::radians(in[1]));
    out[1] = in[0]*std::sin(in[1]);//out[1] = in[0]*std::sin(PM3::radians(in[1]));
    out[2] = in[2];
    return out;
}
template <class T>
vcg::Point3<T> cyl3car(vcg::Point3<T> in)
{
    vcg::Point3<T> out;
    out[1] = in[1]*std::cos(in[2]);//out[0] = in[0]*std::cos(PM3::radians(in[1]));
    out[2] = in[1]*std::sin(in[2]);//out[1] = in[0]*std::sin(PM3::radians(in[1]));
    out[0] = in[0];
    return out;
}
template <class T>
vcg::Point3<T> cyl4car(vcg::Point3<T> in)
{
    vcg::Point3<T> out;
    out[1] = in[2];
    out[2] = in[0];
    out[0] = in[1];
    return out;
}

vcg::Point3d car2pol(vcg::Point3d in);
vcg::Point3d pol2car(vcg::Point3d in);
vcg::Point3d cyl2pol(vcg::Point3d in);
vcg::Point3d pol2cyl(vcg::Point3d in);

}

#endif // SYSTEM_H
