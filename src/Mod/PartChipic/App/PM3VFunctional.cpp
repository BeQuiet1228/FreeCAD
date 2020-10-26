#include "PM3VFunctional.h"
#include "../core/pm3parser.h"
#include "../core/Iso3D.h"
#include "core/system.h"

#include "PreCompiled.h"

#ifndef _PreComp_
# include <cmath>
# include <cstdlib>
# include <sstream>
# include <QString>
# include <BRepLib.hxx>
# include <BSplCLib.hxx>
# include <Bnd_Box.hxx>
# include <BRep_Builder.hxx>
# include <BRep_Tool.hxx>
# include <BRepAdaptor_Curve.hxx>
# include <BRepAdaptor_CompCurve.hxx>
# include <BRepAdaptor_HCurve.hxx>
# include <BRepAdaptor_HCompCurve.hxx>
# include <BRepAdaptor_Surface.hxx>
# include <BRepAlgoAPI_Common.hxx>
# include <BRepAlgoAPI_Cut.hxx>
# include <BRepAlgoAPI_Fuse.hxx>
# include <BRepAlgo_Fuse.hxx>
# include <BRepAlgoAPI_Section.hxx>
# include <BRepBndLib.hxx>
# include <BRepBuilderAPI_FindPlane.hxx>
# include <BRepLib_FindSurface.hxx>
# include <BRepBuilderAPI_GTransform.hxx>
# include <BRepBuilderAPI_MakeEdge.hxx>
# include <BRepBuilderAPI_MakeFace.hxx>
# include <BRepBuilderAPI_MakePolygon.hxx>
# include <BRepBuilderAPI_MakeSolid.hxx>
# include <BRepBuilderAPI_MakeVertex.hxx>
# include <BRepBuilderAPI_MakeWire.hxx>
# include <BRepBuilderAPI_MakeShell.hxx>
# include <BRepBuilderAPI_NurbsConvert.hxx>
# include <BRepBuilderAPI_FaceError.hxx>
# include <BRepBuilderAPI_Copy.hxx>
# include <BRepBuilderAPI_Transform.hxx>
# include <BRepCheck_Analyzer.hxx>
# include <BRepCheck_ListIteratorOfListOfStatus.hxx>
# include <BRepCheck_Result.hxx>
# include <BRepClass_FaceClassifier.hxx>
# include <BRepFilletAPI_MakeFillet.hxx>
# include <BRepGProp.hxx>
# include <BRepMesh_IncrementalMesh.hxx>
# include <BRepMesh_Triangle.hxx>
# include <BRepMesh_Edge.hxx>
# include <BRepOffsetAPI_MakeThickSolid.hxx>
# include <BRepOffsetAPI_MakeOffsetShape.hxx>
# include <BRepOffsetAPI_MakeOffset.hxx>
# include <BRepOffsetAPI_MakePipe.hxx>
# include <BRepOffsetAPI_MakePipeShell.hxx>
# include <BRepOffsetAPI_Sewing.hxx>
# include <BRepOffsetAPI_ThruSections.hxx>
# include <BRepPrimAPI_MakePrism.hxx>
# include <BRepPrimAPI_MakeRevol.hxx>
# include <BRepTools.hxx>
# include <BRepTools_ReShape.hxx>
# include <BRepTools_ShapeSet.hxx>
# include <BRepTools_WireExplorer.hxx>
# include <BRepFill_CompatibleWires.hxx>
# include <GCE2d_MakeSegment.hxx>
# include <GCPnts_AbscissaPoint.hxx>
# include <GCPnts_UniformAbscissa.hxx>
# include <Geom2d_Line.hxx>
# include <Geom2d_TrimmedCurve.hxx>
# include <GeomLProp_SLProps.hxx>
# include <GeomAPI_ProjectPointOnSurf.hxx>
# include <GeomFill_CorrectedFrenet.hxx>
# include <GeomFill_CurveAndTrihedron.hxx>
# include <GeomFill_EvolvedSection.hxx>
# include <GeomFill_Pipe.hxx>
# include <GeomFill_SectionLaw.hxx>
# include <GeomFill_Sweep.hxx>
# include <GeomLib.hxx>
# include <GProp_GProps.hxx>
# include <Law_BSpFunc.hxx>
# include <Law_BSpline.hxx>
# include <Law_BSpFunc.hxx>
# include <Law_Constant.hxx>
# include <Law_Linear.hxx>
# include <Law_S.hxx>
# include <TopTools_HSequenceOfShape.hxx>
# include <Interface_Static.hxx>
# include <IGESControl_Controller.hxx>
# include <IGESControl_Writer.hxx>
# include <IGESControl_Reader.hxx>
# include <IGESData_GlobalSection.hxx>
# include <IGESData_IGESModel.hxx>
# include <STEPControl_Writer.hxx>
# include <STEPControl_Reader.hxx>
# include <TopTools_MapOfShape.hxx>
# include <TopoDS.hxx>
# include <TopoDS_Compound.hxx>
# include <TopoDS_Iterator.hxx>
# include <TopoDS_Solid.hxx>
# include <TopoDS_Vertex.hxx>
# include <TopExp.hxx>
# include <TopExp_Explorer.hxx>
# include <TopTools_ListIteratorOfListOfShape.hxx>
# include <Geom2d_Ellipse.hxx>
# include <Geom_BezierCurve.hxx>
# include <Geom_BezierSurface.hxx>
# include <Geom_BSplineCurve.hxx>
# include <Geom_BSplineSurface.hxx>
# include <Geom_SurfaceOfLinearExtrusion.hxx>
# include <Geom_SurfaceOfRevolution.hxx>
# include <Geom_Circle.hxx>
# include <Geom_ConicalSurface.hxx>
# include <Geom_CylindricalSurface.hxx>
# include <Geom_Ellipse.hxx>
# include <Geom_Hyperbola.hxx>
# include <Geom_Line.hxx>
# include <Geom_Parabola.hxx>
# include <Geom_Plane.hxx>
# include <Geom_CartesianPoint.hxx>
# include <Geom_SphericalSurface.hxx>
# include <Geom_ToroidalSurface.hxx>
# include <Poly_Triangulation.hxx>
# include <Standard_Failure.hxx>
# include <StlAPI_Writer.hxx>
# include <Standard_Failure.hxx>
# include <gp_GTrsf.hxx>
# include <ShapeAnalysis_Shell.hxx>
# include <ShapeBuild_ReShape.hxx>
# include <ShapeExtend_Explorer.hxx>
# include <ShapeFix_Edge.hxx>
# include <ShapeFix_Face.hxx>
# include <ShapeFix_Shell.hxx>
# include <ShapeFix_Solid.hxx>
# include <ShapeUpgrade_ShellSewing.hxx>
# include <ShapeUpgrade_RemoveInternalWires.hxx>
# include <Standard_Version.hxx>
#endif
# include <BinTools.hxx>
# include <BinTools_ShapeSet.hxx>
# include <Poly_Polygon3D.hxx>
# include <Poly_PolygonOnTriangulation.hxx>
# include <BRepBuilderAPI_Sewing.hxx>
# include <ShapeFix_Shape.hxx>
# include <XSControl_WorkSession.hxx>
# include <Transfer_TransientProcess.hxx>
# include <Transfer_FinderProcess.hxx>
# include <XSControl_TransferWriter.hxx>
# include <APIHeaderSection_MakeHeader.hxx>
# include <ShapeAnalysis_FreeBoundsProperties.hxx>
# include <ShapeAnalysis_FreeBoundData.hxx>

