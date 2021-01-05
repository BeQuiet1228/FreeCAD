#ifndef _PM3_MESH_H_
#define _PM3_MESH_H_

//#include <GL/glew.h>

#include <stdio.h>
#include <time.h>
#include <vector>
//#include <vcg/complex/complex.h>
//#include <vcg/complex/allocate.h>
//#include <vcg/complex/algorithms/intersection.h>
//#include <vcg/simplex/face/topology.h>

//#include <vcg/complex/algorithms/update/bounding.h>
//#include <vcg/complex/algorithms/update/color.h>
//#include <vcg/complex/algorithms/update/flag.h>
//#include <vcg/complex/algorithms/update/normal.h>
//#include <vcg/complex/algorithms/update/position.h>
//#include <vcg/complex/algorithms/update/quality.h>
//#include <vcg/complex/algorithms/update/selection.h>
//#include <vcg/complex/algorithms/update/topology.h>

//#include <wrap/gl/trimesh.h>
//#include <wrap/callback.h>
//#include <wrap/io_trimesh/io_mask.h>
//#include <wrap/io_trimesh/additionalinfo.h>

#include "PM3Volume.h"
#include "core/createVolume.h"
#include "PM3VGrid.h"
//#include <vcg/space/color4.h>
//#include <vcg/space/box3.h>
using namespace vcg;
using namespace std;
namespace PM3
{
//template <typename T>
//inline std::string convertToString(T x)
//{
//   std::ostringstream o;
//   if (o << x)
//     return o.str();
//   // 这儿进行一些错误处理...
//   return "conversion error";
//}

// Forward declarations needed for creating the used types
class CVertexO;
class CEdgeO;
class CFaceO;

// Declaration of the semantic of the used types
class CUsedTypesO: public vcg::UsedTypes < vcg::Use<CVertexO>::AsVertexType,
        vcg::Use<CEdgeO   >::AsEdgeType,
        vcg::Use<CFaceO  >::AsFaceType >{};


// The Main Vertex Class
// Most of the attributes are optional and must be enabled before use.
// Each vertex needs 40 byte, on 32bit arch. and 44 byte on 64bit arch.

class CVertexO  : public vcg::Vertex< CUsedTypesO,
        vcg::vertex::InfoOcf,           /*  4b */
        vcg::vertex::Coord3f,           /* 12b */
        vcg::vertex::BitFlags,          /*  4b */
        vcg::vertex::Normal3f,          /* 12b */
        vcg::vertex::Qualityf,          /*  4b */
        vcg::vertex::Color4b,           /*  4b */
        vcg::vertex::VFAdjOcf,          /*  0b */
        vcg::vertex::MarkOcf,           /*  0b */
        vcg::vertex::TexCoordfOcf,      /*  0b */
        vcg::vertex::CurvaturefOcf,     /*  0b */
        vcg::vertex::CurvatureDirfOcf,  /*  0b */
        vcg::vertex::RadiusfOcf         /*  0b */
>{
};


// The Main Edge Class
// Currently it does not contains anything.
class CEdgeO : public vcg::Edge<CUsedTypesO,
        vcg::edge::BitFlags,          /*  4b */
        vcg::edge::EVAdj,
        vcg::edge::EEAdj
>{
};

// Each face needs 32 byte, on 32bit arch. and 48 byte on 64bit arch.
class CFaceO    : public vcg::Face<  CUsedTypesO,
        vcg::face::InfoOcf,              /* 4b */
        vcg::face::VertexRef,            /*12b */
        vcg::face::BitFlags,             /* 4b */
        vcg::face::Normal3f,             /*12b */
        vcg::face::QualityfOcf,          /* 0b */
        vcg::face::MarkOcf,              /* 0b */
        vcg::face::Color4bOcf,           /* 0b */
        vcg::face::FFAdjOcf,             /* 0b */
        vcg::face::VFAdjOcf,             /* 0b */
        vcg::face::WedgeTexCoordfOcf     /* 0b */
> {};

class CMeshO    : public vcg::tri::TriMesh< vcg::vertex::vector_ocf<CVertexO>, vcg::face::vector_ocf<CFaceO> >
{
public :
        int sfn;    //The number of selected faces.
        int svn;    //The number of selected vertices.
        vcg::Matrix44f Tr; // Usually it is the identity. It is applied in rendering and filters can or cannot use it. (most of the filter will ignore this)

        const vcg::Box3f &trBB()
        {
                static vcg::Box3f bb;
                bb.SetNull();
                bb.Add(Tr,bbox);
                return bb;
        }
        void clean();
};


class Polygon
{
public:
        Polygon(int n){visble = true;t=n;v.resize(n);c=vcg::Color4b(255,255,255,255);};

        Polygon() {visble = true;t=0;}
        int t;
        std::vector<vcg::Point3f> v;
        bool visble;
        vcg::Point3f n;
        vcg::Color4b c;
};
class Edge
{
public:
        Edge(int v0, int v1)
        {
            visble = true;v[0]=v0;v[1]=v1;
            c=vcg::Color4b(255,255,255,255);
            if(v[0]>v[1]) std::swap(v[0],v[1]);
        }
        bool operator < (const Edge &p) const
        {
                return (v[1]!=p.v[1])?(v[1]<p.v[1]):
                                       (v[0]<p.v[0]);				}

