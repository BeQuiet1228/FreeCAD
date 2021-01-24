/***************************************************************************
 *   Copyright (C) 2005 by Warp                                            *
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
//==============================
// Function parser v2.7 by Warp
//==============================

// Comment out the following line if your compiler supports the (non-standard)
// asinh, acosh and atanh functions and you want them to be supported. If
// you are not sure, just leave it (those function will then not be supported).
#define NO_ASINH


// Uncomment the following line to disable the eval() function if it could
// be too dangerous in the target application:
//#define DISABLE_EVAL


// Comment this line out if you are not going to use the optimizer and want
// a slightly smaller library. The Optimize() method can still be called,
// but it will not do anything.
// If you are unsure, just leave it. It won't slow down the other parts of
// the library.
#define SUPPORT_OPTIMIZER


//============================================================================

#include "../pm3parser.h"
#include "../defvalue.h"
#include <cstdlib>
#include <cstring>
#include <cctype>
#include <cmath>
#include "../basicstring.h"
#include "../basicmath.h"
//#include <algorithm>
using namespace std;

#ifndef M_PI
#define M_PI 3.1415926535897932384626433832795
#endif
namespace PM3
{
////////////////
namespace
{
// The functions must be in alphabetical order:
    enum OPCODE
    {
        cAbs, cAcos,
#ifndef NO_ASINH
        cAcosh,
#endif
        cAsin,
#ifndef NO_ASINH
        cAsinh,
#endif
        cAtan,
        cAtan2,
#ifndef NO_ASINH
        cAtanh,
#endif
        cCeil, cCos, cCosh, cCot, cCsc,
#ifndef DISABLE_EVAL
        cEval,
#endif
        cExp, cFloor, cIf, cInt, cLog, cLog10, cMax, cMin,cStep,
        cSec, cSin, cSinh, cSqrt, cTan, cTanh,

// These do not need any ordering:
        cImmed, cJump,
        cNeg, cAdd, cSub, cMul, cDiv, cMod, cPow,
        cEqual, cLess, cGreater, cAnd, cOr,

        cDeg, cRad,

        cFCall, cPCall,

#ifdef SUPPORT_OPTIMIZER
        cVar, cDup, cInv,
#endif

        VarBegin
    };

    struct FuncDefinition
    {
        const char* name;
        unsigned nameLength;
        unsigned opcode;
        unsigned params;

        // This is basically strcmp(), but taking 'nameLength' as string
        // length (not ending '\0'):
        bool operator<(const FuncDefinition& rhs) const
        {
            for(unsigned i = 0; i < nameLength; ++i)
            {
                if(i == rhs.nameLength) return false;
                const char c1 = name[i], c2 = rhs.name[i];
                if(c1 < c2) return true;
                if(c2 < c1) return false;
            }
            return nameLength < rhs.nameLength;
        }
    };


// This list must be in alphabetical order:
    const FuncDefinition Functions[]=
    {

        { "abs", 3, cAbs, 1 },
        { "acos", 4, cAcos, 1 },
#ifndef NO_ASINH
        { "acosh", 5, cAcosh, 1 },
#endif
        { "asin", 4, cAsin, 1 },
#ifndef NO_ASINH
        { "asinh", 5, cAsinh, 1 },
#endif
        { "atan", 4, cAtan, 1 },
        { "atan2", 5, cAtan2, 2 },
#ifndef NO_ASINH
        { "atanh", 5, cAtanh, 1 },
#endif
        { "ceil", 4, cCeil, 1 },
        { "cos", 3, cCos, 1 },
        { "cosh", 4, cCosh, 1 },
        { "cot", 3, cCot, 1 },
        { "csc", 3, cCsc, 1 },
#ifndef DISABLE_EVAL
        { "eval", 4, cEval, 0 },
#endif
        { "exp", 3, cExp, 1 },
        { "floor", 5, cFloor, 1 },
        { "if", 2, cIf, 0 },
        { "int", 3, cInt, 1 },
        { "log", 3, cLog, 1 },
        { "log10", 5, cLog10, 1 },
        { "max", 3, cMax, 2 },
        { "min", 3, cMin, 2 },
		{ "step", 3, cStep, 2 },
        { "sec", 3, cSec, 1 },
        { "sin", 3, cSin, 1 },
        { "sinh", 4, cSinh, 1 },
        { "sqrt", 4, cSqrt, 1 },
        { "tan", 3, cTan, 1 },
        { "tanh", 4, cTanh, 1 }
    };

    const unsigned FUNC_AMOUNT = sizeof(Functions)/sizeof(Functions[0]);


    // BCB4 does not implement the standard lower_bound function.
    // This is used instead:
    const FuncDefinition* fp_lower_bound(const FuncDefinition* first,
                                         const FuncDefinition* last,
                                         const FuncDefinition& value)
    {
        while(first < last)
        {
            const FuncDefinition* middle = first+(last-first)/2;
            if(*middle < value) first = middle+1;
            else last = middle;
        }
        return last;
    }


    // Returns a pointer to the FuncDefinition instance which 'name' is
    // the same as the one given by 'F'. If no such function name exists,
    // returns 0.
    inline const FuncDefinition* FindFunction(const char* F)
    {
        FuncDefinition func = { F, 0, 0, 0 };
        while(isalnum(F[func.nameLength])) ++func.nameLength;
        if(func.nameLength)
        {
            const FuncDefinition* found =
                fp_lower_bound(Functions, Functions+FUNC_AMOUNT, func);
            if(found == Functions+FUNC_AMOUNT || func < *found)
                return 0;
            return found;
        }
        return 0;
    }
};


//---------------------------------------------------------------------------
// Copy-on-write method
//---------------------------------------------------------------------------
inline void ExpParser::copyOnWrite()
{
    if(data->referenceCounter > 1)
    {
        Data* oldData = data;
        data = new Data(*oldData);
        --(oldData->referenceCounter);
        data->referenceCounter = 1;
    }
}


//---------------------------------------------------------------------------
// Constructors and destructors
//---------------------------------------------------------------------------
//===========================================================================
ExpParser::ExpParser():
    parseErrorType(FP_NO_ERROR), evalErrorType(0),
    data(new Data)
{
    data->referenceCounter = 1;
    AddConstant("pi", M_PI);
    AddConstant("null", 0);
    AddConstant("NULL", 0);
    AddConstant("x", 0);
    AddConstant("y", 0);
    AddConstant("z", 0);
    AddConstant("r", 0);
    AddConstant("t", 0);
    AddConstant("c", 2.99792458e8);
    AddUnit("mils", "*2.54e-5f");
    AddUnit("mil", "*2.54e-5f");
    AddUnit("inches", "*2.54e-2f");
    AddUnit("feet", "*12.*2.54e-2f");
    AddUnit("foot", "*12.*2.54e-2f");
    AddUnit("km", "*1.E3f");
    AddUnit("m", "*1.f");
    AddUnit("meter", "*1.f");
    //AddUnit("sec", "*1.f");
    AddUnit("second", "*1.f");
    AddUnit("hz", "*1.f");
    AddUnit("a", "*1.f");
    AddUnit("amp", "*1.f");
    AddUnit("volt", "*1.f");
    AddUnit("tesla", "*1.f");
    AddUnit("joule", "*1.f");
    AddUnit("watt", "*1.f");
    AddUnit("rad", "*1.f");//AddUnit("rad", "*pi/180.f");
    AddUnit("radian", "*1.f");//AddUnit("radian", "*pi/180.f");
    AddUnit("cm", "*1.e-2f");
    AddUnit("mm", "*1.e-3f");
    AddUnit("deg", "*pi/180.f");//AddUnit("deg", "*1.f");
    AddUnit("degree", "*pi/180.f");//AddUnit("degree", "*1.f");
    AddUnit("atto", "*1.E-18f");
    AddUnit("femto", "*1.E-15f");
    AddUnit("pico", "*1.E-12f");
    AddUnit("nano", "*1.E-9f");
    AddUnit("micro", "*1.E-6f");
    AddUnit("gauss", "*1.E-4f");
    AddUnit("milli", "*1.E-3f");
    AddUnit("kilo", "*1.E3f");
    AddUnit("kv", "*1.E3f");
    AddUnit("khz", "*1.E3f");
    AddUnit("mega", "*1.E6f");
    AddUnit("mhz", "*1.E6f");
    AddUnit("giga", "*1.E9f");
    AddUnit("ghz", "*1.E9f");
    AddUnit("tera", "*1.E12f");
    AddUnit("thz", "*1.E12f");
    AddUnit("eta", "*1.E15f");
    AddUnit("exa", "*1.E18f");
    //AddUnit("c", "*2.99792458e8f");
    AddUnit("ev", "*1.6021892E-19f");
    AddUnit("kev", "*1.6021892E-16f");
    AddUnit("mev", "*1.6021892E-13f");
    AddUnit("gev", "*1.6021892E-10f");
    AddUnit("kilometer", "*1.E3f");
    AddUnit("kilometers", "*1.E3f");
    AddUnit("kilovolt", "*1.E3f");
    AddUnit("kilovolts", "*1.E3f");
    AddUnit("kilohertz", "*1.E3f");

    AddUnit("s", "*1.f");
    AddUnit("a", "*1.f");
    AddUnit("v", "*1.f");
    AddUnit("t", "*1.f");
    AddUnit("j", "*1.f");
    AddUnit("w", "*1.f");

    AddFunction("nint",nint, 1);
    AddFunction("sign",sign, 1);
	AddFunction("negtive", negtive, 1);
    AddFunction("step",step, 2);
    AddFunction("theta",theta, 1);
    AddFunction("ramp",ramp, 1);
    AddFunction("smooth_ramp",smooth_ramp, 1);
    AddFunction("Max",ramp,2);
    AddFunction("sqrt",fsqrt,1);
    //AddFunction("atan2",atan2, 2);
}

ExpParser::~ExpParser()
{
    if(--(data->referenceCounter) == 0)
    {
        delete data;
    }
}

ExpParser::ExpParser(const ExpParser& cpy):
    parseErrorType(cpy.parseErrorType),
    evalErrorType(cpy.evalErrorType),
    data(cpy.data)
{
    ++(data->referenceCounter);
}

ExpParser& ExpParser::operator=(const ExpParser& cpy)
{
    if(data != cpy.data)
    {
        if(--(data->referenceCounter) == 0) delete data;

        parseErrorType = cpy.parseErrorType;
        evalErrorType = cpy.evalErrorType;
        data = cpy.data;

        ++(data->referenceCounter);
    }

    return *this;
}


ExpParser::Data::Data():
    useDegreeConversion(false),
    ByteCode(0), ByteCodeSize(0),
    Immed(0), ImmedSize(0),
    Stack(0), StackSize(0)
{}

ExpParser::Data::~Data()
{
    if(ByteCode) { delete[] ByteCode; ByteCode=0; }
    if(Immed) { delete[] Immed; Immed=0; }
    if(Stack) { delete[] Stack; Stack=0; }
}

// Makes a deep-copy of Data:
ExpParser::Data::Data(const Data& cpy):
    varAmount(cpy.varAmount), useDegreeConversion(cpy.useDegreeConversion),
    Variables(cpy.Variables), Constants(cpy.Constants),
    FuncPtrNames(cpy.FuncPtrNames), FuncPtrs(cpy.FuncPtrs),
    FuncParserNames(cpy.FuncParserNames), FuncParsers(cpy.FuncParsers),
    ByteCode(0), ByteCodeSize(cpy.ByteCodeSize),
    Immed(0), ImmedSize(cpy.ImmedSize),
    Stack(0), StackSize(cpy.StackSize)
{
    if(ByteCodeSize) ByteCode = new unsigned[ByteCodeSize];
    if(ImmedSize) Immed = new double[ImmedSize];
    if(StackSize) Stack = new double[StackSize];

    for(unsigned i=0; i<ByteCodeSize; ++i) ByteCode[i] = cpy.ByteCode[i];
    for(unsigned i=0; i<ImmedSize; ++i) Immed[i] = cpy.Immed[i];

    // No need to copy the stack contents because it's obsolete outside Eval()
}


//---------------------------------------------------------------------------
// Function parsing
//---------------------------------------------------------------------------
//===========================================================================
namespace
{
    // Error messages returned by ErrorMsg():
    const char* ParseErrorMessage[]=
    {
        "Syntax error",                             // 0
        "Mismatched parenthesis",                   // 1
        "Missing ')'",                              // 2
        "Empty parentheses",                        // 3
        "Syntax error: Operator expected",          // 4
        "Not enough memory",                        // 5
        "An unexpected error ocurred. Please make a full bug report "
        "to warp@iki.fi",                           // 6
        "Syntax error in parameter 'Vars' given to "
        "ExpParser::Parse()",                  // 7
        "Illegal number of parameters to function", // 8
        "Syntax error: Premature end of string",    // 9
        "Syntax error: Expecting ( after function", // 10
        ""
    };


    // Parse variables
    bool ParseVars(const string& Vars, map<string, unsigned>& dest)
    {
        unsigned varNumber = VarBegin;
        unsigned ind1 = 0, ind2;

        while(ind1 < Vars.size())
        {
            if(!isalpha(Vars[ind1]) && Vars[ind1]!='_') return false;
            for(ind2=ind1+1; ind2<Vars.size() && Vars[ind2]!=','; ++ind2)
                if(!isalnum(Vars[ind2]) && Vars[ind2]!='_') return false;
            const string varName = Vars.substr(ind1, ind2-ind1);

            if(dest.insert(make_pair(varName, varNumber++)).second == false)
                return false;

            ind1 = ind2+1;
        }
        return true;
    }
};

bool ExpParser::isValidName(const std::string& name) const
{
    if(name.empty() || (!isalpha(name[0]) && name[0] != '_')) return false;
    for(unsigned i=0; i<name.size(); ++i)
        if(!isalnum(name[i]) && name[i] != '_')
            if(name[i]!='.')
                return false;

    if(FindFunction(name.c_str())) return false;
    //变量名
    //常数名
    return true;
}

// Constants:
bool ExpParser::AddConstant(const string& name, double value)
{
    if(isValidName(name))
    {
        const char* n = name.c_str();
        if(FindVariable(n, data->FuncParserNames) !=
           data->FuncParserNames.end() ||
           FindVariable(n, data->FuncPtrNames) !=
           data->FuncPtrNames.end()||
            FindUnit(n) != data->Units.end()||
           FindDef1DPara(n) != data->Def1DParas.end()
                )
            return false;

        copyOnWrite();

        data->Constants[name] = value;
        return true;
    }
    return false;
}

// Units:
bool ExpParser::AddUnit(const string& name, string value)
{
    if(isValidName(name))
    {
        const char* n = name.c_str();
        if(FindVariable(n, data->FuncParserNames) !=
           data->FuncParserNames.end() ||
           FindVariable(n, data->FuncPtrNames) !=
           data->FuncPtrNames.end()||
           FindConstant(n) != data->Constants.end()||
           FindDef1DPara(n) != data->Def1DParas.end()
                    )
            return false;

        copyOnWrite();

        data->Units[name] = value;
        return true;
    }
    return false;
}

//
bool ExpParser::AddDef1DPara(std::string name0, std::string value0, std::string &er)
{
    PM3::deSpace(name0);
    std::string name = PM3::QStringToStdString(name0);
    if(isValidName(name))
    {
        const char* n = name.c_str();
        if(FindVariable(n, data->FuncParserNames) != data->FuncParserNames.end()) {
           // er = "变量名"+name0+"定义非法, 与函数同名!"; 
			return false;
        }
        if(FindVariable(n, data->FuncPtrNames) != data->FuncPtrNames.end()) {
            //er =("变量名")+name0+("定义非法, 与函数同名!"); 
			return false;
        }
        if(FindConstant(n) != data->Constants.end())  {
            //er =("变量名")+name0+("定义非法, 与常数同名!"); 
			return false;
        }
        if(FindUnit(n) != data->Units.end())  {
           //er = ("变量名")+name0+("定义非法, 与单位同名!"); 
		   return false;
        }
        if(FindDef1DPara(n) != data->Def1DParas.end()) {
            //er = ("变量名")+name0+("定义非法, 变量名已定义!"); 
			return false;
        }
        if(FindDef3DPara(n) != data->Def3DParas.end()){
            //er = ("变量名")+name0+("定义非法, 与点同名!"); 
			return false;
        }
        if(ParseExp(value0, er) >= 0) {
            //er = value0+"定义非法!";
             return false;
        }


        copyOnWrite();        

        data->Def1DParas[name] = PM3::QStringToStdString(value0);
        data->Def1DParasNames.push_back(name);
        return true;
    }

    er = ("变量名定义非法!");
    return false;
}

bool ExpParser::AddDef3DPara(std::string name0, Data::stringlist value0, std::string &er)
 {
     PM3::deSpace(name0);
     //PM3::deSpace(value1);
     std::string name = PM3::QStringToStdString(name0);
     if(isValidName(name))
     {
         const char* n = name.c_str();
         if(FindVariable(n, data->FuncParserNames) != data->FuncParserNames.end()) {
             //er = ("点名")+name0+("定义非法, 与函数同名!"); 
			 return false;
         }
         if(FindVariable(n, data->FuncPtrNames) != data->FuncPtrNames.end()) {
             //er = ("点名")+name0+("定义非法, 与函数同名!"); 
			 return false;
         }
         if(FindConstant(n) != data->Constants.end())  {
             //er = ("点名")+name0+("定义非法, 与常数同名!");
			 return false;
         }
         if(FindUnit(n) != data->Units.end())  {
            //er = ("点名")+name0+("定义非法, 与单位同名!"); 
			return false;
         }
         if(FindDef1DPara(n) != data->Def1DParas.end()) {
             //er = ("点名")+name0+("定义非法, 与变量同名!");
			 return false;
         }
         if(FindDef3DPara(n) != data->Def3DParas.end()){
             //er = ("点名")+name0+("定义非法, 点名已定义!"); 
			 return false;
         }
         std::string value[3];
         value[0] = value0[0];
         value[1] = value0[1];
         value[2] = value0[2];
         if(ParseExp(value[0],er) >= 0){
             //er = "值"+value[0]+"定义非法!";
             return false;
         }
         if(ParseExp(value[1],er) >= 0){
             //er = "值"+value[1]+"定义非法!";
             return false;
         }
         if(ParseExp(value[2],er) >= 0){
             //er = "值"+value[2]+"定义非法!";
             return false;
         }

         copyOnWrite();
         value0[0] = PM3::QStringToStdString(value[0]);
         value0[1] = PM3::QStringToStdString(value[1]);
         value0[2] = PM3::QStringToStdString(value[2]);
         data->Def3DParas[name] = value0;
         data->Def3DParasNames.push_back(name);
         return true;
     }
     er = ("点名定义非法!");
     return false;
 }
// Function pointers
bool ExpParser::AddFunction(const std::string& name,
                                 FunctionPtr func, unsigned paramsAmount)
{
    if(paramsAmount == 0) return false; // Currently must be at least one

    if(isValidName(name))
    {
        const char* n = name.c_str();
        if(FindVariable(n, data->FuncParserNames) !=
           data->FuncParserNames.end() ||
           FindConstant(n) != data->Constants.end() ||
                FindConstant(n) != data->Constants.end()||
                FindDef1DPara(n) != data->Def1DParas.end()||
                FindUnit(n) != data->Units.end()  ||
                FindDef1DPara(n) != data->Def1DParas.end()||
                FindDef3DPara(n) != data->Def3DParas.end()
                )
            return false;

        copyOnWrite();

        data->FuncPtrNames[name] = data->FuncPtrs.size();
        data->FuncPtrs.push_back(Data::FuncPtrData(func, paramsAmount));
        return true;
    }
    return false;
}

bool ExpParser::checkRecursiveLinking(const ExpParser* fp) const
{
    if(fp == this) return true;
    for(unsigned i=0; i<fp->data->FuncParsers.size(); ++i)
        if(checkRecursiveLinking(fp->data->FuncParsers[i])) return true;
    return false;
}

bool ExpParser::AddFunction(const std::string& name,
                                 ExpParser& parser)
{
    if(parser.data->varAmount == 0) // Currently must be at least one
        return false;

    if(isValidName(name))
    {
        const char* n = name.c_str();
        if(FindVariable(n, data->FuncPtrNames) != data->FuncPtrNames.end() ||
           FindConstant(n) != data->Constants.end())
            return false;

        if(checkRecursiveLinking(&parser)) return false;

        copyOnWrite();

        data->FuncParserNames[name] = data->FuncParsers.size();
        data->FuncParsers.push_back(&parser);
        return true;
    }
    return false;
}

bool ExpParser::getUpdate(DefValue1D &in)
{
    if((in.selfDefName != "-1")&&(in.selfDefName != "NULL"))
    {
        ExpParser::Data::Def1DMap_t::const_iterator iter =
                data->Def1DParas.find(PM3::QStringToStdString(in.selfDefName));
        if(iter != data->Def1DParas.end())
        {
            in.value = PM3::StdStringToQString(iter->second);
        }
        else
            return false;
    }
    return true;
}

bool ExpParser::getUpdate(DefValue3D &in)
{
    if((in.selfDefName != "-1")&&(in.selfDefName != "NULL"))
    {
        ExpParser::Data::Def3DMap_t::const_iterator iter =
                data->Def3DParas.find(PM3::QStringToStdString(in.selfDefName));
        if(iter != data->Def3DParas.end())
        {
            in.value[0] = PM3::StdStringToQString(iter->second[0]);
            in.value[1] = PM3::StdStringToQString(iter->second[1]);
            in.value[2] = PM3::StdStringToQString(iter->second[2]);
        }
        else
            return false;
    }
    return true;
}

// 解析无变量的表达式
// 如果成功将去掉所有空格---------------------
//返回:-1 成功
//     >=0：错误
//
int ExpParser::ParseExp(std::string& Functionin, std::string &er, const std::string& Vars,
                          bool useDegrees)
{

    copyOnWrite();
	std::string Function = Functionin;//.toLower();
    PM3::deSpace(Function);

    data->Variables.clear();

    if(!ParseVars(Vars, data->Variables))
    {
        parseErrorType = INVALID_VARS;
        //er =("非法的函数变量定义,只支持x,y,z,t!");
        return Function.size();
    }
    data->varAmount = 0;//data->Variables.size(); // this is for Eval()

    parseErrorType = FP_NO_ERROR;
    std::string ex = Function;
    int Result = CheckSyntaxExp(ex);
    if(Result>=0)   {
       // er += ("表达式")+Functionin+("定义错误!");
        return Result;
    }

    const char* Func = ex.c_str();
    data->useDegreeConversion = useDegrees;
    if(!Compile(Func)) {
        //er += ("表达式")+Functionin+("定义错误!");
        return Function.size();
    }

    data->Variables.clear();

    parseErrorType = FP_NO_ERROR;

    Functionin = Function;//如果成功将返回去掉所有空格的正规表达式
    return -1;
}
// Main parsing function
// ---------------------
int ExpParser::Parse(const std::string& Function,
                          const std::string& Vars,
                          bool useDegrees)
{
    copyOnWrite();

    data->Variables.clear();

    if(!ParseVars(Vars, data->Variables))
    {
        parseErrorType = INVALID_VARS;
        return Function.size();
    }
    data->varAmount = data->Variables.size(); // this is for Eval()

    const char* Func = Function.c_str();

    parseErrorType = FP_NO_ERROR;

    int Result = CheckSyntax(Func);
    if(Result>=0) return Result;

    data->useDegreeConversion = useDegrees;
    if(!Compile(Func)) return Function.size();

    data->Variables.clear();

    parseErrorType = FP_NO_ERROR;
    return -1;
}

namespace
{
    // Is given char an operator?
    inline bool IsOperator(int c)
    {
        return strchr("+-*/%^=<>&|",c)!=NULL;
    }

    // skip whitespace
    inline void sws(const char* F, int& Ind)
    {
        while(F[Ind] && isspace(F[Ind])) ++Ind;
    }
};

