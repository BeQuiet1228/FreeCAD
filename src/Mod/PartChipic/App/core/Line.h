#ifndef LINE_H
#define LINE_H

#include "../core/pm3core.h"
#include "ableout.h"
#include "ableglrender.h"
#include "Point.h"
#include <vcg/space/box3.h>
namespace PM3
{
	enum LINE{
        CONFORMAL=0,
        OBLIQUE,
        CIRCULAR,//2D
        ELLIPTICAL//2D
    };
/*
 LINE  line {CONFORMAL  point1  point2... ,
                OBLIQUE  point1  point2... ,
                CIRCULAR  point1  point2  point3 ,
               ELLIPTICAL  point  x_radius  y_radius start_angle  end_angle } ;
 */
//不支持2D
class CLine:public ableOut, ableGLRender
{
public:
    CLine(std::string n,LINE t=CONFORMAL){};
    ~CLine(){};
    LINE type;
    //std::string line;               // —  name of spatial line, user-defined.

    std::vector<CPoint> point;//— spatial coordinates or name of spatial point defined in POINT command.
    //2D
    float x_radius;//    —  radius in x-axis (m).
    float y_radius;//    —  radius in y-axis (m).
    float start_angle;//—end-point angle (rad).
    float end_angle;//  —end-point angle (rad).
};
}
#endif // LINE_H
