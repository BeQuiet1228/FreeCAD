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
/***************************************************************************\
|* Function parser v2.7 by Warp                                            *|
|* ----------------------------                                            *|
|* Parses and evaluates the given function with the given variable values. *|
|*                                                                         *|
\***************************************************************************/

#ifndef ONCE_PM3_FPARSER_H_
#define ONCE_PM3_FPARSER_H_
#include <string>
#include <map>
#include <vector>
#include "paraDefine.h"
#include "system.h"
#ifdef FUNCTIONPARSER_SUPPORT_DEBUG_OUTPUT
#include <iostream>
#endif


namespace PM3
{
class DefValue1D;
class DefValue3D;
class ExpParser
{
public:
    enum ParseErrorType
    {
        SYNTAX_ERROR=0, MISM_PARENTH, MISSING_PARENTH, EMPTY_PARENTH,
        EXPECT_OPERATOR, OUT_OF_MEMORY, UNEXPECTED_ERROR, INVALID_VARS,
        ILL_PARAMS_AMOUNT, PREMATURE_EOS, EXPECT_PARENTH_FUNC,
        FP_NO_ERROR
    };

	int ParseExp(std::string& Function, std::string &er, const std::string& Vars = std::string(),
              bool useDegrees = false);
    int Parse(const std::string& Function, const std::string& Vars,
              bool useDegrees = false);
    const char* ErrorMsg() const;
    inline ParseErrorType GetParseErrorType() const { return parseErrorType; }

    double Eval(const double* Vars);
    inline int EvalError() const { return evalErrorType; }


    void Optimize();


    ExpParser();
    ~ExpParser();

    // Copy constructor and assignment operator (implemented using the
    // copy-on-write technique for efficiency):
    ExpParser(const ExpParser&);
    ExpParser& operator=(const ExpParser&);


#ifdef FUNCTIONPARSER_SUPPORT_DEBUG_OUTPUT
    // For debugging purposes only:
    void PrintByteCode(std::ostream& dest) const;
#endif
    typedef double (*FunctionPtr)(const double*);

//========================================================================
public:
//========================================================================

// Private data:
// ------------
    ParseErrorType parseErrorType;
    int evalErrorType;

    struct Data
    {
        unsigned referenceCounter;

        int varAmount;
        bool useDegreeConversion;

        std::vector<PM3::CanDefineDistance> paraVectorDis;
        typedef std::map<std::string, std::string> UnitMap_t;
        UnitMap_t Units;

        typedef std::map<std::string, std::string> Def1DMap_t;
        Def1DMap_t Def1DParas;
        std::vector<std::string> Def1DParasNames;
        typedef std::vector<std::string> stringlist;
        typedef std::map<std::string, stringlist> Def3DMap_t;
        Def3DMap_t Def3DParas;
        std::vector<std::string> Def3DParasNames;
        typedef std::map<std::string, unsigned> VarMap_t;
        VarMap_t Variables;
		std::vector<std::string> VariablesUse;

        typedef std::map<std::string, double> ConstMap_t;
        ConstMap_t Constants;

        VarMap_t FuncPtrNames;
        struct FuncPtrData
        {
            FunctionPtr ptr; unsigned params;
            FuncPtrData(FunctionPtr p, unsigned par): ptr(p), params(par) {}
        };
        std::vector<FuncPtrData> FuncPtrs;

        VarMap_t FuncParserNames;
        std::vector<ExpParser*> FuncParsers;

        unsigned* ByteCode;
        unsigned ByteCodeSize;
        double* Immed;
        unsigned ImmedSize;
        double* Stack;
        unsigned StackSize;

        Data();
        ~Data();
        Data(const Data&);

        Data& operator=(const Data&); // not implemented on purpose
    };

    Data* data;

    // Temp data needed in Compile():
    unsigned StackPtr;
    std::vector<unsigned>* tempByteCode;
    std::vector<double>* tempImmed;


// Private methods:
// ---------------
    inline void copyOnWrite();


    bool checkRecursiveLinking(const ExpParser*) const;
public:
	bool isHasVarible(std::string v);
    bool isValidName(const std::string&) const;
    bool AddConstant(const std::string& name, double value);
    bool AddUnit(const std::string& name, std::string value);
	bool AddDef1DPara(std::string name, std::string value, std::string &er);
	bool AddDef3DPara(std::string name, Data::stringlist value, std::string &er);



    bool AddFunction(const std::string& name,
                     FunctionPtr, unsigned paramsAmount);
    bool AddFunction(const std::string& name, ExpParser&);
    Data::VarMap_t::const_iterator FindVariable(const char*,
                                                const Data::VarMap_t&) const;
    Data::ConstMap_t::const_iterator FindConstant(const char*) const;
    Data::UnitMap_t::const_iterator FindUnit(const char*) const;
    Data::Def1DMap_t::const_iterator FindDef1DPara(const char*) const;
    Data::Def3DMap_t::const_iterator FindDef3DPara(const char*) const;
    int CheckSyntax(const char*);
    int CheckSyntaxExp( std::string &ex);
    bool Compile(const char*);
    bool IsVariable(int);
    void AddCompiledByte(unsigned);
    void AddImmediate(double);
    void AddFunctionOpcode(unsigned);
    inline void incStackPtr();
    int CompileIf(const char*, int);
    int CompileFunctionParams(const char*, int, unsigned);
    int CompileElement(const char*, int);
    int CompilePow(const char*, int);
    int CompileUnaryMinus(const char*, int);
    int CompileMult(const char*, int);
    int CompileAddition(const char*, int);
    int CompileComparison(const char*, int);
    int CompileAnd(const char*, int);
    int CompileOr(const char*, int);
    int CompileExpression(const char*, int, bool=false);
    bool getUpdate(DefValue1D &in);
    bool getUpdate(DefValue3D &in);

    void MakeTree(void*) const;
};
}
#endif
