#ifndef POINT_H
#define POINT_H


#include "../core/pm3core.h"
#include "ableout.h"
#include "ableglrender.h"
#include <vcg/space/color4.h>
#include <vcg/space/box3.h>
namespace PM3
{
/*
 LINE  line {CONFORMAL  point1  point2... ,
                OBLIQUE  point1  point2... ,
                CIRCULAR  point1  point2  point3 ,
               ELLIPTICAL  point  x_radius  y_radius start_angle  end_angle } ;
 */
//不支持2D
class CPoint:public ableOut, ableGLRender
{
public:
    CPoint(std::string n=""){};
    ~CPoint(){};
    //std::string name;               // —  name of spatial line, user-defined.
	vcg::Point3f p;
    std::string text();
};
}
#endif // POINT_H
