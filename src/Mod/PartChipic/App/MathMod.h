#ifndef _MATH_MOD_H_
#define _MATH_MOD_H_
#include "PreCompiled.h"
#include <string>
#include <vector>
#include "mathmod/pariso/isosurface/MIso3D.h"
#include "mathmod/pariso/objectparameters.h"
#include "mathmod/ui_modules/ParisoMathObject.h"
#include "mathmod/json_parser/parisodef.h"
#include <TopoDS_Compound.hxx>
#include <TopoDS_Wire.hxx>
#include <TopTools_ListOfShape.hxx>
#include <App/ComplexGeoData.h>
#include <Base/Vector3D.h>
#define uint unsigned int 

class MathMod
{
public:
	MathMod(uint maxtri, uint maxpts, uint gridmax,
		uint NbComponent, uint NbVariables, uint NbConstantes,
		uint NbDefinedFunctions, uint NbTextures, int NbSliders, int NbSliderValues,
		uint nbthreads, uint initGrid, uint FactX, uint FactY, uint FactZ);
	~MathMod();

	int  memoryallocation(uint, uint, uint, uint, uint, uint, uint, uint, int, int, uint,
		uint initgrid = 40, uint factx = 4, uint facty = 4, uint factz = 4);
	void BuildIso();
	void ProcessNewIsoSurface(std::vector<Base::Vector3d> &Points, std::vector<Data::ComplexGeoData::Facet> &Facets, double &maxf);
	void SetParameters(std::string text, std::string Fxyz, std::string Xmax, std::string Xmin,
		std::string Ymax, std::string Ymin,
		std::string Zmax, std::string Zmin);
	void MathMod::SaveSceneAsObjPoly(char *filename);
public:
	ParisoMathObject RootObjet;
	jpariso pariso;
	MIso3D *IsoObjet;
	ObjectParameters *oPara;
	//ObjectProperties  LocalScene;
};
#endif