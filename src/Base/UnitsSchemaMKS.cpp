/***************************************************************************
 *   Copyright (c) 2009 Juergen Riegel (FreeCAD@juergen-riegel.net)        *
 *                                                                         *
 *   This file is part of the FreeCAD CAx development system.              *
 *                                                                         *
 *   This library is free software; you can redistribute it and/or         *
 *   modify it under the terms of the GNU Library General Public           *
 *   License as published by the Free Software Foundation; either          *
 *   version 2 of the License, or (at your option) any later version.      *
 *                                                                         *
 *   This library  is distributed in the hope that it will be useful,      *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU Library General Public License for more details.                  *
 *                                                                         *
 *   You should have received a copy of the GNU Library General Public     *
 *   License along with this library; see the file COPYING.LIB. If not,    *
 *   write to the Free Software Foundation, Inc., 59 Temple Place,         *
 *   Suite 330, Boston, MA  02111-1307, USA                                *
 *                                                                         *
 ***************************************************************************/


#include "PreCompiled.h"
#ifdef __GNUC__
# include <unistd.h>
#endif

#include <QString>
#include <QLocale>
#include "Exception.h"
#include "UnitsApi.h"
#include "UnitsSchemaMKS.h"
#include <cmath>

#include"Quantity.h"
using namespace Base;


