#include "Pm3VGrid.h"
namespace PM3
{
VGrid::VGrid(std::string n,VOLUME_TYPE type ):CVolume(n,type)
{
    name = std::string("SIMUVOLUME");
    setSystem(gsysType);
}

void  VGrid::setSystem(PM3::SYSTEM s)
{
    checkBox = false;
    para=std::string("");
    num.value = 0;

    CVolume::setSystem(s);

    if(gsysType == PM3::SYSCYLINDRICAL)
    {
    x1_1.setValue("0mm");
    x1_2.setValue("0mm");
    x1_3.setValue("1mm");
    x2_1.setValue("0deg");
    x2_2.setValue("360deg");
    x2_3.setValue("1deg");
    x3_1.setValue("0mm");
    x3_2.setValue("0mm");
    x3_3.setValue("1mm");
    }
    if(gsysType == PM3::SYSMYCC)
    {
    x1_1.setValue("0mm");
    x1_2.setValue("0mm");
    x1_3.setValue("1mm");
    x2_1.setValue("0mm");
    x2_2.setValue("0mm");
    x2_3.setValue("1mm");
    x3_1.setValue("0deg");
    x3_2.setValue("360deg");
    x3_3.setValue("1deg");
    }
    if(gsysType == PM3::SYSCARTESIAN)
    {
        x1_1.setValue("0mm");
        x1_2.setValue("0mm");
        x1_3.setValue("1mm");
        x2_1.setValue("0mm");
        x2_2.setValue("0mm");
        x2_3.setValue("1mm");
        x3_1.setValue("0mm");
        x3_2.setValue("0mm");
        x3_3.setValue("1mm");
    }
}

float VGrid::getresolu()
{
    std::string re;
    if(gsysType == PM3::SYSCYLINDRICAL )
    {
        float x,y,z;
        x1_3.Parser(pexparser, x, re);
        x2_3.Parser(pexparser, y, re);
        x3_3.Parser(pexparser, z, re);
        return std::min(x,y)*0.01;//0.05
    }
    else
    {
        float x,y,z;
        x1_3.Parser(pexparser, x, re);
        x2_3.Parser(pexparser, y, re);
        x3_3.Parser(pexparser, z, re);
        return std::min(std::min(x,y),z)*0.01;
    }
}


float VGrid::getRadius()
{
    std::string re;
    if(gsysType == PM3::SYSMYCC)
    {
        float x1 = 0;
        float x2 = 0;
        float x3 = 0;
        float x4 = 0;
        x1_1.Parser(this->pexparser, x1, re);
        x1_2.Parser(this->pexparser, x2, re);
        x2_1.Parser(this->pexparser, x3, re);
        x2_2.Parser(this->pexparser, x4, re);
        x1 = fabs(x1);
        x2 = fabs(x2);
        x3 = fabs(x3);
        x4 = fabs(x4);
        float m1  = fmax(x1,x2);
        float m2  = fmax(x3,x4);

        float m = fmax(m1,m2);

        return m/getresolu();
    }
    if(gsysType == PM3::SYSCYLINDRICAL)
    {
        float x1 = 0;
        float x2 = 0;
        float x5 = 0;
        float x6 = 0;
        x1_1.Parser(this->pexparser, x1, re);
        x1_2.Parser(this->pexparser, x2, re);
        x3_1.Parser(this->pexparser, x5, re);
        x3_2.Parser(this->pexparser, x6, re);
        x1 = fabs(x1);
        x2 = fabs(x2);
        x5 = fabs(x5);
        x6 = fabs(x6);
        float m1  = fmax(x1,x2);
        float m3  = fmax(x5,x6);

        float m = fmax(m1,m3);

        return m/getresolu();
    }
    else if(gsysType == PM3::SYSCARTESIAN)
    {
        float x1 = 0;
        float x2 = 0;
        float x3 = 0;
        float x4 = 0;
        float x5 = 0;
        float x6 = 0;

        x1_1.Parser(this->pexparser, x1, re);
        x1_2.Parser(this->pexparser, x2, re);
        x2_1.Parser(this->pexparser, x3, re);
        x2_2.Parser(this->pexparser, x4, re);
        x3_1.Parser(this->pexparser, x5, re);
        x3_2.Parser(this->pexparser, x6, re);
        x1 = fabs(x1);
        x2 = fabs(x2);
        x3 = fabs(x3);
        x4 = fabs(x4);
        x5 = fabs(x5);
        x6 = fabs(x6);
        float m1  = fmax(x1,x2);
        float m2  = fmax(x3,x4);
        float m3  = fmax(x5,x6);
        float m4  = fmax(m1,m2);

        float m   = fmax(m3,m4);

        return m/getresolu();

    }
}

std::string VGrid::getGS()
{
    std::string out;
        //out += std::string("  DX1 = %1 ;\n").arg(x1_3.value);
        //out += std::string("  DX2 = %1%2 ;\n").arg(x2_3.value).arg(x2);
        //out += std::string("  DX3 = %1 ;\n").arg(x3_3.value);
    return out;
}

std::string VGrid::getGG()
{
    std::string out;
    //out += std::string("  POINT %1.LO %2, %3%4, %5 ;\n").arg(name).arg(x1_1.value).arg(x2_1.value).arg(x2).arg(x3_1.value);
    //out += std::string("  POINT %1.HI %2, %3%4, %5 ;\n").arg(name).arg(x1_2.value).arg(x2_2.value).arg(x2).arg(x3_2.value);
    //out += std::string("  VOLUME %1 CONFORMAL %2.LO %3.HI ;\n").arg(name).arg(name).arg(name);
   // out += std::string("  MARK %1 X1 SIZE DX1 ;\n").arg(name);
    //out += std::string("  MARK %1 X2 SIZE DX2 ;\n").arg(name);
    //out += std::string("  MARK %1 X3 SIZE DX3 ;\n").arg(name);
    return out;
}

/*bool VGrid::load(QTextStream &stream)
{
    if(!CVolume::load(stream))
        return false;


    std::string line;
    QStringList list;
    do
    {
    line = stream.readLine();
    if (stream.status() != QTextStream::Ok)
        return false;
    }while(line.isEmpty());

    list = line.split(QRegExp("\\s+"));

    if(list.count() == 1)
    {
        name =list.at(0);

    }
    else
        return false;
    if(!x1_1.load(stream)||!x1_2.load(stream)||!x1_3.load(stream)||
    !x2_1.load(stream)||
    !x2_2.load(stream)||
    !x2_3.load(stream)||
    !x3_1.load(stream)||
    !x3_2.load(stream)||
    !x3_3.load(stream)||
    !num.load(stream))
         return false;

    line = stream.readLine();
    checkBox = line.toInt();
    int n = stream.readLine().toInt();
    for(int i = 0; i < n; i++)
        para += stream.readLine()+"\n";

    return true;

}
void VGrid::save(QTextStream &stream)
{
    CVolume::save(stream);

    stream << name  << QLatin1Char('\n');
    x1_1.save(stream);
    x1_2.save(stream);
    x1_3.save(stream);
    x2_1.save(stream);
    x2_2.save(stream);
    x2_3.save(stream);
    x3_1.save(stream);
    x3_2.save(stream);
    x3_3.save(stream);
    num.save(stream);
    stream<< checkBox <<QLatin1Char('\n');
    QStringList lists = para.split("\n");
    stream << lists.size() << QLatin1Char('\n');

    for(int i = 0; i < lists.size(); i++)
    {
        stream << lists[i]<<QLatin1Char('\n');;

    }
}*/
}
