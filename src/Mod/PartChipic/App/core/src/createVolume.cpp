#include "../createVolume.h"
#include "../basicmath.h"

namespace PM3
{
void createVolumecyl(vcg::Point3f s, vcg::Point3f e,std::vector<Vertex> &points, std::vector<Face> &faces)
{
    points.clear();
    faces.clear();
    int i,j;
    double theta;
    vcg::Point3f n,p,q,perp;
    vcg::Point3f p1 = s,//near
            p2 = e;//far
    float theta1 = p1[1];
    float theta2 = p2[1];

    /* Normal pointing from p1 to p2 */
    n = vcg::Point3f(0,0,1);
    perp = n;
    if (n[0] == 0 && n[2] == 0)
        perp[0] += 1;
    else
        perp[1] += 1;
    q = perp ^ n;
    perp = n ^ q;
    perp.Normalize();
    q.Normalize();
    int m = 100;
    for (i=0;i<=m;i++)
    {
       theta = theta1 + (theta2-theta1)*i / m;//PM3::radians(theta1 + (theta2-theta1)*i / m);
       //outer
       p[0] = p2[0]*cos(theta);//top
       p[1] = p2[0]*sin(theta);
       p[2] = p2[2];
       Vertex v2(p);
       v2.n = p - vcg::Point3f(0,0,0);
       v2.n.Normalize();
       points.push_back(v2);

       p[0] = p2[0]*cos(theta);//down
       p[1] = p2[0]*sin(theta);
       p[2] = p1[2];
       Vertex v1(p);
       v1.n = p - vcg::Point3f(0,0,0);
       v1.n.Normalize();
       points.push_back(v1);

       //inner
       p[0] = p1[0]*cos(theta);//top
       p[1] = p1[0]*sin(theta);
       p[2] = p2[2];
       Vertex v3(p);
       v3.n = p - vcg::Point3f(0,0,0);
       v3.n.Normalize();
       points.push_back(v3);

       p[0] = p1[0]*cos(theta);//down
       p[1] = p1[0]*sin(theta);
       p[2] = p1[2];
       Vertex v4(p);
       v4.n = p - vcg::Point3f(0,0,0);
       v4.n.Normalize();
       points.push_back(v4);

    }
//    {
//        Face f(4*(m-1)+0,4*(m-1)+1,4*(m-1)+3,4*(m-1)+2);
//        //f.n = points[i].n+points[i+1].n+points[i+2+2].n+points[i+3+2].n;
//        f.n = (points[4*(m-1)+1].p-points[4*(m-1)+0].p)^(points[4*(m-1)+3].p-points[4*(m-1)+0].p);
//        f.n.Normalize();
//        faces.push_back(f);
//    }
//    {
//        Face f(0,1,3,2);
//        //f.n = points[i].n+points[i+1].n+points[i+2+2].n+points[i+3+2].n;
//        f.n = (points[1].p-points[0].p)^(points[3].p-points[0].p);
//        f.n.Normalize();
//        faces.push_back(f);
//    }
    //outer
    for (i=0;i<4*m;i+=4)
    {
        Face f(i,i+1,i+5,i+4);
        //f.n = points[i].n+points[i+1].n+points[i+2+2].n+points[i+3+2].n;
        f.n = (points[i+1].p-points[i].p)^(points[i+5].p-points[i].p);
        f.n.Normalize();
        faces.push_back(f);
    }
    for (i=2;i<4*m;i+=4)
    {
        Face f(i,i+4,i+5,i+1);//Face f(i,i+1,i+5,i+4);//
        //f.n = (points[i].n+points[i+1].n+points[i+2+2].n+points[i+3+2].n);//*-1.0;
        f.n = (points[i+4].p-points[i].p)^(points[i+5].p-points[i].p);
        f.n.Normalize();
        faces.push_back(f);
    }

    for (i=1;i<4*m;i+=4)
    {
        Face f(i,i+2,i+6,i+4);
        //f.n = tn;//points[i].n+points[i+4].n+points[i+6].n+points[i+2].n;
        f.n = (points[i+2].p-points[i].p)^(points[i+6].p-points[i].p);
        f.n.Normalize();
        faces.push_back(f);
    }

    for (i=0;i<4*m;i+=4)
    {
        Face f(i,i+4,i+6,i+2);
        //f.n = bn;//points[i].n+points[i+4].n+points[i+6].n+points[i+2].n;
        f.n = (points[i+4].p-points[i].p)^(points[i+6].p-points[i].p);
        f.n.Normalize();
        faces.push_back(f);
    }
//    if(theta2 < 2*pi())
//    {
//        Face f(4*m-4,4*m-2,4*m-1,4*m-3);
//        //f.n = bn;//points[i].n+points[i+4].n+points[i+6].n+points[i+2].n;
//        f.n = (points[4*m-2].p-points[4*m-4].p)^(points[4*m-1].p-points[4*m-4].p);
//        f.n.Normalize();
//        faces.push_back(f);
//    }
//    if(theta1 > 0)
//    {
//        Face f(0,1,3,2);
//        //f.n = bn;//points[i].n+points[i+4].n+points[i+6].n+points[i+2].n;
//        f.n = (points[1].p-points[0].p)^(points[3].p-points[0].p);
//        f.n.Normalize();
//        faces.push_back(f);
//    }
    if(theta2 < 2*pi() || theta1 > 0) {
        {
            Face f(4*m-4,4*m-3,4*m-1,4*m-2);
            //f.n = bn;//points[i].n+points[i+4].n+points[i+6].n+points[i+2].n;
            f.n = (points[4*m-3].p-points[4*m-4].p)^(points[4*m-2].p-points[4*m-4].p);
            f.n.Normalize();
            faces.push_back(f);
        }

        {
            Face f(0,2,3,1);
            //f.n = bn;//points[i].n+points[i+4].n+points[i+6].n+points[i+2].n;
            f.n = (points[2].p-points[0].p)^(points[1].p-points[0].p);
            f.n.Normalize();
            faces.push_back(f);
        }
    }
}

void createCylindrical(vcg::Point3f s, vcg::Point3f e,float r, std::vector<Vertex> &points, std::vector<Face> &faces)
{
    points.clear();
    faces.clear();

    int i,j;
    double theta;
    vcg::Point3f n,p,q,perp;
    vcg::Point3f p1 = e, p2 = s;
    /* Normal pointing from p2 to p1 */
    n = p1-p2;
    vcg::Point3f tn = n;
    tn.Normalize();
    vcg::Point3f bn = -tn;

    /*
       Create two perpendicular vectors perp and q
       on the plane of the disk
    */
    perp = n;
    if (n[0] == 0 && n[2] == 0)
        perp[0] += 1;
    else
        perp[1] += 1;
    q = perp ^ n;//CROSSPROD(perp,n,q);
    perp = n ^ q;//CROSSPROD(n,q,perp);
    perp.Normalize();
    q.Normalize();

    int count=64*2;
    {
       for (i=0;i<=count;i++) {
          theta = i * 2*3.1415926 / count;
          n = perp*cos(theta) + q*sin(theta);
          n.Normalize();

          p = p2 + n*r;//bot
          Vertex v2(p);
          v2.n = n;
          points.push_back(v2);

          p = p1+n*r;//top
          Vertex v1(p);
          v1.n = n;
          points.push_back(v1);
       }

       {
           Vertex v2(p2);//bot
           v2.n = points[2*(count+1)-2].n;
           points.push_back(v2);

           Vertex v1(p1);//top
           v1.n = n;//points[2*m-1].n;
           points.push_back(v1);
       }

       for (i=1;i<2*(count+1);i+=2)
       {
           Face f(i,2*(count+1)+1,i+2);
           f.n = (points[2*(count+1)+1].p-points[i].p)^(points[i+2].p-points[i].p);//f.n = n;
           f.n.Normalize();
           faces.push_back(f);
       }

       for (i=0;i<2*count;i+=2)
       {
           Face f(i,i+1,i+3,i+2);
           //f.n = points[i].n+points[i+1].n+points[i+2].n+points[i+3].n;
           f.n = (points[i+1].p-points[i].p)^(points[i+3].p-points[i].p);
           f.n.Normalize();
           faces.push_back(f);
       }

       for (i=0;i<2*(count+1);i+=2)
       {
           Face f(i,i+2,2*(count+1));
           f.n = (points[i+2].p-points[i].p)^(points[2*(count+1)].p-points[i].p);//f.n = n;
           f.n.Normalize();
           faces.push_back(f);
       }
    }
}

void createSpherical(vcg::Point3f o, float r, std::vector<Vertex> &points, std::vector<Face> &faces)
{
    points.clear();
    faces.clear();

    int n;
    int theta,phi;
    vcg::Point3f center = o;
    vcg::Point3f p[4];
    Vertex v[4];
    int dtheta = 5, dphi = 5;
    for (theta=-90;theta<=90-dtheta;theta+=dtheta)
    {
       for (phi=0;phi<=360-dphi;phi+=dphi)
       {
          n = 0;
          p[n][0] = cos(PM3::radians(theta)) * cos(PM3::radians(phi));
          p[n][1]= cos(PM3::radians(theta)) * sin(PM3::radians(phi));
          p[n][2] = sin(PM3::radians(theta));
          p[n] = center+p[n]*r;
          v[n].p = p[n];
          v[n].n = (v[n].p - center).Normalize();
          points.push_back(v[n]);
          n++;
          p[n][0] = cos(PM3::radians(theta+dtheta)) * cos(PM3::radians(phi));
          p[n][1] = cos(PM3::radians(theta+dtheta)) * sin(PM3::radians(phi));
          p[n][2] = sin(PM3::radians(theta+dtheta));
          p[n] = center+p[n]*r;
          v[n].p = p[n];
          v[n].n = (v[n].p - center).Normalize();
          points.push_back(v[n]);
          n++;
          p[n][0] = cos(PM3::radians(theta+dtheta)) * cos(PM3::radians(phi+dphi));
          p[n][1] = cos(PM3::radians(theta+dtheta)) * sin(PM3::radians(phi+dphi));
          p[n][2] = sin(PM3::radians(theta+dtheta));
          p[n] = center+p[n]*r;
          v[n].p = p[n];
          v[n].n = (v[n].p - center).Normalize();
          points.push_back(v[n]);
          n++;
          if (theta > -90 && theta < 90) {
             p[n][0] = cos(PM3::radians(theta)) * cos(PM3::radians(phi+dphi));
             p[n][1] = cos(PM3::radians(theta)) * sin(PM3::radians(phi+dphi));
             p[n][2] = sin(PM3::radians(theta));
             p[n] = center+p[n]*r;
             v[n].p = p[n];
             v[n].n = (v[n].p - center).Normalize();
             points.push_back(v[n]);
             n++;
             int s = points.size();
             Face f(s-1,s-2,s-3,s-4);
             f.n = (p[3]-p[0])^(p[1]-p[0]);
             f.n.Normalize();
             faces.push_back(f);
          }
          else
          {
              int s = points.size();
              Face f(s-1,s-2,s-3);
              f.n = (p[0]-p[1])^(p[2]-p[1]);
              f.n.Normalize();
              faces.push_back(f);
          }

       }
    }
}
static double getAngle(vcg::Point3f p)
{
    double a = 0;//
    float x = p[0],y=p[1];
    if(x == 0) {
       if(y >= 0) a = PM3::pi()/2;//PM3::degrees(PM3::pi()/2);
        else a = PM3::pi()*3/2;//PM3::degrees(PM3::pi()*3/2);
    }
    else if(x > 0)
    {
        if(y >= 0) a = std::atan2(p[1],p[0]);//PM3::degrees(std::atan2(p[1],p[0]));
        else a = PM3::pi()*2+std::atan2(p[1],p[0]);//PM3::degrees(PM3::pi()*2)+PM3::degrees(std::atan2(p[1],p[0]));
    }
    else
    {
        if(y >= 0) a = std::atan2(p[1],p[0]);//PM3::degrees(std::atan2(p[1],p[0]));
        else a = PM3::pi()*2+std::atan2(p[1],p[0]);//PM3::degrees(PM3::pi()*2)+PM3::degrees(std::atan2(p[1],p[0]));
    }
    return a;
}
bool createVolumeHelic(vcg::Point3f top,vcg::Point3f base,vcg::Point3f start, std::vector<Vertex> &points,
                       float pp,float pw,float ri,float ro,
                       std::vector<Face> &faces)
{
    vcg::Point3f n,perp,q;
    n = top - base;
    vcg::Point3f tn = n;
    tn.Normalize();
    vcg::Point3f bn = -tn;
    perp = n;
    if (n[0] == 0 && n[2] == 0)
        perp[0] += 1;
    else
        perp[1] += 1;
    q = perp ^ n;
    perp = n ^ q;
    perp.Normalize();
    q.Normalize();

    float L = n.Norm();
    n.Normalize();
    vcg::Plane3f bplane,tplane;
    bplane.Init(base, tn);
    tplane.Init(top, tn);
    if(vcg::SignedDistancePlanePoint(bplane, start) != 0)
        return false;

    float a = vcg::Angle(q,bplane.Projection(start)-base);
    float b = pp;
    float step = L/(L/pw*12.0);
    //double interval = 2*PM3::pi()*L;
    int c = 0;
        for(float f = -pw; f <= L; f += step)
        {
            float t = a+f*2*PM3::pi()/b;
            vcg::Point3f pp = tn*f+base;
            n = perp*cos(t) + q*sin(t);
            n.Normalize();
            vcg::Point3f p = pp + n*ro;
            if(vcg::SignedDistancePlanePoint(bplane, p) < 0)
                p = bplane.Projection(p);
            else if(vcg::SignedDistancePlanePoint(tplane, p) > 0)
                p = tplane.Projection(p);
            Vertex v2(p);
            v2.n = p-pp;
            v2.n.Normalize();
            points.push_back(v2);
            c++;
        }
        for(float f = 0; f <= L+pw; f += step)
        {
            float t = a+(f-pw)*2*PM3::pi()/b;
            vcg::Point3f pp = tn*f+base;
            n = perp*cos(t) + q*sin(t);
            n.Normalize();
            vcg::Point3f p = pp + n*ro;
            if(vcg::SignedDistancePlanePoint(bplane, p) < 0)
                p = bplane.Projection(p);
            else if(vcg::SignedDistancePlanePoint(tplane, p) > 0)
                p = tplane.Projection(p);
            Vertex v2(p);
            v2.n = p-pp;
            v2.n.Normalize();
            points.push_back(v2);
        }
        for(float f = -pw; f <= L; f += step)
        {
            float t = a+f*2*PM3::pi()/b;
            vcg::Point3f pp = tn*f+base;
            n = perp*cos(t) + q*sin(t);
            n.Normalize();
            vcg::Point3f p = pp+n*ri ;
            if(vcg::SignedDistancePlanePoint(bplane, p) < 0)
                p = bplane.Projection(p);
            else if(vcg::SignedDistancePlanePoint(tplane, p) > 0)
                p = tplane.Projection(p);
            Vertex v2(p);
            v2.n = p-pp;
            v2.n.Normalize();
            points.push_back(v2);
        }
        for(float f = 0; f <= L+pw; f += step)
        {
            float t = a+(f-pw)*2*PM3::pi()/b;
            vcg::Point3f pp = tn*f+base;
            n = perp*cos(t) + q*sin(t);
            n.Normalize();
            vcg::Point3f p = pp+n*ri ;
            if(vcg::SignedDistancePlanePoint(bplane, p) < 0)
                p = bplane.Projection(p);
            else if(vcg::SignedDistancePlanePoint(tplane, p) > 0)
                p = tplane.Projection(p);
            Vertex v2(p);
            v2.n = p-pp;
            v2.n.Normalize();
            points.push_back(v2);
        }
        for(int i = 0; i < c-1; i++)
        {
//            Face f(i,(i+2*c),(i+2*c)+1,i+1 );
//            f.n = (points[i+2*c].p-points[i].p)^(points[(i+2*c)+1].p-points[i].p);
            Face f(i,i+1,(i+2*c)+1, (i+2*c));
            f.n = (points[i+1].p-points[i].p)^(points[i+2*c].p-points[i].p);
            f.n.Normalize();
            faces.push_back(f);
        }
        for(int i = 0; i < c-1; i++)
        {
            //Face f(c+i,c+i+1,(c+i+2*c)+1,(c+i+2*c) );
            //f.n = (points[c+i+1].p-points[c+i].p)^(points[(c+i+2*c)+1].p-points[c+i].p);
            Face f(c+i,(c+i+2*c),(c+i+2*c)+1,c+i+1 );
            f.n = (points[c+i+2*c].p-points[c+i].p)^(points[(c+i+2*c)+1].p-points[c+i].p);
            f.n.Normalize();
            faces.push_back(f);
        }
        for(int i = 0; i < c-1; i++)
        {
            //Face f(i,i+1,(c+i)+1,(c+i) );
            //f.n = (points[1+i].p-points[i].p)^(points[(c+i)+1].p-points[i].p);
            Face f(i,(c+i),(c+i)+1,i+1 );
            f.n = (points[c+i].p-points[i].p)^(points[(c+i)+1].p-points[i].p);
            f.n.Normalize();
            faces.push_back(f);
        }
        for(int i = 0; i < c-1; i++)
        {
            //Face f(2*c+i,(2*c+c+i),(2*c+c+i)+1,2*c+i+1 );
            //f.n = (points[2*c+c+i].p-points[2*c+i].p)^(points[(2*c+c+i)+1].p-points[2*c+i].p);
            Face f(2*c+i,2*c+i+1,(2*c+c+i)+1,(2*c+c+i) );
            f.n = (points[2*c+i+1].p-points[2*c+i].p)^(points[(2*c+c+i)].p-points[2*c+i].p);
            f.n.Normalize();
            faces.push_back(f);
        }
        {
            Face f(0,2*c,3*c,c );
            f.n = (points[c].p-points[0].p)^(points[3*c].p-points[0].p);
            f.n.Normalize();
            faces.push_back(f);
        }
        {
            Face f(c-1,c+c-1,3*c+c-1,2*c+c-1);
            f.n = (points[2*c+c-1].p-points[c-1].p)^(points[3*c+c-1].p-points[c-1].p);
            f.n.Normalize();
            faces.push_back(f);
        }
//    for(float f = 0; f <= L; f += 0.1)
//    {
//        float t = PM3::radians(270)+f*2*PM3::pi();
//        vcg::Point3f pp = n*f+point_base.value;
//        vcg::Point3f p = vcg::Point3f(radius_outer.value * cos(t),
//                                    radius_outer.value * sin(t),
//                                    b*f)+point_base.value/*+n*f*/;
//        Vertex v2(p);
//        v2.n = p-pp;
//        v2.n.Normalize();
//        points.push_back(v2);
//        c++;
//    }
//    for(float f = 0; f <= L; f += 0.1)
//    {
//        float t = PM3::radians(270)+f*2*PM3::pi();
//        vcg::Point3f pp = n*f+point_base.value;
//        vcg::Point3f p = vcg::Point3f(radius_outer.value * cos(t),
//                                    radius_outer.value * sin(t),
//                                      b*f)+point_base.value*(1+width.value)/*+n*f*/;
//        Vertex v2(p);
//        v2.n = p-pp;
//        v2.n.Normalize();
//        points.push_back(v2);
//    }
//    for(int i = 0; i < c-1; i++)
//    {
//        Face f(i,(i+c),(i+c)+1,i+1 );
//        f.n = (points[i+c].p-points[i].p)^(points[(i+c)+1].p-points[i+c].p);
//        f.n.Normalize();
//        faces.push_back(f);
//    }

        return true;
}

bool createVolumeAnnular_section(vcg::Point3f p1,vcg::Point3f p2,vcg::Point3f p3, vcg::Point3f p4,
                                                  float r1,float r2,float theta1,float theta2,
                                                  std::vector<Vertex> &points,std::vector<Face> &faces)
{    
    int m = 100;
    /*if(type == VCYLINDRICAL )
       r1 = 0;//p2 is bot
    else if(type == VCONE)
         r2 = r1;
    else if(type==VANNULAR)
        if(r1>r2) return;
    //void CreateCone(XYZ p1,XYZ p2,double r1,double r2,int m,
     //  double theta1,double theta2)
*/
    int i,j;
    double theta;
    vcg::Point3f n,p,q,perp;

    // Normal pointing from p1 to p2
    n = p2-p1;
    vcg::Point3f tn = n;
    tn.Normalize();
    vcg::Point3f bn = -tn;

    perp = n;
    if (n[0] == 0 && n[2] == 0)
        perp[0] += 1;
    else
        perp[1] += 1;
    q = perp ^ n;//CROSSPROD(perp,n,q);
    perp = n ^ q;//CROSSPROD(n,q,perp);
    perp.Normalize();
    q.Normalize();

//    vcg::Plane3f plane;
//    plane.Init(p1, tn);
//    theta1 = vcg::Angle(q,plane.Projection(p3)-p1);
//    theta2 = vcg::Angle(q,plane.Projection(p4)-p1);

    float temp1 = fmin(theta1,theta2);
    float temp2 = fmax(theta1,theta2);
    theta2 = temp2;
    theta1 = temp1;

    vcg::Point3f temp = perp;
    perp = q;//x
    q = temp;//y
    float step = (theta2 - theta1)/60.0;

    //if(step < 0.1) step = 0.01;
    {
        m=0;
        if(step <= 0)
            return false;
        for(float t = theta1; t <= theta2; t+=step)//for (i=0;i<=m;i++)
        {
           theta = t;//PM3::radians(t);
           //theta = theta1 + i * (theta2 - theta1) / m;
           n = perp*cos(theta) + q*sin(theta);
           n.Normalize();
           //outer
           p = p2 + n*r2;//bot
           Vertex v2(p);
           v2.n = n;
           points.push_back(v2);

           p = p1+n*r2;//top
           Vertex v1(p);
           v1.n = n;
           points.push_back(v1);
           //inner
           p = p2 + n*r1;//bot
           Vertex v3(p);
           v3.n = n*-1;
           points.push_back(v3);

           p = p1+n*r1;//top
           Vertex v4(p);
           v4.n = n*-1;
           points.push_back(v4);
           m++;
        }

//        {
//           theta = PM3::radians(theta2);
//           //theta = theta1 + i * (theta2 - theta1) / m;
//           n = perp*cos(theta) + q*sin(theta);
//           n.Normalize();
//           //outer
//           p = p2 + n*r2;//bot
//           Vertex v2(p);
//           v2.n = n;
//           points.push_back(v2);

//           p = p1+n*r2;//top
//           Vertex v1(p);
//           v1.n = n;
//           points.push_back(v1);
//           //inner
//           p = p2 + n*r1;//bot
//           Vertex v3(p);
//           v3.n = n*-1;
//           points.push_back(v3);

//           p = p1+n*r1;//top
//           Vertex v4(p);
//           v4.n = n*-1;
//           points.push_back(v4);
//           m++;
//        }
        //outer
        for (i=0;i<4*(m-1);i+=4)
        {
            Face f(i,i+1,i+5,i+4);
            //f.n = points[i].n+points[i+1].n+points[i+2+2].n+points[i+3+2].n;
            f.n = (points[i+1].p-points[i].p)^(points[i+5].p-points[i].p);
            f.n.Normalize();
            faces.push_back(f);
        }
        for (i=2;i<4*(m-1);i+=4)
        {
            Face f(i,i+4,i+5,i+1);//Face f(i,i+1,i+5,i+4);//
            //f.n = (points[i].n+points[i+1].n+points[i+2+2].n+points[i+3+2].n);//*-1.0;
            f.n = (points[i+4].p-points[i].p)^(points[i+5].p-points[i].p);
            f.n.Normalize();
            faces.push_back(f);
        }
        {
        Face f(0,2,3,1);
        //f.n =points[0].n+points[1].n+points[2].n+points[3].n;
        f.n = (points[2].p-points[0].p)^(points[3].p-points[0].p);
        f.n.Normalize();
        faces.push_back(f);
        }
        {
        Face f((m-1)*4,(m-1)*4+1,(m-1)*4+3,(m-1)*4+2);
        //f.n = points[(m-1)*4].n+points[(m-1)*4+1].n+points[(m-1)*4+2].n+points[(m-1)*4+3].n;
        f.n = (points[(m-1)*4+1].p-points[(m-1)*4].p)^(points[(m-1)*4+3].p-points[(m-1)*4].p);
        f.n.Normalize();
        faces.push_back(f);
        }
        //if(r1*r2 != 0)
        {
            //if(m_top)
            {
                for (i=1;i<4*(m-1);i+=4)
                {
                    Face f(i,i+2,i+6,i+4);
                    //f.n = tn;//points[i].n+points[i+4].n+points[i+6].n+points[i+2].n;
                    f.n = (points[i+2].p-points[i].p)^(points[i+6].p-points[i].p);
                    f.n.Normalize();
                    faces.push_back(f);
                }
            }
        }
            //if(m_bottom)
            {
                for (i=0;i<4*(m-1);i+=4)
                {
                    Face f(i,i+4,i+6,i+2);
                    //f.n = bn;//points[i].n+points[i+4].n+points[i+6].n+points[i+2].n;
                    f.n = (points[i+4].p-points[i].p)^(points[i+6].p-points[i].p);
                    f.n.Normalize();
                    faces.push_back(f);
                }
            }
    }
    return true;
}
}
