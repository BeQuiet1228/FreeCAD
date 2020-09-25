#ifndef ABLEOUT_H
#define ABLEOUT_H
#include <string>
//#include <QStringList>
//#include <QTextStream>
#include "createVolume.h"
namespace PM3
{
class ableOut
{
public:
    ableOut():_id(-1){};
    ~ableOut() {};
	std::string name;
    int _id;//模型序号
	virtual std::string text() { return ""; };
	virtual std::string textgl() { return text(); };
	virtual std::string getPAP(){ return ""; };
	virtual std::string getAP(){ return ""; };
    virtual bool getWorkRegion(){return false;};
    virtual void getFaceAndPoint(std::vector<Vertex> &points,std::vector<Face> &faces){};
};
}
#endif // ABLEOUT_H
