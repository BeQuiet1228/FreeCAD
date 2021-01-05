#include "../paraDefine.h"

namespace PM3
{
/*template<>
bool CanDefineInt::load(QTextStream &stream)
{
    QString line;
    QStringList list;
    do
    {
    line = stream.readLine();
//    stream >> str
//           >> selfDef
//           >> refcount
//           >> value
//           >> name;
    if (stream.status() != QTextStream::Ok)
        return false;
    }while(line.isEmpty());

    list = line.split(QRegExp("\\s+"));
    if(list.at(0) != CANDEFINE_NAMES[defType])
        return false;
    if(list.count() == 5)
    {
        selfDef = list.at(1).toInt();
        refcount = list.at(2).toInt();
        value  = list.at(3).toInt();
        name = list.at(4);
    }
    else if(list.count() == 4)
    {
        selfDef = list.at(1).toInt();
        refcount = list.at(2).toInt();
        value  = list.at(3).toInt();
    }
    else
        return false;
    return true;
}

template<>
void CanDefineInt::save(QTextStream &stream)
{
    stream << CANDEFINE_NAMES[defType]  << QLatin1Char(' ')
           << selfDef  << QLatin1Char(' ')
           << refcount  << QLatin1Char(' ')
           << value  << QLatin1Char(' ')
           << name  << QLatin1Char('\n');
}
template<>
bool CanDefineDistance::load(QTextStream &stream)
{
    QString line;
    QStringList list;
    do
    {
    line = stream.readLine();
//    stream >> str
//           >> selfDef
//           >> refcount
//           >> value
//           >> name;
    if (stream.status() != QTextStream::Ok)
        return false;
    }while(line.isEmpty());

    list = line.split(QRegExp("\\s+"));
    if(list.at(0) != CANDEFINE_NAMES[defType])
        return false;
    if(list.count() == 5)
    {
        selfDef = list.at(1).toInt();
        refcount = list.at(2).toInt();
        value  = list.at(3).toFloat();
        name = list.at(4);
    }
    else if(list.count() == 4)
    {
        selfDef = list.at(1).toInt();
        refcount = list.at(2).toInt();
        value  = list.at(3).toFloat();
    }
    else
        return false;
    return true;
}

template<>
void CanDefineDistance::save(QTextStream &stream)
{
    stream << CANDEFINE_NAMES[defType]  << QLatin1Char(' ')
           << selfDef  << QLatin1Char(' ')
           << refcount  << QLatin1Char(' ')
           << value  << QLatin1Char(' ')
           << name  << QLatin1Char('\n');
}

template<>
bool CanDefinePoint::load(QTextStream &stream)
{
    QString line;
    QStringList list;
    do{
    line = stream.readLine();
//    stream >> str
//           >> selfDef
//           >> refcount
//           >> value[0]
//           >> value[1]
//           >> value[2]
//              >> name;

    if (stream.status() != QTextStream::Ok)
        return false;
    }while(line.isEmpty());
    list = line.split(QRegExp("\\s+"));
    if(list.at(0) != CANDEFINE_NAMES[defType])
        return false;
    if(list.count() == 7)
    {
        selfDef = list.at(1).toInt();
        refcount = list.at(2).toInt();
        value[0]  = list.at(3).toFloat();
        value[1]  = list.at(4).toFloat();
        value[2]  = list.at(5).toFloat();
        name = list.at(6);
    }
    else if(list.count() == 6)
    {
        selfDef = list.at(1).toInt();
        refcount = list.at(2).toInt();
        value[0]  = list.at(3).toFloat();
        value[1]  = list.at(4).toFloat();
        value[2]  = list.at(5).toFloat();
    }
    else
        return false;
    return true;
}

template<>
void CanDefinePoint::save(QTextStream &stream)
{
    stream << CANDEFINE_NAMES[defType]  << QLatin1Char(' ')
           << selfDef  << QLatin1Char(' ')
           << refcount  << QLatin1Char(' ')
           << value[0]  << QLatin1Char(' ')
              << value[1]  << QLatin1Char(' ')
                 << value[2]  << QLatin1Char(' ')
                    << name  << QLatin1Char('\n');
}*/
}