#if OCC_VERSION_HEX >= 0x060600
#include <BOPAlgo_ArgumentAnalyzer.hxx>
#include <BOPAlgo_ListOfCheckResult.hxx>
#endif

#include <Base/Builder3D.h>
#include <Base/FileInfo.h>
#include <Base/Exception.h>
#include <Base/Tools.h>
#include <Base/Console.h>

#include<Base/Sequencer.h>

#include "Mod/Part/App/TopoShape.h"
#include "Mod/Part/App/CrossSection.h"
#include "Mod/Part/App/TopoShapeFacePy.h"
#include "Mod/Part/App/TopoShapeEdgePy.h"
#include "Mod/Part/App/TopoShapeVertexPy.h"
#include "Mod/Part/App/ProgressIndicator.h"
#include "Mod/Part/App/modelRefine.h"
#include "Mod/Part/App/Tools.h"
#include "Mod/Part/App/encodeFilename.h"
#include "Mod/Part/App/FaceMakerBullseye.h"

#include <vcg/complex/algorithms/clean.h>
#include <vcg/complex/algorithms/hole.h>
#include<vcg/complex/algorithms/update/bounding.h>
using namespace Part;

namespace PM3
{
VFunctional::VFunctional(std::string base,VOLUME_TYPE t): Mesh(base,t)
{
    bclosed=false;
	setSystem(gsysType);
    near_point.setValue("-1.9mm,0mm,4.3mm");
    far_point.setValue("1.8mm,2.5mm,65mm");
    
	f = "-0.00434**2+(x)**2+(y+0.00217)**2";// "(x^2+y^2+z^2-2^2)*step(x,-1)*step(1,x)";
    dim = 3;
    nature.value = 0;

	iso = new Iso3D();

	yreso = 1.0;//默认1deg
}

VFunctional::~VFunctional()
{
	delete iso;
}

void  VFunctional::setSystem(PM3::SYSTEM s)
{
    CVolume::setSystem(s);
    if(gsysType == PM3::SYSCARTESIAN)
    {
        near_point.setValue("0,0,0");
        far_point.setValue("0,0,0");
    }
    if(gsysType == PM3::SYSCYLINDRICAL)
    {
        near_point.setValue("0,0deg,0");
        far_point.setValue("0,360deg,0");
    }
    if(gsysType == PM3::SYSMYCC)
    {
        near_point.setValue("0,0,0deg");
        far_point.setValue("0,0,0deg");
    }
}
bool VFunctional::getWorkRegion()
{
    workRegion[0] = near_point;
    workRegion[1] = far_point;
    return true;
}
std::string VFunctional::text()
{
//    !! AreaObj3
//            FUNCTION AreaObj3.F(Z,R) = nvbnvbn ;
//    POINT AreaObj3.LO 0.MM, 0.MM ;
//    POINT AreaObj3.HI 10.MM, 10.MM ;
//    AREA AreaObj3 FUNCTIONAL AreaObj3.F AreaObj3.LO AreaObj3.HI ;
//    MARK AreaObj3 X1 SIZE DX1 ;
//    MARK AreaObj3 X2 SIZE DX2 ;

	std::string out;
//    vcg::Point3f p1,//top
//            p2;//base
//    float l1,l2,l3;
//    if(
//            !near_point.Parser(pexparser, p1) ||
//            !far_point.Parser(pexparser, p2)||
//            !lineEdit_markxD.Parser(pexparser, l1)||
//            !lineEdit_markyD.Parser(pexparser, l2)||
//            !lineEdit_markzD.Parser(pexparser, l3))//error
//        return "express error!";

    /*out += std::string("  !! %1\n").arg(name);
    if(gsysType == PM3::SYSCARTESIAN)
        out += std::string("  FUNCTION %1.F(X,Y,Z) = %2 ;\n").arg(name).arg(f);
    if(gsysType == PM3::SYSCYLINDRICAL)
        out += std::string("  FUNCTION %1.F(R,PHI,Z) = %2 ;\n").arg(name).arg(f);
    out += std::string("  POINT %1.LO %2, %3%4, %5 ;\n").arg(name).arg(near_point.value[0]).arg(near_point.value[1]).arg(x2).arg(near_point.value[2]);
    out += std::string("  POINT %1.HI %2, %3%4, %5 ;\n").arg(name).arg(far_point.value[0]).arg(far_point.value[1]).arg(x2).arg(far_point.value[2]);
    out += std::string("  VOLUME %1 FUNCTIONAL %2.F %3.LO %4.HI ;\n").arg(name).arg(name).arg(name).arg(name);
    if(markxD)
        out += std::string("  MARK %1 X1 SIZE %2 ;\n").arg(name).arg(lineEdit_markxD.value);
    if(markyD)
        out += std::string("  MARK %1 X2 SIZE %2%3 ;\n").arg(name).arg(lineEdit_markyD.value).arg(x2);
    if(markzD)
        out += std::string("  MARK %1 X3 SIZE %2 ;\n").arg(name).arg(lineEdit_markzD.value);
		*/
    return out;
}


std::string VFunctional::getPAP()
{
	std::string out;
   /* switch(property)
    {
    case 0:
		out += std::string("");
        break;
    case 1:
        out += std::string("  CONDUCTOR %1 ;\n").arg(name);
        break;
    case 2:
        //        if(gsysType == PM3::SYSCARTESIAN)
        //        {
                    if(checkSigma)
                    {
        //                out += std::string("  FUNCTION %1.SIGMA(X,Y,Z) = %2 ;\n").arg(name).arg(lineEditSigma);
                        out += std::string("  CONDUCTANCE %1 %2 ;\n").arg(name).arg(lineEditSigma);
                    }
                    if(checkEps)
                    {
                        if(checkn1)
                        {
        //                    out += std::string("  FUNCTION %1.EPS(X,Y,Z) = %2 ;\n").arg(name).arg(lineEditEps1);
                            out += std::string("  DIELECTRIC %1 %2 ;\n").arg(name).arg(lineEditEps1);
                        }else if(!checkn1)
                        {
        //                    out += std::string("  FUNCTION %1.EPS1(X,Y,Z) = %2 ;\n").arg(name).arg(lineEditEps1);
                            out += std::string("  DIELECTRIC %1 %2 EPS1 ;\n").arg(name).arg(lineEditEps1);
        //                    out += std::string("  FUNCTION %1.EPS2(X,Y,Z) = %2 ;\n").arg(name).arg(lineEditEps2);
                            out += std::string("  DIELECTRIC %1 %2 EPS2 ;\n").arg(name).arg(lineEditEps2);
        //                    out += std::string("  FUNCTION %1.EPS3(X,Y,Z) = %2 ;\n").arg(name).arg(lineEditEps3);
                            out += std::string("  DIELECTRIC %1 %2 EPS3 ;\n").arg(name).arg(lineEditEps3);
                        }
                    }
        //        }else if(gsysType == PM3::SYSCYLINDRICAL)
        //        {
        //            if(checkSigma)
        //            {
        //                out += std::string("  FUNCTION %1.SIGMA(R,P,Z) = %2 ;\n").arg(name).arg(lineEditSigma);
        //                out += std::string("  CONDUCTANCE %1 %2.SIGMA ;\n").arg(name).arg(name);
        //            }
        //            if(checkEps)
        //            {
        //                if(checkn1)
        //                {
        //                    out += std::string("  FUNCTION %1.EPS(R,P,Z) = %2 ;\n").arg(name).arg(lineEditEps1);
        //                    out += std::string("  DIELECTRIC %1 %2.EPS ;\n").arg(name).arg(name);
        //                }else if(!checkn1)
        //                {
        //                    out += std::string("  FUNCTION %1.EPS1(R,P,Z) = %2 ;\n").arg(name).arg(lineEditEps1);
        //                    out += std::string("  DIELECTRIC %1 %2.EPS1 EPS1 ;\n").arg(name).arg(name);
        //                    out += std::string("  FUNCTION %1.EPS2(R,P,Z) = %2 ;\n").arg(name).arg(lineEditEps2);
        //                    out += std::string("  DIELECTRIC %1 %2.EPS2 EPS2 ;\n").arg(name).arg(name);
        //                    out += std::string("  FUNCTION %1.EPS3(R,P,Z) = %2 ;\n").arg(name).arg(lineEditEps3);
        //                    out += std::string("  DIELECTRIC %1 %2.EPS3 EPS3 ;\n").arg(name).arg(name);
        //                }
        //            }
        //        }
        break;
    case 3:
        out += std::string("  VOID %1 ;\n").arg(name);
        break;
    }*/
    return out;
}
TopoDS_Shape VFunctional::update_mesh_topology(double &maxf)
{
	std::vector<Vertex> points;
	std::vector<Face> faces;

	vcg::Point3f p1, p2;

	       convert2MeshO(points,faces);

	//    if(!pexparser->getUpdate(near_point)||!near_point.Parser(pexparser, p1) ||
	//       !pexparser->getUpdate(far_point)||     !far_point.Parser(pexparser, p2))//error
	//        return false;

	int i, j;
	// process the new surface
	//ProcessNewIsoSurface( );
	DefValue3D p, pp;
	p = far_point;
	pp = near_point;
	
	if (gsysType == PM3::SYSMYCC)
	{


		p.value[0] = far_point.value[1];
		p.value[1] = far_point.value[2];
		p.value[2] = far_point.value[0];

		pp.value[0] = near_point.value[1];
		pp.value[1] = near_point.value[2];
		pp.value[2] = near_point.value[0];

		iso->gsysType = PM3::SYSCYLINDRICAL;

	}
	else
	{
		iso->gsysType = gsysType;
	}

	iso->pValParser = this->pexparser;
	std::transform(f.begin(), f.end(), f.begin(), ::tolower);

	iso->ImplicitFunction = replace_str(f, "**", "^");//f.toLower().replace("**", "^");
	iso->limitSup = p;//
	iso->limitInf = pp;
	std::string res = "0";// getStringFromFloat(pgrid->getresolu());
	if (property == PM3::PRO_EMPTY)
	{
		iso->limitSup.setValue(0, p.value[0] + "+" + res);
		iso->limitSup.setValue(1, p.value[1] + "+" + res);
		iso->limitSup.setValue(2, p.value[2] + "+" + res);
		iso->limitInf.setValue(0, pp.value[0] + "-" + res);
		iso->limitInf.setValue(1, pp.value[1] + "-" + res);
		iso->limitInf.setValue(2, pp.value[2] + "-" + res);
	}
	bool br = iso->ComputeIsoMap();
	maxf = -1;
	for (i = 0; i < iso->NbPointIsoMap; i++)
	{
		Vertex v;
		double *p = iso->IsoPointMapOriginal[i].V();
		v.p = vcg::Point3f(p[0], p[1], p[2]);
		p = iso->IsoNormMapOriginal[i].V();
		v.n = -vcg::Point3f(p[0], p[1], p[2]);
		maxf = fmax(maxf, fmax(fabs(p[0]), fmax(fabs(p[1]), fabs(p[2]))));
		points.push_back(v);
	}
	for (i = 0; i < iso->NbTriangleIsoSurface; i++)
	{
		if (iso->TypeIsoSurfaceTriangleListeCND[i] != 0) {
			vcg::Point3i index(iso->IsoSurfaceTriangleListe[i]);
			Face f(index.Z(), index.Y(), index.X());
			double *p = iso->NormOriginal[i].V();
			f.n = -vcg::Point3f(p[0], p[1], p[2]);
			faces.push_back(f);
		}
	}

	convert2MeshO(points,faces);
	int r1 = tri::Clean<CMeshO>::RemoveUnreferencedVertex(this->cm);
	int r2 = tri::Clean<CMeshO>::RemoveDuplicateVertex(this->cm);
	int r3 = tri::Clean<CMeshO>::RemoveDuplicateFace(this->cm);
	int r4 = tri::Clean<CMeshO>::RemoveFaceFoldByFlip(this->cm);
	gp_XYZ gp1, gp2, gp3;
	TopoDS_Vertex Vertex1, Vertex2, Vertex3;
	TopoDS_Face newFace;
	TopoDS_Wire newWire;
	BRepBuilderAPI_Sewing aSewingTool;
	Standard_Real x1, y1, z1;
	Standard_Real x2, y2, z2;
	Standard_Real x3, y3, z3;

	//aSewingTool.Init(Accuracy,Standard_True);

	TopoDS_Compound aComp;
	TopoDS_Shell shell;
	BRep_Builder BuildTool;
	BuildTool.MakeCompound(aComp);
	BuildTool.MakeShell(shell);
	////加上进度条
	//std::unique_ptr<Base::SequencerLauncher> _seq;
	//_seq.reset(new Base::SequencerLauncher("make Face...", Topo.size()));
	int I1, I2, I3;
	double *v1, *v2, *v3;
	for (i = 0; i < iso->NbTriangleIsoSurface; i++) {
		if (iso->TypeIsoSurfaceTriangleListeCND[i] != 0) {
			vcg::Point3i index(iso->IsoSurfaceTriangleListe[i]);
			//Face f(index.Z(),index.Y(),index.X());
			Data::ComplexGeoData::Facet face;
			I1 = index.Z();
			I2 = index.Y();
			I3 = index.X();
			v1 = iso->IsoPointMapOriginal[I1].V();
			v2 = iso->IsoPointMapOriginal[I2].V();
			v3 = iso->IsoPointMapOriginal[I3].V();
			x1 = v1[0]; y1 = v1[1]; z1 = v1[2];
			x2 = v2[0]; y2 = v2[1]; z2 = v2[2];
			x3 = v3[0]; y3 = v3[1]; z3 = v3[2];
			gp1.SetCoord(x1, y1, z1);
			gp2.SetCoord(x2, y2, z2);
			gp3.SetCoord(x3, y3, z3);
			newWire = BRepBuilderAPI_MakePolygon(gp1, gp2, gp3, Standard_True);
			if (!newWire.IsNull()) {
				newFace = BRepBuilderAPI_MakeFace(newWire, Standard_True);
				if (!newFace.IsNull())
					//BuildTool.Add(shell, newFace);
				   aSewingTool.Add(newFace); // //BuildTool.Add(aComp, newFace);
			}
		}
	}
	aSewingTool.Perform();
	TopoDS_Shape _Shape = aSewingTool.SewedShape();
	if (_Shape.IsNull())
		_Shape = aComp;
	
	
	//return shell;
	return _Shape;
}

bool VFunctional::update_mesh_topology(std::vector<Base::Vector3d> &Points, std::vector<Data::ComplexGeoData::Facet> &Facets, double &maxf)
{
    std::vector<Vertex> points;
       std::vector<Face> faces;

       vcg::Point3f p1, p2;

       convert2MeshO(points,faces);

   //    if(!pexparser->getUpdate(near_point)||!near_point.Parser(pexparser, p1) ||
   //       !pexparser->getUpdate(far_point)||     !far_point.Parser(pexparser, p2))//error
   //        return false;

       int i,j;
       // process the new surface
      //ProcessNewIsoSurface( );
       DefValue3D p,pp;
       p = far_point;
       pp = near_point;
       
       if(gsysType==PM3::SYSMYCC)
       {
          p.value[0] = far_point.value[1];
          p.value[1] = far_point.value[2];
          p.value[2] = far_point.value[0];

          pp.value[0] = near_point.value[1];
          pp.value[1] = near_point.value[2];
          pp.value[2] = near_point.value[0];

          iso->gsysType = PM3::SYSCYLINDRICAL;

       }else
       {
            iso->gsysType = gsysType;
       }

       iso->pValParser = this->pexparser;
	   std::transform(f.begin(), f.end(), f.begin(), ::tolower);
	   //std::string temstr = replace_str(f, "theta", "(atan2(y,x)");
	   //temstr = replace_str(temstr, "r", "(sqrt(x*x+y*y)");
	   std::string temstr = replace_str(f, "theta", "phi");
	   iso->ImplicitFunction = replace_str(temstr, "**", "^");//f.toLower().replace("**", "^");
       iso->limitSup = p;//
       iso->limitInf = pp;
	   std::string res = "0";// getStringFromFloat(pgrid->getresolu());
       if(property == PM3::PRO_EMPTY)
       {
           iso->limitSup.setValue(0, p.value[0]+"+"+res);
           iso->limitSup.setValue(1, p.value[1]+"+"+res);
           iso->limitSup.setValue(2, p.value[2]+"+"+res);
           iso->limitInf.setValue(0, pp.value[0]+"-"+res);
           iso->limitInf.setValue(1, pp.value[1]+"-"+res);
           iso->limitInf.setValue(2, pp.value[2]+"-"+res);
       }
	   iso->yreso = this->yreso;
       bool br = iso->ComputeIsoMap();
	   maxf = -1;
	  /* std::vector<Vertex> tpoints;
	   std::vector<Face> tfaces;
	   tpoints.resize(iso->NbPointIsoMap);
	   for (i = 0; i < iso->NbPointIsoMap; i++)
	   {
		   Vertex v;
		   double *p = iso->IsoPointMapOriginal[i].V();
		   v.p = vcg::Point3f(p[0], p[1], p[2]);
		   p = iso->IsoNormMapOriginal[i].V();
		   v.n = -vcg::Point3f(p[0], p[1], p[2]);
		   maxf = fmax(maxf, fmax(fabs(p[0]), fmax(fabs(p[1]), fabs(p[2]))));
		   tpoints[i]=(v);
	   }
	  
	   std::vector<int> use(iso->NbPointIsoMap);
	   for (i = 0; i < iso->NbTriangleIsoSurface; i++)
	   {
		   if (iso->TypeIsoSurfaceTriangleListeCND[i] != 0) {
			   vcg::Point3i index(iso->IsoSurfaceTriangleListe[i]);
			  
			   use[index.Z()] = 1;
			   use[index.Y()] = 1;
			   use[index.X()] = 1;
		   }
	   }
	   int count = 0, index = 0;
		for (i = 0; i < iso->NbPointIsoMap; i++) count += use[i];
		std::vector<int> mmp(iso->NbPointIsoMap);
	   points.resize(count);
	   for (i = 0; i < iso->NbPointIsoMap; i++) {
		   if (use[i] == 1) {
			   points[index] = tpoints[i];
			   mmp[i] = index;
			   index++;
		   }
	   }
	   faces.resize(iso->NbTriangleIsoSurface);
	   for (i = 0; i < iso->NbTriangleIsoSurface; i++)
	   {
		   if (iso->TypeIsoSurfaceTriangleListeCND[i] != 0) {
			   vcg::Point3i index(iso->IsoSurfaceTriangleListe[i]);
			   Face f(mmp[index.X()], mmp[index.Y()], mmp[index.Z()]);
			   double *p = iso->NormOriginal[i].V();
			   f.n = -vcg::Point3f(p[0], p[1], p[2]);
			   faces[i] = (f);
		   }
	   } */
	   /*points.resize(iso->NbPointIsoMap);
	   for (i = 0; i < iso->NbPointIsoMap; i++)
	   {
		   Vertex v;
		   double *p = iso->IsoPointMapOriginal[i].V();
		   v.p = vcg::Point3f(p[0], p[1], p[2]);
		   //p = iso->IsoNormMapOriginal[i].V();
		   //v.n = -vcg::Point3f(p[0], p[1], p[2]);
		   maxf = fmax(maxf, fmax(fabs(p[0]), fmax(fabs(p[1]), fabs(p[2]))));
		   points[i] = (v);
	   }
	   faces.resize(iso->NbTriangleIsoSurface);
	   for (i = 0; i < iso->NbTriangleIsoSurface; i++)
	   {
		   if (iso->TypeIsoSurfaceTriangleListeCND[i] != 0) {
			   vcg::Point3i index(iso->IsoSurfaceTriangleListe[i]);
			   Face f(index[0], index[1], index[2]);
			   //double *p = iso->NormOriginal[i].V();
			   //f.n = -vcg::Point3f(p[0], p[1], p[2]);
			   faces[i] = (f);
		   }
	   }
	   convert2MeshO(points, faces);
*/
	   {
		   int j;
		   cm.Clear();

		   CMeshO::VertexIterator vi = vcg::tri::Allocator<CMeshO>::AddVertices(cm, iso->NbPointIsoMap);
		   //float i[3];
		   float res = 1.0;// pgrid->getresolu();
		   for (j = 0; j<iso->NbPointIsoMap; ++j)
		   {
			   //i[0] = (int64_t(points[j].p[0] / res+0.5))*res;
			   //i[1] = (int64_t(points[j].p[1] / res+0.5))*res;
			   //i[2] = (int64_t(points[j].p[2] / res+0.5))*res;
			   double *p = iso->IsoPointMapOriginal[j].V();
			   (*vi).P()[0] = p[0];// / res;//i[0];//i;
			   (*vi).P()[1] = p[1];// / res;//i[1];//
			   (*vi).P()[2] = p[2];// / res;//i[2];//
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
		   for (j = 0, vi = cm.vert.begin(); j<cm.vn; ++j, ++vi)
			   index[j] = &*vi;
		   int fn = 0;
		   for (j = 0; j < iso->NbTriangleIsoSurface; j++)
		   {
			   if (iso->TypeIsoSurfaceTriangleListeCND[j] != 0) fn += 1;
		   }
		   CMeshO::FaceIterator fi = vcg::tri::Allocator<CMeshO>::AddFaces(cm, fn);
		   int *v = 0;
		   for (j = 0; j < iso->NbTriangleIsoSurface; j++)
		   {
			   if (iso->TypeIsoSurfaceTriangleListeCND[j] != 0) {
				   (*fi).Alloc(3);
				   v = iso->IsoSurfaceTriangleListe[j].V();
				   (*fi).V(0) = index[v[0]];
				   (*fi).V(1) = index[v[1]];
				   (*fi).V(2) = index[v[2]];
				   //for (int k = 0; k<3; ++k)
					//   (*fi).V(k) = index[faces[j].v[k]];
				   //(*fi).N() = faces[j].n;
				   ++fi;
			   }
		   }
		   //cm.clean();
		   //if (name == "bbox")
			//   vcg::tri::Clean<CMeshO>::RemoveUnreferencedVertex(cm);
		   //saveOBJ(PM3::getOutOBJName("d://ori" + name + ".obj"));
		   //tri::UpdateBounding<CMeshO>::Box(cm);
		   blist = true;
	   }
	   cm.bbox.min;
	   cm.bbox.max;
	  // saveOBJ(PM3::getOutOBJName("d://ori" + name + ".obj"));

//	   int r1 = tri::Clean<CMeshO>::RemoveUnreferencedVertex(this->cm);//todo
//	   int r2 = tri::Clean<CMeshO>::RemoveDuplicateVertex(this->cm);
//	   int r3 = tri::Clean<CMeshO>::RemoveDuplicateFace(this->cm);
	   //int r4 = tri::Clean<CMeshO>::RemoveFaceFoldByFlip(this->cm);
	   //int r6 = tri::Clean<CMeshO>::RemoveNonManifoldFace(this->cm);
	   std::vector<int> VertexId(cm.vert.size());
	   int numvert = 0;
	   CMeshO::VertexIterator vi;
	   for (vi = cm.vert.begin(); vi != cm.vert.end(); ++vi)//for (i = 0; i < iso->NbPointIsoMap; i++)
		   if (!(*vi).IsD())
       {
		   VertexId[vi - cm.vert.begin()] = numvert;
          // //Vertex v;
           //double *p = iso->IsoPointMapOriginal[i].V();
           ////v.p = vcg::Point3f(p[0],p[1],p[2]);
           ////p = iso->IsoNormMapOriginal[i].V();
           ////v.n = -vcg::Point3f(p[0],p[1],p[2]);
		   maxf = fmax(maxf, fmax(fabs((*vi).P()[0]), fmax(fabs((*vi).P()[1]), fabs((*vi).P()[2]))));
		   Points.push_back(Base::Vector3d((*vi).P()[0], (*vi).P()[1], (*vi).P()[2]));

		   numvert++;
       }
	   for (CMeshO::FaceIterator fi = cm.face.begin(); fi != cm.face.end(); ++fi)//for (i = 0; i < iso->NbTriangleIsoSurface; i++)
		   if (!(*fi).IsD())
       {
           /*if(iso->TypeIsoSurfaceTriangleListeCND[i] != 0) {
				vcg::Point3i index(iso->IsoSurfaceTriangleListe[i]);
				//Face f(index.Z(),index.Y(),index.X());
				Data::ComplexGeoData::Facet face;
				if (index.Z() * index.Y() * index.X() <= 0)
					;
				face.I1 = index.X();
				face.I2 = index.Y();
				face.I3 = index.Z();
				Facets.push_back(face);
           }*/
		   Data::ComplexGeoData::Facet face;
		   face.I1 = VertexId[tri::Index(cm, (*fi).V(0))];
		   face.I2 = VertexId[tri::Index(cm, (*fi).V(1))];
		   face.I3 = VertexId[tri::Index(cm, (*fi).V(2))];
		   Facets.push_back(face);		   
       }

//       convert2MeshO(points,faces);


	   return 1;
}

/*bool VFunctional::load(QTextStream &stream)
{

    if(!Mesh::load(stream))
            return false;
    do{
        f = stream.readLine();
    }while(f.isEmpty());

   if(!near_point.load(stream) ||
            !far_point.load(stream)||
           !nature.load(stream))
        return false;
    return true;
}

void VFunctional::save(QTextStream &stream)
{
    Mesh::save(stream);
    stream << f << QLatin1Char('\n');
    near_point.save(stream);
    far_point.save(stream);
    nature.save(stream);
}
*/
}