// Returns an iterator to the variable with the same name as 'F', or to
// Variables.end() if no such variable exists:
inline ExpParser::Data::VarMap_t::const_iterator
ExpParser::FindVariable(const char* F, const Data::VarMap_t& vars) const
{
    if(vars.size())
    {
        unsigned ind = 0;
        while(isalnum(F[ind]) || F[ind] == '_') ++ind;
        if(ind)
        {
            string name(F, ind);
            return vars.find(name);
        }
    }
    return vars.end();
}

inline ExpParser::Data::ConstMap_t::const_iterator
ExpParser::FindConstant(const char* F) const
{
    if(data->Constants.size())
    {
        unsigned ind = 0;
        while(isalnum(F[ind]) || F[ind] == '_') ++ind;
        if(ind)
        {
            string name(F, ind);
            return data->Constants.find(name);
        }
    }
    return data->Constants.end();
}
inline ExpParser::Data::UnitMap_t::const_iterator
ExpParser::FindUnit(const char* F) const
{
    if(data->Units.size())
    {
        unsigned ind = 0;
        while(isalnum(F[ind]) || F[ind] == '_') ++ind;
        if(ind)
        {
            string name(F, ind);
            return data->Units.find(name);
        }
    }
    return data->Units.end();
}
inline ExpParser::Data::Def1DMap_t::const_iterator
ExpParser::FindDef1DPara(const char* F) const
{
    if(data->Def1DParas.size())
    {
        unsigned ind = 0;
        while(isalnum(F[ind]) || F[ind] == '_'||F[ind]=='.') ++ind;
        if(ind)
        {
            string name(F, ind);
            return data->Def1DParas.find(name);
        }
    }
    return data->Def1DParas.end();
}

