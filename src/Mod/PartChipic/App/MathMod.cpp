#include "MathMod.h"
#include "mathmod/pariso/objectparameters.h"

MathMod::MathMod(uint maxtri, uint maxpts, uint gridmax,
	uint NbComponent, uint NbVariables, uint NbConstantes,
	uint NbDefinedFunctions, uint NbTextures, int NbSliders, int NbSliderValues,
	uint nbthreads, uint initGrid, uint FactX, uint FactY, uint FactZ) {

	IsoObjet = new MIso3D(maxtri, maxpts, gridmax, NbComponent, NbVariables, NbConstantes,
		NbDefinedFunctions, NbTextures, NbSliders, NbSliderValues, nbthreads,
		initGrid, FactX, FactY, FactZ);

	//ParObjetThread = new ParThread(new Par3D(maxpts, nbthreads));
	oPara = new ObjectParameters(maxpts, maxtri);

}

MathMod::~MathMod() {
	delete IsoObjet;
	delete oPara;
}

int MathMod::memoryallocation(uint maxtri, uint maxpts, uint gridmax,
	uint NbComponent, uint NbVariables, uint NbConstantes,
	uint NbDefinedFunctions, uint NbTextures, int NbSliders, int NbSliderValues, uint nbthreads,
	uint initGrid, uint FactX, uint FactY, uint FactZ)
{
	//memoryallocation
	
	
	return  1;
}

void MathMod::BuildIso()
{
	IsoObjet->BuildIso();
}

