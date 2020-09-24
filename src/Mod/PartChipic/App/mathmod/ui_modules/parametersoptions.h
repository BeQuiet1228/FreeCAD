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

#ifndef PARAMETERSOPTIONS_H
#define PARAMETERSOPTIONS_H


struct ListeModelTexture
{
    QStringList listeModels;
    QStringList listeTextures;
    QStringList listePigments;
};

class Parametersoptions
{
public:
    Parametersoptions();
    QString dotsymbol;
    QString model;
    QString fullpath;
    QString filecollection;
    QString fileconfig;
    QString advancedmodels;

    QString autoFilePath;

    //QJsonObject JConfig, Collection, IsoParam;
    //QPalette mypalette, mypalette2, darkpalette;
    //QApplication * MainApp;
    int ControlX;
    int ControlY;
    int GlwinX;
    int GlwinY;
    int ControlW;
    int ControlH;
    int GlwinW;
    int GlwinH;
    float Specular[4];
    int Threads[3];
    int CalculFactor[3];
    int Shininess;
    int NbSliders, NbSliderValues;
    int MaxTri, MaxPt, MaxGrid;
    int NbComponent,
        NbConstantes,
        NbDefinedFunctions,
        NbVariables,
        NbTextures,
        InitParGrid,
        InitIsoGrid;

};

#endif