QString UnitsSchemaMKS::schemaTranslate(const Quantity &quant, double &factor, QString &unitString)
{
    double UnitValue = std::abs(quant.getValue());
    Unit unit = quant.getUnit();

    // now do special treatment on all cases seems necessary:
    //if (unit == Unit::Length) {  // Length handling ============================
		  //  /*unitString = QString::fromLatin1("m");
		  //  factor = 1.0;*/
    //    if (UnitValue < 0.000000001) {// smaller then 0.001 nm -> scientific notation
    //        unitString = QString::fromLatin1("m");
    //        factor = 1000.0;
    //    }
    //    else if(UnitValue < 0.001) {
    //        unitString = QString::fromLatin1("nm");
    //        factor = 0.000001;
    //    }
    //    else if(UnitValue < 0.1) {
    //        unitString = QString::fromUtf8("\xC2\xB5m");
    //        factor = 0.001;
    //    }
    //    else if(UnitValue < 100.0) {
    //        unitString = QString::fromLatin1("mm");
    //        factor = 1.0;
    //    }
    //    else if(UnitValue < 10000000.0) {
    //        unitString = QString::fromLatin1("m");
    //        factor = 1000.0;
    //    }
    //    else if(UnitValue < 100000000000.0 ) {
    //        unitString = QString::fromLatin1("km");
    //        factor = 1000000.0;
    //    }
    //    else { // bigger then 1000 km -> scientific notation
    //        unitString = QString::fromLatin1("m");
    //        factor = 1000.0;
    //    }
    //}
	if (unit == Unit::Length) {  // Length handling ============================
		//Quantity::NanoMetre = Quantity::Quantity(1.0e-6, Unit(1));
		//Quantity::MicroMetre = Quantity::Quantity(1.0e-3, Unit(1));
		//Quantity::MilliMetre = Quantity::Quantity(1.0, Unit(1));
		//Quantity::CentiMetre = Quantity::Quantity(10.0, Unit(1));
		//Quantity::DeciMetre = Quantity::Quantity(100.0, Unit(1));
		//Quantity::Metre = Quantity::Quantity(1000.0, Unit(1));
		//Quantity::KiloMetre = Quantity::Quantity(1000000.0, Unit(1));
		if (UnitsApi::defaultLengthUnit==0){
			unitString = QString::fromLatin1("mm");
			factor = 0.001;
		}
		else if (UnitsApi::defaultLengthUnit==1)
		{
			unitString = QString::fromLatin1("cm");
			factor = 0.01;
		}
		else if (UnitsApi::defaultLengthUnit==2)
		{
			unitString = QString::fromLatin1("m");
			factor = 1.0;
		}
		//if (UnitValue < 0.1) {// smaller then 0.001 nm -> scientific notation
		//	unitString = QString::fromLatin1("mm");
		//	factor = 0.001;
		//}
		//else if (UnitValue < 1){
		//	unitString = QString::fromLatin1("cm");
		//	factor = 0.01;
		//}
		//else if (UnitValue < 1000){
		//	unitString = QString::fromLatin1("m");
		//	factor = 1.0;
		//}
		//else { // bigger then 1000 km -> scientific notation
		//	unitString = QString::fromLatin1("km");
		//	factor = 1000.0;
		//}
	}
	else if (unit == Unit::Angle){
		if (UnitsApi::defaultAngleUnit==0){
			unitString = QString::fromLatin1("deg");
			factor = 1.0;
		}
		else{
			unitString = QString::fromLatin1("rad");
			factor = 180 / M_PI;
		}
	}
	else if (unit == Unit::TimeSpan){
		if (UnitsApi::defaultTimeSpanUnit==0){
			unitString = QString::fromLatin1("ms");
			factor = 0.001;
		}
		else if (UnitsApi::defaultTimeSpanUnit==1){
			unitString = QString::fromLatin1("s");
			factor = 1.0;
		}
		else if (UnitsApi::defaultTimeSpanUnit==2){
			unitString = QString::fromLatin1("min");
			factor = 60;
		}
		else {
			unitString = QString::fromLatin1("h");
			factor = 3600;
		}
	}
	else if (unit == Unit::ElectricCurrent){
		if (UnitsApi::defaultElectricCurrentUnit == 0){
			unitString = QString::fromLatin1("A");
			factor = 1.0;
		}
		else if (UnitsApi::defaultElectricCurrentUnit == 1){
			unitString = QString::fromLatin1("kA");
			factor = 1000.0;
		}
		else{
			unitString = QString::fromLatin1("MA");
			factor = 1.0e+6;
		}
	}
	else if (unit == Unit::ElectricPotential) {
		if (UnitsApi::defaultElectricPotentialUnit == 0){
			unitString = QString::fromLatin1("V");
			factor = 1;
		}

		else if (UnitsApi::defaultElectricPotentialUnit == 1){
			unitString = QString::fromLatin1("kV");
			factor = 1000.0;
		}
		else{
			unitString = QString::fromLatin1("MV");
			factor = 1000000.0;
		}
	}
	else if (unit == Unit::Frequency){
		if (UnitsApi::defaultFrequencyUnit==0){
			unitString = QString::fromLatin1("Hz");
			factor = 1.0;
		}
		else if (UnitsApi::defaultFrequencyUnit==1){
			unitString = QString::fromLatin1("kHz");
			factor = 1000.0;
		}
		else if (UnitsApi::defaultFrequencyUnit==2){
			unitString = QString::fromLatin1("MHz");
			factor = 1000000.0;
		}
		else if (UnitsApi::defaultFrequencyUnit==3){
			unitString = QString::fromLatin1("GHz");
			factor = 1000000000;
		}
		else{
			unitString = QString::fromLatin1("THz");
			factor = 1000000000000;
		}
	}
    else if (unit == Unit::Area) {
        if (UnitValue < 100.0) {// smaller than 1 square cm
            unitString = QString::fromLatin1("mm^2");
            factor = 1.0;
        }
        else if (UnitValue < 10000000000000.0) {
            unitString = QString::fromLatin1("m^2");
            factor = 1000000.0;
        }
        else { // bigger then 1 square kilometer
            unitString = QString::fromLatin1("km^2");
            factor = 1000000000000.0;
        }
    }
    else if (unit == Unit::Mass) {
        // TODO Cascade for the wights
        // default action for all cases without special treatment:
        unitString = quant.getUnit().getString();
        factor = 1.0;
    }
    else if (unit == Unit::Density) {
        if (UnitValue < 0.0001) {
            unitString = QString::fromLatin1("kg/m^3");
            factor = 0.000000001;
        }
        else if (UnitValue < 1.0) {
            unitString = QString::fromLatin1("kg/cm^3");
            factor = 0.001;
        }
        else {
            unitString = QString::fromLatin1("kg/mm^3");
            factor = 1.0;
        }
    }

    else if (unit == Unit::Volume) {
        if (UnitValue < 1000000.0) {// smaller than 10 cubic cm
            unitString = QString::fromLatin1("mm^3");
            factor = 1.0;
        }
        else if (UnitValue < 1000000000000000000.0) {
            unitString = QString::fromLatin1("m^3");
            factor = 1000000000.0;
        }
        else { // bigger then 1 cubic kilometer
            unitString = QString::fromLatin1("km^3");
            factor = 1000000000000000000.0;
        }
    }
    else if ((unit == Unit::Pressure) || (unit == Unit::Stress)) {
        if (UnitValue < 10.0) {// Pa is the smallest
            unitString = QString::fromLatin1("Pa");
            factor = 0.001;
        }
        else if (UnitValue < 10000.0) {
            unitString = QString::fromLatin1("kPa");
            factor = 1.0;
        }
        else if (UnitValue < 10000000.0) {
            unitString = QString::fromLatin1("MPa");
            factor = 1000.0;
        }
        else if (UnitValue < 10000000000.0) {
            unitString = QString::fromLatin1("GPa");
            factor = 1000000.0;
        }
        else { // bigger then 1000 GPa -> scientific notation
            unitString = QString::fromLatin1("Pa");
            factor = 0.001;
        }
    }
    else if (unit == Unit::ThermalConductivity) {
        if (UnitValue > 1000000) {
            unitString = QString::fromLatin1("W/mm/K");
            factor = 1000000.0;
        }
        else {
            unitString = QString::fromLatin1("W/m/K");
            factor = 1000.0;
        }
    }
    else if (unit == Unit::ThermalExpansionCoefficient) {
        if (UnitValue < 0.001) {
            unitString = QString::fromUtf8("\xC2\xB5m/m/K");
            factor = 0.000001;
        }
        else {
            unitString = QString::fromLatin1("m/m/K");
            factor = 1.0;
        }
    }
    else if (unit == Unit::SpecificHeat) {
        unitString = QString::fromLatin1("J/kg/K");
        factor = 1000000.0;
    }
    else if (unit == Unit::ThermalTransferCoefficient) {
        unitString = QString::fromLatin1("W/m^2/K");
        factor = 1.0;
    }
    else if (unit == Unit::Power) {
        unitString = QString::fromLatin1("W");
        factor = 1000000;
    }
    
	

    else if (unit == Unit::SpecificEnergy) {
        unitString = QString::fromLatin1("m^2/s^2");
        factor = 1000000;
    }
    else if (unit == Unit::HeatFlux) {
        unitString = QString::fromLatin1("W/m^2");
        factor = 1.0;
    }
    else if (unit == Unit::Velocity) {
        unitString = QString::fromLatin1("m/s");
        factor = 1000.0;
    }
    else if (unit == Unit::DynamicViscosity) {
        unitString = QString::fromLatin1("kg/(m*s)");
        factor = 0.001;
    }
    else {
        // default action for all cases without special treatment:
        unitString = quant.getUnit().getString();
        factor = 1.0;
    }

    return toLocale(quant, factor, unitString);
}
