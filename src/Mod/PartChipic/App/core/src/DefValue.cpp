#include "../DefValue.h"
#include "../basicstring.h"
#include "../pm3parser.h"
namespace PM3
{

void DefValue1D::setValue(std::string in)
{
    /*File file("./unit.KEY");
    std::string unit;
    if(file.open(QIODevice::ReadOnly|QIODevice::WriteOnly))
    {
         QByteArray byte = file.readAll();
        if(!byte.isNull())
        {
            unit = QString(byte);
        }

    }
    for(int i = 0 ;i <in.length();i++)
    {

        if(in[i]>='0'&&in[i]<='9'||in[i]=='.')
        {
            if((i+1)==in.length())
            {
                in=in+unit;
            }
        }else{
            break;
        }
    }*/

    value = in;
    deSpace(value);
}

bool DefValue1D::Parser(ExpParser *pexparser, float &pt, std::string &er)
{
    double vals[4] = {0};
	std::transform(value.begin(), value.end(), value.begin(), ::tolower);
	std::string temp = replace_str(value, "**", "^");
    //QString temp = value.toLower().replace("**", "^");
    if(-1 != pexparser->ParseExp(temp,er)) {//error
        //er = ("表达式")+value +("解析错误!") ;
        return false;
    }
    pt = pexparser->Eval(vals);

    return true;
}
double DefValue1D::getNumber(ExpParser *pexparser)
{
    double pt;
	std::string er;
    double vals[4] = {0};
	std::transform(value.begin(), value.end(), value.begin(), ::tolower);
	std::string temp = replace_str(value, "**", "^");
    //QString temp = value.toLower().replace("**", "^");
    if(-1 != pexparser->ParseExp(temp,er)) {//error
        //er = ("表达式")+value +("解析错误!") ;
        return false;
    }
    pt = pexparser->Eval(vals);

    return pt;
}
bool DefValue1D::Parser(ExpParser *pexparser, double &pt, std::string &er)
{
    double vals[4] = {0};
	std::transform(value.begin(), value.end(), value.begin(), ::tolower);
	std::string temp = replace_str(value, "**", "^");
    //QString temp = value.toLower().replace("**", "^");
    if(-1 != pexparser->ParseExp(temp,er)) {//error
        //er = ("表达式")+value +("解析错误!") ;
        return false;
    }
    pt = pexparser->Eval(vals);

    return true;
}

std::string DefValue1D::getPAP()
{
    if(selfDefName == "-1")
        return value;

    return selfDefName;
}

/*bool DefValue1D::load(QTextStream &stream)
{
    QString line;
    QStringList list;
    do
    {
    line = stream.readLine();
    if (stream.status() != QTextStream::Ok)
        return false;
    }while(line.isEmpty());
    list = line.split(QRegExp(","));
    if(list.at(0) != DEFVALUE_TYPE[0])
        return false;
    if(list.count() == 4)
    {
        name = list.at(1);
        selfDefName = list.at(2);
        value  = list.at(3);
    }
    return true;
}


void DefValue1D::save(QTextStream &stream)
{
    stream << DEFVALUE_TYPE[0] << QLatin1Char(',') <<
              name << QLatin1Char(',') <<
              selfDefName  << QLatin1Char(',') <<
              value << QLatin1Char('\n');
}
bool DefValue3D::isNull()
{
    for(int i=0;i<3;i++)
    {

        if(value[i].isNull())
            return true ;
    }
    return false;
}*/
void DefValue3D::setValue(std::string in)
{
    /*QStringList list;
    deSpace(in);
    QFile file("./unit.KEY");
    QString unit;
    if(file.open(QIODevice::ReadOnly|QIODevice::WriteOnly))
    {
         QByteArray byte = file.readAll();
        if(!byte.isNull())
        {
            unit = QString(byte);
        }

    }*/
	std::string unit = "m";
	std::vector<std::string> list = PM3::split(in, ',');// in.split(QRegExp(","));
    for(int i=0;i<list.size();i++)
    {
      std::string in =  list[i];
        for(int a = 0 ;a <in.length();a++)
        {

			if (in[a] >= '0'&&in[a] <= '9' || in[a] == '.' || in[a] == '-')
            {
                if((a+1)==in.length())
                {
                    value[i] = list.at(i)+unit;
                }
            }else{
                value[i] = list.at(i);
                break;
            }
        }
    }
}

void DefValue3D::setValue(int i,std::string in)
{
    value[i] =in;
    deSpace(value[i]);
}

vcg::Point3f DefValue3D::getNumber(ExpParser *pexparser)
{
    vcg::Point3f pt;
    vcg::Point3f py;
    std::string er;

    double vals[4] = {0};
	std::transform(value[0].begin(), value[0].end(), value[0].begin(), ::tolower);
	std::string temp = replace_str(value[0], "**", "^");
    //QString temp = value[0].toLower().replace("**", "^");
    if(-1 != pexparser->ParseExp(temp,er)){ //error
        return py;
    }
    pt.X() = pexparser->Eval(vals);
	std::transform(value[1].begin(), value[1].end(), value[1].begin(), ::tolower);
	temp = replace_str(value[1], "**", "^");
    //temp = value[1].toLower().replace("**", "^");
    if(-1 != pexparser->ParseExp(temp,er)) {//error
        return py;
    }
    pt.Y() = pexparser->Eval(vals);
	std::transform(value[2].begin(), value[2].end(), value[2].begin(), ::tolower);
	temp = replace_str(value[2], "**", "^");
    //temp = value[2].toLower().replace("**", "^");
    if(-1 != pexparser->ParseExp(temp,er)) {//error
        return py;
    }
    pt.Z() = pexparser->Eval(vals);

    return pt;
}
bool DefValue3D::Parser(ExpParser *pexparser, vcg::Point3f &pt, std::string &er)
{
    double vals[4] = {0};
	std::transform(value[0].begin(), value[0].end(), value[0].begin(), ::tolower);
	std::string temp = replace_str(value[0], "**", "^");
    //QString temp = value[0].toLower().replace("**", "^");
    if(-1 != pexparser->ParseExp(temp,er)){ //error
        //er =("变量")+name+("表达式")+value[0] +("解析错误!") ;
        return false;
    }
    pt.X() = pexparser->Eval(vals);
	std::transform(value[1].begin(), value[1].end(), value[1].begin(), ::tolower);
	temp = replace_str(value[1], "**", "^");
    //temp = value[1].toLower().replace("**", "^");
    if(-1 != pexparser->ParseExp(temp,er)) {//error
        //er = QString::fromLocal8Bit("变量")+name+QString::fromLocal8Bit("表达式")+value[1] +QString::fromLocal8Bit("解析错误!") ;
        return false;
    }
    pt.Y() = pexparser->Eval(vals);
	std::transform(value[2].begin(), value[2].end(), value[2].begin(), ::tolower);
	temp = replace_str(value[2], "**", "^");
    //temp = value[2].toLower().replace("**", "^");
    if(-1 != pexparser->ParseExp(temp,er)) {//error
        //er = QString::fromLocal8Bit("变量")+name+QString::fromLocal8Bit("表达式")+value[2] +QString::fromLocal8Bit("解析错误!") ;
        return false;
    }
    pt.Z() = pexparser->Eval(vals);

    return true;
}

bool DefValue3D::Parser(ExpParser *pexparser, vcg::Point3d &pt, std::string &er)
{
    double vals[4] = {0};
	std::transform(value[0].begin(), value[0].end(), value[0].begin(), ::tolower);
	std::string temp = replace_str(value[0], "**", "^");
    //QString temp = value[0].toLower().replace("**", "^");
    if(-1 != pexparser->ParseExp(temp,er)) {//error
        //er = QString::fromLocal8Bit("点")+name+QString::fromLocal8Bit("的第一个组分")+value[0] +QString::fromLocal8Bit("解析错误!") ;
        return false;
    }
    pt.X() = pexparser->Eval(vals);
	std::transform(value[1].begin(), value[1].end(), value[1].begin(), ::tolower);
	 temp = replace_str(value[1], "**", "^");
   // temp = value[1].toLower().replace("**", "^");
    if(-1 != pexparser->ParseExp(temp,er)) {//error
       // er = QString::fromLocal8Bit("点")+name+QString::fromLocal8Bit("的第一个组分")+value[1] +QString::fromLocal8Bit("解析错误!") ;
        return false;
    }
    pt.Y() = pexparser->Eval(vals);
	std::transform(value[2].begin(), value[2].end(), value[2].begin(), ::tolower);
	temp = replace_str(value[2], "**", "^");
    //temp = value[2].toLower().replace("**", "^");
    if(-1 != pexparser->ParseExp(temp,er)) {//error
        //er = QString::fromLocal8Bit("点")+name+QString::fromLocal8Bit("的第一个组分")+value[2] +QString::fromLocal8Bit("解析错误!") ;
        return false;
    }
    pt.Z() = pexparser->Eval(vals);

    return true;
}

/*bool DefValue3D::load(QTextStream &stream)
{
    QString line;
    QStringList list;
    do
    {
    line = stream.readLine();
//    stream
//           >> selfDefName
//           >> value
    if (stream.status() != QTextStream::Ok)
        return false;
    }while(line.isEmpty());

    list = line.split(QRegExp(","));
    if(list.at(0) != DEFVALUE_TYPE[1])
        return false;
    if(list.count() == 6)
    {
        name = list.at(1);
        selfDefName = list.at(2);
        value[0]  = list.at(3);
        value[1]  = list.at(4);
        value[2]  = list.at(5);
    }
    return true;
}


void DefValue3D::save(QTextStream &stream)
{
    stream << DEFVALUE_TYPE[1] << QLatin1Char(',') <<
              name << QLatin1Char(',') <<
              selfDefName  << QLatin1Char(',') <<
              value[0]   << QLatin1Char(',') <<
              value[1]   << QLatin1Char(',') <<
              value[2]   << QLatin1Char('\n');
}
*/
}

