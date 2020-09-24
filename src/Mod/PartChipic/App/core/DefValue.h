#ifndef DEF_VALUE_H
#define DEF_VALUE_H

#include <string>
//#include <QTextStream>
#include <vcg/complex/complex.h>


namespace PM3
{
class ExpParser;
//对话框的模型参数值
enum DEFVALUE_TYPE {
    DEFV1D,
    DEFV3D
};
const std::string SefDefFlag = "-1";
const std::string DEFVALUE_TYPE[] = { "V1D", "V3D" };
class DefValue1D
{
public:
    DefValue1D():selfDefName(SefDefFlag){setValue();}
    ~DefValue1D(){}
//private:
	std::string value;
public:
	std::string selfDefName;//-1为自定义
	std::string name;
    inline DefValue1D& operator=(const DefValue1D& m);
	void setValue(std::string in = "0");
	std::string getValue() { return value; }
    //bool load(QTextStream &stream);
    //void save(QTextStream &stream);
	std::string getPAP();
    double getNumber(ExpParser *pexparser);
	bool Parser(ExpParser *pexparser, float &pt, std::string &er);
	bool Parser(ExpParser *pexparser, double &pt, std::string &er);
};

inline DefValue1D& DefValue1D::operator=(const DefValue1D& m)
{
    selfDefName = m.selfDefName;
    value = m.value;
    return *this;
}

class DefValue3D
{
public:
    DefValue3D():selfDefName(SefDefFlag){setValue();}
    ~DefValue3D(){}
//private:
	std::string value[3];
    bool isNull();
public:

    vcg::Point3f getNumber(ExpParser *pexparser);

	std::string selfDefName;//-1为自定义

	std::string name;
    inline DefValue3D& operator=(const DefValue3D& m);
	void setValue(std::string in);
	void setValue(int i, std::string in);
    void setValue(){}
	std::string getValue(int i) { return value[i]; }
    //bool load(QTextStream &stream);
    //void save(QTextStream &stream);
	bool Parser(ExpParser *pexparser, vcg::Point3f &pt, std::string &er);
	bool Parser(ExpParser *pexparser, vcg::Point3d &pt, std::string &er);

	inline std::string & operator [] (const int i)
    {
            assert(i>=0 && i<3);
            return value[i];
    }
	inline const std::string &X() const { return value[0]; }
	inline const std::string &Y() const { return value[1]; }
	inline const std::string &Z() const { return value[2]; }
	inline std::string &X() { return value[0]; }
	inline std::string &Y() { return value[1]; }
	inline std::string &Z() { return value[2]; }
};

inline DefValue3D& DefValue3D::operator=(const DefValue3D& m)
{
    selfDefName = m.selfDefName;
    value[0] = m.value[0];
    value[1] = m.value[1];
    value[2] = m.value[2];
    return *this;
}

}
#endif // PARADEFINE_H
