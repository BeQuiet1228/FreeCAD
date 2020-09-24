#ifndef _PM3_VGRID_H
#define _PM3_VGRID_H

#include "pm3volume.h"

namespace PM3
{
class VGrid : public CVolume
{
public:
	VGrid(std::string name = "SIMUVOLUME", VOLUME_TYPE type = GRID);
    ~VGrid(){};
	std::string name;
     PM3::DefValue1D x1_1,x1_2,x1_3,x2_1,x2_2,x2_3,x3_1,x3_2,x3_3;
     bool checkBox;
     std::string getGS();
	 std::string getGG();
	 std::string para;
     CanDefineInt num;
     //bool load(QTextStream &stream);
     //void save(QTextStream &stream);

     float getRadius();
     float getresolu();

void setSystem(SYSTEM s = SYSCARTESIAN);
};
}
#endif // VGRID_H
