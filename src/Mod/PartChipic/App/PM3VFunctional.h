#ifndef VFUNCTIONAL_H
#define VFUNCTIONAL_H
#include "PreCompiled.h"
#include "PM3mesh.h"
#include <TopoDS_Compound.hxx>
#include <TopoDS_Wire.hxx>
#include <TopTools_ListOfShape.hxx>
#include <App/ComplexGeoData.h>
#include <Base/Vector3D.h>
#include "../core/Iso3D.h"
namespace PM3
{
class VFunctional:public PM3::Mesh
{
public:
	VFunctional(std::string n = "VolmFunc", VOLUME_TYPE t = VFUNCTIONAL);
    ~VFunctional();
	std::string f;
    DefValue3D near_point,far_point ;
	myIso3D *iso;
	double yreso;
    //PM3::;
public:
	TopoDS_Shape update_mesh_topology(double &maxf);
	bool update_mesh_topology(std::vector<Base::Vector3d> &Points, std::vector<Data::ComplexGeoData::Facet> &Facets, double &maxf);
	//bool update_mesh_topologyFix(std::vector<Base::Vector3d> &Points, std::vector<Data::ComplexGeoData::Facet> &Facets, double &maxf);
	std::string text();
	std::string getPAP();
    //bool load(QTextStream &stream);
    //void save(QTextStream &stream);
    bool getWorkRegion();

    void setSystem(PM3::SYSTEM s = SYSCARTESIAN);
};
}

#endif // VFUNCTIONAL_H