inline ExpParser::Data::Def3DMap_t::const_iterator
ExpParser::FindDef3DPara(const char* F) const
{
    if(data->Def3DParas.size())
    {
        unsigned ind = 0;
        while(isalnum(F[ind]) || F[ind] == '_') ++ind;
        if(ind)
        {
            string name(F, ind);
            return data->Def3DParas.find(name);
        }
    }
    return data->Def3DParas.end();
}
//---------------------------------------------------------------------------
// Check function string syntax
// ----------------------------
int ExpParser::CheckSyntax(const char* Function)
{
    const Data::VarMap_t& Variables = data->Variables;
    const Data::ConstMap_t& Constants = data->Constants;
    const Data::UnitMap_t& Units = data->Units;
    const Data::VarMap_t& FuncPtrNames = data->FuncPtrNames;
    const Data::VarMap_t& FuncParserNames = data->FuncParserNames;

    vector<int> functionParenthDepth;

    int Ind=0, ParenthCnt=0;
    char c;
    char* Ptr;

    while(true)
    {
        sws(Function, Ind);
        c=Function[Ind];

// Check for valid operand (must appear)

        // Check for leading -
        if(c=='-') { sws(Function, ++Ind); c=Function[Ind]; }
        if(c==0) { parseErrorType=PREMATURE_EOS; return Ind; }

        // Check for math function
        bool foundFunc = false;
        const FuncDefinition* fptr = FindFunction(&Function[Ind]);
        if(fptr)
        {
            Ind += fptr->nameLength;
            foundFunc = true;
        }
        else
        {
            // Check for user-defined function
            Data::VarMap_t::const_iterator fIter =
                FindVariable(&Function[Ind], FuncPtrNames);
            if(fIter != FuncPtrNames.end())
            {
                Ind += fIter->first.size();
                foundFunc = true;
            }
            else
            {
                Data::VarMap_t::const_iterator pIter =
                    FindVariable(&Function[Ind], FuncParserNames);
                if(pIter != FuncParserNames.end())
                {
                    Ind += pIter->first.size();
                    foundFunc = true;
                }
            }
        }

        if(foundFunc)
        {
            sws(Function, Ind);
            c = Function[Ind];
            if(c!='(') { parseErrorType=EXPECT_PARENTH_FUNC; return Ind; }
            functionParenthDepth.push_back(ParenthCnt+1);
        }

        // Check for opening parenthesis
        if(c=='(')
        {
            ++ParenthCnt;
            sws(Function, ++Ind);
            if(Function[Ind]==')') { parseErrorType=EMPTY_PARENTH; return Ind;}
            continue;
        }

        // Check for number
        if(isdigit(c) || (c=='.' && isdigit(Function[Ind+1])))
        {
            strtod(&Function[Ind], &Ptr);
            Ind += int(Ptr-&Function[Ind]);
            sws(Function, Ind);
            c = Function[Ind];
        }
        else
        { // Check for variable
            Data::VarMap_t::const_iterator vIter =
                FindVariable(&Function[Ind], Variables);
            if(vIter != Variables.end())
                Ind += vIter->first.size();
            else
            {
                // Check for constant
                Data::ConstMap_t::const_iterator cIter =
                    FindConstant(&Function[Ind]);
                if(cIter != Constants.end())
                    Ind += cIter->first.size();
                else
                { parseErrorType=SYNTAX_ERROR; return Ind; }
            }
            sws(Function, Ind);
            c = Function[Ind];
        }

        // Check for closing parenthesis
        while(c==')')
        {
            if(functionParenthDepth.size() &&
               functionParenthDepth.back() == ParenthCnt)
                functionParenthDepth.pop_back();
            if((--ParenthCnt)<0) { parseErrorType=MISM_PARENTH; return Ind; }
            sws(Function, ++Ind);
            c=Function[Ind];
        }

// If we get here, we have a legal operand and now a legal operator or
// end of string must follow

        // Check for EOS
        if(c==0) break; // The only way to end the checking loop without error
        // Check for operator
        if(!IsOperator(c) &&
           (c != ',' || functionParenthDepth.empty() ||
            functionParenthDepth.back() != ParenthCnt))
        {
            //解析单位
            // Check for constant
            Data::UnitMap_t::const_iterator cIter =
                FindUnit(&Function[Ind]);
            if(cIter != Units.end())
                Ind += cIter->first.size();
            else {
                parseErrorType=EXPECT_OPERATOR;
                return Ind;
            }
            sws(Function, Ind);
            c = Function[Ind];
            if(c==0) break;
        }

// If we get here, we have an operand and an operator; the next loop will
// check for another operand (must appear)
        ++Ind;
    } // while

    // Check that all opened parentheses are also closed
    if(ParenthCnt>0) { parseErrorType=MISSING_PARENTH; return Ind; }

// The string is ok
    parseErrorType=FP_NO_ERROR;
    return -1;
}