void MathMod::SetParameters(std::string text, std::string Fxyz, std::string Xmax, std::string Xmin,
	std::string Ymax, std::string Ymin,
	std::string Zmax, std::string Zmin)
{
	//for (int i = 0; i<this->RootObjet.MyJsonObjectSelection.count(); i++)
	//	this->RootObjet.MyJsonObjectSelection.removeAt(i);
	this->RootObjet.NbIsoStruct = this->RootObjet.NbParamStruct = 0;
	this->pariso.JPar.clear();
	this->pariso.JIso.clear();
	jiso newjiso;
	this->pariso.JIso.append(newjiso);

	//if (Jobj["Iso3D"].isObject())
	{
		//QObj = Jobj["Iso3D"].toObject();
		// Fxyz
		//lst = QObj["Fxyz"].toArray();		
		this->IsoObjet->masterthread->ImplicitFunction = Fxyz;
		this->IsoObjet->masterthread->ImplicitFunctionSize = 1;
		//this->RootObjet.CurrentTreestruct.fxyz = result.split(";", QString::SkipEmptyParts);
		// Condition:
		//lst = QObj["Cnd"].toArray();		
		this->IsoObjet->masterthread->Condition = "";
		//MathmodRef->RootObjet.CurrentTreestruct.Cnd = result.split(";", QString::SkipEmptyParts);

		// Varu
		//lst = QObj["Varu"].toArray();		
		this->IsoObjet->masterthread->Varu = "";
		this->IsoObjet->masterthread->VaruSize = 1;
		//MathmodRef->RootObjet.CurrentTreestruct.Varu = result.split(";", QString::SkipEmptyParts);

		// Const
		//lst = QObj["Const"].toArray();
		this->IsoObjet->masterthread->Const = "";
		//MathmodRef->RootObjet.CurrentTreestruct.Const = result.split(";", QString::SkipEmptyParts);

		// Funct
		//lst = QObj["Funct"].toArray();
		this->IsoObjet->masterthread->Funct = "";
		this->IsoObjet->masterthread->FunctSize = 1;
		//MathmodRef->RootObjet.CurrentTreestruct.Funct = result.split(";", QString::SkipEmptyParts);

		//Noise:
		//QString noise = "";
		//noise = Jobj["Noise"].toString();
		this->IsoObjet->masterthread->Noise = "";
		//MathmodRef->RootObjet.CurrentTreestruct.Noise = noise;

		// Colors
		//QString noise1 = "";
		//noise1 = QTextureObj["Noise"].toString();
		//lst = QTextureObj["Colors"].toArray();		
		this->IsoObjet->masterthread->Rgbt = "";
		//MathmodRef->RootObjet.CurrentTreestruct.RGBT = result.split(";", QString::SkipEmptyParts);
		//if (noise == "")
		{
			this->IsoObjet->masterthread->Noise = "";
			//MathmodRef->RootObjet.CurrentTreestruct.Noise = noise1;
		}

		// Pigment		
		this->IsoObjet->masterthread->Gradient = "";
		this->IsoObjet->masterthread->VRgbt = "";
		//MathmodRef->RootObjet.CurrentTreestruct.VRGBT = result.split(";", QString::SkipEmptyParts);
		//if (noise == "" && noise1 == "")
		{
			this->IsoObjet->masterthread->Noise = "";
			//MathmodRef->RootObjet.CurrentTreestruct.Noise = noise2;
		}
		// Grid
		this->IsoObjet->masterthread->Grid = "";
		//MathmodRef->RootObjet.CurrentTreestruct.Grid = result.split(";", QString::SkipEmptyParts);


		// XlimitSup
		//lst = QObj["Xmax"].toArray();
		this->IsoObjet->masterthread->XlimitSup = Xmax;
		//MathmodRef->RootObjet.CurrentTreestruct.xmax = result.split(";", QString::SkipEmptyParts);

		// YlimitSup
		//lst = QObj["Ymax"].toArray();
		this->IsoObjet->masterthread->YlimitSup = Ymax;
		//MathmodRef->RootObjet.CurrentTreestruct.ymax = result.split(";", QString::SkipEmptyParts);

		// ZlimitSup
		//lst = QObj["Zmax"].toArray();
		this->IsoObjet->masterthread->ZlimitSup = Zmax;
		//MathmodRef->RootObjet.CurrentTreestruct.zmax = result.split(";", QString::SkipEmptyParts);

		// XlimitInf
		//lst = QObj["Xmin"].toArray();
		this->IsoObjet->masterthread->XlimitInf = Xmin;
		//MathmodRef->RootObjet.CurrentTreestruct.xmin = result.split(";", QString::SkipEmptyParts);

		// YlimitInf
		//lst = QObj["Ymin"].toArray();
		this->IsoObjet->masterthread->YlimitInf = Ymin;
		//MathmodRef->RootObjet.CurrentTreestruct.ymin = result.split(";", QString::SkipEmptyParts);

		// ZlimitInf
		//lst = QObj["Zmin"].toArray();
		this->IsoObjet->masterthread->ZlimitInf = Zmin;
		//MathmodRef->RootObjet.CurrentTreestruct.zmin = result.split(";", QString::SkipEmptyParts);

		// Component
		//lst = QObj["Component"].toArray();
		//MathmodRef->RootObjet.CurrentTreestruct.Component = result.split(";", QString::SkipEmptyParts);

		// Name
		//lst = QObj["Name"].toArray();
		//MathmodRef->RootObjet.CurrentTreestruct.name = result.split(";", QString::SkipEmptyParts);

		//MathmodRef->RootObjet.CurrentTreestruct.text = text;

		
		/// process the new surface
		
		{
			//if (MathmodRef->RootObjet.CurrentTreestruct.fxyz.count() > 0)
			//	this->ProcessNewIsoSurface();
		}
	}
}
static uint TypeDrawin = 10;
static uint TypeDrawinNormStep = 4;
//on_updateButton_clicked
void MathMod::ProcessNewIsoSurface(std::vector<Base::Vector3d> &Points, std::vector<Data::ComplexGeoData::Facet> &Facets, double &maxf)
{
	{
		IsoObjet->masterthread->ParserIso();
		IsoObjet->ThreadParsersCopy();
		//int result = ParseIso();
		//if (result == -1) return;
		this->oPara->objectproperties.typedrawing = 1;
		this->IsoObjet->LocalScene = &this->oPara->objectproperties;
		//connect((ui.glWidget)->IsoObjetThread->IsoObjet, SIGNAL(finished()), (ui.glWidget), SLOT(UpdateGL()), Qt::UniqueConnection);
		this->IsoObjet->run();
	}
	double p[3];
	{
		unsigned int i, index[3];
		// save vertices:
		for (i = 0; i< oPara->objectproperties.VertxNumber; i++)
		{
			p[0] = oPara->objectproperties.ArrayNorVer_localPt[TypeDrawin*i + 3 + TypeDrawinNormStep];
			p[1] = oPara->objectproperties.ArrayNorVer_localPt[TypeDrawin*i + 4 + TypeDrawinNormStep];
			p[2] = oPara->objectproperties.ArrayNorVer_localPt[TypeDrawin*i + 5 + TypeDrawinNormStep];
			maxf = fmax(maxf, fmax(fabs(p[0]), fmax(fabs(p[1]), fabs(p[2]))));
			Points.push_back(Base::Vector3d(p[0], p[1], p[2]));
		}
		for (i = 0; i < oPara->objectproperties.PolyNumber; i += 3)
		{

			index[0] = oPara->objectproperties.PolyIndices_localPt[i];// +1;
			index[1] = oPara->objectproperties.PolyIndices_localPt[i + 1];// +1;
			index[2] = oPara->objectproperties.PolyIndices_localPt[i + 2];// +1;
			Data::ComplexGeoData::Facet face;
			if (index[0] * index[1] * index[2] <= 0)
				;
			face.I1 = index[2];
			face.I2 = index[1];
			face.I3 = index[0];
			Facets.push_back(face);
		}
	}
}