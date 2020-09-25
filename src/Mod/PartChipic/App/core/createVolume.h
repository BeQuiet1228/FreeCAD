#ifndef CREATEVOLUME_H
#define CREATEVOLUME_H

#include <vcg/complex/complex.h>

namespace PM3
{
class Vertex
{
public:
    Vertex() {c=vcg::Color4b(255,255,255,255);};
    Vertex(vcg::Point3f _p){p=_p;c=vcg::Color4b(255,255,255,255);}
        vcg::Point3f  p;
        vcg::Point3f  n;
        vcg::Color4b c;
};
class Face
{
public:
        Face(int v0, int v1, int v2){visble = true;t=3;v.resize(3);v[0]=v0;v[1]=v1;v[2]=v2;c=vcg::Color4b(255,255,255,255);};
        Face(int v0, int v1, int v2, int v3){visble = true;t=4;v.resize(4);v[0]=v0;v[1]=v1;v[2]=v2;v[3]=v3;c=vcg::Color4b(255,255,255,255);};
        Face(int n) {visble = true;t=n;v.resize(n);}
        Face() {visble = true;t=0;}
        int t;
        std::vector<int> v;
        bool visble;
        vcg::Point3f n;
        vcg::Color4b c;
};

void createSpherical(vcg::Point3f o, float r, std::vector<Vertex> &pts, std::vector<Face> &fs);
void createCylindrical(vcg::Point3f s, vcg::Point3f e,float r, std::vector<Vertex> &pts, std::vector<Face> &fs);
void createVolumecyl(vcg::Point3f s, vcg::Point3f e,std::vector<Vertex> &pts, std::vector<Face> &fs);
bool createVolumeHelic(vcg::Point3f top,vcg::Point3f base,vcg::Point3f start, std::vector<Vertex> &points,
                       float pp,float pw,float ri,float ro,
                       std::vector<Face> &faces);
bool createVolumeAnnular_section(vcg::Point3f p1,vcg::Point3f p2,vcg::Point3f p3, vcg::Point3f p4,
                                                  float r1,float r2,float theta1,float theta2,
                                                  std::vector<Vertex> &points,std::vector<Face> &faces);
}
#endif // CREATEVOLUME_H