//---------------------------------------------------------------------------
// Check function string syntax
// ----------------------------
int ExpParser::CheckSyntaxExp( std::string &ex)//CheckSyntax(const char* Function)
{
    const Data::VarMap_t& Variables = data->Variables;
    const Data::ConstMap_t& Constants = data->Constants;
    const Data::UnitMap_t& Units = data->Units;
    const Data::Def1DMap_t& Def1DParas = data->Def1DParas;
    const Data::VarMap_t& FuncPtrNames = data->FuncPtrNames;
    const Data::VarMap_t& FuncParserNames = data->FuncParserNames;
    vector<int> functionParenthDepth;

    int Ind=0, ParenthCnt=0;
    char c;
    char* Ptr;

    while(true)
    {
        std::string reexp(ex);
        char* Function = (char*)reexp.c_str();
        sws(Function, Ind);
        c=Function[Ind];

// Check for valid operand (must appear)

        // Check for leading -
        if(c=='-') { sws(Function, ++Ind); c=Function[Ind]; }
        if(c==0) { parseErrorType=PREMATURE_EOS; return Ind; }

        // Check for math function
        bool foundFunc = false;
        const FuncDefinition* fptr = FindFunction(&Function[Ind]);
        if(fptr)
        {
            Ind += fptr->nameLength;
            foundFunc = true;
        }
        else
        {
            // Check for user-defined function
            Data::VarMap_t::const_iterator fIter =
                FindVariable(&Function[Ind], FuncPtrNames);
            if(fIter != FuncPtrNames.end())
            {
                Ind += fIter->first.size();
                foundFunc = true;
            }
            else
            {
                Data::VarMap_t::const_iterator pIter =
                    FindVariable(&Function[Ind], FuncParserNames);
                if(pIter != FuncParserNames.end())
                {
                    Ind += pIter->first.size();
                    foundFunc = true;
                }
            }
        }

        if(foundFunc)
        {
            sws(Function, Ind);
            c = Function[Ind];
            if(c!='(') { parseErrorType=EXPECT_PARENTH_FUNC; return Ind; }
            functionParenthDepth.push_back(ParenthCnt+1);
        }

        // Check for opening parenthesis
        if(c=='(')
        {
            ++ParenthCnt;
            sws(Function, ++Ind);
            if(Function[Ind]==')') { parseErrorType=EMPTY_PARENTH; return Ind;}
            continue;
        }

        // Check for number
        if(isdigit(c)|| (c=='.' && isdigit(Function[Ind+1])))
        {
            strtod(&Function[Ind], &Ptr);
            Ind += int(Ptr-&Function[Ind]);
            sws(Function, Ind);
            c = Function[Ind];
        }
        else
        { // Check for variable
            Data::VarMap_t::const_iterator vIter =
                FindVariable(&Function[Ind], Variables);
            if(vIter != Variables.end())
                Ind += vIter->first.size();
            else
            {
                // Check for constant
                Data::ConstMap_t::const_iterator cIter =
                    FindConstant(&Function[Ind]);
                if(cIter != Constants.end())
                    Ind += cIter->first.size();
                else
                {
                    // Check for constant
                    Data::Def1DMap_t::const_iterator cIter =
                        FindDef1DPara(&Function[Ind]);
                    if(cIter != Def1DParas.end())
                    {
                        std::string text =  cIter->second;
                        std::string temp;
                        int i =text.find('-');
                        if(text.find('+')==std::string::npos&&text.find('-')==std::string::npos)  //参数修改
                        {
                            temp=cIter->second;
                        }else{
                            temp="("+cIter->second+")";
                        }
                        reexp.replace(Ind, cIter->first.size(),temp, 0, temp.size());//
                        //reexp.replace(Ind, cIter->first.size(),cIter->second, 0, cIter->second.size());//
                        Function = (char*)reexp.c_str();
                        Ind = 0;
                        ParenthCnt = 0;
                        functionParenthDepth.clear();
                        ex = reexp;
                        continue;
                        //Ind += cIter->first.size();
                    }
                    else {
                        parseErrorType=SYNTAX_ERROR; return Ind;
                    }
                }
            }
            sws(Function, Ind);
            c = Function[Ind];
        }

        // Check for closing parenthesis
        while(c==')')
        {
            if(functionParenthDepth.size() &&
               functionParenthDepth.back() == ParenthCnt)
                functionParenthDepth.pop_back();
            if((--ParenthCnt)<0) { parseErrorType=MISM_PARENTH; return Ind; }
            sws(Function, ++Ind);
            c=Function[Ind];
        }

// If we get here, we have a legal operand and now a legal operator or
// end of string must follow

        // Check for EOS
        if(c==0) break; // The only way to end the checking loop without error
        // Check for operator
        if(!IsOperator(c) &&
           (c != ',' || functionParenthDepth.empty() ||
            functionParenthDepth.back() != ParenthCnt))
        {
            //解析单位
            // Check for constant
            Data::UnitMap_t::const_iterator cIter =
                FindUnit(&Function[Ind]);
            if(cIter != Units.end())
            {
                //std::string temp="("+cIter->second+")";
                //reexp.replace(Ind, cIter->first.size(),temp, 0, temp.size());//
                reexp.replace(Ind, cIter->first.size(),cIter->second, 0, cIter->second.size()-1);//
                Function = (char*)reexp.c_str();
                Ind = 0;
                ParenthCnt = 0;
                functionParenthDepth.clear();
                ex = reexp;
                continue;
                //Ind += cIter->first.size();
            }
            else {
                if(ex.size())
                {
                    for(Ind = 0;Ind<ex.size();Ind++)
                    {
                        if(!isdigit(Function[Ind]))
                        {
                            Data::Def1DMap_t::const_iterator cIter =
                                FindDef1DPara(&Function[Ind]);
                            if(cIter != Def1DParas.end())
                            {
                                std::string text = ex.substr(0,Ind);
                                text = text + "*("+cIter->second+")";
                                ex = text;
                                break;
                             //  return -1;
                            }else{
                                parseErrorType=EXPECT_OPERATOR;
                                return 1;
                            }
                        }
                    }
                }else
                {
                    parseErrorType=EXPECT_OPERATOR;
                    return 1;
                }



            }
            sws(Function, Ind);
            c = Function[Ind];
            if(c==0) break;
        }

// If we get here, we have an operand and an operator; the next loop will
// check for another operand (must appear)
        ++Ind;
    } // while

    // Check that all opened parentheses are also closed
    if(ParenthCnt>0) { parseErrorType=MISSING_PARENTH; return Ind; }

// The string is ok
    parseErrorType=FP_NO_ERROR;
    return -1;
}
// Compile function string to bytecode
// -----------------------------------
bool ExpParser::Compile(const char* Function)
{
    if(data->ByteCode) { delete[] data->ByteCode; data->ByteCode=0; }
    if(data->Immed) { delete[] data->Immed; data->Immed=0; }
    if(data->Stack) { delete[] data->Stack; data->Stack=0; }

    vector<unsigned> byteCode; byteCode.reserve(1024);
    tempByteCode = &byteCode;

    vector<double> immed; immed.reserve(1024);
    tempImmed = &immed;

    data->StackSize = StackPtr = 0;

    CompileExpression(Function, 0);
    if(parseErrorType != FP_NO_ERROR) return false;

    data->ByteCodeSize = byteCode.size();
    data->ImmedSize = immed.size();

    if(data->ByteCodeSize)
    {
        data->ByteCode = new unsigned[data->ByteCodeSize];
        memcpy(data->ByteCode, &byteCode[0],
               sizeof(unsigned)*data->ByteCodeSize);
    }
    if(data->ImmedSize)
    {
        data->Immed = new double[data->ImmedSize];
        memcpy(data->Immed, &immed[0],
               sizeof(double)*data->ImmedSize);
    }
    if(data->StackSize)
        data->Stack = new double[data->StackSize];

    return true;
}


