#include "PM3Volume.h"



namespace PM3
{
float workspcaeRadius;
void PM3::CVolume::setProperty(PROPERTY p)
{
    property = p;

}

void PM3::CVolume::setProperty(std::string str)
{
    for(int i = 0; i < PROPERTY_COUNT; i++)
    {
        if(PROPERTY_NAMES[i] == str )
            setProperty((PROPERTY)i);
    }
}

/*bool PM3::CVolume::load(QTextStream &stream)
{
;


    std::string line;
    QStringList list;
    do
    {
    line = stream.readLine();
    if (stream.status() != QTextStream::Ok)
        return false;
    }while(line.isEmpty());

    list = line.split(QRegExp("\\s+"));
    if(list.at(0) != "VOLUME")
        return false;
    if(list.count() != 14)
        return false;
    setProperty(list.at(1));
    bvalid=list.at(2).toInt();
    markxD=list.at(3).toInt();
    markyD=list.at(4).toInt();
    markzD=list.at(5).toInt();
    checkSigma=list.at(6).toInt();
    checkEps=list.at(7).toInt();
    checkn1=list.at(8).toInt();

    lineEditSigma =list.at(9);
    lineEditEps1 =list.at(10);
    lineEditEps2 =list.at(11);
    lineEditEps3 =list.at(12);

    dim = list.at(13).toInt();

    if(!lineEdit_markxD.load(stream) ||
       !lineEdit_markyD.load(stream) ||
       !lineEdit_markzD.load(stream))
        return false;

    return true;
}

void PM3::CVolume::save(QTextStream &stream)
{


    stream << "VOLUME" << QLatin1Char(' ')
           << PROPERTY_NAMES[property] << QLatin1Char(' ')
//           << markx << QLatin1Char(' ')
//           << marky << QLatin1Char(' ')
//           << markz << QLatin1Char(' ')
           << bvalid << QLatin1Char(' ')
           << markxD  << QLatin1Char(' ')
           << markyD  << QLatin1Char(' ')
           << markzD  << QLatin1Char(' ')
           << checkSigma << QLatin1Char(' ')
           << checkEps<< QLatin1Char(' ')
           << checkn1 << QLatin1Char(' ')
           << lineEditSigma  << QLatin1Char(' ')
           << lineEditEps1  << QLatin1Char(' ')
           << lineEditEps2  << QLatin1Char(' ')
           << lineEditEps3  << QLatin1Char(' ')
             << dim << QLatin1Char('\n');

    lineEdit_markxD.save(stream);
    lineEdit_markyD.save(stream);
    lineEdit_markzD.save(stream);
}*/
}
