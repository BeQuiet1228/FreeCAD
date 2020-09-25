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
#include <QtGui>
#include <math.h>
#include "parametersoptions.h"

static bool MACOS = false;

Parametersoptions::Parametersoptions()
{
	ControlX = 20;
	ControlY = 20;
	GlwinX = 575;
	GlwinY = 20;
	ControlW = 538;
	ControlH = 700;
	GlwinW = 780;
	GlwinH = 700;
	MaxTri = 300000;
	MaxPt = 150000;
	MaxGrid = 80;
	NbComponent = 10;
	NbConstantes = 30;
	NbDefinedFunctions = 30;
	NbVariables = 20;
	NbTextures = 10;
	NbSliders = 20;
	NbSliderValues = 200;

	dotsymbol = ".";
	model = "CloseIso_2";
	Shininess = 110;
	Specular[0] = Specular[1] = Specular[2] = 0.5;
	Specular[3] = 1.0;
	Threads[0] = 8;
	Threads[1] = 1;
	Threads[2] = 64;
	CalculFactor[0] = 4;
	CalculFactor[1] = 4;
	CalculFactor[2] = 4;
	filecollection = "mathmodcollection.js";
	fileconfig = "mathmodconfig.js";
	advancedmodels = "advancedmodels.js";	
}