inline void ExpParser::AddCompiledByte(unsigned c)
{
    tempByteCode->push_back(c);
}

inline void ExpParser::AddImmediate(double i)
{
    tempImmed->push_back(i);
}

inline void ExpParser::AddFunctionOpcode(unsigned opcode)
{
    if(data->useDegreeConversion)
        switch(opcode)
        {
          case cCos:
          case cCosh:
          case cCot:
          case cCsc:
          case cSec:
          case cSin:
          case cSinh:
          case cTan:
          case cTanh:
              AddCompiledByte(cRad);
        }

    AddCompiledByte(opcode);

    if(data->useDegreeConversion)
        switch(opcode)
        {
          case cAcos:
#ifndef NO_ASINH
          case cAcosh:
          case cAsinh:
          case cAtanh:
#endif
          case cAsin:
          case cAtan:
          case cAtan2:
              AddCompiledByte(cDeg);
        }
}

inline void ExpParser::incStackPtr()
{
    if(++StackPtr > data->StackSize) ++(data->StackSize);
}


// Compile if()
int ExpParser::CompileIf(const char* F, int ind)
{
    int ind2 = CompileExpression(F, ind, true); // condition
    sws(F, ind2);
    if(F[ind2] != ',') { parseErrorType=ILL_PARAMS_AMOUNT; return ind2; }
    AddCompiledByte(cIf);
    unsigned curByteCodeSize = tempByteCode->size();
    AddCompiledByte(0); // Jump index; to be set later
    AddCompiledByte(0); // Immed jump index; to be set later

    --StackPtr;

    ind2 = CompileExpression(F, ind2+1, true); // then
    sws(F, ind2);
    if(F[ind2] != ',') { parseErrorType=ILL_PARAMS_AMOUNT; return ind2; }
    AddCompiledByte(cJump);
    unsigned curByteCodeSize2 = tempByteCode->size();
    unsigned curImmedSize2 = tempImmed->size();
    AddCompiledByte(0); // Jump index; to be set later
    AddCompiledByte(0); // Immed jump index; to be set later

    --StackPtr;

    ind2 = CompileExpression(F, ind2+1, true); // else
    sws(F, ind2);
    if(F[ind2] != ')') { parseErrorType=ILL_PARAMS_AMOUNT; return ind2; }

    // Set jump indices
    (*tempByteCode)[curByteCodeSize] = curByteCodeSize2+1;
    (*tempByteCode)[curByteCodeSize+1] = curImmedSize2;
    (*tempByteCode)[curByteCodeSize2] = tempByteCode->size()-1;
    (*tempByteCode)[curByteCodeSize2+1] = tempImmed->size();

    return ind2+1;
}

