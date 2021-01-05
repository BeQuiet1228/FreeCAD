#ifndef PM3_VOLUME_H
#define PM3_VOLUME_H
#include "core/pm3core.h"
#include "core/ableout.h"
#include "core/ableglrender.h"
#include "core/Point.h"
#include "core/Line.h"

namespace PM3
{
//name    — name of volume object, user—defined.

//shape    — defined volumetric shapes.

const int VOLUME_COUNT = 48;//30+16;
enum VOLUME_TYPE {VANNULAR=0,  VANNULAR_SECTION,  VCONE,  VCONFORMAL,
                  VCYLINDRICAL,  VEXTRUDED,  VFUNCTIONAL,  VHELICAL,
                  VLATHE,  VPARALLELEPIPEDAL,  VPYRAMID,  VRHOMBUS,
                  VROTATE, VSPHERICAL,  VTETRAHEDRON,  VTOROIDAL_SECTION,  VWEDGE,
                  VPORTWAVE=17,VFREESAPCE=18,VSYSBOUNDARY=19,VCURRENTSOURCE=20,VINDUCTANCE=21,VTIMEOB=22,VCONTOUR=23,VFOIL,VVECTOR,VRANGE,VDEFPOINT,VDEFLINE,VDEFSURFACE,
                  PHASE_SPACE=30,  TIMER,  BEAN,  EXPLOSIVE,
                                    GYRO,  HIGH_FIELD,THERMIONIC,GRID,VDEFTIMER,VRUNOPTIONS,VSIMUSET,VDUMPOP,HEADER,VCOMPRE,NEWMATERIAL,VSOLENOID,
                   LOOKSURFACE,CIRCULATION
                 };
const std::string VOLUME_TYPE_NAME[VOLUME_COUNT] = {"ANNULAR","ANNULAR_SECTION","CONE", "CONFORMAL",
                             "CYLINDRICAL", "EXTRUDED", "FUNCTIONAL", "HELICAL",
                             "LATHE", "PARALLELEPIPEDAL","PYRAMID", "RHOMBUS",
                             "ROTATE", "SPHERICAL",  "TETRAHEDRON", "TOROIDAL_SECTION", "WEDGE",
                                                "Waveguide_port","FREE_SPACE","Symmetric_Boundary","CURRENT_SOURCE","INDUCTANCE","TimeOb","Contour",
                                                "Foil","Vector","Range","DefPoint","DefLine","DefSurface","Phase","Timer", "Beam","Explosive", "gyro","High_field","Thermionic","grid","Deftimer","Runoptions","Simuset","Dumpop","Header","Compre","Newmaterial","SOLENOID","LOOKSURFACE"};
const int PROPERTY_COUNT = 4;
enum PROPERTY {PRO_NODEFINE=0, PRO_IDEAL, PRO_DEFINE, PRO_EMPTY};
const std::string PROPERTY_NAMES[PROPERTY_COUNT] = { "NODEFINE", "IDEAL", "DEFINE", "EMPTY" };
const std::string CURRENT_SRC_NAME[] = {
    "PointSrc","LineSrc","SurfaceSrc","VolumeSrc"
};
enum CURRENT_SRC_TYPE {
    CUR_POINT_SRC = 0,CUR_LINE_SRC,CUR_SURFACE_SRC,CUR_VOLUME_SRC
};
const std::string TIME_OB_NAME[] = {
    "PointOb","LineOb","SurfaceOb","VolumeOb"
};
enum TIME_OB_TYPE {
    TIME_POINT_OB = 0,TIME_LINE_OB,TIME_SURFACE_OB,TIME_VOLUME_OB
};

/*enum Property{
    NOSET=0,//???
    IDEAL,//?????
    SET,//????
    VACCUM//????
}pro;*/


//class ableOut
//{
//public:
//    ableOut(VOLUME_TYPE t):_id(-1),volType(t){};
//    ~ableOut() {};
//    VOLUME_TYPE volType;
//    std::string name;
//    int _id;//????
//    virtual std::string text() {return "";};
//};
extern float workspcaeRadius;
class CVolume :public PM3::ableOut, public PM3::ableGLRender
{
public:
	CVolume(std::string n, VOLUME_TYPE t, SYSTEM s = SYSCARTESIAN) :vol(0), pexparser(0), volType(t), bvalid(true),
        property(PRO_NODEFINE),lineEditSigma("0.05"),lineEditEps1("1.0"),lineEditEps2("1.0"),
        lineEditEps3("1.0"),checkSigma(true),checkEps(true),checkn1(true),
        markxD(true),markyD(true),
        markzD(true),x2(""),convexity(2),dim(3){setSystem(s);name = n;lineEdit_markxD.value = "DX1";
                                                            lineEdit_markyD.value = "DX2";lineEdit_markzD.value = "DX3";}
    ~CVolume(){};
	PM3::ExpParser *pexparser;
    VOLUME_TYPE volType;
    SYSTEM gsysType;
    PROPERTY property;
    bool markxD,markyD,markzD,checkSigma,checkEps,checkn1;
    bool bvalid;
	std::string lineEditSigma, lineEditEps1, lineEditEps2, lineEditEps3;
    PM3::DefValue1D lineEdit_markxD,lineEdit_markyD,lineEdit_markzD;
    float vol;
    int convexity ;
    int dim;
	std::string x2;
    void setSystem(SYSTEM s = SYSCARTESIAN) {gsysType = s;
                                                  if(gsysType == SYSCARTESIAN)
													  x2 = std::string("");
                                                    else if(gsysType == SYSCYLINDRICAL)
														x2 = std::string("");
	}
    void setProperty(PROPERTY);
	void setProperty(std::string str);
   // bool load(QTextStream &stream);
   // void save(QTextStream &stream);
};
}

#endif // VOLUME_H
