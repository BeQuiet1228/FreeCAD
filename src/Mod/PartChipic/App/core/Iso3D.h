/***************************************************************************
 *   Copyright (C) 2006 by Abderrahman Taha                                *
 *                                                                         *
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 *   This program is distributed in the hope that it will be useful,       *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU General Public License for more details.                          *
 *                                                                         *
 *   You should have received a copy of the GNU General Public License     *
 *   along with this program; if not, write to the                         *
 *   Free Software Foundation, Inc.,                                       *
 *   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA            *
 ***************************************************************************/
#ifndef _CHIPIC_ISO3D_H_
#define _CHIPIC_ISO3D_H_
//#include <GL/glew.h>

#include <stdio.h>
#include <time.h>

#include <vcg/complex/complex.h>

using namespace vcg;
using namespace std;
//#include <qgl.h>
//#include <qpointarray.h>
//#include <qpainter.h>
//#include <qbrush.h>
#include <string>
#include <iostream>
#include <string>
#include <cmath>
#include <vector>
#include <list>
#include "DefValue.h"
#include "IsoMatrix3D.h"
#include "pm3parser.h"
#include "system.h"

using std::string;
using std::vector;
using std::list;

///************* A new Structure that represents a Voxel *********///
struct  Voxel3D {
	double PositionX, PositionY, PositionZ;
	int Edge_Points[12]; //reference to the Edge Points
	int  Signature; // From 0 to 255
	int NbEdgePoint;
	int Index[4];
	double Value;   // The value of the implicit function.
};

///************* A new Structure that represents a Triangle *********///
struct  IsoTriangle {
	std::vector<vcg::Point3i>/*QPointArray*/ * pl;
	double valeur_z;
	double valeur_cos;
	int TypeCND; /// Two types : 1 --> Draw like a normal triangle; 2 --> Draw in Red
};

#define MAX_VSIZE 30

class Iso3D
{
public :
   std::vector<vcg::Point3d> IsoPointMapOriginal;//[3*60000]; // Up to 40.000 Pts[60000]
   //vcg::Point3d IsoPointMapProjectd[10000]; // Up to 40.000 Pts
   //vcg::Point3d IsoPointMapTransfrm[60000]; // Up to 40.000 Points

/// Conditional data :
   std::vector<int> WichPointVeryCond;//[100000]
   std::vector<int> TypeIsoSurfaceTriangleListeCND; // From 1 to 7 Up to 100.000[100000]
   //double IsoPointMapOriginalCD[3*10000]; // Up to 10.000 Pts
   //double IsoPointMapProjectdCD[3*10000]; // Up to 10.000 Pts
   //double IsoPointMapTransfrmCD[3*10000]; // Up to 10.000 Points

//   std::vector<vcg::Point3d> IsoNormMapOriginal; // Up to 100.000 Norm[100000]
   //double IsoNormMapTransfrm[3*100000]; // Up to 100.000 Norm


   std::vector<vcg::Point3i> IsoSurfaceTriangleListe;// Up to 100.000 Triangles[100000]
   double local[3][MAX_VSIZE];// XLocal[MAX_VSIZE], YLocal[MAX_VSIZE], ZLocal[MAX_VSIZE]; //Up to 200x200x200 voxels
   Voxel3D GridVoxel[MAX_VSIZE][MAX_VSIZE][MAX_VSIZE];
   int isSunk;
//   std::vector<vcg::Point3d> NormOriginal;// Up to 100.000 Triangles[100000]
   int type;//1:volume 0:surface
   int ndim;////0x1y2z else volume
   int NbPointIsoMap; // Init to 0 ; Up to 10.000
   int NbPointIsoMapCND; // Init to 0 ; Up to 10.000
   int NbTriangleIsoSurface;
   int NbTriangleIsoSurfaceCND;
   int i,j,k,l;
   double yreso;
   PM3::SYSTEM gsysType;
   PM3::ExpParser //ImplicitFunctionParser,
                *pValParser;
                  //XSupParser, XInfParser,
                  //YSupParser, YInfParser,
                  //ZSupParser, ZInfParser,

   std::string ImplicitFunction, IsoCondition;
   PM3::DefValue3D limitSup, limitInf;

   double newcoeffx, newcoeffy, newcoeffz;
   vcg::Point3d Start, End;
   int nGrid[3], //0 nb_ligne, 1nb_colon, 2nb_depth,
        clipping, CutLigne, CutColon, CutDepth,
        IsoConditionRequired;
    double D; // Distance observator
    double Oprime[3], Obser[3];
	vcg::Point3d Step;
    double MINX,MINY,MINZ,MINW,MINT,MINS,
           MAXX,MAXY,MAXZ,MAXW,MAXT,MAXS,
           DIFX,DIFY,DIFZ,DIFW,DIFT,DIFS,
           DIFMAXIMUM, decalage_xo, decalage_yo, decalage_zo,
           IsoValue, anglex, angley, ancienx, ancieny, ScalCoeff,//morph_param, 
           step, axe_size,
           newscalex, newscaley, newscalez;
    int    demi_hauteur, demi_largeur, hauteur_fenetre;
    IsoMatrix3D MatGen, MatRot, MatRotSave, MatSca, MatInv;
    int  frontsurfr, frontsurfg, frontsurfb,
         backsurfr,  backsurfg,  backsurfb,
         CNDsurfr,  CNDsurfg,  CNDsurfb,
         gridr, gridg, gridb, gridtransparent,
         PovActivate, fronttrans, backtrans, CNDtrans;
	std::vector<vcg::Point3i>/*QPointArray**/ tableaureferences[10000];
    IsoTriangle * tableau;
	std::vector<vcg::Point3i>/*QPointArray*/  isotriangle;
    vector<IsoTriangle *> VectorIsoTriangle;


    int IsoMesh, IsoInfos, NbTriangleUsed,
        axe_width, axe_center, DrawAxe_Ok, CNDMesh,
        CNDDraw, BorderDraw, Borderlimite;

int NbPolygonImposedLimit ;
//float NormVertexTab[50*66000];
//unsigned int IndexPolyTab[50*48000];
int NbVertex;
unsigned int NbPolygn;
unsigned int NbPolygnNbVertex[2 * 50];
int CurrentStep; /// To hold the current step in the Morph process
public :
	Iso3D();
	~Iso3D();
   void VoxelEvaluation ();
   void PointEdgeComputation();
   void DrawIsoSurface();
   void InitParser();
   void InitParameter();
   void SignatureComputation();
   void ConstructIsoSurface();
   void ConstructIsoNormale();

   bool ComputeIsoMap();
   bool ParseExpression();
   void SaveIsoMap();
   void SaveIsoMapUnifColor();
};


#endif




