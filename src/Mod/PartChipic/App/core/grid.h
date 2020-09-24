#ifndef GRID_H
#define GRID_H
#include "defvalue.h"
namespace PM3
{
class Grid{
public:
    Grid();
    ~Grid();
    PM3::DefValue1D x1_1,x1_2,x1_3,x2_1,x2_2,x2_3,x3_1,x3_2,x3_3;
};
}
#endif // GRID_H
