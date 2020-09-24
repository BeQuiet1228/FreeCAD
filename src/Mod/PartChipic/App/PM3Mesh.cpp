#include "PreCompiled.h"
#include "PM3Mesh.h"
//#include <GL/glew.h>

//#include <wrap/gl/space.h>


#include<vcg/complex/complex.h>
#include<vcg/complex/append.h>

// input output
#include<wrap/io_trimesh/import.h>
#include<wrap/io_trimesh/export.h>

// topology computation
#include<vcg/complex/algorithms/update/topology.h>
#include<vcg/complex/algorithms/update/bounding.h>
#include<vcg/complex/algorithms/update/normal.h>
#include <vcg/complex/algorithms/update/position.h>
#include <vcg/complex/algorithms/update/quality.h>
#include <vcg/complex/algorithms/stat.h>

#include <vcg/complex/algorithms/intersection.h>
#include <vcg/complex/algorithms/refine.h>
//#include <wrap/gl/glu_tessellator_cap.h>


namespace PM3
{



	int PM3::Mesh::countmesh = 0;

void CMeshO::clean()
{
    vcg::tri::Clean<CMeshO>::RemoveDuplicateVertex(*this);
	//vcg::tri::Clean<CMeshO>::RemoveUnreferencedVertex(*this);
    vcg::tri::Clean<CMeshO>::RemoveDegenerateVertex(*this);
    vcg::tri::Clean<CMeshO>::RemoveDuplicateFace(*this);
    vcg::tri::Clean<CMeshO>::RemoveDegenerateFace(*this);
    //vcg::tri::Clean<CMeshO>::RemoveNonManifoldFace(*this);
}


//MeshLabRenderMesh::MeshLabRenderMesh()
//    :glw(),cm(),bvisable(true),glObject(-1)
//{
//    cm.Tr.SetIdentity();
//    glw.m = &cm;
//}

//MeshLabRenderMesh::MeshLabRenderMesh(CMeshO& mesh )
//    :glw(),cm(),bvisable(true),glObject(-1)
//{
//    vcg::tri::Append<CMeshO,CMeshO>::MeshCopy(cm,mesh);
//    //cm.Tr = mesh.Tr;
//    cm.Tr.SetIdentity();
//    cm.sfn = mesh.sfn;
//    cm.svn = mesh.svn;
//    glw.m = &cm;
//}



//MeshLabRenderMesh::~MeshLabRenderMesh()
//{
//    glw.m = NULL;
//    cm.Clear();
//    CMeshO::VertContainer tempVert;
//    CMeshO::FaceContainer tempFace;
//    cm.vert.swap(tempVert);
//    cm.face.swap(tempFace);
//}

Mesh::Mesh(std::string n, VOLUME_TYPE t): CVolume(n, t),
    bclosed(true),cm(),pgrid(0)//,glw()
{
	blist = true;
    cm.Tr.SetIdentity();
    cm.face.EnableFFAdjacency();
    //glw.m=&cm;
    _id = countmesh;
        countmesh++;
        polyoffset = 0;

}

Mesh::~Mesh()
{
    //glw.m = NULL;
    cm.Clear();
    CMeshO::VertContainer tempVert;
    CMeshO::FaceContainer tempFace;
    cm.vert.swap(tempVert);
    cm.face.swap(tempFace);
}


//one ring
bool SplitMesh(CMeshO &m,             /// The mesh that has to be splitted. It is NOT changed
               CMeshO &A, CMeshO &B,  /// The two resulting pieces, correct only if true is returned
               Plane3f plane)
{
  tri::Append<CMeshO,CMeshO>::Mesh(A,m);
  tri::UpdateQuality<CMeshO>::VertexFromPlane(A, plane);
  tri::QualityMidPointFunctor<CMeshO> slicingfunc(0.0f);
  tri::QualityEdgePredicate<CMeshO> slicingpred(0.0f);
  tri::UpdateTopology<CMeshO>::FaceFace(A);
  // The Actual Slicing
  tri::RefineE<CMeshO, tri::QualityMidPointFunctor<CMeshO>, tri::QualityEdgePredicate<CMeshO> > (A, slicingfunc, slicingpred, false);

  tri::Append<CMeshO,CMeshO>::Mesh(B,A);

  tri::UpdateSelection<CMeshO>::VertexFromQualityRange(A,-(std::numeric_limits<float>::max)(),0);
  tri::UpdateSelection<CMeshO>::FaceFromVertexStrict(A);
  for(CMeshO::FaceIterator fi=A.face.begin();fi!=A.face.end();++fi)
      if(!(*fi).IsD() && (*fi).IsS() ) tri::Allocator<CMeshO>::DeleteFace(A,*fi);
  tri::Clean<CMeshO>::RemoveUnreferencedVertex(A);

//  tri::UpdateSelection<CMeshO>::VertexFromQualityRange(B,0,std::numeric_limits<float>::max());
//  tri::UpdateSelection<CMeshO>::FaceFromVertexStrict(B);
//  for(CMeshO::FaceIterator fi=B.face.begin();fi!=B.face.end();++fi)
//      if(!(*fi).IsD() && (*fi).IsS() ) tri::Allocator<CMeshO>::DeleteFace(B,*fi);
//  tri::Clean<CMeshO>::RemoveUnreferencedVertex(B);

//  tri::UpdateTopology<CMeshO>::FaceFace(m);

//  CMeshO Cap;
//  CapHole(A,Cap,0);
//  tri::Append<CMeshO,CMeshO>::Mesh(A,Cap);

////  CapHole(B,Cap,0);
////  tri::Append<CMeshO,CMeshO>::Mesh(B,Cap);

//  tri::Clean<CMeshO>::RemoveDuplicateVertex(A);
//  tri::Clean<CMeshO>::RemoveDuplicateVertex(B);
  return true;
}
//void GetRandPlane(Box3f &bb, Plane3f &plane)
//{
//  Point3f planeCenter = bb.Center();
//  Point3f planeDir = Point3f(-0.5f+float(rand())/RAND_MAX,-0.5f+float(rand())/RAND_MAX,-0.5f+float(rand())/RAND_MAX);
//  planeDir.Normalize();

//  plane.Init(planeCenter+planeDir*0.3f*bb.Diag()*float(rand())/RAND_MAX,planeDir);
//}

//int main( int argc, char **argv )
//{
//  if(argc<2)
//  {
//    printf("Usage trimesh_base <meshfilename.ply>\n");
//    return -1;
//  }

//  CMeshO m, // The loaded mesh
//         em, // the 2D polyline representing the section
//         slice, // the planar mesh resulting from the triangulation of the above
//         sliced; // the 3D mesh resulting by the actual slicing of m into two capped sub pieces

//  if(tri::io::ImporterPLY<CMeshO>::Open(m,argv[1])!=0)
//  {
//    printf("Error reading file  %s\n",argv[1]);
//    exit(0);
//  }
//  tri::UpdateBounding<CMeshO>::Box(m);
//  printf("Input mesh  vn:%i fn:%i\n",m.VN(),m.FN());
//  srand(time(0));

//  Plane3f slicingPlane;
//  GetRandPlane(m.bbox,slicingPlane);
//  printf("slicing dir %5.2f %5.2f %5.2f\n",slicingPlane.Direction()[0],slicingPlane.Direction()[1],slicingPlane.Direction()[2]);
//  vcg::IntersectionPlaneMesh<CMeshO, CMeshO, float>(m, slicingPlane, em );
//  tri::Clean<CMeshO>::RemoveDuplicateVertex(em);
//  vcg::tri::CapEdgeMesh(em,slice);
//  printf("Slice  mesh has %i vert and %i faces\n", slice.VN(), slice.FN() );

//  CMeshO A,B;
//  SplitMesh(m,A,B,slicingPlane);
//  tri::UpdatePosition<CMeshO>::Translate(A, slicingPlane.Direction()*m.bbox.Diag()/80.0);
//  tri::UpdatePosition<CMeshO>::Translate(B,-slicingPlane.Direction()*m.bbox.Diag()/80.0);
//  tri::Append<CMeshO,CMeshO>::Mesh(sliced,A);
//  tri::Append<CMeshO,CMeshO>::Mesh(sliced,B);
//  printf("Sliced mesh has %i vert and %i faces\n", sliced.VN(), sliced.FN() );

//  tri::io::ExporterPLY<CMeshO>::Save(slice,"slice.ply",false);
//  tri::io::ExporterPLY<CMeshO>::Save(sliced,"sliced.ply",false);

//  return 0;
//}

void Mesh::cut(vcg::Plane3f slicingPlane, bool b)
{
    update_mesh_topology();

    bool binverse = slicingPlane.Direction().dot(vcg::Point3f(1,0,0))>0;
    cpolgon.clear();

    CMeshO em;
    vcg::IntersectionPlaneMesh<CMeshO, CMeshO, float>(cm, slicingPlane, em );
    //tri::Clean<CMeshO>::RemoveDegenerateEdge(cm);
    tri::Clean<CMeshO>::RemoveDuplicateVertex(em);
    //vcg::tri::Clean<CMeshO>::RemoveDegenerateVertex(em);
    //vcg::tri::Clean<CMeshO>::RemoveUnreferencedVertex( cm, true);   // V1.0;
    CMeshO A,B;
    A.face.EnableFFAdjacency();
    B.face.EnableFFAdjacency();
    SplitMesh(cm,A,B,slicingPlane);
//    if(1) {
//        CMeshO Cap;
//        CapHole(A,Cap,0);
//        tri::Append<CMeshO,CMeshO>::Mesh(A,Cap);
//        tri::Clean<CMeshO>::RemoveDuplicateVertex(A);
//    }
    if(bclosed)
    {
        ptVec2D cc;
        encloseRing(em, cc);

        for(int k = 0; k < cc.size(); k++)
        {            
            int nv = cc[k].size();
            if(nv > 2)
            {
                CMeshO Cap;
                CMeshO::VertexIterator vi=vcg::tri::Allocator<CMeshO>::AddVertices(Cap,nv);
                for (size_t i=0;i<cc[k].size();i++,++vi)
                    (&*vi)->P()=cc[k][i];
                std::vector<CMeshO::VertexPointer> index;
                index.resize(Cap.vn);
                int j;
                for(j=0,vi=Cap.vert.begin();j<Cap.vn;++j,++vi)
                    index[j] = &*vi;
                int N = nv/4;
                int mo = nv%2;
                int fn = (nv/2-1)*2;
                if(mo == 0)
                    ;
                else if(mo == 1)
                    fn++;

                CMeshO::FaceIterator fi=tri::Allocator<CMeshO>::AddFaces(Cap,fn);
                //                for (size_t i=0; i<nv-2; i++,++fi)
                //                {
                //                    (*&fi)->V(0)=index[0];//&Cap.vert[ 0 ];
                //                    (*&fi)->V(1)=index[i+1];//&Cap.vert[ i+1 ];
                //                    (*&fi)->V(2)=index[i+2];//&Cap.vert[ i+2 ];
                //                }
                if(b)
                {
                    int i = 0;
                    for (i=0; N > 0 && i<(nv/2-1); i++)
                    {
                        (*&fi)->V(0)=index[i];//&Cap.vert[ 0 ];
                        (*&fi)->V(1)=index[i+1];//&Cap.vert[ i+1 ];
                        (*&fi)->V(2)=index[nv-1-i];//&Cap.vert[ i+2 ];
                        ++fi;
                        (*&fi)->V(0)=index[i+1];//&Cap.vert[ 0 ];
                        (*&fi)->V(1)=index[nv-1-i-1];//&Cap.vert[ i+1 ];
                        (*&fi)->V(2)=index[nv-1-i];//&Cap.vert[ i+2 ];
                        ++fi;
                    }
                    if(mo == 1)
                    {
                        (*&fi)->V(0)=index[i];//&Cap.vert[ 0 ];
                        (*&fi)->V(1)=index[i+1];//&Cap.vert[ i+1 ];
                        (*&fi)->V(2)=index[nv-1-i];//&Cap.vert[ i+2 ];
                    }
                }
                else
                {
                int i = 0;
                for (i=0; N > 0 && i<(nv/2-1); i++)
                {
                    (*&fi)->V(0)=index[nv-1-i];//&Cap.vert[ i+2 ];
                    (*&fi)->V(1)=index[i+1];//&Cap.vert[ i+1 ];
                    (*&fi)->V(2)=index[i];//&Cap.vert[ 0 ];
                    ++fi;
                    (*&fi)->V(0)=index[nv-1-i];//&Cap.vert[ i+2 ];
                    (*&fi)->V(1)=index[nv-1-i-1];//&Cap.vert[ i+1 ];
                    (*&fi)->V(2)=index[i+1];//&Cap.vert[ 0 ];
                    ++fi;
                }
                if(mo == 1)
                {
                    (*&fi)->V(0)=index[nv-1-i];//&Cap.vert[ i+2 ];
                    (*&fi)->V(1)=index[i+1];//&Cap.vert[ i+1 ];
                    (*&fi)->V(2)=index[i];//&Cap.vert[ 0 ];
                }
                }
                tri::Append<CMeshO,CMeshO>::Mesh(A,Cap);
                tri::Clean<CMeshO>::RemoveDuplicateVertex(A);
             }
        }
    }
    cm.Clear();
    tri::Append<CMeshO,CMeshO>::Mesh(cm,A);
    cm.clean();
    tri::UpdateBounding<CMeshO>::Box(cm);
//    for(int j = 0; j < cm.face.size(); j++)
//    {
//        CMeshO::VertexPointer i1 = cm.face[j].V(0);
//        cm.face[j].V(0) =  cm.face[j].V(2);
//        cm.face[j].V(2) = i1;
//    }
    if(cm.fn>0) {
      tri::UpdateNormal<CMeshO>::PerFaceNormalized(cm);
      tri::UpdateNormal<CMeshO>::PerVertexAngleWeighted(cm);
    }
	tri::io::ExporterOBJ<CMeshO>::Save(cm, "CUT.ply", false);

    vcg::tri::UpdateBounding<CMeshO>::Box(cm);
}

int Mesh::saveOBJ(std::string filename) {

	tri::io::ExporterOBJ<CMeshO>::Save(cm, filename.c_str(), false);

	return 1;
}

void Mesh::encloseRing(CMeshO &mm, ptVec2D &cc)
{
    int j;
    std::vector<int> edgeVec, eindex[2],pindex;//store vertex index
    ptVec1D pts;
    CMeshO::VertexIterator vi;
    std::map<CMeshO::VertexPointer, int> map;
    for(j = 0,vi = mm.vert.begin(); vi < mm.vert.end(); vi++)
    {
        if(!(*vi).IsD())
        {
            map[&(*vi)] = j;
            pindex.push_back(j);
            pts.push_back((*vi).P());
            j++;
        }
    }
    j = 0;
    for(int i = 0; i < mm.edge.size(); i++)
    {
        if(!mm.edge[i].IsD()) {
            edgeVec.push_back(j);
            eindex[0].push_back(map[mm.edge[i].V(0)]);
            eindex[1].push_back(map[mm.edge[i].V(1)]);
            j++;
        }
    }

    while(edgeVec.size() > 0)
    {
        int stIndex = edgeVec[0];
        int stPoint = 0;
        std::vector<vcg::Point3f> c;
        do//while(stIndex >= 0)
        {
            int old = stPoint;
            //
            //stPoint = 0
            //c.push_back(mm.edge[stIndex].V(stPoint)->cP());
            int next = stPoint==0 ? eindex[1][stIndex] : eindex[0][stIndex];//int next = mm.edge[stIndex].V(stPoint==0?1:0)->Index();
            //c.push_back(*cap.cm.edge[stIndex].V(1)));
            std::vector<int>::iterator it;
            for(it = edgeVec.begin();it != edgeVec.end(); it++)
            {
                if(*it == stIndex)
                {
                        edgeVec.erase(it);
                        break;
                }
            }
            int xx = -1;
            int yy = -1;
            for(int k = 0; k < edgeVec.size(); k++)
            {
                    //if(mm.edge[edgeVec[k]].V(0)->Index()== next)
                if(eindex[0][edgeVec[k]]== next)
                    {
                        xx =edgeVec[k];
                        yy = 0;
                        break;
                    }
                    //if(mm.edge[edgeVec[k]].V(1)->Index() == next)
                if(eindex[1][edgeVec[k]]== next)
                    {
                        xx = edgeVec[k];
                        yy = 1;
                        break;
                    }
            }

            if(xx >= 0)
            {
                c.push_back(pts[eindex[stPoint][stIndex]]);
                stIndex = xx;
                stPoint = yy;
                continue;
            }
            else// if(stIndex == -1)
            {
                stPoint = 1;
                int next = stPoint==0 ? eindex[1][stIndex] : eindex[0][stIndex];//int next = mm.edge[stIndex].V(stPoint==0?1:0)->Index();
                //c.push_back(*cap.cm.edge[stIndex].V(1)));
                std::vector<int>::iterator it;
                for(it = edgeVec.begin();it != edgeVec.end(); it++)
                {
                        if(*it == stIndex)
                        {
                                edgeVec.erase(it);
                                break;
                        }
                }
                int xx = -1;
                int yy = -1;
                for(int k = 0; k < edgeVec.size(); k++)
                {
                        //if(mm.edge[edgeVec[k]].V(0)->Index()== next)
                    if(eindex[0][edgeVec[k]]== next)
                        {
                                xx =edgeVec[k];
                                yy = 0;
                                break;
                        }
                        //if(mm.edge[edgeVec[k]].V(1)->Index() == next)
                    if(eindex[1][edgeVec[k]]== next)
                        {
                                xx = edgeVec[k];
                                yy = 1;
                                break;
                        }
                }

                if(xx >= 0)
                {
                    c.push_back(pts[eindex[stPoint][stIndex]]);
                    stIndex = xx;
                    stPoint = yy;
                    continue;
                }
            }
            c.push_back(pts[eindex[old][stIndex]]);
            break;
        }while(1);
        cc.push_back(c);
    }    
}


//void Mesh::removeDuplicateEdges()
//{
//    int siz = edges.size();
//    if(siz > 0 )
//    {
//        std::sort(edges.begin(),edges.end());

//        std::vector<Edge> temp;
//        for(int i=0;i<siz-1;++i)
//        {
//              if(edges[i]==edges[i+1])
//              {
//                  continue;
//              }
//              temp.push_back(edges[i]);
//        }
//        temp.push_back(edges[siz-1]);
//        edges.clear();
//        edges = temp;
//    }
//}
//void Mesh::intersectionPlaneEdge(vcg::Plane3f pl)
//{
//    update_mesh_topology();
//    removeDuplicateEdges();
//    float epsilon = (1e-8);
//    std::vector<IntersectionPoint> inc;
//    for(int j = 0; j < edges.size(); j++)
//    {
//        float k = pl.Direction().dot((points[edges[j].v[1]].p-points[edges[j].v[0]].p));
//        if( (k > -epsilon) && (k < epsilon))
//            continue;
//        float r = (pl.Offset() - pl.Direction().dot(points[edges[j].v[0]].p))/k;	// Compute ray distance
//        if( (r<0) || (r > 1.0))
//            continue;
//        IntersectionPoint po;
//        po.p = points[edges[j].v[0]].p*(1-r)+points[edges[j].v[1]].p * r;
//        po.e = j;
//        inc.push_back(po);
//    }
//    intersectionPlane(inc);
//}

//void Mesh::intersectionPlane(std::vector<IntersectionPoint> incs)
//{

//}




//void Mesh::DrawFill(NormalMode nm, ColorMode cm)
//{
//    if(m.fn==0) return;
//    //int fn = faces.size();
//    //if(fn==0) return;
//    //typename FACE_POINTER_CONTAINER::iterator fp;

//    CMeshO::FaceIterator fi;

//    //std::vector<typename CMeshO::FaceType*>::iterator fip;

//    unsigned char transparency = this->material.transparency * 255;

//    c[3] = transparency;
//    if(cm == CMPerMesh)
//    {
//        glColor(c);
//    }
//    fi = m.face.begin();
//    glBegin(GL_TRIANGLES);

//    while( fi!=m.face.end())
//    {
//        CMeshO::FaceType & f = *fi;

//        if(!f.IsD())
//        {
//            if(nm == NMPerFace)	glNormal(f.cN());
//            if(nm == NMPerVert)	glNormal(f.V(0)->cN());
//            if(nm == NMPerWedge)glNormal(f.WN(0));

//            if(cm == CMPerFace)	glColor(f.C());
//            if(cm == CMPerVert)	glColor(f.V(0)->C());
//            //if(tm==TMPerVert) glTexCoord(f.V(0)->T().P());
//            //if( (tm==TMPerWedge)||(tm==TMPerWedgeMulti) )glTexCoord(f.WT(0).t(0));
//            glVertex(f.V(0)->P());

//            if(nm == NMPerVert)	glNormal(f.V(1)->cN());
//            if(nm == NMPerWedge)glNormal(f.WN(1));
//            if(cm == CMPerVert)	glColor(f.V(1)->C());
//            //if(tm==TMPerVert) glTexCoord(f.V(1)->T().P());
//            //if( (tm==TMPerWedge)|| (tm==TMPerWedgeMulti)) glTexCoord(f.WT(1).t(0));
//            glVertex(f.V(1)->P());

//            if(nm == NMPerVert)	glNormal(f.V(2)->cN());
//            if(nm == NMPerWedge)glNormal(f.WN(2));
//            if(cm == CMPerVert) glColor(f.V(2)->C());
//            //if(tm==TMPerVert) glTexCoord(f.V(2)->T().P());
//            //if( (tm==TMPerWedge)|| (tm==TMPerWedgeMulti)) glTexCoord(f.WT(2).t(0));
//            glVertex(f.V(2)->P());
//        }
//            ++fi;
//    }

//    glEnd();

//    {
//        int fn = this->cpolgon.size();
//        for(int j = 0; j < fn; j++)
//        {
//            glBegin(GL_POLYGON);
//            Polygon &f = cpolgon[j];
//            if(f.visble)
//                for(int i = 0; i < f.t; i++)

//            {
//                glNormal(f.n);
//                glColor(f.c);
//                //if(nm == NMPerFace)	glNormal(f.n);
//                //if(nm == NMPerVert)	glNormal(f[i].n);
//                //if(nm == NMPerWedge)    glNormal(f.WN(0));

//                //if(cm == CMPerFace)	{glColor(f.c);}
//                //if(cm == CMPerVert)	{glColor(f[i].c);}

//                glVertex(f.v[i]);

//            }
//            glEnd();

//        }
//    }

////        for(int j = 0; j < fn; j++)
////        {
////            glBegin(GL_POLYGON);
////            Face &f = faces[j];
////            if(f.visble)
////                for(int i = 0; i < f.t; i++)

////            {

////                if(nm == NMPerFace)	glNormal(f.n);
////                if(nm == NMPerVert)	glNormal(points[f.v[i]].n);
////                //if(nm == NMPerWedge)    glNormal(f.WN(0));

////                if(cm == CMPerFace)	{glColor(f.c);}
////                if(cm == CMPerVert)	{glColor(points[f.v[i]].c);}

////                glVertex(points[f.v[i]].p);

////            }
////            glEnd();

////        }

////        {

////                //glBegin(GL_QUADS);//glBegin(GL_TRIANGLES);

////                for(int j = 0; j < fn; j++)
////                {
////                    glBegin(GL_POLYGON);
////                    Face &f = faces[j];
////                    if(f.t == 4)
////                    if(f.visble)
////                    {

////                        if(nm == NMPerFace)	glNormal(f.n);
////                        if(nm == NMPerVert)	glNormal(points[f.v[0]].n);
////                        //if(nm == NMPerWedge)    glNormal(f.WN(0));

////                        if(cm == CMPerFace)	glColor(f.c);
////                        if(cm == CMPerVert)	glColor(points[f.v[0]].c);

////                        glVertex(points[f.v[0]].p);

////                        if(nm == NMPerVert)	glNormal(points[f.v[1]].n);
////                        //if(nm == NMPerWedge)glNormal(f.WN(1));
////                        if(cm == CMPerVert)	glColor(points[f.v[1]].c);

////                        glVertex(points[f.v[1]].p);

////                        if(nm == NMPerVert)	glNormal(points[f.v[2]].n);
////                        //if(nm == NMPerWedge)glNormal(f.WN(1));
////                        if(cm == CMPerVert)	glColor(points[f.v[2]].c);

////                        glVertex(points[f.v[2]].p);

////                        if(nm == NMPerVert)	glNormal(points[f.v[3]].n);
////                        //if(nm == NMPerWedge)glNormal(f.WN(1));
////                        if(cm == CMPerVert)	glColor(points[f.v[3]].c);

////                        glVertex(points[f.v[3]].p);
////                    }
////                    glEnd();

////                }



////                //glBegin(GL_TRIANGLES);

////                for(int j = 0; j < fn; j++)
////                {
////                    glBegin(GL_POLYGON);
////                    Face &f = faces[j];
////                    if(f.t == 3)
////                    if(f.visble)
////                    {

////                        if(nm == NMPerFace)	glNormal(f.n);
////                        if(nm == NMPerVert)	glNormal(points[f.v[0]].n);
////                        //if(nm == NMPerWedge)    glNormal(f.WN(0));

////                        if(cm == CMPerFace)	glColor(f.c);
////                        if(cm == CMPerVert)	glColor(points[f.v[0]].c);

////                        glVertex(points[f.v[0]].p);

////                        if(nm == NMPerVert)	glNormal(points[f.v[1]].n);
////                        //if(nm == NMPerWedge)glNormal(f.WN(1));
////                        if(cm == CMPerVert)	glColor(points[f.v[1]].c);

////                        glVertex(points[f.v[1]].p);

////                        if(nm == NMPerVert)	glNormal(points[f.v[2]].n);
////                        //if(nm == NMPerWedge)glNormal(f.WN(1));
////                        if(cm == CMPerVert)	glColor(points[f.v[2]].c);

////                        glVertex(points[f.v[2]].p);

////                    }
////                    glEnd();
////                }



////        }
//}


//void Mesh::DrawBBox(ColorMode cm)
//{
//    if(cm==CMPerMesh)
//        vcg::glColor(c);
//     vcg::glBoxWire(bbox);
//}

/*bool Mesh::load(QTextStream &stream)
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
//    if(list.at(0) != "COLOR")
//        return false;
//    if(list.count() != 6)
//        return false;
//    c = vcg::Color4b(list.at(1).toInt(),list.at(2).toInt(),list.at(3).toInt(),list.at(4).toInt());
//    bvisable = list.at(5).toInt();
        if(list.at(0) != "VISIBLE")
            return false;
        if(list.count() != 2)
            return false;

        bvisable = list.at(1).toInt();
    if(!material.load(stream))
        return false;
//    do
//    {
//    line = stream.readLine();
//    if (stream.status() != QTextStream::Ok)
//        return false;
//    }while(line.isEmpty());

//    list = line.split(QRegExp("\\s+"));
//    if(list.at(0) != "MATERIAL")
//        return false;
//    if(list.count() != 17)
//        return false;
//    material.set(list.at(1).toLocal8Bit());
//    material.ambientColor[0] = list.at(2).toFloat();
//    material.ambientColor[1] = list.at(3).toFloat();
//    material.ambientColor[2] = list.at(4).toFloat();
//    material.diffuseColor[0] = list.at(5).toFloat();
//    material.diffuseColor[1] = list.at(6).toFloat();
//    material.diffuseColor[2] = list.at(7).toFloat();
//    material.emissiveColor[0] = list.at(8).toFloat();
//    material.emissiveColor[1] = list.at(9).toFloat();
//    material.emissiveColor[2] = list.at(10).toFloat();
//    material.specularColor[0] = list.at(11).toFloat();
//    material.specularColor[1] = list.at(12).toFloat();
//    material.specularColor[2] = list.at(13).toFloat();
//    material.shininess = list.at(14).toFloat();
//    material.transparency = list.at(15).toFloat();
//    bvisable = list.at(16).toInt();
//    int t[4];
//    stream >> t[0] >> t[1] >> t[2] >> t[3];
//    c = vcg::Color4b(t[0],t[1],t[2],t[3]);
//    if (stream.status() != QTextStream::Ok)
//        return false;
//    //Material material;
//    std::string str;
//    stream >> str
//           >> material.ambientColor[0] >> material.ambientColor[1] >> material.ambientColor[2]
//           >> material.diffuseColor[0] >> material.diffuseColor[1] >> material.diffuseColor[2]
//           >> material.emissiveColor[0] >> material.emissiveColor[1] >> material.emissiveColor[2]
//           >> material.specularColor[0] >> material.specularColor[1] >> material.specularColor[2]
//           >> material.shininess >>  material.transparency >> t[0];
//    if (stream.status() != QTextStream::Ok)
//        return false;
//    material.set(str.toStdString().c_str());//MATERIALS_NAME[material.getType()]
//    bvisable = t[0];

    return true;
}

void Mesh::save(QTextStream &stream)
{
    CVolume::save(stream);
    //stream << "COLOR" << QLatin1Char(' ') << C()[0] << QLatin1Char(' ') << C()[1] << QLatin1Char(' ') << C()[2]
    //       << QLatin1Char(' ') << C()[3] << QLatin1Char(' ') << bvisable<< QLatin1Char('\n');
    stream << "VISIBLE" << QLatin1Char(' ') << bvisable<< QLatin1Char('\n');
    material.save(stream);
//    //Material material;
//    stream << "MATERIAL" << QLatin1Char(' ')
//            << MATERIALS_NAME[material.getType()] << QLatin1Char(' ')
//           << material.ambientColor[0] << QLatin1Char(' ') << material.ambientColor[1] << QLatin1Char(' ') << material.ambientColor[2] << QLatin1Char(' ')
//           << material.diffuseColor[0] << QLatin1Char(' ') << material.diffuseColor[1] << QLatin1Char(' ') << material.diffuseColor[2] << QLatin1Char(' ')
//           << material.emissiveColor[0] << QLatin1Char(' ') << material.emissiveColor[1] << QLatin1Char(' ') << material.emissiveColor[2] << QLatin1Char(' ')
//           << material.specularColor[0] << QLatin1Char(' ') << material.specularColor[1] << QLatin1Char(' ') << material.specularColor[2] << QLatin1Char(' ')
//           << material.shininess << QLatin1Char(' ') << material.transparency << QLatin1Char(' ')
//           << bvisable << QLatin1Char('\n');
}

bool CProperty::load(QTextStream &stream)
{
    std::string line;
    QStringList list;
    do
    {
    line = stream.readLine();
    if (stream.status() != QTextStream::Ok)
        return false;
    }while(line.isEmpty());

    list = line.split(QRegExp("\\s+"));
    if(list.at(0) != "PROPERTY")
        return false;
    if(list.count() != 2)
        return false;
    type = (PM3::PROPERTY)list.at(1).toInt();

    do
    {
    line = stream.readLine();
    if (stream.status() != QTextStream::Ok)
        return false;
    }while(line.isEmpty());

    list = line.split(QRegExp("\\s+"));
    if(list.at(0) != "MESH")
        return false;
    if(list.count() != 5)
        return false;
    cm = vcg::Color4b(list.at(1).toInt(),list.at(2).toInt(),list.at(3).toInt(),list.at(4).toInt());

    do
    {
    line = stream.readLine();
    if (stream.status() != QTextStream::Ok)
        return false;
    }while(line.isEmpty());

    list = line.split(QRegExp("\\s+"));
    if(list.at(0) != "FACE")
        return false;
    if(list.count() != 5)
        return false;
    cf = vcg::Color4b(list.at(1).toInt(),list.at(2).toInt(),list.at(3).toInt(),list.at(4).toInt());

    do
    {
    line = stream.readLine();
    if (stream.status() != QTextStream::Ok)
        return false;
    }while(line.isEmpty());

    list = line.split(QRegExp("\\s+"));
    if(list.at(0) != "VERTEX")
        return false;
    if(list.count() != 5)
        return false;
    cv = vcg::Color4b(list.at(1).toInt(),list.at(2).toInt(),list.at(3).toInt(),list.at(4).toInt());

    if(!material.load(stream))
        return false;
}

void CProperty::save(QTextStream &stream)
{
    stream << "PROPERTY" << QLatin1Char(' ') << type << QLatin1Char('\n');
    stream << "MESH" << cm[0] << QLatin1Char(' ') << cm[1] << QLatin1Char(' ')
           << cm[2] << QLatin1Char(' ') << cm[3] << QLatin1Char('\n');
    stream << "FACE" << cf[0] << QLatin1Char(' ') << cf[1] << QLatin1Char(' ')
           << cf[2] << QLatin1Char(' ') << cf[3] << QLatin1Char('\n');
    stream << "VERTEX" << cv[0] << QLatin1Char(' ') << cv[1] << QLatin1Char(' ')
           << cv[2] << QLatin1Char(' ') << cv[3] << QLatin1Char('\n');
    material.save(stream);

}
*/
void Mesh::convert2MeshO(std::vector<Vertex> points,
                   std::vector<Face> faces)
{
    int j;
    cm.Clear();

    CMeshO::VertexIterator vi=vcg::tri::Allocator<CMeshO>::AddVertices(cm,points.size());
    //float i[3];
	float res = 1.0;// pgrid->getresolu();
    for(j=0;j<points.size();++j)
    {
        //i[0] = (int64_t(points[j].p[0] / res+0.5))*res;
        //i[1] = (int64_t(points[j].p[1] / res+0.5))*res;
        //i[2] = (int64_t(points[j].p[2] / res+0.5))*res;

		(*vi).P()[0] = points[j].p[0];// / res;//i[0];//i;
		(*vi).P()[1] = points[j].p[1];// / res;//i[1];//
		(*vi).P()[2] = points[j].p[2];// / res;//i[2];//
        /*(*vi).N()[0] = points[j].n[0];
        (*vi).N()[1] = points[j].n[1];
        (*vi).N()[2] = points[j].n[2];
        (*vi).C()[0] = points[j].c[0];
        (*vi).C()[1] = points[j].c[1];
        (*vi).C()[2] = points[j].c[2];
        (*vi).C()[3] = 255;*/
        ++vi;
    }
    std::vector<CMeshO::VertexPointer> index;
    index.resize(cm.vn);
    for(j=0,vi=cm.vert.begin();j<cm.vn;++j,++vi)
        index[j] = &*vi;
    int fn = 0;
    for(j = 0; j < faces.size(); j++)
    {
        if(faces[j].t == 4) fn+=2;
        if(faces[j].t == 3) fn+=1;
    }
    CMeshO::FaceIterator fi=vcg::tri::Allocator<CMeshO>::AddFaces(cm,fn);
    for(j = 0; j < faces.size(); j++)
    {
        if(faces[j].t == 4 || faces[j].t == 3) {
            (*fi).Alloc(3);
            for(int k=0;k<3;++k)
                (*fi).V(k) = index[faces[j].v[k] ];
            //(*fi).N() = faces[j].n;
            ++fi;
        }
        if(faces[j].t == 4) {
            (*fi).Alloc(3);
            for(int k=0;k<3;++k)
                (*fi).V(k) = index[ faces[j].v[(2+k)%4] ];
            //(*fi).N() = faces[j].n;
            ++fi;
        }
    }
    cm.clean();

   // vcg::tri::UpdateBounding<CMeshO>::Box(cm);

	blist = true;
}

vcg::Point3f ptextend(vcg::Point3f p, CMeshO::VertexType::NormalType n)
{
    vcg::Point3f t = p;
//    if(n[0] > 0) t[0] += 0.001*t[0];
//    else t[0] -= 0.0001*t[0];
//    if(n[1] > 0) t[1] += 0.001*t[1];
//    else t[1] -= 0.0001*t[1];
//    if(n[2] > 0) t[2] += 0.001*t[2];
//    else t[2] -= 0.0001*t[2];
    return t;
}





}

