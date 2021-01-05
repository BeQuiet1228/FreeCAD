#include "../Point.h"
namespace PM3
{
std::string CPoint::text()
 {
     std::string out;
     out += "POINT ";
     out += name;
     out += " ";
     //out += x();
    // out += y();
    // out += z();
     out += "\n";

     return out;
 }
}