int ExpParser::CompileFunctionParams(const char* F, int ind,
                                          unsigned requiredParams)
{
    unsigned curStackPtr = StackPtr;
    int ind2 = CompileExpression(F, ind);

    if(StackPtr != curStackPtr+requiredParams)
    { parseErrorType=ILL_PARAMS_AMOUNT; return ind; }

    StackPtr -= requiredParams - 1;
    sws(F, ind2);
    return ind2+1; // F[ind2] is ')'
}

// Compiles element
int ExpParser::CompileElement(const char* F, int ind)
{
    sws(F, ind);
    char c = F[ind];

    if(c == '(')
    {
        ind = CompileExpression(F, ind+1);
        sws(F, ind);
        return ind+1; // F[ind] is ')'
    }

    if(isdigit(c) || c=='.' /*|| c=='-'*/) // Number
    {
        const char* startPtr = &F[ind];
        char* endPtr;
        double val = strtod(startPtr, &endPtr);
        AddImmediate(val);
        AddCompiledByte(cImmed);
        incStackPtr();
        return ind+(endPtr-startPtr);
    }

    if(isalpha(c) || c == '_') // Function, variable or constant
    {
        const FuncDefinition* func = FindFunction(F+ind);
        if(func) // is function
        {
            int ind2 = ind + func->nameLength;
            sws(F, ind2); // F[ind2] is '('
            if(strcmp(func->name, "if") == 0) // "if" is a special case
            {
                return CompileIf(F, ind2+1);
            }

#ifndef DISABLE_EVAL
            unsigned requiredParams =
                strcmp(func->name, "eval") == 0 ?
                data->Variables.size() : func->params;
#else
            unsigned requiredParams = func->params;
#endif
            ind2 = CompileFunctionParams(F, ind2+1, requiredParams);
            AddFunctionOpcode(func->opcode);
            return ind2; // F[ind2-1] is ')'
        }

        Data::VarMap_t::const_iterator vIter =
            FindVariable(F+ind, data->Variables);
        if(vIter != data->Variables.end()) // is variable
        {
            AddCompiledByte(vIter->second);
            incStackPtr();
            return ind + vIter->first.size();
        }

        Data::ConstMap_t::const_iterator cIter = FindConstant(F+ind);
        if(cIter != data->Constants.end()) // is constant
        {
            AddImmediate(cIter->second);
            AddCompiledByte(cImmed);
            incStackPtr();
            return ind + cIter->first.size();
        }

        Data::VarMap_t::const_iterator fIter =
            FindVariable(F+ind, data->FuncPtrNames);
        if(fIter != data->FuncPtrNames.end()) // is user-defined func pointer
        {
            unsigned index = fIter->second;

            int ind2 = ind + fIter->first.length();
            sws(F, ind2); // F[ind2] is '('

            ind2 = CompileFunctionParams(F, ind2+1,
                                         data->FuncPtrs[index].params);

            AddCompiledByte(cFCall);
            AddCompiledByte(index);
            return ind2;
        }

        Data::VarMap_t::const_iterator pIter =
            FindVariable(F+ind, data->FuncParserNames);
        if(pIter != data->FuncParserNames.end()) // is user-defined func parser
        {
            unsigned index = pIter->second;

            int ind2 = ind + pIter->first.length();
            sws(F, ind2); // F[ind2] is '('

            ind2 = CompileFunctionParams
                (F, ind2+1, data->FuncParsers[index]->data->varAmount);

            AddCompiledByte(cPCall);
            AddCompiledByte(index);
            return ind2;
        }
    }

    parseErrorType = UNEXPECTED_ERROR;
    return ind;
}

// Compiles '^'
int ExpParser::CompilePow(const char* F, int ind)
{
    int ind2 = CompileElement(F, ind);
    sws(F, ind2);

    while(F[ind2] == '^')
    {
        ind2 = CompileUnaryMinus(F, ind2+1);
        sws(F, ind2);
        AddCompiledByte(cPow);
        --StackPtr;
    }

    return ind2;
}

