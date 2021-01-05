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
#ifndef _POV_FUNCTIONS_H_
#define _POV_FUNCTIONS_H_

double maxim(double p1, double p2);

double p_skeletal_int(const double* pp);

double f_hex_y(const double* pp);

double fmesh(const double* pp);

double  fhelix1(const double* pp);
double fhelix2(const double* pp) ;
#endif