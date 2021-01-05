#include "../system.h"

namespace PM3
{


//enum SYSTEM {CARTESIAN, //( x,  y,  z )
//             CYLINDRICAL,//( z,  r,  f )
//             POLAR};//( r,  f,  z )
/*vcg::Point3d car2cyl(vcg::Point3d in)
{
    vcg::Point3d out;
    out[0] = in[2];
    out[1] = std::sqrt(in[0]*in[0]+in[1]*in[1]);
    out[2] = std::atan(in[1]/in[0]);
    return out;
}*/

/*vcg::Point3d cyl2car(vcg::Point3d in)
{
    vcg::Point3d out;
    out[0] = in[1]*std::cos(in[2]);
    out[1] = in[1]*std::sin(in[2]);
    out[2] = in[0];
    return out;
}*/
//enum SYSTEM {CARTESIAN, //( x,  y,  z )
//             CYLINDRICAL,//( z,  r,  f )
//             POLAR};//( r,  f,  z )
vcg::Point3d car2pol(vcg::Point3d in)
{
    vcg::Point3d out;
    out[0] = std::sqrt(in[0]*in[0]+in[1]*in[1]+in[2]*in[2]);
    out[1] = std::atan(in[1]/in[0]);
    out[2] = std::atan(std::sqrt(in[0]*in[0]+in[1]*in[1])/in[2]);
    return out;
}

vcg::Point3d pol2car(vcg::Point3d in)
{
    vcg::Point3d out;
    out[0] = in[0]*std::cos(in[0])*std::sin(in[2]);
    out[1] = in[0]*std::sin(in[0])*std::sin(in[2]);
    out[2] = in[0]*std::cos(in[2]);
    return out;
}
//enum SYSTEM {CARTESIAN, //( x,  y,  z )
//             CYLINDRICAL,//( z,  r,  f )
//             POLAR};//( r,  f,  z )
vcg::Point3d cyl2pol(vcg::Point3d in)
{
    vcg::Point3d out;
    out[0] = std::sqrt(in[0]*in[0]+in[1]*in[1]);
    out[1] = in[2];
    out[2] = std::atan(in[1]/in[0]);
    return out;
}

vcg::Point3d pol2cyl(vcg::Point3d in)
{
    vcg::Point3d out;
    out[0] = in[0]*std::cos(in[2]);
    out[1] = in[0]*std::sin(in[2]);
    out[2] = in[1];
    return out;

}


}
