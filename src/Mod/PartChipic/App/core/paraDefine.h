#ifndef PARADEFINE_H
#define PARADEFINE_H

#include <string>
#include <vcg/complex/complex.h>
namespace PM3
{
enum CANDEFINE_TYPE {
    CANINT,
    CANFLOAT,
    CANPOINT,
    CANANY
};
const std::string CANDEFINE_NAMES[] = {"CANINT","CANFLO","CANPOI","CANANY"};
template <class T, CANDEFINE_TYPE V = CANFLOAT>
class CanDefine
{
public:
    CanDefine():defType(V),refcount(0),selfDef(-1){};
    ~CanDefine(){};
    CANDEFINE_TYPE defType;
    //
    int selfDef;//-1为自定义
    int refcount;//被应用次数
    std::string name;

    T value;

    inline CanDefine& operator=(const CanDefine& m);
    //bool load(QTextStream &stream);
    //void save(QTextStream &stream);
};
typedef CanDefine<int, CANINT> CanDefineInt;
typedef CanDefine<float, CANFLOAT> CanDefineDistance, CanDefineDegree;
typedef CanDefine<vcg::Point3f,CANPOINT> CanDefinePoint;

template <class T, CANDEFINE_TYPE V>
inline CanDefine<T,V>& CanDefine<T,V>::operator=(const CanDefine<T,V>& m)
{
    defType = m.defType;
    selfDef = m.selfDef;
    refcount = m.refcount;
    name = m.name;
    value = m.value;
    return *this;
}

//class CanDefineDistance:public CanDefine
//{
//public:
//    CanDefineDistance(CANDEFINE_TYPE t = CANFLOAT):CanDefine(t),value(0){};
//    ~CanDefineDistance(){};


//};

//class CanDefinePoint:public CanDefine
//{
//public:
//    CanDefinePoint(CANDEFINE_TYPE t = CANPOINT):CanDefine(t),value(0,0,0){};
//    ~CanDefinePoint(){};

//    vcg::Point3f value;

//};

}
#endif // PARADEFINE_H