// Compiles unary '-'
int ExpParser::CompileUnaryMinus(const char* F, int ind)
{
    sws(F, ind);
    if(F[ind] == '-')
    {
        int ind2 = ind+1;
        sws(F, ind2);
        ind2 = CompilePow(F, ind2);
        sws(F, ind2);

        // if we are negating a constant, negate the constant itself:
        if(tempByteCode->back() == cImmed)
            tempImmed->back() = -tempImmed->back();

        // if we are negating a negation, we can remove both:
        else if(tempByteCode->back() == cNeg)
            tempByteCode->pop_back();

        else
            AddCompiledByte(cNeg);

        return ind2;
    }

    int ind2 = CompilePow(F, ind);
    sws(F, ind2);
    return ind2;
}

// Compiles '*', '/' and '%'
int ExpParser::CompileMult(const char* F, int ind)
{
    int ind2 = CompileUnaryMinus(F, ind);
    sws(F, ind2);
    char op;

    while((op = F[ind2]) == '*' || op == '/' || op == '%')
    {
        ind2 = CompileUnaryMinus(F, ind2+1);
        sws(F, ind2);
        switch(op)
        {
          case '*': AddCompiledByte(cMul); break;
          case '/': AddCompiledByte(cDiv); break;
          case '%': AddCompiledByte(cMod); break;
        }
        --StackPtr;
    }

    return ind2;
}

// Compiles '+' and '-'
int ExpParser::CompileAddition(const char* F, int ind)
{
    int ind2 = CompileMult(F, ind);
    sws(F, ind2);
    char op;

    while((op = F[ind2]) == '+' || op == '-')
    {
        ind2 = CompileMult(F, ind2+1);
        sws(F, ind2);
        AddCompiledByte(op=='+' ? cAdd : cSub);
        --StackPtr;
    }

    return ind2;
}

// Compiles '=', '<' and '>'
int ExpParser::CompileComparison(const char* F, int ind)
{
    int ind2 = CompileAddition(F, ind);
    sws(F, ind2);
    char op;

    while((op = F[ind2]) == '=' || op == '<' || op == '>')
    {
        ind2 = CompileAddition(F, ind2+1);
        sws(F, ind2);
        switch(op)
        {
          case '=': AddCompiledByte(cEqual); break;
          case '<': AddCompiledByte(cLess); break;
          case '>': AddCompiledByte(cGreater); break;
        }
        --StackPtr;
    }

    return ind2;
}

// Compiles '&'
int ExpParser::CompileAnd(const char* F, int ind)
{
    int ind2 = CompileComparison(F, ind);
    sws(F, ind2);

    while(F[ind2] == '&')
    {
        ind2 = CompileComparison(F, ind2+1);
        sws(F, ind2);
        AddCompiledByte(cAnd);
        --StackPtr;
    }

    return ind2;
}

// Compiles '|'
int ExpParser::CompileOr(const char* F, int ind)
{
    int ind2 = CompileAnd(F, ind);
    sws(F, ind2);

    while(F[ind2] == '|')
    {
        ind2 = CompileAnd(F, ind2+1);
        sws(F, ind2);
        AddCompiledByte(cOr);
        --StackPtr;
    }

    return ind2;
}

// Compiles ','
int ExpParser::CompileExpression(const char* F, int ind, bool stopAtComma)
{
    int ind2 = CompileOr(F, ind);
    sws(F, ind2);

    if(stopAtComma) return ind2;

    while(F[ind2] == ',')
    {
        ind2 = CompileOr(F, ind2+1);
        sws(F, ind2);
    }

    return ind2;
}


// Return parse error message
// --------------------------
const char* ExpParser::ErrorMsg() const
{
    if(parseErrorType != FP_NO_ERROR) return ParseErrorMessage[parseErrorType];
    return 0;
}

//---------------------------------------------------------------------------
// Function evaluation
//---------------------------------------------------------------------------
//===========================================================================
namespace
{
    inline int doubleToInt(double d)
    {
        return d<0 ? -int((-d)+.5) : int(d+.5);
    }

    inline double Min(double d1, double d2)
    {
        return d1<d2 ? d1 : d2;
    }
    inline double Max(double d1, double d2)
    {
        return d1>d2 ? d1 : d2;
    }


    inline double DegreesToRadians(double degrees)
    {
        return degrees*(M_PI/180.0);
    }
    inline double RadiansToDegrees(double radians)
    {
        return radians*(180.0/M_PI);
    }
}

