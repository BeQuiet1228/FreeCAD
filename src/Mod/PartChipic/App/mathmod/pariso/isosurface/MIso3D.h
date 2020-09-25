#ifndef _MISO_3D_H_
#define _MISO_3D_H_
/***************************************************************************
 *   Copyright (C) 2019 by Abderrahman Taha                                *
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

#include <iostream>
#include <string.h>
#include <cmath>
#include "../objectparameters.h"


/*


                     4.-----------4----------------.5
                     /|                                     /|
                    7 |                                 5 |
                   /  |                                  /  |
                 7.---|-----------6------------.6  |
                  |   |                                 |   |
                  |   8                               |   9
                  |   |                                 |   |
                  |   ^ j                               |   |
               11   |                               10   |
                  |   |     i                           |   |
                  |  0.----->-----0------------|---.1
                  |  /                                  |  /
                  | 3 k                               | 1
                  |/                                    |/
                 3.---------------2------------.2
*/


class IsoWorkerThread
{
public :
    FunctionParser *implicitFunctionParser, *Fct;
    uint   Xgrid, Ygrid, Zgrid;
    uint iStart, iFinish;
    int morph_activated;
	uint maximumgrid, Nb_newvariables, MyIndex;// , WorkerThreadsNumber;
    double stepMorph, pace;
    double *xLocal2, *yLocal2, *zLocal2;
    double *vr2;
    ErrorMessage stdError;
    unsigned int NbPolygn, NbPolygnNbVertex[2];
    bool StopCalculations, ParsersAllocated;
    int signalVal;
public :
    void IsoCompute();
    void VoxelEvaluation();
    void AllocateParsersForWorkerThread(int,int);
    void DeleteWorkerParsers();
    void IsoWorkerTable();
    void run();
    IsoWorkerThread();
	~IsoWorkerThread();
};

class IsoMasterThread : public IsoWorkerThread
{
public :
    FunctionParser *IsoConditionParser, Cstparser, *RgbtParser, *VRgbtParser, *GradientParser, *NoiseParser,
                   *xSupParser, *xInfParser,
                   *ySupParser, *yInfParser,
                   *zSupParser, *zInfParser,
                   *Var;
    std::string ImplicitFunction, Condition,
        XlimitSup, XlimitInf,
        YlimitSup, YlimitInf,
        ZlimitSup, ZlimitInf, Grid,
        Const, *Consts, *ConstNames,
        *SliderNames,
        Varu, *Varus, *VarName,
        Funct,*Functs, *FunctNames,
        Rgbt, *Rgbts, *RgbtNames,
        VRgbt, *VRgbts, *VRgbtNames,
        Gradient, Noise, varliste;
    int IsoConditionRequired, Nb_Sliders,
        ImplicitFunctionSize, ConditionSize, ConstSize, VaruSize, FunctSize, RgbtSize, VRgbtSize;
    uint Nb_rgbts, Nb_vrgbts, Nb_constants, Nb_implicitfunctions, Nb_functs;
    double *ConstValues, *SliderValues;
    double *x_Step, *y_Step, *z_Step;
    int *GridTable;
    double Octaves, Lacunarity, Gain;
    ImplicitStructure *ImplicitStructs;
    bool *UsedFunct, *UsedFunct2;
public :
    void DeleteMasterParsers();
    void AllocateMasterParsers();
    void InitMasterParsers();
    inline ErrorMessage ParseExpression(std::string);
    uint HowManyIsosurface(std::string,uint);
    uint HowManyVariables(std::string, uint);
    ErrorMessage ParserIso();
    void IsoMasterTable();
    void initparser();
    IsoMasterThread();
    ~IsoMasterThread();
};

class MIso3D
{
public :
    ObjectProperties *LocalScene;
    //IsoWorkerThread *workerthreads;
    IsoMasterThread *masterthread;
    uint   Xgrid, Ygrid, Zgrid;
    //uint WorkerThreadsNumber;
    uint   *     IsoSurfaceTriangleListe;
    bool *     PointVerifyCond, StopCalculations;
    int *     TypeIsoSurfaceTriangleListeCND;
    //unsigned int *  IndexPolyTab;
    uint NbTriangleIsoSurface,NbPointIsoMap;
    ScriptErrorType messageerror;
    QString message;
public :
    MIso3D(uint, uint,
          uint gridmax=NbMaxGrid,
          uint NbCmp=NbComponent,
          uint NbVar=NbVariables,
          uint NbCst=NbConstantes,
          uint NbdeFct=NbDefinedFunctions,
          uint NbText=NbTextures,
          int nbSlid=NbSliders,
          int nbSlidV=NbSliderValues,
          uint nbThreads=6,
          uint nbGrid=20,
          uint factX=4,
          uint factY=4,
          uint factZ=4);
    ~MIso3D();
    inline   void SignatureComputation();
    inline   uint ConstructIsoSurface();
    inline   void ConstructIsoNormale();
    inline   uint PointEdgeComputation();
    inline uint CNDCalculation(uint &, struct ComponentInfos *);
    void IsoBuild(float *, unsigned int *, unsigned int *,unsigned  int *, unsigned int *,unsigned  int *, struct ComponentInfos *, int *, bool *);
    void SaveIsoGLMap();
    uint SetMiniMmeshStruct();
    uint CNDtoUse(uint index, struct ComponentInfos *components);
    void CalculateColorsPoints(struct ComponentInfos *components);
    void BuildIso();
    void UpdateThredsNumber(uint);
    void stopcalculations(bool);
    void WorkerThreadCopy(IsoWorkerThread *);
    ErrorMessage IsoMorph();
    ErrorMessage parse_expression2();
    ErrorMessage ThreadParsersCopy();
    void ReinitVarTablesWhenMorphActiv(uint);
    void copycomponent(struct ComponentInfos*, struct ComponentInfos*);
    void run();
};

#endif