        bool operator == (const Edge &s) const
        {
         if( (v[0]==s.v[0]) && (v[1]==s.v[1]) ) return true;
         return false;
        }

        int v[2];
        bool visble;
        vcg::Point3f n;
        vcg::Color4b c;
};

class IntersectionPoint
{
public:
    vcg::Point3f p;
    int e;
};

typedef std::vector<vcg::Point3f> ptVec1D;
typedef std::vector<ptVec1D> ptVec2D;

//one ring
void CapHole(CMeshO &m, CMeshO &capMesh, bool reverseFlag);
bool SplitMesh(CMeshO &m,             /// The mesh that has to be splitted. It is NOT changed
               CMeshO &A, CMeshO &B,  /// The two resulting pieces, correct only if true is returned
               vcg::Plane3f plane);

struct IndexSeq
{
    int index;
    int seq;
};

class Mesh : public CVolume
{
public:/*
        MeshLabRenderMesh();
        ~MeshLabRenderMesh();*/

        //WARNING!!!!!: the constructor create a copy of the mesh passed as parameter.
        //The parameter should be const but this is impossible cause of vcg::tri::Append::MeshCopy implementation in the vcglib
//        MeshLabRenderMesh(CMeshO& mesh);

       
        DefValue3D workRegion[2];


		bool blist;

        //vcg::GlTrimesh<CMeshO> glw;
        CMeshO cm;
        std::vector<Polygon> cpolgon;
        VGrid *pgrid;//
        inline vcg::Color4b &C() {return cm.C();};

public:
    Mesh(std::string n, VOLUME_TYPE t);
    ~Mesh();
    /*
    This enum specify the various simplex components
    It is used in various parts of the framework:
    - to know what elements are currently active and therefore can be saved on a file
    - to know what elements are required by a filter and therefore should be made ready before starting the filter (e.g. if a
    - to know what elements are changed by a filter and therefore should be saved/restored in case of dynamic filters with a preview
    */
    enum MeshElement{
            MM_NONE             = 0x00000000,
            MM_VERTCOORD        = 0x00000001,
            MM_VERTNORMAL       = 0x00000002,
            MM_VERTFLAG         = 0x00000004,
            MM_VERTCOLOR        = 0x00000008,
            MM_VERTQUALITY      = 0x00000010,
            MM_VERTMARK	        = 0x00000020,
            MM_VERTFACETOPO     = 0x00000040,
            MM_VERTCURV	        = 0x00000080,
            MM_VERTCURVDIR      = 0x00000100,
            MM_VERTRADIUS       = 0x00000200,
            MM_VERTTEXCOORD     = 0x00000400,
            MM_VERTNUMBER       = 0x00000800,

            MM_FACEVERT         = 0x00001000,
            MM_FACENORMAL       = 0x00002000,
            MM_FACEFLAG	        = 0x00004000,
            MM_FACECOLOR        = 0x00008000,
            MM_FACEQUALITY      = 0x00010000,
            MM_FACEMARK	        = 0x00020000,
            MM_FACEFACETOPO     = 0x00040000,
            MM_FACENUMBER       = 0x00080000,

            MM_WEDGTEXCOORD     = 0x00100000,
            MM_WEDGNORMAL       = 0x00200000,
            MM_WEDGCOLOR        = 0x00400000,

            // 	Selection
            MM_VERTFLAGSELECT   = 0x00800000,
            MM_FACEFLAGSELECT   = 0x01000000,

            // Per Mesh Stuff....
            MM_CAMERA			= 0x08000000,
            MM_TRANSFMATRIX     = 0x10000000,
            MM_COLOR            = 0x20000000,
            MM_POLYGONAL        = 0x40000000,
            MM_UNKNOWN          = 0x80000000,

            MM_ALL				= 0xffffffff
    };
//    enum Property{
//        NOSET=0,//不指定
//        IDEAL,//理想导体，
//        SET,//定义属性
//        VACCUM//真空区域
//    }pro;
    static int countmesh;//总的模型计数
    CanDefineInt nature;
    float polyoffset;

	/// Stores the primitive type ("point_groups", "polyhedra", "teapot", etc).


public:
    bool bclosed;
        void Clear();
        void UpdateBoxAndNormals(); // This is the STANDARD method that you should call after changing coords.
        void cut(vcg::Plane3f pl, bool b);
        void encloseRing(CMeshO &mm, ptVec2D &cc);
        void convert2MeshO(std::vector<Vertex> points,
                           std::vector<Face> faces);
public:
            virtual bool update_mesh_topology(PM3::CanDefineDistance ) {return true;};
            virtual bool update_mesh_topology(PM3::CanDefinePoint ){return true; };
            virtual bool update_mesh_topology() {return true;};
            //bool load(QTextStream &stream);
           // void save(QTextStream &stream);
			int saveOBJ(std::string filename);
            void quantizeVertices();
private:

};
//typedef QList<PM3::Mesh*> MeshList;
}//end pm3
#endif