double ExpParser::Eval(const double* Vars)
{
    const unsigned* const ByteCode = data->ByteCode;
    const double* const Immed = data->Immed;
    double* const Stack = data->Stack;
    const unsigned ByteCodeSize = data->ByteCodeSize;
    unsigned IP, DP=0;
    int SP=-1;

    for(IP=0; IP<ByteCodeSize; ++IP)
    {
        switch(ByteCode[IP])
        {
// Functions:
          case   cAbs: Stack[SP] = fabs(Stack[SP]); break;
          case  cAcos: if(Stack[SP] < -1 || Stack[SP] > 1)
                       { evalErrorType=4; return 0; }
                       Stack[SP] = acos(Stack[SP]); break;
#ifndef NO_ASINH
          case cAcosh: Stack[SP] = acosh(Stack[SP]); break;
#endif
          case  cAsin: if(Stack[SP] < -1 || Stack[SP] > 1)
                       { evalErrorType=4; return 0; }
                       Stack[SP] = asin(Stack[SP]); break;
#ifndef NO_ASINH
          case cAsinh: Stack[SP] = asinh(Stack[SP]); break;
#endif
          case  cAtan: Stack[SP] = atan(Stack[SP]); break;
          case cAtan2: Stack[SP-1] = std::atan2(Stack[SP-1], Stack[SP]);
                       --SP; break;
#ifndef NO_ASINH
          case cAtanh: Stack[SP] = atanh(Stack[SP]); break;
#endif
          case  cCeil: Stack[SP] = ceil(Stack[SP]); break;
          case   cCos: Stack[SP] = cos(Stack[SP]); break;
          case  cCosh: Stack[SP] = cosh(Stack[SP]); break;

          case   cCot:
              {
                  double t = tan(Stack[SP]);
                  if(t == 0) { evalErrorType=1; return 0; }
                  Stack[SP] = 1/t; break;
              }
          case   cCsc:
              {
                  double s = sin(Stack[SP]);
                  if(s == 0) { evalErrorType=1; return 0; }
                  Stack[SP] = 1/s; break;
              }


#ifndef DISABLE_EVAL
          case  cEval:
              {
                  data->Stack = new double[data->StackSize];
                  double retVal = Eval(&Stack[SP-data->varAmount+1]);
                  delete[] data->Stack;
                  data->Stack = Stack;
                  SP -= data->varAmount-1;
                  Stack[SP] = retVal;
                  break;
              }
#endif

          case   cExp: Stack[SP] = exp(Stack[SP]); break;
          case cFloor: Stack[SP] = floor(Stack[SP]); break;

          case    cIf:
              {
                  unsigned jumpAddr = ByteCode[++IP];
                  unsigned immedAddr = ByteCode[++IP];
                  if(doubleToInt(Stack[SP]) == 0)
                  {
                      IP = jumpAddr;
                      DP = immedAddr;
                  }
                  --SP; break;
              }

          case   cInt: Stack[SP] = floor(Stack[SP]+.5); break;
          case   cLog: if(Stack[SP] <= 0) { evalErrorType=3; return 0; }
                       Stack[SP] = log(Stack[SP]); break;
          case cLog10: if(Stack[SP] <= 0) { evalErrorType=3; return 0; }
                       Stack[SP] = log10(Stack[SP]); break;
          case   cMax: Stack[SP-1] = fmax(Stack[SP-1], Stack[SP]);
                       --SP; break;
          case   cMin: Stack[SP-1] = Min(Stack[SP-1], Stack[SP]);
                       --SP; break;
		  case cStep: {
						  double e2 = fabs(Stack[SP - 1] - Stack[SP]);
						  if (e2 < 0.000001) Stack[SP - 1] = 0.5;
						  else {
							  if (Stack[SP - 1] > Stack[SP]) Stack[SP - 1] = 1;
							  else Stack[SP - 1] = 0;
						  }
						  --SP; break;
		  }
          case   cSec:
              {
                  double c = cos(Stack[SP]);
                  if(c == 0) { evalErrorType=1; return 0; }
                  Stack[SP] = 1/c; break;
              }
          case   cSin: Stack[SP] = sin(Stack[SP]); break;
          case  cSinh: Stack[SP] = sinh(Stack[SP]); break;
          case  cSqrt: if(Stack[SP] < 0) { evalErrorType=2; return 0; }
                       Stack[SP] = sqrt(Stack[SP]); break;
          case   cTan: Stack[SP] = tan(Stack[SP]); break;
          case  cTanh: Stack[SP] = tanh(Stack[SP]); break;
		   


// Misc:
          case cImmed: Stack[++SP] = Immed[DP++]; break;
          case  cJump: DP = ByteCode[IP+2];
                       IP = ByteCode[IP+1];
                       break;

// Operators:-,+,-,*,/,%,pow,==,<,>,&,|,degree,radius
          case   cNeg: Stack[SP] = -Stack[SP]; break;
          case   cAdd: Stack[SP-1] += Stack[SP]; --SP; break;
          case   cSub: Stack[SP-1] -= Stack[SP]; --SP; break;
          case   cMul: Stack[SP-1] *= Stack[SP]; --SP; break;
          case   cDiv: if(Stack[SP] == 0) { evalErrorType=1; return 0; }
                       Stack[SP-1] /= Stack[SP]; --SP; break;
          case   cMod: if(Stack[SP] == 0) { evalErrorType=1; return 0; }
                       Stack[SP-1] = fmod(Stack[SP-1], Stack[SP]);
                       --SP; break;
          case   cPow: Stack[SP-1] = pow(Stack[SP-1], Stack[SP]);
                       --SP; break;

          case cEqual: Stack[SP-1] = (Stack[SP-1] == Stack[SP]);
                       --SP; break;
          case  cLess: Stack[SP-1] = (Stack[SP-1] < Stack[SP]);
                       --SP; break;
          case cGreater: Stack[SP-1] = (Stack[SP-1] > Stack[SP]);
                         --SP; break;
          case   cAnd: Stack[SP-1] =
                           (doubleToInt(Stack[SP-1]) &&
                            doubleToInt(Stack[SP]));
                       --SP; break;
          case    cOr: Stack[SP-1] =
                           (doubleToInt(Stack[SP-1]) ||
                            doubleToInt(Stack[SP]));
                       --SP; break;

// Degrees-radians conversion:
          case   cDeg: Stack[SP] = RadiansToDegrees(Stack[SP]); break;
          case   cRad: Stack[SP] = DegreesToRadians(Stack[SP]); break;

// User-defined function calls:
          case cFCall:
              {
                  unsigned index = ByteCode[++IP];
                  unsigned params = data->FuncPtrs[index].params;
                  double retVal =
                      data->FuncPtrs[index].ptr(&Stack[SP-params+1]);
                  SP -= params-1;
                  Stack[SP] = retVal;
                  break;
              }

          case cPCall:
              {
                  unsigned index = ByteCode[++IP];
                  unsigned params = data->FuncParsers[index]->data->varAmount;
                  double retVal =
                      data->FuncParsers[index]->Eval(&Stack[SP-params+1]);
                  SP -= params-1;
                  Stack[SP] = retVal;
                  break;
              }


#ifdef SUPPORT_OPTIMIZER
          case   cVar: break; // Paranoia. These should never exist
          case   cDup: Stack[SP+1] = Stack[SP]; ++SP; break;
          case   cInv:
              if(Stack[SP] == 0.0) { evalErrorType=1; return 0; }
              Stack[SP] = 1.0/Stack[SP];
              break;
#endif

// Variables:
          default:
              Stack[++SP] = Vars[ByteCode[IP]-VarBegin];
        }
    }

    evalErrorType=0;
    return Stack[SP];
}


#ifdef ExpParser_SUPPORT_DEBUG_OUTPUT
namespace
{
    inline void printHex(std::ostream& dest, unsigned n)
    {
        dest.width(8); dest.fill('0'); hex(dest); //uppercase(dest);
        dest << n;
    }
}

void ExpParser::PrintByteCode(std::ostream& dest) const
{
    const unsigned* const ByteCode = data->ByteCode;
    const double* const Immed = data->Immed;

    for(unsigned IP=0, DP=0; IP<data->ByteCodeSize; ++IP)
    {
        printHex(dest, IP);
        dest << ": ";

        unsigned opcode = ByteCode[IP];

        switch(opcode)
        {
          case cIf:
              dest << "jz\t";
              printHex(dest, ByteCode[IP+1]+1);
              dest << endl;
              IP += 2;
              break;

          case cJump:
              dest << "jump\t";
              printHex(dest, ByteCode[IP+1]+1);
              dest << endl;
              IP += 2;
              break;
          case cImmed:
              dest.precision(10);
              dest << "push\t" << Immed[DP++] << endl;
              break;

          case cFCall:
              {
                  unsigned index = ByteCode[++IP];
                  Data::VarMap_t::const_iterator iter =
                      data->FuncPtrNames.begin();
                  while(iter->second != index) ++iter;
                  dest << "call\t" << iter->first << endl;
                  break;
              }

          case cPCall:
              {
                  unsigned index = ByteCode[++IP];
                  Data::VarMap_t::const_iterator iter =
                      data->FuncParserNames.begin();
                  while(iter->second != index) ++iter;
                  dest << "call\t" << iter->first << endl;
                  break;
              }

          default:
              if(opcode < VarBegin)
              {
                  string n;
                  switch(opcode)
                  {
                    case cNeg: n = "neg"; break;
                    case cAdd: n = "add"; break;
                    case cSub: n = "sub"; break;
                    case cMul: n = "mul"; break;
                    case cDiv: n = "div"; break;
                    case cMod: n = "mod"; break;
                    case cPow: n = "pow"; break;
                    case cEqual: n = "eq"; break;
                    case cLess: n = "lt"; break;
                    case cGreater: n = "gt"; break;
                    case cAnd: n = "and"; break;
                    case cOr: n = "or"; break;
                    case cDeg: n = "deg"; break;
                    case cRad: n = "rad"; break;

#ifndef DISABLE_EVAL
                    case cEval: n = "call\t0"; break;
#endif

#ifdef SUPPORT_OPTIMIZER
                    case cVar: n = "(var)"; break;
                    case cDup: n = "dup"; break;
                    case cInv: n = "inv"; break;
#endif

                    default: n = Functions[opcode-cAbs].name;
                  }
                  dest << n << endl;
              }
              else
              {
                  dest << "push\tVar" << opcode-VarBegin << endl;
              }
        }
    }
}
#endif
}
