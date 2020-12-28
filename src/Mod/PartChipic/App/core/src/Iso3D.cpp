/***************************************************************************
*   Copyright (C) 2006 by Abderrahman Taha                                *
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

#include "../Iso3D.h"
#include "../basicstring.h"
#include <boost/regex.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/format.hpp>
/*


4.-----------4----------------.5
/|                           /|
7 |                          5 |
/  |                         /  |
7.---|-----------6------------.6  |
|   |                        |   |
|   8                        |   9
|   |                        |   |
|   ^ j                      |   |
11   |                       10   |
|   |     i                  |   |
|  0.----->-----0------------|---.1
|  /                         |  /
| 3 k                        | 1
|/                           |/
3.---------------2------------.2
*/

/*


4.-----------4----------------.5
/|                           /|
7 |                          5 |
/  |                         /  |
7.---|-----------6------------.6  |
|   |                        |   |
|   8                        |   9
|   |                        |   |
|   ^ j                      |   |
11   |                       10   |
|   |     i                  |   |
|  0.----->-----0------------|---.1
|  /                         |  /
| 3 k                        | 1
|/                           |/
3.---------------2------------.2
*/





using std::vector;
using std::list;
#define VSIZE 18

#ifndef DISTANCE_RESOL_MAX
	#define DISTANCE_RESOL_MAX 8
	#define DISTANCE_RESOL_MIN 2
#endif
int triTable[256][16] = {

	{ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 0, 8, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 0, 1, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 1, 8, 3, 9, 8, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 1, 2, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 0, 8, 3, 1, 2, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 9, 2, 10, 0, 2, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 2, 8, 3, 2, 10, 8, 10, 9, 8, -1, -1, -1, -1, -1, -1, -1 },
	{ 3, 11, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 0, 11, 2, 8, 11, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 1, 9, 0, 2, 3, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 1, 11, 2, 1, 9, 11, 9, 8, 11, -1, -1, -1, -1, -1, -1, -1 },
	{ 3, 10, 1, 11, 10, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 0, 10, 1, 0, 8, 10, 8, 11, 10, -1, -1, -1, -1, -1, -1, -1 },
	{ 3, 9, 0, 3, 11, 9, 11, 10, 9, -1, -1, -1, -1, -1, -1, -1 },
	{ 9, 8, 10, 10, 8, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 4, 7, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 4, 3, 0, 7, 3, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 0, 1, 9, 8, 4, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 4, 1, 9, 4, 7, 1, 7, 3, 1, -1, -1, -1, -1, -1, -1, -1 },
	{ 1, 2, 10, 8, 4, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 3, 4, 7, 3, 0, 4, 1, 2, 10, -1, -1, -1, -1, -1, -1, -1 },
	{ 9, 2, 10, 9, 0, 2, 8, 4, 7, -1, -1, -1, -1, -1, -1, -1 },
	{ 2, 10, 9, 2, 9, 7, 2, 7, 3, 7, 9, 4, -1, -1, -1, -1 },
	{ 8, 4, 7, 3, 11, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 11, 4, 7, 11, 2, 4, 2, 0, 4, -1, -1, -1, -1, -1, -1, -1 },
	{ 9, 0, 1, 8, 4, 7, 2, 3, 11, -1, -1, -1, -1, -1, -1, -1 },
	{ 4, 7, 11, 9, 4, 11, 9, 11, 2, 9, 2, 1, -1, -1, -1, -1 },
	{ 3, 10, 1, 3, 11, 10, 7, 8, 4, -1, -1, -1, -1, -1, -1, -1 },
	{ 1, 11, 10, 1, 4, 11, 1, 0, 4, 7, 11, 4, -1, -1, -1, -1 },
	{ 4, 7, 8, 9, 0, 11, 9, 11, 10, 11, 0, 3, -1, -1, -1, -1 },
	{ 4, 7, 11, 4, 11, 9, 9, 11, 10, -1, -1, -1, -1, -1, -1, -1 },
	{ 9, 5, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 9, 5, 4, 0, 8, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 0, 5, 4, 1, 5, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 8, 5, 4, 8, 3, 5, 3, 1, 5, -1, -1, -1, -1, -1, -1, -1 },
	{ 1, 2, 10, 9, 5, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 3, 0, 8, 1, 2, 10, 4, 9, 5, -1, -1, -1, -1, -1, -1, -1 },
	{ 5, 2, 10, 5, 4, 2, 4, 0, 2, -1, -1, -1, -1, -1, -1, -1 },
	{ 2, 10, 5, 3, 2, 5, 3, 5, 4, 3, 4, 8, -1, -1, -1, -1 },
	{ 9, 5, 4, 2, 3, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 0, 11, 2, 0, 8, 11, 4, 9, 5, -1, -1, -1, -1, -1, -1, -1 },
	{ 0, 5, 4, 0, 1, 5, 2, 3, 11, -1, -1, -1, -1, -1, -1, -1 },
	{ 2, 1, 5, 2, 5, 8, 2, 8, 11, 4, 8, 5, -1, -1, -1, -1 },
	{ 10, 3, 11, 10, 1, 3, 9, 5, 4, -1, -1, -1, -1, -1, -1, -1 },
	{ 4, 9, 5, 0, 8, 1, 8, 10, 1, 8, 11, 10, -1, -1, -1, -1 },
	{ 5, 4, 0, 5, 0, 11, 5, 11, 10, 11, 0, 3, -1, -1, -1, -1 },
	{ 5, 4, 8, 5, 8, 10, 10, 8, 11, -1, -1, -1, -1, -1, -1, -1 },
	{ 9, 7, 8, 5, 7, 9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 9, 3, 0, 9, 5, 3, 5, 7, 3, -1, -1, -1, -1, -1, -1, -1 },
	{ 0, 7, 8, 0, 1, 7, 1, 5, 7, -1, -1, -1, -1, -1, -1, -1 },
	{ 1, 5, 3, 3, 5, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 9, 7, 8, 9, 5, 7, 10, 1, 2, -1, -1, -1, -1, -1, -1, -1 },
	{ 10, 1, 2, 9, 5, 0, 5, 3, 0, 5, 7, 3, -1, -1, -1, -1 },
	{ 8, 0, 2, 8, 2, 5, 8, 5, 7, 10, 5, 2, -1, -1, -1, -1 },
	{ 2, 10, 5, 2, 5, 3, 3, 5, 7, -1, -1, -1, -1, -1, -1, -1 },
	{ 7, 9, 5, 7, 8, 9, 3, 11, 2, -1, -1, -1, -1, -1, -1, -1 },
	{ 9, 5, 7, 9, 7, 2, 9, 2, 0, 2, 7, 11, -1, -1, -1, -1 },
	{ 2, 3, 11, 0, 1, 8, 1, 7, 8, 1, 5, 7, -1, -1, -1, -1 },
	{ 11, 2, 1, 11, 1, 7, 7, 1, 5, -1, -1, -1, -1, -1, -1, -1 },
	{ 9, 5, 8, 8, 5, 7, 10, 1, 3, 10, 3, 11, -1, -1, -1, -1 },
	{ 5, 7, 0, 5, 0, 9, 7, 11, 0, 1, 0, 10, 11, 10, 0, -1 },
	{ 11, 10, 0, 11, 0, 3, 10, 5, 0, 8, 0, 7, 5, 7, 0, -1 },
	{ 11, 10, 5, 7, 11, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 10, 6, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 0, 8, 3, 5, 10, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 9, 0, 1, 5, 10, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 1, 8, 3, 1, 9, 8, 5, 10, 6, -1, -1, -1, -1, -1, -1, -1 },
	{ 1, 6, 5, 2, 6, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 1, 6, 5, 1, 2, 6, 3, 0, 8, -1, -1, -1, -1, -1, -1, -1 },
	{ 9, 6, 5, 9, 0, 6, 0, 2, 6, -1, -1, -1, -1, -1, -1, -1 },
	{ 5, 9, 8, 5, 8, 2, 5, 2, 6, 3, 2, 8, -1, -1, -1, -1 },
	{ 2, 3, 11, 10, 6, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 11, 0, 8, 11, 2, 0, 10, 6, 5, -1, -1, -1, -1, -1, -1, -1 },
	{ 0, 1, 9, 2, 3, 11, 5, 10, 6, -1, -1, -1, -1, -1, -1, -1 },
	{ 5, 10, 6, 1, 9, 2, 9, 11, 2, 9, 8, 11, -1, -1, -1, -1 },
	{ 6, 3, 11, 6, 5, 3, 5, 1, 3, -1, -1, -1, -1, -1, -1, -1 },
	{ 0, 8, 11, 0, 11, 5, 0, 5, 1, 5, 11, 6, -1, -1, -1, -1 },
	{ 3, 11, 6, 0, 3, 6, 0, 6, 5, 0, 5, 9, -1, -1, -1, -1 },
	{ 6, 5, 9, 6, 9, 11, 11, 9, 8, -1, -1, -1, -1, -1, -1, -1 },
	{ 5, 10, 6, 4, 7, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 4, 3, 0, 4, 7, 3, 6, 5, 10, -1, -1, -1, -1, -1, -1, -1 },
	{ 1, 9, 0, 5, 10, 6, 8, 4, 7, -1, -1, -1, -1, -1, -1, -1 },
	{ 10, 6, 5, 1, 9, 7, 1, 7, 3, 7, 9, 4, -1, -1, -1, -1 },
	{ 6, 1, 2, 6, 5, 1, 4, 7, 8, -1, -1, -1, -1, -1, -1, -1 },
	{ 1, 2, 5, 5, 2, 6, 3, 0, 4, 3, 4, 7, -1, -1, -1, -1 },
	{ 8, 4, 7, 9, 0, 5, 0, 6, 5, 0, 2, 6, -1, -1, -1, -1 },
	{ 7, 3, 9, 7, 9, 4, 3, 2, 9, 5, 9, 6, 2, 6, 9, -1 },
	{ 3, 11, 2, 7, 8, 4, 10, 6, 5, -1, -1, -1, -1, -1, -1, -1 },
	{ 5, 10, 6, 4, 7, 2, 4, 2, 0, 2, 7, 11, -1, -1, -1, -1 },
	{ 0, 1, 9, 4, 7, 8, 2, 3, 11, 5, 10, 6, -1, -1, -1, -1 },
	{ 9, 2, 1, 9, 11, 2, 9, 4, 11, 7, 11, 4, 5, 10, 6, -1 },
	{ 8, 4, 7, 3, 11, 5, 3, 5, 1, 5, 11, 6, -1, -1, -1, -1 },
	{ 5, 1, 11, 5, 11, 6, 1, 0, 11, 7, 11, 4, 0, 4, 11, -1 },
	{ 0, 5, 9, 0, 6, 5, 0, 3, 6, 11, 6, 3, 8, 4, 7, -1 },
	{ 6, 5, 9, 6, 9, 11, 4, 7, 9, 7, 11, 9, -1, -1, -1, -1 },
	{ 10, 4, 9, 6, 4, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 4, 10, 6, 4, 9, 10, 0, 8, 3, -1, -1, -1, -1, -1, -1, -1 },
	{ 10, 0, 1, 10, 6, 0, 6, 4, 0, -1, -1, -1, -1, -1, -1, -1 },
	{ 8, 3, 1, 8, 1, 6, 8, 6, 4, 6, 1, 10, -1, -1, -1, -1 },
	{ 1, 4, 9, 1, 2, 4, 2, 6, 4, -1, -1, -1, -1, -1, -1, -1 },
	{ 3, 0, 8, 1, 2, 9, 2, 4, 9, 2, 6, 4, -1, -1, -1, -1 },
	{ 0, 2, 4, 4, 2, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 8, 3, 2, 8, 2, 4, 4, 2, 6, -1, -1, -1, -1, -1, -1, -1 },
	{ 10, 4, 9, 10, 6, 4, 11, 2, 3, -1, -1, -1, -1, -1, -1, -1 },
	{ 0, 8, 2, 2, 8, 11, 4, 9, 10, 4, 10, 6, -1, -1, -1, -1 },
	{ 3, 11, 2, 0, 1, 6, 0, 6, 4, 6, 1, 10, -1, -1, -1, -1 },
	{ 6, 4, 1, 6, 1, 10, 4, 8, 1, 2, 1, 11, 8, 11, 1, -1 },
	{ 9, 6, 4, 9, 3, 6, 9, 1, 3, 11, 6, 3, -1, -1, -1, -1 },
	{ 8, 11, 1, 8, 1, 0, 11, 6, 1, 9, 1, 4, 6, 4, 1, -1 },
	{ 3, 11, 6, 3, 6, 0, 0, 6, 4, -1, -1, -1, -1, -1, -1, -1 },
	{ 6, 4, 8, 11, 6, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 7, 10, 6, 7, 8, 10, 8, 9, 10, -1, -1, -1, -1, -1, -1, -1 },
	{ 0, 7, 3, 0, 10, 7, 0, 9, 10, 6, 7, 10, -1, -1, -1, -1 },
	{ 10, 6, 7, 1, 10, 7, 1, 7, 8, 1, 8, 0, -1, -1, -1, -1 },
	{ 10, 6, 7, 10, 7, 1, 1, 7, 3, -1, -1, -1, -1, -1, -1, -1 },
	{ 1, 2, 6, 1, 6, 8, 1, 8, 9, 8, 6, 7, -1, -1, -1, -1 },
	{ 2, 6, 9, 2, 9, 1, 6, 7, 9, 0, 9, 3, 7, 3, 9, -1 },
	{ 7, 8, 0, 7, 0, 6, 6, 0, 2, -1, -1, -1, -1, -1, -1, -1 },
	{ 7, 3, 2, 6, 7, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 2, 3, 11, 10, 6, 8, 10, 8, 9, 8, 6, 7, -1, -1, -1, -1 },
	{ 2, 0, 7, 2, 7, 11, 0, 9, 7, 6, 7, 10, 9, 10, 7, -1 },
	{ 1, 8, 0, 1, 7, 8, 1, 10, 7, 6, 7, 10, 2, 3, 11, -1 },
	{ 11, 2, 1, 11, 1, 7, 10, 6, 1, 6, 7, 1, -1, -1, -1, -1 },
	{ 8, 9, 6, 8, 6, 7, 9, 1, 6, 11, 6, 3, 1, 3, 6, -1 },
	{ 0, 9, 1, 11, 6, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 7, 8, 0, 7, 0, 6, 3, 11, 0, 11, 6, 0, -1, -1, -1, -1 },
	{ 7, 11, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 7, 6, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 3, 0, 8, 11, 7, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 0, 1, 9, 11, 7, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 8, 1, 9, 8, 3, 1, 11, 7, 6, -1, -1, -1, -1, -1, -1, -1 },
	{ 10, 1, 2, 6, 11, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 1, 2, 10, 3, 0, 8, 6, 11, 7, -1, -1, -1, -1, -1, -1, -1 },
	{ 2, 9, 0, 2, 10, 9, 6, 11, 7, -1, -1, -1, -1, -1, -1, -1 },
	{ 6, 11, 7, 2, 10, 3, 10, 8, 3, 10, 9, 8, -1, -1, -1, -1 },
	{ 7, 2, 3, 6, 2, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 7, 0, 8, 7, 6, 0, 6, 2, 0, -1, -1, -1, -1, -1, -1, -1 },
	{ 2, 7, 6, 2, 3, 7, 0, 1, 9, -1, -1, -1, -1, -1, -1, -1 },
	{ 1, 6, 2, 1, 8, 6, 1, 9, 8, 8, 7, 6, -1, -1, -1, -1 },
	{ 10, 7, 6, 10, 1, 7, 1, 3, 7, -1, -1, -1, -1, -1, -1, -1 },
	{ 10, 7, 6, 1, 7, 10, 1, 8, 7, 1, 0, 8, -1, -1, -1, -1 },
	{ 0, 3, 7, 0, 7, 10, 0, 10, 9, 6, 10, 7, -1, -1, -1, -1 },
	{ 7, 6, 10, 7, 10, 8, 8, 10, 9, -1, -1, -1, -1, -1, -1, -1 },
	{ 6, 8, 4, 11, 8, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 3, 6, 11, 3, 0, 6, 0, 4, 6, -1, -1, -1, -1, -1, -1, -1 },
	{ 8, 6, 11, 8, 4, 6, 9, 0, 1, -1, -1, -1, -1, -1, -1, -1 },
	{ 9, 4, 6, 9, 6, 3, 9, 3, 1, 11, 3, 6, -1, -1, -1, -1 },
	{ 6, 8, 4, 6, 11, 8, 2, 10, 1, -1, -1, -1, -1, -1, -1, -1 },
	{ 1, 2, 10, 3, 0, 11, 0, 6, 11, 0, 4, 6, -1, -1, -1, -1 },
	{ 4, 11, 8, 4, 6, 11, 0, 2, 9, 2, 10, 9, -1, -1, -1, -1 },
	{ 10, 9, 3, 10, 3, 2, 9, 4, 3, 11, 3, 6, 4, 6, 3, -1 },
	{ 8, 2, 3, 8, 4, 2, 4, 6, 2, -1, -1, -1, -1, -1, -1, -1 },
	{ 0, 4, 2, 4, 6, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 1, 9, 0, 2, 3, 4, 2, 4, 6, 4, 3, 8, -1, -1, -1, -1 },
	{ 1, 9, 4, 1, 4, 2, 2, 4, 6, -1, -1, -1, -1, -1, -1, -1 },
	{ 8, 1, 3, 8, 6, 1, 8, 4, 6, 6, 10, 1, -1, -1, -1, -1 },
	{ 10, 1, 0, 10, 0, 6, 6, 0, 4, -1, -1, -1, -1, -1, -1, -1 },
	{ 4, 6, 3, 4, 3, 8, 6, 10, 3, 0, 3, 9, 10, 9, 3, -1 },
	{ 10, 9, 4, 6, 10, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 4, 9, 5, 7, 6, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 0, 8, 3, 4, 9, 5, 11, 7, 6, -1, -1, -1, -1, -1, -1, -1 },
	{ 5, 0, 1, 5, 4, 0, 7, 6, 11, -1, -1, -1, -1, -1, -1, -1 },
	{ 11, 7, 6, 8, 3, 4, 3, 5, 4, 3, 1, 5, -1, -1, -1, -1 },
	{ 9, 5, 4, 10, 1, 2, 7, 6, 11, -1, -1, -1, -1, -1, -1, -1 },
	{ 6, 11, 7, 1, 2, 10, 0, 8, 3, 4, 9, 5, -1, -1, -1, -1 },
	{ 7, 6, 11, 5, 4, 10, 4, 2, 10, 4, 0, 2, -1, -1, -1, -1 },
	{ 3, 4, 8, 3, 5, 4, 3, 2, 5, 10, 5, 2, 11, 7, 6, -1 },
	{ 7, 2, 3, 7, 6, 2, 5, 4, 9, -1, -1, -1, -1, -1, -1, -1 },
	{ 9, 5, 4, 0, 8, 6, 0, 6, 2, 6, 8, 7, -1, -1, -1, -1 },
	{ 3, 6, 2, 3, 7, 6, 1, 5, 0, 5, 4, 0, -1, -1, -1, -1 },
	{ 6, 2, 8, 6, 8, 7, 2, 1, 8, 4, 8, 5, 1, 5, 8, -1 },
	{ 9, 5, 4, 10, 1, 6, 1, 7, 6, 1, 3, 7, -1, -1, -1, -1 },
	{ 1, 6, 10, 1, 7, 6, 1, 0, 7, 8, 7, 0, 9, 5, 4, -1 },
	{ 4, 0, 10, 4, 10, 5, 0, 3, 10, 6, 10, 7, 3, 7, 10, -1 },
	{ 7, 6, 10, 7, 10, 8, 5, 4, 10, 4, 8, 10, -1, -1, -1, -1 },
	{ 6, 9, 5, 6, 11, 9, 11, 8, 9, -1, -1, -1, -1, -1, -1, -1 },
	{ 3, 6, 11, 0, 6, 3, 0, 5, 6, 0, 9, 5, -1, -1, -1, -1 },
	{ 0, 11, 8, 0, 5, 11, 0, 1, 5, 5, 6, 11, -1, -1, -1, -1 },
	{ 6, 11, 3, 6, 3, 5, 5, 3, 1, -1, -1, -1, -1, -1, -1, -1 },
	{ 1, 2, 10, 9, 5, 11, 9, 11, 8, 11, 5, 6, -1, -1, -1, -1 },
	{ 0, 11, 3, 0, 6, 11, 0, 9, 6, 5, 6, 9, 1, 2, 10, -1 },
	{ 11, 8, 5, 11, 5, 6, 8, 0, 5, 10, 5, 2, 0, 2, 5, -1 },
	{ 6, 11, 3, 6, 3, 5, 2, 10, 3, 10, 5, 3, -1, -1, -1, -1 },
	{ 5, 8, 9, 5, 2, 8, 5, 6, 2, 3, 8, 2, -1, -1, -1, -1 },
	{ 9, 5, 6, 9, 6, 0, 0, 6, 2, -1, -1, -1, -1, -1, -1, -1 },
	{ 1, 5, 8, 1, 8, 0, 5, 6, 8, 3, 8, 2, 6, 2, 8, -1 },
	{ 1, 5, 6, 2, 1, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 1, 3, 6, 1, 6, 10, 3, 8, 6, 5, 6, 9, 8, 9, 6, -1 },
	{ 10, 1, 0, 10, 0, 6, 9, 5, 0, 5, 6, 0, -1, -1, -1, -1 },
	{ 0, 3, 8, 5, 6, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 10, 5, 6, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 11, 5, 10, 7, 5, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 11, 5, 10, 11, 7, 5, 8, 3, 0, -1, -1, -1, -1, -1, -1, -1 },
	{ 5, 11, 7, 5, 10, 11, 1, 9, 0, -1, -1, -1, -1, -1, -1, -1 },
	{ 10, 7, 5, 10, 11, 7, 9, 8, 1, 8, 3, 1, -1, -1, -1, -1 },
	{ 11, 1, 2, 11, 7, 1, 7, 5, 1, -1, -1, -1, -1, -1, -1, -1 },
	{ 0, 8, 3, 1, 2, 7, 1, 7, 5, 7, 2, 11, -1, -1, -1, -1 },
	{ 9, 7, 5, 9, 2, 7, 9, 0, 2, 2, 11, 7, -1, -1, -1, -1 },
	{ 7, 5, 2, 7, 2, 11, 5, 9, 2, 3, 2, 8, 9, 8, 2, -1 },
	{ 2, 5, 10, 2, 3, 5, 3, 7, 5, -1, -1, -1, -1, -1, -1, -1 },
	{ 8, 2, 0, 8, 5, 2, 8, 7, 5, 10, 2, 5, -1, -1, -1, -1 },
	{ 9, 0, 1, 5, 10, 3, 5, 3, 7, 3, 10, 2, -1, -1, -1, -1 },
	{ 9, 8, 2, 9, 2, 1, 8, 7, 2, 10, 2, 5, 7, 5, 2, -1 },
	{ 1, 3, 5, 3, 7, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 0, 8, 7, 0, 7, 1, 1, 7, 5, -1, -1, -1, -1, -1, -1, -1 },
	{ 9, 0, 3, 9, 3, 5, 5, 3, 7, -1, -1, -1, -1, -1, -1, -1 },
	{ 9, 8, 7, 5, 9, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 5, 8, 4, 5, 10, 8, 10, 11, 8, -1, -1, -1, -1, -1, -1, -1 },
	{ 5, 0, 4, 5, 11, 0, 5, 10, 11, 11, 3, 0, -1, -1, -1, -1 },
	{ 0, 1, 9, 8, 4, 10, 8, 10, 11, 10, 4, 5, -1, -1, -1, -1 },
	{ 10, 11, 4, 10, 4, 5, 11, 3, 4, 9, 4, 1, 3, 1, 4, -1 },
	{ 2, 5, 1, 2, 8, 5, 2, 11, 8, 4, 5, 8, -1, -1, -1, -1 },
	{ 0, 4, 11, 0, 11, 3, 4, 5, 11, 2, 11, 1, 5, 1, 11, -1 },
	{ 0, 2, 5, 0, 5, 9, 2, 11, 5, 4, 5, 8, 11, 8, 5, -1 },
	{ 9, 4, 5, 2, 11, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 2, 5, 10, 3, 5, 2, 3, 4, 5, 3, 8, 4, -1, -1, -1, -1 },
	{ 5, 10, 2, 5, 2, 4, 4, 2, 0, -1, -1, -1, -1, -1, -1, -1 },
	{ 3, 10, 2, 3, 5, 10, 3, 8, 5, 4, 5, 8, 0, 1, 9, -1 },
	{ 5, 10, 2, 5, 2, 4, 1, 9, 2, 9, 4, 2, -1, -1, -1, -1 },
	{ 8, 4, 5, 8, 5, 3, 3, 5, 1, -1, -1, -1, -1, -1, -1, -1 },
	{ 0, 4, 5, 1, 0, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 8, 4, 5, 8, 5, 3, 9, 0, 5, 0, 3, 5, -1, -1, -1, -1 },
	{ 9, 4, 5, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 4, 11, 7, 4, 9, 11, 9, 10, 11, -1, -1, -1, -1, -1, -1, -1 },
	{ 0, 8, 3, 4, 9, 7, 9, 11, 7, 9, 10, 11, -1, -1, -1, -1 },
	{ 1, 10, 11, 1, 11, 4, 1, 4, 0, 7, 4, 11, -1, -1, -1, -1 },
	{ 3, 1, 4, 3, 4, 8, 1, 10, 4, 7, 4, 11, 10, 11, 4, -1 },
	{ 4, 11, 7, 9, 11, 4, 9, 2, 11, 9, 1, 2, -1, -1, -1, -1 },
	{ 9, 7, 4, 9, 11, 7, 9, 1, 11, 2, 11, 1, 0, 8, 3, -1 },
	{ 11, 7, 4, 11, 4, 2, 2, 4, 0, -1, -1, -1, -1, -1, -1, -1 },
	{ 11, 7, 4, 11, 4, 2, 8, 3, 4, 3, 2, 4, -1, -1, -1, -1 },
	{ 2, 9, 10, 2, 7, 9, 2, 3, 7, 7, 4, 9, -1, -1, -1, -1 },
	{ 9, 10, 7, 9, 7, 4, 10, 2, 7, 8, 7, 0, 2, 0, 7, -1 },
	{ 3, 7, 10, 3, 10, 2, 7, 4, 10, 1, 10, 0, 4, 0, 10, -1 },
	{ 1, 10, 2, 8, 7, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 4, 9, 1, 4, 1, 7, 7, 1, 3, -1, -1, -1, -1, -1, -1, -1 },
	{ 4, 9, 1, 4, 1, 7, 0, 8, 1, 8, 7, 1, -1, -1, -1, -1 },
	{ 4, 0, 3, 7, 4, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 4, 8, 7, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 9, 10, 8, 10, 11, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 3, 0, 9, 3, 9, 11, 11, 9, 10, -1, -1, -1, -1, -1, -1, -1 },
	{ 0, 1, 10, 0, 10, 8, 8, 10, 11, -1, -1, -1, -1, -1, -1, -1 },
	{ 3, 1, 10, 11, 3, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 1, 2, 11, 1, 11, 9, 9, 11, 8, -1, -1, -1, -1, -1, -1, -1 },
	{ 3, 0, 9, 3, 9, 11, 1, 2, 9, 2, 11, 9, -1, -1, -1, -1 },
	{ 0, 2, 11, 8, 0, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 3, 2, 11, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 2, 3, 8, 2, 8, 10, 10, 8, 9, -1, -1, -1, -1, -1, -1, -1 },
	{ 9, 10, 2, 0, 9, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 2, 3, 8, 2, 8, 10, 0, 1, 8, 1, 10, 8, -1, -1, -1, -1 },
	{ 1, 10, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 1, 3, 8, 9, 1, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 0, 9, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ 0, 3, 8, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 },
	{ -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 }
};




Iso3D::Iso3D(){
	gsysType == PM3::SYSCARTESIAN;
	Oprime[0] = (double)0.0;
	Oprime[1] = (double)0.0;
	Oprime[2] = (double)800.0;
	D = 460;
	isSunk = 0;
	MatGen.unit();
	MatRot.unit();
	MatRotSave.unit();
	type = 1;//volume
	NbPointIsoMap = 0;
	NbTriangleIsoSurface = 0;

	morph_param = 1;
	step = 0.05;
	yreso = 1.0;
	ImplicitFunction = "1-((1/2)^2*(x^2 + y^2 + z^2) )-6- ((1/2)^8 *((x^8 + y^8 + z^8) )^6)";
	ImplicitFunction = "x^4 - x^3 + y^2 + z^2";
	ImplicitFunction = "x^4 + y^4 + z^4 -1";
	ImplicitFunction = "x*x + y*y + z*z - 1";
	IsoCondition = "step(1,x)";//(x^2 + y^2 > 0.05) & ( x+y+z > -1)";
	IsoConditionRequired = 1;
	//ImplicitFunction ="cos(x*y) - z^2";
	//ImplicitFunction ="cos(x)*sin(y) - z";
	//ImplicitFunction ="4*x*exp(-x^2-y^2) -z";

	limitSup.setValue("4,4,4");
	limitInf.setValue("-4,-4,-4");

	Start = vcg::Point3d(-4, -4, -4);
	End = vcg::Point3d(4, 4, 4);

	nb_ligne = nb_colon = nb_depth = VSIZE;
	IsoValue = 0;

	backsurfr = 249;
	backsurfg = 170;
	backsurfb = 0;

	frontsurfr = 0;
	frontsurfg = 210;
	frontsurfb = 0;

	CNDsurfr = 210;
	CNDsurfg = 0;
	CNDsurfb = 0;
	CutLigne = CutDepth = CutColon = 0;
	fronttrans = backtrans = CNDtrans = -1;

	NbPolygonImposedLimit = 99000;
	DrawAxe_Ok = -1;

	gridr = 0;
	gridg = 100;
	gridb = 4;
	gridtransparent = 1;
	IsoMesh = -1;
	IsoInfos = 1; /// To show infos
	Borderlimite = 0;

	CNDMesh = 1; CNDDraw = 1; BorderDraw = 1;

	axe_width = 2;
	axe_size = 1;
	axe_center = 1;

	PovActivate = -1; /// To save the shape for the output file
	hauteur_fenetre = 650;
	demi_hauteur = demi_largeur = hauteur_fenetre / 2;

	for (int i = 0; i < 10000; i++)
		tableaureferences[i].resize(3);// = new std::vector<QPoint>(3);

	tableau = new IsoTriangle[10000];

	InitParser();
};

///+++++++++++++++++++++++++++++++++++++++++
bool Iso3D::ParseExpression() {
	std::string er;
	double vals[] = { 0, 0, 0, 0, 0, 0 };
	std::vector<std::string> list;
	list = PM3::split(ImplicitFunction, ';');//list = ImplicitFunction.split(";");
	if (list.size() > 1)
	{
		ImplicitFunction = list.at(0);
		IsoCondition = list.at(1);
		IsoConditionRequired = 1;
	}
	else if (list.size() == 1)
	{
		ImplicitFunction = list.at(0);
		IsoCondition = "1";
		IsoConditionRequired = -1;
	}
	else
		return false;

	if (ImplicitFunction == "")
		return false;
	if (IsoCondition == "")
	{
		IsoCondition = "1";
		IsoConditionRequired = -1;
	}

	//ImplicitFunctionParser.Parse(std::string((const char *)(ImplicitFunction.toLocal8Bit())), "x,y,z,t");
	//pValParser->Parse(std::string((const char *)(IsoCondition.toLocal8Bit())), "x,y,z,t");
	if (pValParser->ParseExp(IsoCondition, er, gsysType == PM3::SYSCARTESIAN ? "x,y,z" : "r,phi,z") != -1)
		return false;

	if (!limitSup.Parser(pValParser, End, er) ||
		!limitInf.Parser(pValParser, Start, er))
		return false;
	if (gsysType == PM3::SYSCARTESIAN)
	{
		/*vcg::Point3d dit = (End - Start) / (VSIZE - 4);
		Start = Start - dit;
		End = End + dit;
		boost::format fmt("if(x=%2%,0,if(x=%3%,0,if(y=%4%,0,if(y=%5%,0,if(z=%6%,0,if(z=%7%,0,%1%))))))");
		fmt%ImplicitFunction% Start[0] % End[0] % Start[1] % End[1] % Start[2] % End[2];
		ImplicitFunction = fmt.str();*/
		;
	}
	/*else {
	Start = PM3::cyl2car(Start);
	End = PM3::cyl2car(End);

	vcg::Point3d dit = (End - Start) / 20.;
	Start = Start - dit;
	End = End + dit;
	boost::format fmt("if(x=%2%,0,if(x=%3%,0,if(y=%4%,0,if(y=%5%,0,if(z=%6%,0,if(z=%7%,0,%1%))))))");
	fmt%ImplicitFunction% Start[0] % End[0] % Start[1] % End[1] % Start[2] % End[2];
	ImplicitFunction = fmt.str();
	}*/
	else {
		/*vcg::Point3d dit = (End - Start) / (VSIZE - 4);
		if (yreso > 0) dit[1] = yreso;
		else dit[1] = 0;
		Start = Start - dit;
		if (Start[0] < 0) Start[0] = 0;
		//if (Start[1] < 0) Start[1] = 0;
		//if (Start[1] > 2 * M_PI) Start[1] = 2 * M_PI;
		End = End + dit;
		if (End[0] < 0) End[0] = 0;
		//if (End[1] < 0) End[1] = 0;
		//if (End[1] > 2 * M_PI) End[1] = 2 * M_PI;		*/
		//		boost::format fmt("if(r=%2%,0,if(r=%3%,0,if(phi=%4%,0,if(phi=%5%,0,if(z=%6%,0,if(z=%7%,0,%1%))))))");
		//		fmt%ImplicitFunction% Start[0] % End[0] % Start[1] % End[1] % Start[2] % End[2];
		//		ImplicitFunction = fmt.str();
		;
	}
	/*		boost::format fmt("if(r=%2%,0,if(r=%3%,0,if(phi=%4%,0,if(phi=%5%,0,if(z=%6%,0,if(z=%7%,0,%1%))))))");
	fmt%ImplicitFunction% Start[0] % End[0] % Start[1] % End[1] % Start[2] % End[2];
	ImplicitFunction = fmt.str();*/
	if ((pValParser->ParseExp(ImplicitFunction, er, gsysType == PM3::SYSCARTESIAN ? "x,y,z" : "r,phi,z") != -1))
		return false;

	//       pValParser->ParseExp(XlimitSup);//std::string((const char *)(XlimitSup.toLocal8Bit())), "x,y,z,t");
	//       X_Start = valParser.Eval(vals);

	//       valParser.ParseExp(YlimitSup);//std::string((const char *)(YlimitSup.toLocal8Bit())), "x,y,z,t");
	//       Y_Start = valParser.Eval(vals);

	//       valParser.ParseExp(ZlimitSup);//std::string((const char *)(ZlimitSup.toLocal8Bit())), "x,y,z,t");
	//       Z_Start = valParser.Eval(vals);

	//       valParser.ParseExp(XlimitInf);//std::string((const char *)(XlimitInf.toLocal8Bit())), "x,y,z,t");
	//       X_End = valParser.Eval(vals);

	//       valParser.ParseExp(YlimitInf);//std::string((const char *)(YlimitInf.toLocal8Bit())), "x,y,z,t");
	//       Y_End = valParser.Eval(vals);

	//       valParser.ParseExp(ZlimitInf);//std::string((const char *)(ZlimitInf.toLocal8Bit())), "x,y,z,t");
	//       Z_End = valParser.Eval(vals);
	return true;
};


///+++++++++++++++++++++++++++++++++++++++++
void Iso3D::InitParser(){
	pValParser = 0;
};

///+++++++++++++++++++++++++++++++++++++++++
bool Iso3D::ComputeIsoMap()
{
	if (!ParseExpression()) return false;
	VoxelEvaluation();
	SaveIsoMapUnifColor();
	PointEdgeComputation();
	SignatureComputation();
	ConstructIsoSurface();
	//ConstructIsoNormale();

	return true;
}

///+++++++++++++++++++++++++++++++++++++++++
void Iso3D::ConstructIsoNormale()
{
	double val1, val2, val3, val4, val5, val6;
	vcg::Point3d pt1, pt2, pt3;
	int IndexFirstPoint, IndexSecondPoint, IndexThirdPoint;

	if (gsysType == PM3::SYSCYLINDRICAL)
	{
		for (i = 0; i < NbPointIsoMap; i++)
		{
			double *p = IsoPointMapOriginal[i].V();
			vcg::Point3d out;
			out = PM3::cyl2car(IsoPointMapOriginal[i]);
			p[0] = out[0];
			p[1] = out[1];
			p[2] = out[2];
		}
	}

	for (i = 0; i<NbTriangleIsoSurface; ++i)
	{
		IndexFirstPoint = IsoSurfaceTriangleListe[i].X();
		IndexSecondPoint = IsoSurfaceTriangleListe[i].Y();
		IndexThirdPoint = IsoSurfaceTriangleListe[i].Z();

		pt1 = IsoPointMapOriginal[IndexFirstPoint];
		pt2 = IsoPointMapOriginal[IndexSecondPoint];
		pt3 = IsoPointMapOriginal[IndexThirdPoint];

		val1 = pt2.Y() - pt1.Y();
		val2 = pt3.Z() - pt1.Z();
		val3 = pt2.Z() - pt1.Z();
		val4 = pt3.Y() - pt1.Y();
		val5 = pt3.X() - pt1.X();
		val6 = pt2.X() - pt1.X();

		NormOriginal[i] = vcg::Point3d(val1*val2 - val3*val4,
			val3*val5 - val6*val2,
			val6*val4 - val1*val5);
		NormOriginal[i].Normalize();
	}
};


///+++++++++++++++++++++++++++++++++++++++++
Iso3D::~Iso3D()
{
	delete[] tableau;
	//for (i=0; i < 10000; i++)  {delete  tableaureferences[i];};
}



///++++++++++++++++++++ ConstructIsoSurface +++++++++++++++++++++++++++

void Iso3D::ConstructIsoSurface()
{
#define TOL 1.0e-6
	int IndexNbTriangle, Alfa, Index, IndexPoint, IndexFirstPoint,
		IndexSeconPoint, IndexThirdPoint,
		IndexAprime, IndexBprime, IndexCprime;
	vcg::Point3d  Aprime, Bprime, Cprime, Diff;
	// DiffX, DiffY, DiffZ;

	NbTriangleIsoSurface = 0;
	NbPointIsoMapCND = 0;
	NbTriangleIsoSurfaceCND = 0;

	if (true)//IsoConditionRequired == -1)
	{
		for (i = 0; i < nb_ligne; i++)
			for (j = 0; j < nb_colon; j++)
				for (k = 0; k < nb_depth; k++)
					//for (i = 0; i < nb_ligne - 1 - CutLigne; i++)
					//for (k = 0; k < nb_depth - 1 - CutDepth; k++)
					//for (j = 0; j < nb_colon - 1 - CutColon; j++)
				{
					Index = GridVoxel[i][j][k].Signature;
					for (l = 0; triTable[Index][l] != -1 && NbTriangleIsoSurface < NbPolygonImposedLimit; l += 3)
					{
						//                if(i==0 || i==nb_ligne-1)
						//                {
						//                    IndexFirstPoint = GridVoxel[i][j][k].Edge_Points[triTable[Index][l]];
						//                    IndexThirdPoint = GridVoxel[i][j][k].Edge_Points[triTable[Index][l + 1]];
						//                    IndexSeconPoint = GridVoxel[i][j][k].Edge_Points[triTable[Index][l + 2]];
						//                }
						//                else
						{
							IndexFirstPoint = GridVoxel[i][j][k].Edge_Points[triTable[Index][l]];
							IndexSeconPoint = GridVoxel[i][j][k].Edge_Points[triTable[Index][l + 1]];
							IndexThirdPoint = GridVoxel[i][j][k].Edge_Points[triTable[Index][l + 2]];
						}
						if (IndexFirstPoint != -20 && IndexSeconPoint != -20 && IndexThirdPoint != -20)
						{
							IsoSurfaceTriangleListe[NbTriangleIsoSurface] = vcg::Point3i(IndexFirstPoint,
								IndexSeconPoint,
								IndexThirdPoint);
							TypeIsoSurfaceTriangleListeCND[NbTriangleIsoSurface] = 1; /// Normals Triangles
							NbTriangleIsoSurface++;
						}
					}
				}
	}
	//    /// Here we have to compute some missing points...
	else
		for (i = 0; i < nb_ligne - 1 - CutLigne; i++)
			for (k = 0; k < nb_depth - 1 - CutDepth; k++)
				for (j = 0; j < nb_colon - 1 - CutColon; j++)
				{
					Index = GridVoxel[i][j][k].Signature;
					for (l = 0; triTable[Index][l] != -1 && NbTriangleIsoSurface < NbPolygonImposedLimit; l += 3) {
						IndexFirstPoint = GridVoxel[i][j][k].Edge_Points[triTable[Index][l]];
						IndexSeconPoint = GridVoxel[i][j][k].Edge_Points[triTable[Index][l + 1]];
						IndexThirdPoint = GridVoxel[i][j][k].Edge_Points[triTable[Index][l + 2]];
						if (IndexFirstPoint != -20 && IndexSeconPoint != -20 && IndexThirdPoint != -20){
							///++++++++++++++++First Case +++++++++++++++++++++++++++++++++++++++++++///
							/// All points verifient the condition
							if (WichPointVeryCond[IndexFirstPoint] * WichPointVeryCond[IndexSeconPoint] * WichPointVeryCond[IndexThirdPoint] != 0) {
								IsoSurfaceTriangleListe[NbTriangleIsoSurface] = vcg::Point3i(IndexFirstPoint, IndexSeconPoint, IndexThirdPoint);
								///All points in this triangle verify the condition. Type = 1
								/// There is no new Isopoints to Add.
								TypeIsoSurfaceTriangleListeCND[NbTriangleIsoSurface] = 1;
								NbTriangleIsoSurface++;
							}/// End if(WichPointVeryCond[IndexFirstPoint]...
							///+++++++++++++++++ Second Case ++++++++++++++++++++++++++++++++++++++++++///
							/// All points don't verify the condition
							else if (WichPointVeryCond[IndexFirstPoint] == 0 &&
								WichPointVeryCond[IndexSeconPoint] == 0 &&
								WichPointVeryCond[IndexThirdPoint] == 0) {
								IsoSurfaceTriangleListe[NbTriangleIsoSurface] = vcg::Point3i(IndexFirstPoint, IndexSeconPoint, IndexThirdPoint);
								///All points in this triangle verify the condition. Type = 0
								/// There is no new Isopoints to Add.
								TypeIsoSurfaceTriangleListeCND[NbTriangleIsoSurface] = 0;
								NbTriangleIsoSurface++;
							}
							///++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++///
							/// We still have 6 cases to treat here
							else {
								if (WichPointVeryCond[IndexFirstPoint] == 0) {
									if (WichPointVeryCond[IndexSeconPoint] == 0){
										if (WichPointVeryCond[IndexThirdPoint] != 0){
											///  First Case : A == 0; B == 0; C != 0
											/// Compute 2 points : Aprime and Bprime
											/// Aprime
											Aprime = IsoPointMapOriginal[IndexThirdPoint];
											Diff = (IsoPointMapOriginal[IndexFirstPoint] - IsoPointMapOriginal[IndexThirdPoint]) / 10.;
											Alfa = 0;
											while ((this->pValParser->Eval(Aprime.V())> TOL) && (Alfa < 10)) {
												Aprime += Diff;
												Alfa += 1;
											}
											/// Bprime
											Bprime = IsoPointMapOriginal[IndexThirdPoint];
											Diff = (IsoPointMapOriginal[IndexSeconPoint] - IsoPointMapOriginal[IndexThirdPoint]) / 10.;
											Alfa = 0;
											while ((this->pValParser->Eval(Bprime.V()) > TOL) && (Alfa < 10)) {
												Bprime += Diff;
												Alfa += 1;
											}
											///+++++++++++++++++++++++++///
											/// Save theses points  and the triangles here
											/// We have to new points to add

											/// Add Aprime
											IsoPointMapOriginal[NbPointIsoMap] = Aprime;
											IndexAprime = NbPointIsoMap;
											NbPointIsoMap++;

											/// Add Bprime
											IsoPointMapOriginal[NbPointIsoMap] = Bprime;
											IndexBprime = NbPointIsoMap;
											NbPointIsoMap++;

											/// Add two new triangles :
											///(Aprime, Bprime,C)
											IsoSurfaceTriangleListe[NbTriangleIsoSurface] = vcg::Point3i(IndexAprime, IndexBprime, IndexThirdPoint);
											TypeIsoSurfaceTriangleListeCND[NbTriangleIsoSurface] = 1;
											NbTriangleIsoSurface++;

											///(A, B, Bprime)
											IsoSurfaceTriangleListe[NbTriangleIsoSurface] = vcg::Point3i(IndexFirstPoint, IndexSeconPoint, IndexBprime);
											TypeIsoSurfaceTriangleListeCND[NbTriangleIsoSurface] = 0;
											NbTriangleIsoSurface++;

											///(A, Bprime, Aprime)
											IsoSurfaceTriangleListe[NbTriangleIsoSurface] = vcg::Point3i(IndexFirstPoint, IndexBprime, IndexAprime);
											TypeIsoSurfaceTriangleListeCND[NbTriangleIsoSurface] = 0;
											NbTriangleIsoSurface++;

											///(Aprime, Bprime)
											IsoSurfaceTriangleListe[NbTriangleIsoSurface] = vcg::Point3i(IndexAprime, IndexBprime, IndexBprime);
											TypeIsoSurfaceTriangleListeCND[NbTriangleIsoSurface] = 4;
											NbTriangleIsoSurface++;
											///+++++++++++++++++++++++++///
										} /// End of if(WichPointVeryCond[IndexThirdPoint] != 0)...
									}/// End of if(WichPointVeryCond[IndexSeconPoint] == 0)
									else {
										/// Second case : A == 0; B != 0; C == 0;
										if (WichPointVeryCond[IndexThirdPoint] == 0){
											/// Aprime
											Aprime = IsoPointMapOriginal[IndexSeconPoint];
											Diff = (IsoPointMapOriginal[IndexFirstPoint] - IsoPointMapOriginal[IndexSeconPoint]) / 10.;
											Alfa = 0;
											while (this->pValParser->Eval(Aprime.V())>TOL && (Alfa < 10))
											{
												Aprime += Diff;
												//std::cout <<DiffX <<", X = "<< Aprime[0] <<"\n";
												Alfa += 1;
											}
											/// Cprime
											Cprime = IsoPointMapOriginal[IndexSeconPoint];
											Diff = (IsoPointMapOriginal[IndexThirdPoint] - IsoPointMapOriginal[IndexSeconPoint]) / 10;
											Alfa = 0;
											while (this->pValParser->Eval(Cprime.V()) > TOL && (Alfa < 10)) {
												Cprime += Diff;
												Alfa += 1;
											}

											///+++++++++++++++++++++++++///
											/// Save theses points  and the triangle here

											/// Add Aprime
											IsoPointMapOriginal[NbPointIsoMap] = Aprime;
											NbPointIsoMap++;

											/// Add Cprime
											IsoPointMapOriginal[NbPointIsoMap] = Cprime;
											NbPointIsoMap++;

											/// Add Three new triangles :
											IndexAprime = (NbPointIsoMap - 2);
											IndexCprime = (NbPointIsoMap - 1);

											///(Aprime, B, Cprime)
											IsoSurfaceTriangleListe[NbTriangleIsoSurface] = vcg::Point3i(IndexAprime, IndexSeconPoint, IndexCprime);
											TypeIsoSurfaceTriangleListeCND[NbTriangleIsoSurface] = 1;
											NbTriangleIsoSurface++;

											/// (A , Aprime, Cprime)
											IsoSurfaceTriangleListe[NbTriangleIsoSurface] = vcg::Point3i(IndexFirstPoint, IndexAprime, IndexCprime);
											TypeIsoSurfaceTriangleListeCND[NbTriangleIsoSurface] = 0;
											NbTriangleIsoSurface++;

											/// (A, Cprime, C)
											IsoSurfaceTriangleListe[NbTriangleIsoSurface] = vcg::Point3i(IndexFirstPoint, IndexCprime, IndexThirdPoint);
											TypeIsoSurfaceTriangleListeCND[NbTriangleIsoSurface] = 0;
											NbTriangleIsoSurface++;

											/// (Aprime, Cprime) --> The border
											IsoSurfaceTriangleListe[NbTriangleIsoSurface] = vcg::Point3i(IndexAprime, IndexCprime, IndexCprime);
											TypeIsoSurfaceTriangleListeCND[NbTriangleIsoSurface] = 4;
											NbTriangleIsoSurface++;
											///+++++++++++++++++++++++++///
										}
										/// Thid Case : : A == 0; B != 0; C != 0;
										else {
											/// Bprime
											Bprime = IsoPointMapOriginal[IndexSeconPoint];
											Diff = (IsoPointMapOriginal[IndexFirstPoint] - IsoPointMapOriginal[IndexSeconPoint]) / 10.;
											Alfa = 0;
											while (this->pValParser->Eval(Bprime.V()) > TOL && (Alfa < 10)) {
												Bprime += Diff;
												Alfa += 1;
											}

											/// Cprime

											Cprime = IsoPointMapOriginal[IndexThirdPoint];
											Diff = (IsoPointMapOriginal[IndexFirstPoint] - IsoPointMapOriginal[IndexThirdPoint]) / 10;
											Alfa = 0;
											while (this->pValParser->Eval(Cprime.V()) > TOL && (Alfa < 10)) {
												Cprime += Diff;
												Alfa += 1;
											}
											///+++++++++++++++++++++++++///
											/// Save theses points  and the triangle here
											/// Add Bprime
											IsoPointMapOriginal[NbPointIsoMap] = Bprime;
											NbPointIsoMap++;

											/// Add Cprime
											IsoPointMapOriginal[NbPointIsoMap] = Cprime;
											NbPointIsoMap++;

											/// Add Three new triangles :
											IndexBprime = (NbPointIsoMap - 2);
											IndexCprime = (NbPointIsoMap - 1);

											/// (A, Bprime, Cprime)
											IsoSurfaceTriangleListe[NbTriangleIsoSurface] = vcg::Point3i(IndexFirstPoint, IndexBprime, IndexCprime);
											TypeIsoSurfaceTriangleListeCND[NbTriangleIsoSurface] = 0;
											NbTriangleIsoSurface++;

											/// (Bprime, B, C)
											IsoSurfaceTriangleListe[NbTriangleIsoSurface] = vcg::Point3i(IndexBprime, IndexSeconPoint, IndexThirdPoint);
											TypeIsoSurfaceTriangleListeCND[NbTriangleIsoSurface] = 1;
											NbTriangleIsoSurface++;

											/// (Bprime, C, Cprime)
											IsoSurfaceTriangleListe[NbTriangleIsoSurface] = vcg::Point3i(IndexBprime, IndexThirdPoint, IndexCprime);
											TypeIsoSurfaceTriangleListeCND[NbTriangleIsoSurface] = 1;
											NbTriangleIsoSurface++;

											/// (Bprime, Cprime)
											IsoSurfaceTriangleListe[NbTriangleIsoSurface] = vcg::Point3i(IndexBprime, IndexCprime, IndexCprime);
											TypeIsoSurfaceTriangleListeCND[NbTriangleIsoSurface] = 4;
											NbTriangleIsoSurface++;

											///+++++++++++++++++++++++++///
										}
									}
								}
								else {
									/// Fourth Case : A != 0; B == 0, C == 0
									if (WichPointVeryCond[IndexSeconPoint] == 0 && WichPointVeryCond[IndexThirdPoint] == 0) {
										/// Bprime
										Bprime = IsoPointMapOriginal[IndexFirstPoint];
										Diff = (IsoPointMapOriginal[IndexSeconPoint] - IsoPointMapOriginal[IndexFirstPoint]) / 10;
										Alfa = 0;
										while (this->pValParser->Eval(Bprime.V()) == 1 && (Alfa < 10)) {
											Bprime += Diff;
											Alfa += 1;
										}

										/// Cprime

										Cprime = IsoPointMapOriginal[IndexFirstPoint];
										Diff = (IsoPointMapOriginal[IndexThirdPoint] - IsoPointMapOriginal[IndexFirstPoint]) / 10;
										Alfa = 0;
										while (this->pValParser->Eval(Cprime.V()) > TOL && (Alfa < 10)) {
											Cprime += Diff;
											Alfa += 1;
										}
										///+++++++++++++++++++++++++///
										/// Save theses points  and the triangle here
										/// Add Bprime
										IsoPointMapOriginal[NbPointIsoMap] = Bprime;
										NbPointIsoMap++;

										/// Add Cprime
										IsoPointMapOriginal[NbPointIsoMap] = Cprime;
										NbPointIsoMap++;


										/// Add Three new triangles :
										IndexBprime = (NbPointIsoMap - 2);
										IndexCprime = (NbPointIsoMap - 1);

										/// (A, Bprime, Cprime)
										IsoSurfaceTriangleListe[NbTriangleIsoSurface] = vcg::Point3i(IndexFirstPoint, IndexBprime, IndexCprime);
										TypeIsoSurfaceTriangleListeCND[NbTriangleIsoSurface] = 1;
										NbTriangleIsoSurface++;

										/// (Bprime, B, C)
										IsoSurfaceTriangleListe[NbTriangleIsoSurface] = vcg::Point3i(IndexBprime, IndexSeconPoint, IndexThirdPoint);
										TypeIsoSurfaceTriangleListeCND[NbTriangleIsoSurface] = 0;
										NbTriangleIsoSurface++;

										/// (Bprime, C, Cprime)
										IsoSurfaceTriangleListe[NbTriangleIsoSurface] = vcg::Point3i(IndexBprime, IndexThirdPoint, IndexCprime);
										TypeIsoSurfaceTriangleListeCND[NbTriangleIsoSurface] = 0;
										NbTriangleIsoSurface++;

										/// (Bprime, Cprime) --> the border
										IsoSurfaceTriangleListe[NbTriangleIsoSurface] = vcg::Point3i(IndexBprime, IndexCprime, IndexCprime);
										TypeIsoSurfaceTriangleListeCND[NbTriangleIsoSurface] = 4; /// Type = 4-->Border
										NbTriangleIsoSurface++;
										///+++++++++++++++++++++++++///
									}
									/// Fifth Case : A != 0; B == 0, C != 0
									/// We generate Two Triangles
									else if (WichPointVeryCond[IndexSeconPoint] == 0 && WichPointVeryCond[IndexThirdPoint] != 0) {
										/// Aprime :
										Aprime = IsoPointMapOriginal[IndexFirstPoint];
										Diff = (IsoPointMapOriginal[IndexSeconPoint] - IsoPointMapOriginal[IndexFirstPoint]) / 10;
										Alfa = 0;
										while (this->pValParser->Eval(Aprime.V())> TOL && (Alfa < 10)) {
											Aprime += Diff;
											Alfa += 1;
										}

										/// Cprime
										Cprime = IsoPointMapOriginal[IndexThirdPoint];
										Diff = (IsoPointMapOriginal[IndexSeconPoint] - IsoPointMapOriginal[IndexThirdPoint]) / 10;
										Alfa = 0;
										while (this->pValParser->Eval(Cprime.V()) > TOL && (Alfa < 10)) {
											Cprime += Diff;
											Alfa += 1;
										}
										///+++++++++++++++++++++++++///
										/// Save theses points  and the triangle here
										/// Save theses points  and the triangle here
										/// Add Aprime
										IsoPointMapOriginal[NbPointIsoMap] = Aprime;
										NbPointIsoMap++;

										/// Add Cprime
										IsoPointMapOriginal[NbPointIsoMap] = Cprime;
										NbPointIsoMap++;


										/// Add Three new triangles :
										IndexAprime = (NbPointIsoMap - 2);
										IndexCprime = (NbPointIsoMap - 1);

										/// (B, Cprime, Aprime)
										IndexNbTriangle = NbTriangleIsoSurface * 3;
										IsoSurfaceTriangleListe[NbTriangleIsoSurface] = vcg::Point3i(IndexSeconPoint, IndexCprime, IndexAprime);
										TypeIsoSurfaceTriangleListeCND[NbTriangleIsoSurface] = 0;
										NbTriangleIsoSurface++;

										/// (Aprime, Cprime, C)
										IndexNbTriangle = NbTriangleIsoSurface * 3;
										IsoSurfaceTriangleListe[NbTriangleIsoSurface] = vcg::Point3i(IndexAprime, IndexCprime, IndexThirdPoint);
										TypeIsoSurfaceTriangleListeCND[NbTriangleIsoSurface] = 1;
										NbTriangleIsoSurface++;

										/// (Aprime, C, A)
										IndexNbTriangle = NbTriangleIsoSurface * 3;
										IsoSurfaceTriangleListe[NbTriangleIsoSurface] = vcg::Point3i(IndexAprime, IndexThirdPoint, IndexFirstPoint);
										TypeIsoSurfaceTriangleListeCND[NbTriangleIsoSurface] = 1;
										NbTriangleIsoSurface++;

										/// (Aprime, Cprime)
										IndexNbTriangle = NbTriangleIsoSurface * 3;
										IsoSurfaceTriangleListe[NbTriangleIsoSurface] = vcg::Point3i(IndexAprime, IndexCprime, IndexCprime);
										TypeIsoSurfaceTriangleListeCND[NbTriangleIsoSurface] = 4;
										NbTriangleIsoSurface++;

										///+++++++++++++++++++++++++///
									}
									/// Sixth Case : A != 0; B != 0, C == 0
									/// We generate Two Triangles
									else if (WichPointVeryCond[IndexSeconPoint] != 0 && WichPointVeryCond[IndexThirdPoint] == 0) {
										/// Aprime

										Aprime = IsoPointMapOriginal[IndexFirstPoint];
										Diff = (IsoPointMapOriginal[IndexThirdPoint] - IsoPointMapOriginal[IndexFirstPoint]) / 10;
										Alfa = 0;
										while (this->pValParser->Eval(Aprime.V()) > TOL && (Alfa < 10)) {
											Aprime += Diff;
											Alfa += 1;
										}
										/// Bprime
										Bprime = IsoPointMapOriginal[IndexSeconPoint];
										Diff = (IsoPointMapOriginal[IndexThirdPoint] - IsoPointMapOriginal[IndexSeconPoint]) / 10;
										Alfa = 0;
										while (this->pValParser->Eval(Bprime.V()) > TOL && (Alfa < 10)) {
											Bprime += Diff;
											Alfa += 1;
										}
										///+++++++++++++++++++++++++///
										/// Save theses points  and the triangle here
										/// Add Aprime
										IsoPointMapOriginal[NbPointIsoMap] = Aprime;
										NbPointIsoMap++;

										/// Add Bprime
										IsoPointMapOriginal[NbPointIsoMap] = Bprime;
										NbPointIsoMap++;
										/// Add Three new triangles :
										IndexAprime = (NbPointIsoMap - 2);
										IndexBprime = (NbPointIsoMap - 1);

										/// (Aprime, Bprime, C)
										IndexNbTriangle = NbTriangleIsoSurface * 3;
										IsoSurfaceTriangleListe[NbTriangleIsoSurface] = vcg::Point3i(IndexAprime, IndexBprime, IndexThirdPoint);
										TypeIsoSurfaceTriangleListeCND[NbTriangleIsoSurface] = 0;
										NbTriangleIsoSurface++;

										/// (A, B, Bprime)
										IsoSurfaceTriangleListe[NbTriangleIsoSurface] = vcg::Point3i(IndexFirstPoint, IndexSeconPoint, IndexBprime);
										TypeIsoSurfaceTriangleListeCND[NbTriangleIsoSurface] = 1;
										NbTriangleIsoSurface++;

										/// (A, Bprime, Aprime)
										IsoSurfaceTriangleListe[NbTriangleIsoSurface] = vcg::Point3i(IndexFirstPoint, IndexBprime, IndexAprime);
										TypeIsoSurfaceTriangleListeCND[NbTriangleIsoSurface] = 1;
										NbTriangleIsoSurface++;

										/// (Aprime, Bprime)
										IsoSurfaceTriangleListe[NbTriangleIsoSurface] = vcg::Point3i(IndexAprime, IndexBprime, IndexBprime);
										TypeIsoSurfaceTriangleListeCND[NbTriangleIsoSurface] = 4;
										NbTriangleIsoSurface++;
										///+++++++++++++++++++++++++///
									}
								}
							}/// End if if(IndexFirstPoint != -20...
						}
					}
				}
}


/*if (gsysType != PM3::SYSCARTESIAN)
Step[0] = (End[0] - Start[0]) / (nb_ligne - 2);
else
Step[0] = (End[0] - Start[0]) / (nb_ligne - 2 - 1);
Step[1] = (End[1] - Start[1]) / (nb_colon - 2 - 1);
Step[2] = (End[2] - Start[2]) / (nb_depth - 2 - 1);
if (gsysType != PM3::SYSCARTESIAN)
for (i = 0; i < nb_ligne; i++) XLocal[i] = Start[0] + (i - 0)*Step[0];
else
for (i = 0; i < nb_ligne; i++) XLocal[i] = Start[0] + (i - 1)*Step[0];
for (j = 0; j < nb_colon; j++) YLocal[j] = Start[1] + (j - 1)*Step[1];
for (k = 0; k < nb_depth; k++) ZLocal[k] = Start[2] + (k - 1)*Step[2];*/
/*std::string json =
"{\n"
"    \"MathModels\": [\n"
"        {\n"
"            \"Iso3D\": {\n"
"                \"Cnd\": [\n"
"                    \"\"\n"
"                ],\n"
"                \"Component\": [\n"
"                    \"Model\"\n"
"                ],\n"
"                \"Fxyz\": [\n"
"                    \"if(r=%2%,1,if(r=%3%,1,if(phi=%4%,1,if(phi=%5%,1,if(z=%6%,1,if(z=%7%,1,%1%))))))\"\n"
"                ],\n"
"                \"Name\": [\n"
"                    \"Model\"\n"
"                ],\n"
"                \"Xmax\": [\n"
"                    \"%3%\"\n"
"                ],\n"
"                \"Xmin\": [\n"
"                    \"%2%\"\n"
"                ],\n"
"                \"Ymax\": [\n"
"                    \"%5%\"\n"
"                ],\n"
"                \"Ymin\": [\n"
"                    \"%4%\"\n"
"                ],\n"
"                \"Zmax\": [\n"
"                    \"%7%\"\n"
"                ],\n"
"                \"Zmin\": [\n"
"                    \"%6%\"\n"
"                ]\n"
"            }\n"
"        }\n"
"    ]\n"
"}\n";
boost::format fmt(json);
fmt%ImplicitFunction% XLocal[0] % XLocal[nb_ligne - 1] % YLocal[1] % YLocal[nb_colon - 1] % ZLocal[1] % ZLocal[nb_depth-1];
//fmt%ImplicitFunction% Start[0] % End[0] % Start[1] % End[1] % Start[2] % End[2];
ImplicitFunction = fmt.str();
std::string er;
if ((pValParser->ParseExp(ImplicitFunction, er, gsysType == PM3::SYSCARTESIAN ? "x,y,z" : "r,phi,z") != -1))
return;*/
/*std::string iso;
if (gsysType == PM3::SYSCARTESIAN)
iso = "x > %1% & x < %2% & y > %3% & y < %4% & z > %5% & z < %6%";
else
iso = "r > %1% & r < %2% & phi > %3% & phi < %4% & z > %5% & z < %6%";
boost::format fmt(iso);
fmt% XLocal[0] % XLocal[nb_ligne - 1] % YLocal[1] % YLocal[nb_colon - 1] % ZLocal[1] % ZLocal[nb_depth - 1];
IsoCondition = fmt.str();*/
/*if (gsysType == PM3::SYSCYLINDRICAL && yreso > 0)
{
vcg::Point3d in(vals), out;
out = PM3::cyl2car(in);
vals[0] = out[0];
vals[1] = out[1];
vals[2] = out[2];
}*/
///+++++++++++++++++++++++++++++++++++++++++
void Iso3D::VoxelEvaluation()
{
	/// this is for the morph effect...
	//	if (morph_param >= 0.0)  vals[3] = morph_param;
	//	else  vals[3] = -morph_param;
	morph_param += step;
	if (morph_param == 1) morph_param = 0;
	if (gsysType != PM3::SYSCARTESIAN && yreso > 0) {
		yreso = 10. * M_PI / 180.;
		nb_colon = (End[1] - Start[1]) / yreso + 0.5;
		if (nb_colon > VSIZE) nb_colon = VSIZE;
		if (nb_colon < 2) nb_colon = 2;
	}
	//Can be optimised by considering Three array of 30 values each
	// Each array contain the 30 value of one axe...
	//        Step[0] = (Start[0] - End[0]) / (nb_ligne - 1-2);
	//        Step[1] = (Start[1] - End[1]) / (nb_colon - 1-2);
	//        Step[2] = (Start[2] - End[2]) / (nb_depth - 1-2);
	//        for (i = 0; i < nb_ligne; i++) XLocal[i] = Start[0] - (i-1)*Step[0];
	//        for (j = 0; j < nb_colon; j++) YLocal[j] = Start[1] - (j-1)*Step[1];
	//        for (k = 0; k < nb_depth; k++) ZLocal[k] = Start[2] - (k-1)*Step[2];

	if (gsysType != PM3::SYSCARTESIAN) {
		Step[0] = (End[0] - Start[0]) / (nb_ligne - 1);
		Step[1] = (End[1] - Start[1]) / (nb_colon - 0 - 1);
		Step[2] = (End[2] - Start[2]) / (nb_depth - 1);

		for (i = 0; i < nb_ligne; i++) XLocal[i] = Start[0] + (i - 0)*Step[0];
		for (j = 0; j < nb_colon; j++) YLocal[j] = Start[1] + (j - 0)*Step[1];
		for (k = 0; k < nb_depth; k++) ZLocal[k] = Start[2] + (k - 0)*Step[2];
	}
	else {
		Step[0] = (End[0] - Start[0]) / (nb_ligne - 1);
		Step[1] = (End[1] - Start[1]) / (nb_colon - 0 - 1);
		Step[2] = (End[2] - Start[2]) / (nb_depth - 1);

		for (i = 0; i < nb_ligne; i++) XLocal[i] = Start[0] + (i - 0)*Step[0];
		for (j = 0; j < nb_colon; j++) YLocal[j] = Start[1] + (j - 0)*Step[1];
		for (k = 0; k < nb_depth; k++) ZLocal[k] = Start[2] + (k - 0)*Step[2];
	}

	//#pragma omp parallel for
	for (int i = 0; i<nb_ligne; i++) {
		double vals[] = { 0, 0, 0, 0 };
		for (j = 0; j<nb_colon; j++) {

			for (k = 0; k<nb_depth; k++) {
				vals[0] = XLocal[i];
				vals[1] = YLocal[j];
				vals[2] = ZLocal[k];
				GridVoxel[i][j][k].Value = pValParser->Eval(vals);
				if (!isfinite(GridVoxel[i][j][k].Value)) {
					GridVoxel[i][j][k].Value = 0;
				}
				GridVoxel[i][j][k].Signature = 0; // Signature initialisation
				GridVoxel[i][j][k].NbEdgePoint = 0; // No EdgePoint yet!
				GridVoxel[i][j][k].Index[0] = i;
				GridVoxel[i][j][k].Index[1] = j;
				GridVoxel[i][j][k].Index[2] = k;

				for (l = 0; l<12; l++)
					GridVoxel[i][j][k].Edge_Points[l] = -20; /// just for verification



				GridVoxel[i][j][k].PositionX = vals[0];
				GridVoxel[i][j][k].PositionY = vals[1];
				GridVoxel[i][j][k].PositionZ = vals[2];
			}
		}
	}
	if (type == 12) {
		for (i = 0; i == 0; i++) {

			for (j = 0; j < nb_colon; j++) {

				for (k = 0; k < nb_depth; k++) {
					if (GridVoxel[i][j][k].Value < 0)
					{
						//GridVoxel[i][j][k].Value = -GridVoxel[i+1][j][k].Value;//pValParser->Eval(vals);
						//GridVoxel[i+1][j][k].Value = 0;
						GridVoxel[i][j][k].Value = 0;
					}
				}
			}
		}
		for (i = nb_ligne - 1; i == nb_ligne - 1; i++) {

			for (j = 0; j < nb_colon; j++) {

				for (k = 0; k < nb_depth; k++) {
					if (GridVoxel[i][j][k].Value < 0)
					{
						//GridVoxel[i][j][k].Value = -GridVoxel[i-1][j][k].Value;//pValParser->Eval(vals);
						//GridVoxel[i-1][j][k].Value = 0;
						GridVoxel[i][j][k].Value = 0;
					}
				}
			}
		}
		j = 0;
		for (i = 0; i < nb_ligne; i++) {

			{

				for (k = 0; k < nb_depth; k++) {
					if (GridVoxel[i][j][k].Value < 0)
					{
						//GridVoxel[i][j][k].Value = -GridVoxel[i][j+1][k].Value;//pValParser->Eval(vals);
						//GridVoxel[i][j+1][k].Value = 0;
						GridVoxel[i][j][k].Value = 0;
					}
				}
			}
		}
		j = nb_colon - 1;
		for (i = 0; i < nb_ligne; i++) {

			{

				for (k = 0; k < nb_depth; k++) {
					if (GridVoxel[i][j][k].Value < 0)
					{
						//GridVoxel[i][j][k].Value = -GridVoxel[i][j-1][k].Value;//pValParser->Eval(vals);
						//GridVoxel[i][j-1][k].Value = 0;
						GridVoxel[i][j][k].Value = 0;
					}
				}
			}
		}
		k = 0;
		for (i = 0; i < nb_ligne; i++) {

			for (j = 0; j < nb_colon; j++) {

				{
					if (GridVoxel[i][j][k].Value < 0)
					{
						//GridVoxel[i][j][k].Value = -GridVoxel[i][j][k+1].Value;//pValParser->Eval(vals);
						//GridVoxel[i][j][k+1].Value = 0;
						GridVoxel[i][j][k].Value = 0;
					}
				}
			}
		}
		k = nb_depth - 1;
		for (i = 0; i < nb_ligne; i++) {

			for (j = 0; j < nb_colon; j++) {
				{
					if (GridVoxel[i][j][k].Value < 0)
					{
						//GridVoxel[i][j][k].Value = -GridVoxel[i][j][k-1].Value;//pValParser->Eval(vals);
						//GridVoxel[i][j][k-1].Value = 0;
						GridVoxel[i][j][k].Value = 0;
					}
				}
			}
		}
	}
	int cutIndex[6] = { 0, 0, 0, 0, 0, 0 };
	{//计算相切
		for (i = 0; i < nb_ligne; i++) {//xmin
			for (j = 0; j < nb_colon; j++) {
				for (k = 0; k < nb_depth; k++) {
					if (GridVoxel[i][j][k].Value < 0)
					{
						cutIndex[0] = i;
						if (i > 0) cutIndex[0] = i - 1;
						i = nb_ligne;
						j = nb_colon;
						k = nb_depth;
						break;
					}
				}
			}
		}
		for (i = nb_ligne - 1; i >= 0; i--) {//xmax
			for (j = 0; j < nb_colon; j++) {
				for (k = 0; k < nb_depth; k++) {
					if (GridVoxel[i][j][k].Value < 0)
					{
						cutIndex[1] = i;
						if (i < nb_ligne - 1) cutIndex[1] = i + 1;
						i = -1;
						j = nb_colon;
						k = nb_depth;
						break;
					}
				}
			}
		}
		for (j = 0; j < nb_colon; j++) {////ymin
			for (i = 0; i < nb_ligne; i++) {
				for (k = 0; k < nb_depth; k++) {
					if (GridVoxel[i][j][k].Value < 0)
					{
						cutIndex[2] = j;
						if (j > 0) cutIndex[2] = j - 1;
						i = nb_ligne;
						j = nb_colon;
						k = nb_depth;
						break;
					}
				}
			}
		}
		for (j = nb_colon - 1; j >= 0; j--) {////ymax
			for (i = 0; i < nb_ligne; i++) {
				for (k = 0; k < nb_depth; k++) {
					if (GridVoxel[i][j][k].Value < 0)
					{
						cutIndex[3] = j;
						if (j < nb_colon - 1) cutIndex[3] = j + 1;
						i = nb_ligne;
						j = -1;
						k = nb_depth;
						break;
					}
				}
			}
		}
		for (k = 0; k < nb_depth; k++) {////zmin
			for (i = 0; i < nb_ligne; i++) {
				for (j = 0; j < nb_colon; j++) {
					if (GridVoxel[i][j][k].Value < 0)
					{
						cutIndex[4] = k;
						if (k > 0) cutIndex[4] = k - 1;
						i = nb_ligne;
						j = nb_colon;
						k = nb_depth;
						break;
					}
				}
			}
		}
		for (k = nb_depth - 1; k >= 0; k--) {////zmax
			for (i = 0; i < nb_ligne; i++) {
				for (j = 0; j < nb_colon; j++) {
					if (GridVoxel[i][j][k].Value < 0)
					{
						cutIndex[5] = k;
						if (k < nb_depth - 1) cutIndex[5] = k + 1;
						i = nb_ligne;
						j = nb_colon;
						k = -1;
						break;
					}
				}
			}
		}
	}
	if ((cutIndex[0] == cutIndex[1]) || (cutIndex[2] == cutIndex[3]) || (cutIndex[4] == cutIndex[5])) {
		nb_depth = nb_colon = nb_ligne = 0;
		return;
	}
	std::string json;
	if (gsysType != PM3::SYSCARTESIAN)
	{
		double ss = 0.1 * M_PI / 180.;
		int offset = 1, offset2 = 2, xoffset = 0;
		double slocal[3] = { XLocal[cutIndex[0]], YLocal[cutIndex[2]], ZLocal[cutIndex[4]] };// - (0.00001 * M_PI / 180.)
		double elocal[3] = { XLocal[cutIndex[1]], YLocal[cutIndex[3]], ZLocal[cutIndex[5]] };// + (0.00001 * M_PI / 180.)
		{
			double vals[] = { XLocal[cutIndex[1]], YLocal[cutIndex[2]] - (ss), ZLocal[cutIndex[4]] };
			double temp = pValParser->Eval(vals);
			if (temp > 0)
				slocal[1] += (ss);
			else
				slocal[1] -= (ss);
		}
		{
			double vals[] = { XLocal[cutIndex[1]], YLocal[cutIndex[3]] + (ss), ZLocal[cutIndex[5]] };
			double temp = pValParser->Eval(vals);
			if (temp > 0)
				elocal[1] -= (ss);
			else
				elocal[1] += (ss);
		}
		if (slocal[0] > Start[0]) Start[0] = slocal[0];
		if (slocal[1] > Start[1]) Start[1] = slocal[1];
		if (slocal[2] > Start[2]) Start[2] = slocal[2];
		if (elocal[0] < End[0]) End[0] = elocal[0];
		if (elocal[1] < End[1]) End[1] = elocal[1];
		if (elocal[2] < End[2]) End[2] = elocal[2];
		vcg::Point3d m = End - Start;
		double mx = fabs(m[0]);
		double my = fabs(m[1]);
		double mz = fabs(m[2]);
		double mm = max(mx, max(my, mz));
		double s = 0.01;// mm / 8 + 0.000001;
		nb_ligne = mx / s + 0.5, nb_colon = my / s + 0.5, nb_depth = mz / s + 0.5;
		if (gsysType != PM3::SYSCARTESIAN)
			nb_colon = my / (10. * M_PI / 180.) + 0.5;
		if (nb_ligne > 8) nb_ligne = 8;
		if (nb_colon > 8) nb_colon = 8;
		if (nb_depth > 8) nb_depth = 8;
		if (nb_ligne < 2) nb_ligne = 2;
		if (nb_colon < 2) nb_colon = 2;
		if (nb_depth < 2) nb_depth = 2;
		nb_ligne += (xoffset + offset2);
		nb_colon += (offset + offset2);
		nb_depth += (offset + offset2);
		Step[0] = (elocal[0] - slocal[0]) / (nb_ligne - offset2 - xoffset);
		//POLOR下面的if是在极坐标下稳定的版本
		if (isSunk != 0) {
			if (Step[0] > slocal[0]) {
				//nb_ligne -= xoffset;
				xoffset = 0;

				Step[0] = (elocal[0] - slocal[0]) / (nb_ligne - offset2 - xoffset);
			}
		}
		Step[1] = (elocal[1] - slocal[1]) / (nb_colon - offset - offset2);
		Step[2] = (elocal[2] - slocal[2]) / (nb_depth - offset - offset2);

		for (i = 0; i < nb_ligne; i++) {
			XLocal[i] = slocal[0] + (i - xoffset)*Step[0];
			//if (fabs(XLocal[i]) < 0.000001) XLocal[i] = Step[0] / 100;
		}
		for (j = 0; j < nb_colon; j++) {
			YLocal[j] = slocal[1] + (j - offset)*Step[1];
			//if (fabs(YLocal[j]) < 0.000001) YLocal[j] = Step[1] / 100;
		}
		for (k = 0; k < nb_depth; k++) {
			ZLocal[k] = slocal[2] + (k - offset)*Step[2];
			//if (fabs(ZLocal[k]) < 0.000001) ZLocal[k] = Step[2] / 100;
		}
		json = "if(r=%2%,1,if(r=%3%,1,if(phi=%4%,1,if(phi=%5%,1,if(z=%6%,1,if(z=%7%,1,%1%))))))";
	}
	else
	{		
		int offset = 1, offset2 = 2, xoffset = 1;
		double slocal[3] = { XLocal[cutIndex[0]], YLocal[cutIndex[2]], ZLocal[cutIndex[4]] };
		double elocal[3] = { XLocal[cutIndex[1]], YLocal[cutIndex[3]], ZLocal[cutIndex[5]] };
		if (slocal[0] > Start[0]) Start[0] = slocal[0];
		if (slocal[1] > Start[1]) Start[1] = slocal[1];
		if (slocal[2] > Start[2]) Start[2] = slocal[2];
		if (elocal[0] < End[0]) End[0] = elocal[0];
		if (elocal[1] < End[1]) End[1] = elocal[1];
		if (elocal[2] < End[2]) End[2] = elocal[2];
		vcg::Point3d m = End - Start;
		double mx = fabs(m[0]);
		double my = fabs(m[1]);
		double mz = fabs(m[2]);
		double mm = max(mx, max(my, mz));
		double s = 0.01;// mm / 8 + 0.000001;
		nb_ligne = mx / s + 0.5, nb_colon = my / s + 0.5, nb_depth = mz / s + 0.5;
		if (gsysType != PM3::SYSCARTESIAN)
			nb_colon = my / (10. * M_PI / 180.) + 0.5;
		if (nb_ligne > DISTANCE_RESOL_MAX) nb_ligne = DISTANCE_RESOL_MAX;
		if (nb_colon > DISTANCE_RESOL_MAX) nb_colon = DISTANCE_RESOL_MAX;
		if (nb_depth > DISTANCE_RESOL_MAX) nb_depth = DISTANCE_RESOL_MAX;
		if (nb_ligne < DISTANCE_RESOL_MIN) nb_ligne = DISTANCE_RESOL_MIN;
		if (nb_colon < DISTANCE_RESOL_MIN) nb_colon = DISTANCE_RESOL_MIN;
		if (nb_depth < DISTANCE_RESOL_MIN) nb_depth = DISTANCE_RESOL_MIN;
		nb_ligne += (offset + offset2);
		nb_colon += (offset + offset2);
		nb_depth += (offset + offset2);
		Step[0] = (elocal[0] - slocal[0]) / (nb_ligne - offset - offset2);
		Step[1] = (elocal[1] - slocal[1]) / (nb_colon - offset - offset2);
		Step[2] = (elocal[2] - slocal[2]) / (nb_depth - offset - offset2);

		for (i = 0; i < nb_ligne; i++)  {
			XLocal[i] = slocal[0] + (i - offset)*Step[0];
			//if (fabs(XLocal[i]) < 0.000001) XLocal[i] = Step[0] / 100;
		}
		for (j = 0; j < nb_colon; j++) {
			YLocal[j] = slocal[1] + (j - offset)*Step[1];
			//if (fabs(YLocal[j]) < 0.000001) YLocal[j] = Step[1] / 100;
		}
		for (k = 0; k < nb_depth; k++) {
			ZLocal[k] = slocal[2] + (k - offset)*Step[2];
			//if (fabs(ZLocal[k]) < 0.000001) ZLocal[k] = Step[2] / 100;
		}
		json = "if(x=%2%,1,if(x=%3%,1,if(y=%4%,1,if(y=%5%,1,if(z=%6%,1,if(z=%7%,1,%1%))))))";
	}
	//boost::format fmt(json);
	//fmt%ImplicitFunction% XLocal[0] % XLocal[nb_ligne - 1] % YLocal[0] % YLocal[nb_colon - 1] % ZLocal[0] % ZLocal[nb_depth - 1];
	//fmt%ImplicitFunction% Start[0] % End[0] % Start[1] % End[1] % Start[2] % End[2];
	//ImplicitFunction = fmt.str();
	//std::string er;
	//if ((pValParser->ParseExp(ImplicitFunction, er, gsysType == PM3::SYSCARTESIAN ? "x,y,z" : "r,phi,z") != -1))
	//	return;
	//#pragma omp parallel for
	for (int i = 0; i<nb_ligne; i++) {
		double vals[] = { 0, 0, 0, 0 };
		for (j = 0; j<nb_colon; j++) {
			for (k = 0; k<nb_depth; k++) {
				vals[0] = XLocal[i];
				vals[1] = YLocal[j];
				vals[2] = ZLocal[k];
				GridVoxel[i][j][k].Value = pValParser->Eval(vals);
				if (!isfinite(GridVoxel[i][j][k].Value)) {
					GridVoxel[i][j][k].Value = 0;
				}
				GridVoxel[i][j][k].Signature = 0; // Signature initialisation
				GridVoxel[i][j][k].NbEdgePoint = 0; // No EdgePoint yet!
				GridVoxel[i][j][k].Index[0] = i;
				GridVoxel[i][j][k].Index[1] = j;
				GridVoxel[i][j][k].Index[2] = k;

				for (l = 0; l<12; l++)
					GridVoxel[i][j][k].Edge_Points[l] = -20; /// just for verification

				GridVoxel[i][j][k].PositionX = vals[0];
				GridVoxel[i][j][k].PositionY = vals[1];
				GridVoxel[i][j][k].PositionZ = vals[2];
			}
		}
	}

	if (type == 1) {
		float v = 1;
		//凹陷POLOR下面的if是在极坐标下稳定的版本
		if (isSunk != 0){
			if (gsysType != PM3::SYSCARTESIAN)
				v = 0;
		}
		if (gsysType == PM3::SYSCARTESIAN)
		{
			for (i = 0; i == 0; i++) {

				for (j = 0; j < nb_colon; j++) {

					for (k = 0; k < nb_depth; k++) {
						if (GridVoxel[i][j][k].Value < 0)
						{
							//GridVoxel[i][j][k].Value = -GridVoxel[i+1][j][k].Value;//pValParser->Eval(vals);
							//GridVoxel[i+1][j][k].Value = 0;
							//if (gsysType != PM3::SYSCARTESIAN)
							//	GridVoxel[i][j][k].Value = 0;
							//else
							GridVoxel[i][j][k].Value = v;
						}
					}
				}
			}
		}
		for (i = nb_ligne - 1; i == nb_ligne - 1; i++) {

			for (j = 0; j < nb_colon; j++) {

				for (k = 0; k < nb_depth; k++) {
					if (GridVoxel[i][j][k].Value < 0)
					{
						//GridVoxel[i][j][k].Value = -GridVoxel[i-1][j][k].Value;//pValParser->Eval(vals);
						//GridVoxel[i-1][j][k].Value = 0;
						GridVoxel[i][j][k].Value = v;
					}
				}
			}
		}

		j = 0;
		for (i = 0; i < nb_ligne; i++) {

			{

				for (k = 0; k < nb_depth; k++) {
					if (GridVoxel[i][j][k].Value < 0)
					{
						//GridVoxel[i][j][k].Value = -GridVoxel[i][j+1][k].Value;//pValParser->Eval(vals);
						//GridVoxel[i][j+1][k].Value = 0;
						GridVoxel[i][j][k].Value = v;
					}
				}
			}
		}
		j = nb_colon - 1;
		for (i = 0; i < nb_ligne; i++) {

			{

				for (k = 0; k < nb_depth; k++) {
					if (GridVoxel[i][j][k].Value < 0)
					{
						//GridVoxel[i][j][k].Value = -GridVoxel[i][j-1][k].Value;//pValParser->Eval(vals);
						//GridVoxel[i][j-1][k].Value = 0;
						GridVoxel[i][j][k].Value = v;
					}
				}
			}
		}
		k = 0;
		if (gsysType == PM3::SYSCARTESIAN)
			i = 1;
		else i = 0;
		for (i = 0; i < nb_ligne; i++) {

			for (j = 0; j < nb_colon; j++) {

				{
					if (GridVoxel[i][j][k].Value < 0)
					{
						//GridVoxel[i][j][k].Value = -GridVoxel[i][j][k+1].Value;//pValParser->Eval(vals);
						//GridVoxel[i][j][k+1].Value = 0;
						GridVoxel[i][j][k].Value = v;
					}
				}
			}
		}
		k = nb_depth - 1;
		for (i = 0; i < nb_ligne; i++) {

			for (j = 0; j < nb_colon; j++) {
				{
					if (GridVoxel[i][j][k].Value < 0)
					{
						//GridVoxel[i][j][k].Value = -GridVoxel[i][j][k-1].Value;//pValParser->Eval(vals);
						//GridVoxel[i][j][k-1].Value = 0;
						GridVoxel[i][j][k].Value = v;
					}
				}
			}
		}
	}
};

///+++++++++++++++++++++++++++++++++++++++++
void Iso3D::PointEdgeComputation()
{
	int index, i_Start, i_End, j_Start, j_End, k_Start, k_End;
	double vals[4], IsoValue_1, IsoValue_2, rapport;
	double factor;
	std::string er;
	/// We have to compute the edges for the Grid limits ie: i=0, j=0 and k=0
	NbPointIsoMap = 0;

	i_Start = 1;
	j_Start = 1;
	k_Start = 1;

	i_End = nb_ligne - 1;
	j_End = nb_colon - 1;
	k_End = nb_depth - 1;
	/// The code is doubled to eliminate conditions tests
#define SEL <=

#define EXPP1 (IsoValue_1 * IsoValue_2 SEL 0) && ((rapport = IsoValue_2 - IsoValue_1) != 0) && (IsoValue_1 <= 0 || IsoValue_2 <= 0)
#define EXPP (IsoValue_1 * IsoValue_2 SEL 0) && ((rapport = IsoValue_2 - IsoValue_1) != 0)

	pValParser->ParseExp(IsoCondition, er, gsysType == PM3::SYSCARTESIAN ? "x,y,z" : "r,phi,z");
	for (i = i_Start; i < i_End; i++)
		for (j = j_Start; j < j_End; j++)
			for (k = k_Start; k < k_End; k++)
			{
				IsoValue_1 = GridVoxel[i][j][k].Value;
				/// First Case P(i+1)(j)(k)
				IsoValue_2 = GridVoxel[i + 1][j][k].Value;
				if (IsoConditionRequired == 1 ? EXPP1 : EXPP)
				{
					// Edge Point computation and  save in IsoPointMap
					factor = (IsoValue - IsoValue_1) / rapport;
					index = NbPointIsoMap * 3;
					vals[0] = GridVoxel[i][j][k].PositionX + factor * (GridVoxel[i + 1][j][k].PositionX - GridVoxel[i][j][k].PositionX);
					vals[1] = GridVoxel[i][j][k].PositionY + factor * (GridVoxel[i + 1][j][k].PositionY - GridVoxel[i][j][k].PositionY);
					vals[2] = GridVoxel[i][j][k].PositionZ + factor * (GridVoxel[i + 1][j][k].PositionZ - GridVoxel[i][j][k].PositionZ);
					///===========================================================///
					IsoPointMapOriginal[NbPointIsoMap] = vcg::Point3d(vals[0], vals[1], vals[2]);
					// save The reference to this point
					GridVoxel[i][j][k].Edge_Points[0] = NbPointIsoMap;
					GridVoxel[i][j][k].NbEdgePoint += 1;
					// The same Point is used in three other Voxels
					GridVoxel[i][j - 1][k].Edge_Points[4] = NbPointIsoMap;
					GridVoxel[i][j - 1][k].NbEdgePoint += 1;
					GridVoxel[i][j][k - 1].Edge_Points[2] = NbPointIsoMap;
					GridVoxel[i][j][k - 1].NbEdgePoint += 1;
					GridVoxel[i][j - 1][k - 1].Edge_Points[6] = NbPointIsoMap;
					GridVoxel[i][j - 1][k - 1].NbEdgePoint += 1;
					if (IsoConditionRequired != 1) WichPointVeryCond[NbPointIsoMap] = 1;
					else (pValParser->Eval(vals)>0) ? WichPointVeryCond[NbPointIsoMap] = 1 : WichPointVeryCond[NbPointIsoMap] = 0;

					NbPointIsoMap++;
				}
				///+++++++++++++++++++++++++++++++++++++++++
				/// Second Case P(i)(j+1)(k)
				IsoValue_2 = GridVoxel[i][j + 1][k].Value;
				// Edge Point computation and  save in IsoPointMap
				if (IsoConditionRequired == 1 ? EXPP1 : EXPP) {
					factor = (IsoValue - IsoValue_1) / rapport;
					index = NbPointIsoMap * 3;
					vals[0] = GridVoxel[i][j][k].PositionX + factor * (GridVoxel[i][j + 1][k].PositionX - GridVoxel[i][j][k].PositionX);
					vals[1] = GridVoxel[i][j][k].PositionY + factor * (GridVoxel[i][j + 1][k].PositionY - GridVoxel[i][j][k].PositionY);
					vals[2] = GridVoxel[i][j][k].PositionZ + factor * (GridVoxel[i][j + 1][k].PositionZ - GridVoxel[i][j][k].PositionZ);
					IsoPointMapOriginal[NbPointIsoMap] = vcg::Point3d(vals[0], vals[1], vals[2]);
					// save The reference to this point
					GridVoxel[i][j][k].Edge_Points[8] = NbPointIsoMap;
					GridVoxel[i][j][k].NbEdgePoint += 1;
					// The same Point is used in three other Voxels
					GridVoxel[i - 1][j][k].Edge_Points[9] = NbPointIsoMap;
					GridVoxel[i - 1][j][k].NbEdgePoint += 1;
					GridVoxel[i][j][k - 1].Edge_Points[11] = NbPointIsoMap;
					GridVoxel[i][j][k - 1].NbEdgePoint += 1;
					GridVoxel[i - 1][j][k - 1].Edge_Points[10] = NbPointIsoMap;
					GridVoxel[i - 1][j][k - 1].NbEdgePoint += 1;
					if (IsoConditionRequired != 1) WichPointVeryCond[NbPointIsoMap] = 1;
					else (pValParser->Eval(vals)>0) ? WichPointVeryCond[NbPointIsoMap] = 1 : WichPointVeryCond[NbPointIsoMap] = 0;
					NbPointIsoMap++;
				}

				// Third Case P(i)(j)(k+1)
				IsoValue_2 = GridVoxel[i][j][k + 1].Value;
				// Edge Point computation and  save in IsoPointMap
				if (IsoConditionRequired == 1 ? EXPP1 : EXPP) {
					factor = (IsoValue - IsoValue_1) / rapport;
					index = NbPointIsoMap * 3;
					vals[0] = GridVoxel[i][j][k].PositionX + factor * (GridVoxel[i][j][k + 1].PositionX - GridVoxel[i][j][k].PositionX);
					vals[1] = GridVoxel[i][j][k].PositionY + factor * (GridVoxel[i][j][k + 1].PositionY - GridVoxel[i][j][k].PositionY);
					vals[2] = GridVoxel[i][j][k].PositionZ + factor * (GridVoxel[i][j][k + 1].PositionZ - GridVoxel[i][j][k].PositionZ);
					IsoPointMapOriginal[NbPointIsoMap] = vcg::Point3d(vals[0], vals[1], vals[2]);
					// save The reference to this point
					GridVoxel[i][j][k].Edge_Points[3] = NbPointIsoMap;
					GridVoxel[i][j][k].NbEdgePoint += 1;
					// The same Point is used in three other Voxels
					GridVoxel[i - 1][j][k].Edge_Points[1] = NbPointIsoMap;
					GridVoxel[i - 1][j][k].NbEdgePoint += 1;
					GridVoxel[i][j - 1][k].Edge_Points[7] = NbPointIsoMap;
					GridVoxel[i][j - 1][k].NbEdgePoint += 1;
					GridVoxel[i - 1][j - 1][k].Edge_Points[5] = NbPointIsoMap;
					GridVoxel[i - 1][j - 1][k].NbEdgePoint += 1;
					if (IsoConditionRequired != 1) WichPointVeryCond[NbPointIsoMap] = 1;
					else (pValParser->Eval(vals)>0) ? WichPointVeryCond[NbPointIsoMap] = 1 : WichPointVeryCond[NbPointIsoMap] = 0;
					NbPointIsoMap++;
				}
			}
	//if (type == 1)
	{
		/// Now we have to compute the Grid's limits...
		/// The code is quite big but this is much more easy to compute
		/// 1) First case : i =0;
		i = 0;
		for (j = 0; j < nb_colon; j++)
			for (k = 0; k < nb_depth; k++) {

				IsoValue_1 = GridVoxel[0][j][k].Value;
				// First Case P(1)(j)(k)
				IsoValue_2 = GridVoxel[1][j][k].Value;
				if (IsoConditionRequired == 1 ? EXPP1 : EXPP) {
					// Edge Point computation and  save in IsoPointMap
					factor = (IsoValue - IsoValue_1) / rapport;
					index = NbPointIsoMap * 3;
					vals[0] = GridVoxel[0][j][k].PositionX + factor * (GridVoxel[1][j][k].PositionX - GridVoxel[0][j][k].PositionX);
					vals[1] = GridVoxel[0][j][k].PositionY + factor * (GridVoxel[1][j][k].PositionY - GridVoxel[0][j][k].PositionY);
					vals[2] = GridVoxel[0][j][k].PositionZ + factor * (GridVoxel[1][j][k].PositionZ - GridVoxel[0][j][k].PositionZ);
					IsoPointMapOriginal[NbPointIsoMap] = vcg::Point3d(vals[0], vals[1], vals[2]);
					// save The reference to this point
					GridVoxel[0][j][k].Edge_Points[0] = NbPointIsoMap;
					GridVoxel[0][j][k].NbEdgePoint += 1;
					// The same Point is used in three other Voxels
					if (j != 0){
						GridVoxel[0][j - 1][k].Edge_Points[4] = NbPointIsoMap;
						GridVoxel[0][j - 1][k].NbEdgePoint += 1;
					}
					if (k != 0) {
						GridVoxel[0][j][k - 1].Edge_Points[2] = NbPointIsoMap;
						GridVoxel[0][j][k - 1].NbEdgePoint += 1;
					}
					if (j != 0 && k != 0) {
						GridVoxel[0][j - 1][k - 1].Edge_Points[6] = NbPointIsoMap;
						GridVoxel[0][j - 1][k - 1].NbEdgePoint += 1;
					}
					if (IsoConditionRequired != 1) WichPointVeryCond[NbPointIsoMap] = 1;
					else (pValParser->Eval(vals) > 0) ? WichPointVeryCond[NbPointIsoMap] = 1 : WichPointVeryCond[NbPointIsoMap] = 0;

					NbPointIsoMap++;
				}
				// Second Case P(0)(j+1)(k)
				if (j != (nb_colon - 1)){
					IsoValue_2 = GridVoxel[0][j + 1][k].Value;
					// Edge Point computation and  save in IsoPointMap
					if (IsoConditionRequired == 1 ? EXPP1 : EXPP) {
						factor = (IsoValue - IsoValue_1) / rapport;
						index = NbPointIsoMap * 3;
						vals[0] = GridVoxel[0][j][k].PositionX + factor * (GridVoxel[0][j + 1][k].PositionX - GridVoxel[0][j][k].PositionX);
						vals[1] = GridVoxel[0][j][k].PositionY + factor * (GridVoxel[0][j + 1][k].PositionY - GridVoxel[0][j][k].PositionY);
						vals[2] = GridVoxel[0][j][k].PositionZ + factor * (GridVoxel[0][j + 1][k].PositionZ - GridVoxel[0][j][k].PositionZ);
						IsoPointMapOriginal[NbPointIsoMap] = vcg::Point3d(vals[0], vals[1], vals[2]);
						// save The reference to this point
						GridVoxel[0][j][k].Edge_Points[8] = NbPointIsoMap;
						GridVoxel[0][j][k].NbEdgePoint += 1;
						// The same Point is used in three other Voxels
						if (k != 0){
							GridVoxel[0][j][k - 1].Edge_Points[11] = NbPointIsoMap;
							GridVoxel[0][j][k - 1].NbEdgePoint += 1;
						}
						if (IsoConditionRequired != 1) WichPointVeryCond[NbPointIsoMap] = 1;
						else (pValParser->Eval(vals) > 0) ? WichPointVeryCond[NbPointIsoMap] = 1 : WichPointVeryCond[NbPointIsoMap] = 0;

						NbPointIsoMap++;
					}
				} /// If ( j != nb_colon -1) ...

				// Third Case P(0)(j)(k+1)
				if (k != (nb_depth - 1)){
					IsoValue_2 = GridVoxel[0][j][k + 1].Value;
					// Edge Point computation and  save in IsoPointMap
					if (IsoConditionRequired == 1 ? EXPP1 : EXPP) {
						factor = (IsoValue - IsoValue_1) / rapport;
						index = NbPointIsoMap * 3;
						vals[0] = GridVoxel[0][j][k].PositionX + factor * (GridVoxel[0][j][k + 1].PositionX - GridVoxel[0][j][k].PositionX);
						vals[1] = GridVoxel[0][j][k].PositionY + factor * (GridVoxel[0][j][k + 1].PositionY - GridVoxel[0][j][k].PositionY);
						vals[2] = GridVoxel[0][j][k].PositionZ + factor * (GridVoxel[0][j][k + 1].PositionZ - GridVoxel[0][j][k].PositionZ);
						IsoPointMapOriginal[NbPointIsoMap] = vcg::Point3d(vals[0], vals[1], vals[2]);
						// save The reference to this point
						GridVoxel[0][j][k].Edge_Points[3] = NbPointIsoMap;
						GridVoxel[0][j][k].NbEdgePoint += 1;
						// The same Point is used in three other Voxels
						if (j != 0) {
							GridVoxel[0][j - 1][k].Edge_Points[7] = NbPointIsoMap;
							GridVoxel[0][j - 1][k].NbEdgePoint += 1;
						}
						if (IsoConditionRequired != 1) WichPointVeryCond[NbPointIsoMap] = 1;
						else (pValParser->Eval(vals) > 0) ? WichPointVeryCond[NbPointIsoMap] = 1 : WichPointVeryCond[NbPointIsoMap] = 0;

						NbPointIsoMap++;
					}
				} /// End of ( if ( k != nb_depth -1)....
			}
		/// 2) Case i = nb_ligne-1
		i = nb_ligne - 1;
		for (j = 0; j < nb_colon; j++)
			for (k = 0; k < nb_depth; k++)
			{
				IsoValue_1 = GridVoxel[i][j][k].Value;
				// Second Case P(i)(j+1)(k)
				if (j != (nb_colon - 1)){
					IsoValue_2 = GridVoxel[i][j + 1][k].Value;
					// Edge Point computation and  save in IsoPointMap
					if (IsoConditionRequired == 1 ? EXPP1 : EXPP) {
						factor = (IsoValue - IsoValue_1) / rapport;
						index = NbPointIsoMap * 3;
						vals[0] = GridVoxel[i][j][k].PositionX + factor * (GridVoxel[i][j + 1][k].PositionX - GridVoxel[i][j][k].PositionX);
						vals[1] = GridVoxel[i][j][k].PositionY + factor * (GridVoxel[i][j + 1][k].PositionY - GridVoxel[i][j][k].PositionY);
						vals[2] = GridVoxel[i][j][k].PositionZ + factor * (GridVoxel[i][j + 1][k].PositionZ - GridVoxel[i][j][k].PositionZ);
						IsoPointMapOriginal[NbPointIsoMap] = vcg::Point3d(vals[0], vals[1], vals[2]);
						// save The reference to this point
						GridVoxel[i][j][k].Edge_Points[8] = NbPointIsoMap;
						GridVoxel[i][j][k].NbEdgePoint += 1;
						// The same Point is used in three other Voxels
						if (i != 0){
							GridVoxel[i - 1][j][k].Edge_Points[9] = NbPointIsoMap;
							GridVoxel[i - 1][j][k].NbEdgePoint += 1;
						}
						if (k != 0){
							GridVoxel[i][j][k - 1].Edge_Points[11] = NbPointIsoMap;
							GridVoxel[i][j][k - 1].NbEdgePoint += 1;
						}
						if (i != 0 && k != 0){
							GridVoxel[i - 1][j][k - 1].Edge_Points[10] = NbPointIsoMap;
							GridVoxel[i - 1][j][k - 1].NbEdgePoint += 1;
						}

						if (IsoConditionRequired != 1) WichPointVeryCond[NbPointIsoMap] = 1;
						else (pValParser->Eval(vals) > 0) ? WichPointVeryCond[NbPointIsoMap] = 1 : WichPointVeryCond[NbPointIsoMap] = 0;

						NbPointIsoMap++;

					}
				} /// End of if (j != nb_colon -1)...

				// Third Case P(i)(j)(k+1)
				if (k != (nb_depth - 1)){
					IsoValue_2 = GridVoxel[i][j][k + 1].Value;
					// Edge Point computation and  save in IsoPointMap
					if (IsoConditionRequired == 1 ? EXPP1 : EXPP) {
						factor = (IsoValue - IsoValue_1) / rapport;
						index = NbPointIsoMap * 3;

						vals[0] = GridVoxel[i][j][k].PositionX + factor * (GridVoxel[i][j][k + 1].PositionX - GridVoxel[i][j][k].PositionX);

						vals[1] = GridVoxel[i][j][k].PositionY + factor * (GridVoxel[i][j][k + 1].PositionY - GridVoxel[i][j][k].PositionY);

						vals[2] = GridVoxel[i][j][k].PositionZ + factor * (GridVoxel[i][j][k + 1].PositionZ - GridVoxel[i][j][k].PositionZ);


						IsoPointMapOriginal[NbPointIsoMap] = vcg::Point3d(vals[0], vals[1], vals[2]);

						// save The reference to this point
						GridVoxel[i][j][k].Edge_Points[3] = NbPointIsoMap;
						GridVoxel[i][j][k].NbEdgePoint += 1;

						// The same Point is used in three other Voxels
						if (i != 0) {
							GridVoxel[i - 1][j][k].Edge_Points[1] = NbPointIsoMap;
							GridVoxel[i - 1][j][k].NbEdgePoint += 1;
						}
						if (j != 0) {
							GridVoxel[i][j - 1][k].Edge_Points[7] = NbPointIsoMap;
							GridVoxel[i][j - 1][k].NbEdgePoint += 1;
						}
						if (i != 0 && j != 0) {
							GridVoxel[i - 1][j - 1][k].Edge_Points[5] = NbPointIsoMap;
							GridVoxel[i - 1][j - 1][k].NbEdgePoint += 1;
						}

						if (IsoConditionRequired != 1) WichPointVeryCond[NbPointIsoMap] = 1;
						else (pValParser->Eval(vals) > 0) ? WichPointVeryCond[NbPointIsoMap] = 1 : WichPointVeryCond[NbPointIsoMap] = 0;

						NbPointIsoMap++;

					}
				} /// End of if ( k != nb_depth -1)...
			}
		/// 3) Case j = 0
		j = 0;
		for (i = 0; i < nb_ligne; i++)
			for (k = 0; k < nb_depth; k++)
			{
				IsoValue_1 = GridVoxel[i][0][k].Value;
				// First Case P(i+1)(j)(k)
				if (i != (nb_ligne - 1)){
					IsoValue_2 = GridVoxel[i + 1][0][k].Value;
					if (IsoConditionRequired == 1 ? EXPP1 : EXPP) {

						// Edge Point computation and  save in IsoPointMap
						factor = (IsoValue - IsoValue_1) / rapport;
						index = NbPointIsoMap * 3;

						vals[0] = GridVoxel[i][0][k].PositionX + factor * (GridVoxel[i + 1][0][k].PositionX - GridVoxel[i][0][k].PositionX);

						vals[1] = GridVoxel[i][0][k].PositionY + factor * (GridVoxel[i + 1][0][k].PositionY - GridVoxel[i][0][k].PositionY);

						vals[2] = GridVoxel[i][0][k].PositionZ + factor * (GridVoxel[i + 1][0][k].PositionZ - GridVoxel[i][0][k].PositionZ);


						IsoPointMapOriginal[NbPointIsoMap] = vcg::Point3d(vals[0], vals[1], vals[2]);

						// save The reference to this point
						GridVoxel[i][0][k].Edge_Points[0] = NbPointIsoMap;
						GridVoxel[i][0][k].NbEdgePoint += 1;

						// The same Point is used in three other Voxels
						if (k != 0){
							GridVoxel[i][0][k - 1].Edge_Points[2] = NbPointIsoMap;
							GridVoxel[i][0][k - 1].NbEdgePoint += 1;
						}


						if (IsoConditionRequired != 1) WichPointVeryCond[NbPointIsoMap] = 1;
						else (pValParser->Eval(vals) > 0) ? WichPointVeryCond[NbPointIsoMap] = 1 : WichPointVeryCond[NbPointIsoMap] = 0;

						NbPointIsoMap++;
					}
				} /// End of if ( i != nb_ligne -1)...
				// Second Case P(i)(j+1)(k)
				IsoValue_2 = GridVoxel[i][1][k].Value;
				// Edge Point computation and  save in IsoPointMap
				if (IsoConditionRequired == 1 ? EXPP1 : EXPP) {
					factor = (IsoValue - IsoValue_1) / rapport;
					index = NbPointIsoMap * 3;
					vals[0] = GridVoxel[i][0][k].PositionX + factor * (GridVoxel[i][1][k].PositionX - GridVoxel[i][0][k].PositionX);
					vals[1] = GridVoxel[i][0][k].PositionY + factor * (GridVoxel[i][1][k].PositionY - GridVoxel[i][0][k].PositionY);
					vals[2] = GridVoxel[i][0][k].PositionZ + factor * (GridVoxel[i][1][k].PositionZ - GridVoxel[i][0][k].PositionZ);
					IsoPointMapOriginal[NbPointIsoMap] = vcg::Point3d(vals[0], vals[1], vals[2]);
					// save The reference to this point
					GridVoxel[i][0][k].Edge_Points[8] = NbPointIsoMap;
					GridVoxel[i][0][k].NbEdgePoint += 1;
					// The same Point is used in three other Voxels
					if (i != 0){
						GridVoxel[i - 1][0][k].Edge_Points[9] = NbPointIsoMap;
						GridVoxel[i - 1][0][k].NbEdgePoint += 1;
					}
					if (k != 0){
						GridVoxel[i][0][k - 1].Edge_Points[11] = NbPointIsoMap;
						GridVoxel[i][0][k - 1].NbEdgePoint += 1;
					}
					if (i != 0 && k != 0){
						GridVoxel[i - 1][0][k - 1].Edge_Points[10] = NbPointIsoMap;
						GridVoxel[i - 1][0][k - 1].NbEdgePoint += 1;
					}

					if (IsoConditionRequired != 1) WichPointVeryCond[NbPointIsoMap] = 1;
					else (pValParser->Eval(vals) > 0) ? WichPointVeryCond[NbPointIsoMap] = 1 : WichPointVeryCond[NbPointIsoMap] = 0;

					NbPointIsoMap++;

				}
				// Third Case P(i)(j)(k+1)
				if (k != (nb_depth - 1)){
					IsoValue_2 = GridVoxel[i][0][k + 1].Value;
					// Edge Point computation and  save in IsoPointMap
					if (IsoConditionRequired == 1 ? EXPP1 : EXPP) {
						factor = (IsoValue - IsoValue_1) / rapport;
						index = NbPointIsoMap * 3;

						vals[0] = GridVoxel[i][0][k].PositionX + factor * (GridVoxel[i][0][k + 1].PositionX - GridVoxel[i][0][k].PositionX);

						vals[1] = GridVoxel[i][0][k].PositionY + factor * (GridVoxel[i][0][k + 1].PositionY - GridVoxel[i][0][k].PositionY);

						vals[2] = GridVoxel[i][0][k].PositionZ + factor * (GridVoxel[i][0][k + 1].PositionZ - GridVoxel[i][0][k].PositionZ);


						IsoPointMapOriginal[NbPointIsoMap] = vcg::Point3d(vals[0], vals[1], vals[2]);
						// save The reference to this point
						GridVoxel[i][0][k].Edge_Points[3] = NbPointIsoMap;
						GridVoxel[i][0][k].NbEdgePoint += 1;

						// The same Point is used in three other Voxels
						if (i != 0) {
							GridVoxel[i - 1][0][k].Edge_Points[1] = NbPointIsoMap;
							GridVoxel[i - 1][0][k].NbEdgePoint += 1;
						}

						if (IsoConditionRequired != 1) WichPointVeryCond[NbPointIsoMap] = 1;
						else (pValParser->Eval(vals) > 0) ? WichPointVeryCond[NbPointIsoMap] = 1 : WichPointVeryCond[NbPointIsoMap] = 0;

						NbPointIsoMap++;

					}
				} /// End of if(k != (nb_depth -1))...
			}

		/// 4) Case j = nb_colon -1
		j = nb_colon - 1;
		for (i = 0; i < nb_ligne; i++)
			for (k = 0; k < nb_depth; k++)
			{
				IsoValue_1 = GridVoxel[i][j][k].Value;
				// First Case P(i+1)(j)(k)
				if (i != (nb_ligne - 1)) {
					IsoValue_2 = GridVoxel[i + 1][j][k].Value;
					if (IsoConditionRequired == 1 ? EXPP1 : EXPP) {

						// Edge Point computation and  save in IsoPointMap
						factor = (IsoValue - IsoValue_1) / rapport;
						index = NbPointIsoMap * 3;

						vals[0] = GridVoxel[i][j][k].PositionX + factor * (GridVoxel[i + 1][j][k].PositionX - GridVoxel[i][j][k].PositionX);

						vals[1] = GridVoxel[i][j][k].PositionY + factor * (GridVoxel[i + 1][j][k].PositionY - GridVoxel[i][j][k].PositionY);

						vals[2] = GridVoxel[i][j][k].PositionZ + factor * (GridVoxel[i + 1][j][k].PositionZ - GridVoxel[i][j][k].PositionZ);


						IsoPointMapOriginal[NbPointIsoMap] = vcg::Point3d(vals[0], vals[1], vals[2]);
						// save The reference to this point
						GridVoxel[i][j][k].Edge_Points[0] = NbPointIsoMap;
						GridVoxel[i][j][k].NbEdgePoint += 1;

						// The same Point is used in three other Voxels
						if (j != 0){
							GridVoxel[i][j - 1][k].Edge_Points[4] = NbPointIsoMap;
							GridVoxel[i][j - 1][k].NbEdgePoint += 1;
						}
						if (k != 0){
							GridVoxel[i][j][k - 1].Edge_Points[2] = NbPointIsoMap;
							GridVoxel[i][j][k - 1].NbEdgePoint += 1;
						}
						if (j != 0 && k != 0) {
							GridVoxel[i][j - 1][k - 1].Edge_Points[6] = NbPointIsoMap;
							GridVoxel[i][j - 1][k - 1].NbEdgePoint += 1;
						}

						if (IsoConditionRequired != 1) WichPointVeryCond[NbPointIsoMap] = 1;
						else (pValParser->Eval(vals) > 0) ? WichPointVeryCond[NbPointIsoMap] = 1 : WichPointVeryCond[NbPointIsoMap] = 0;

						NbPointIsoMap++;


					}
				} /// End of if( i != (nb_ligne-1))...

				// Third Case P(i)(j)(k+1)
				if (k != (nb_depth - 1)){
					IsoValue_2 = GridVoxel[i][j][k + 1].Value;
					// Edge Point computation and  save in IsoPointMap
					if (IsoConditionRequired == 1 ? EXPP1 : EXPP) {
						factor = (IsoValue - IsoValue_1) / rapport;
						index = NbPointIsoMap * 3;

						vals[0] = GridVoxel[i][j][k].PositionX + factor * (GridVoxel[i][j][k + 1].PositionX - GridVoxel[i][j][k].PositionX);

						vals[1] = GridVoxel[i][j][k].PositionY + factor * (GridVoxel[i][j][k + 1].PositionY - GridVoxel[i][j][k].PositionY);

						vals[2] = GridVoxel[i][j][k].PositionZ + factor * (GridVoxel[i][j][k + 1].PositionZ - GridVoxel[i][j][k].PositionZ);



						IsoPointMapOriginal[NbPointIsoMap] = vcg::Point3d(vals[0], vals[1], vals[2]);

						// save The reference to this point
						GridVoxel[i][j][k].Edge_Points[3] = NbPointIsoMap;
						GridVoxel[i][j][k].NbEdgePoint += 1;

						// The same Point is used in three other Voxels
						if (i != 0){
							GridVoxel[i - 1][j][k].Edge_Points[1] = NbPointIsoMap;
							GridVoxel[i - 1][j][k].NbEdgePoint += 1;
						}
						if (j != 0){
							GridVoxel[i][j - 1][k].Edge_Points[7] = NbPointIsoMap;
							GridVoxel[i][j - 1][k].NbEdgePoint += 1;
						}
						if (i != 0 && j != 0){
							GridVoxel[i - 1][j - 1][k].Edge_Points[5] = NbPointIsoMap;
							GridVoxel[i - 1][j - 1][k].NbEdgePoint += 1;
						}

						if (IsoConditionRequired != 1) WichPointVeryCond[NbPointIsoMap] = 1;
						else (pValParser->Eval(vals) > 0) ? WichPointVeryCond[NbPointIsoMap] = 1 : WichPointVeryCond[NbPointIsoMap] = 0;
						NbPointIsoMap++;

					}
				} /// End of if (k != nb_depth)...
			}





		/// 5) Case k = 0
		k = 0;
		for (i = 0; i < nb_ligne; i++)
			for (j = 0; j < nb_colon; j++)
			{

				IsoValue_1 = GridVoxel[i][j][0].Value;
				// First Case P(i+1)(j)(k)
				if (i != (nb_ligne - 1)){
					IsoValue_2 = GridVoxel[i + 1][j][0].Value;
					if (IsoConditionRequired == 1 ? EXPP1 : EXPP) {

						// Edge Point computation and  save in IsoPointMap
						factor = (IsoValue - IsoValue_1) / rapport;
						index = NbPointIsoMap * 3;

						vals[0] = GridVoxel[i][j][0].PositionX + factor * (GridVoxel[i + 1][j][0].PositionX - GridVoxel[i][j][0].PositionX);

						vals[1] = GridVoxel[i][j][0].PositionY + factor * (GridVoxel[i + 1][j][0].PositionY - GridVoxel[i][j][0].PositionY);

						vals[2] = GridVoxel[i][j][0].PositionZ + factor * (GridVoxel[i + 1][j][0].PositionZ - GridVoxel[i][j][0].PositionZ);


						IsoPointMapOriginal[NbPointIsoMap] = vcg::Point3d(vals[0], vals[1], vals[2]);
						// save The reference to this point
						GridVoxel[i][j][0].Edge_Points[0] = NbPointIsoMap;
						GridVoxel[i][j][0].NbEdgePoint += 1;

						// The same Point is used in one other Voxel
						if (j != 0){
							GridVoxel[i][j - 1][0].Edge_Points[4] = NbPointIsoMap;
							GridVoxel[i][j - 1][0].NbEdgePoint += 1;
						}

						if (IsoConditionRequired != 1) WichPointVeryCond[NbPointIsoMap] = 1;
						else (pValParser->Eval(vals) > 0) ? WichPointVeryCond[NbPointIsoMap] = 1 : WichPointVeryCond[NbPointIsoMap] = 0;
						NbPointIsoMap++;


					}
				} /// End of if(i != (nb_ligne -1))

				// Second Case P(i)(j+1)(k)
				if (j != nb_colon - 1) {
					IsoValue_2 = GridVoxel[i][j + 1][0].Value;
					// Edge Point computation and  save in IsoPointMap
					if (IsoConditionRequired == 1 ? EXPP1 : EXPP) {
						factor = (IsoValue - IsoValue_1) / rapport;
						index = NbPointIsoMap * 3;

						vals[0] = GridVoxel[i][j][0].PositionX + factor * (GridVoxel[i][j + 1][0].PositionX - GridVoxel[i][j][0].PositionX);

						vals[1] = GridVoxel[i][j][0].PositionY + factor * (GridVoxel[i][j + 1][0].PositionY - GridVoxel[i][j][0].PositionY);

						vals[2] = GridVoxel[i][j][0].PositionZ + factor * (GridVoxel[i][j + 1][0].PositionZ - GridVoxel[i][j][0].PositionZ);


						IsoPointMapOriginal[NbPointIsoMap] = vcg::Point3d(vals[0], vals[1], vals[2]);

						// save The reference to this point
						GridVoxel[i][j][0].Edge_Points[8] = NbPointIsoMap;
						GridVoxel[i][j][0].NbEdgePoint += 1;

						// The same Point is used in one other Voxels
						if (i != 0) {
							GridVoxel[i - 1][j][0].Edge_Points[9] = NbPointIsoMap;
							GridVoxel[i - 1][j][0].NbEdgePoint += 1;
						}

						if (IsoConditionRequired != 1) WichPointVeryCond[NbPointIsoMap] = 1;
						else (pValParser->Eval(vals) > 0) ? WichPointVeryCond[NbPointIsoMap] = 1 : WichPointVeryCond[NbPointIsoMap] = 0;
						NbPointIsoMap++;

					}
				}/// End of if(j != nb_colon -1)...

				// Third Case P(i)(j)(k+1)

				IsoValue_2 = GridVoxel[i][j][1].Value;
				// Edge Point computation and  save in IsoPointMap
				if (IsoConditionRequired == 1 ? EXPP1 : EXPP) {
					factor = (IsoValue - IsoValue_1) / rapport;
					index = NbPointIsoMap * 3;

					vals[0] = GridVoxel[i][j][0].PositionX + factor * (GridVoxel[i][j][1].PositionX - GridVoxel[i][j][0].PositionX);

					vals[1] = GridVoxel[i][j][0].PositionY + factor * (GridVoxel[i][j][1].PositionY - GridVoxel[i][j][0].PositionY);

					vals[2] = GridVoxel[i][j][0].PositionZ + factor * (GridVoxel[i][j][1].PositionZ - GridVoxel[i][j][0].PositionZ);


					IsoPointMapOriginal[NbPointIsoMap] = vcg::Point3d(vals[0], vals[1], vals[2]);
					// save The reference to this point
					GridVoxel[i][j][0].Edge_Points[3] = NbPointIsoMap;
					GridVoxel[i][j][0].NbEdgePoint += 1;

					// The same Point is used in three other Voxels
					if (i != 0) {
						GridVoxel[i - 1][j][0].Edge_Points[1] = NbPointIsoMap;
						GridVoxel[i - 1][j][0].NbEdgePoint += 1;
					}
					if (j != 0) {
						GridVoxel[i][j - 1][0].Edge_Points[7] = NbPointIsoMap;
						GridVoxel[i][j - 1][0].NbEdgePoint += 1;
					}
					if (i != 0 && j != 0) {
						GridVoxel[i - 1][j - 1][0].Edge_Points[5] = NbPointIsoMap;
						GridVoxel[i - 1][j - 1][0].NbEdgePoint += 1;
					}

					if (IsoConditionRequired != 1) WichPointVeryCond[NbPointIsoMap] = 1;
					else (pValParser->Eval(vals) > 0) ? WichPointVeryCond[NbPointIsoMap] = 1 : WichPointVeryCond[NbPointIsoMap] = 0;
					NbPointIsoMap++;

				}
			}

		/// 6) Case k = nb_depth -1
		k = nb_depth - 1;
		for (i = 0; i < nb_ligne; i++)
			for (j = 0; j < nb_colon; j++)
			{
				IsoValue_1 = GridVoxel[i][j][k].Value;
				// First Case P(i+1)(j)(k)
				if (i != (nb_ligne - 1)){
					IsoValue_2 = GridVoxel[i + 1][j][k].Value;
					if (IsoConditionRequired == 1 ? EXPP1 : EXPP) {

						// Edge Point computation and  save in IsoPointMap
						factor = (IsoValue - IsoValue_1) / rapport;
						index = NbPointIsoMap * 3;

						vals[0] = GridVoxel[i][j][k].PositionX + factor * (GridVoxel[i + 1][j][k].PositionX - GridVoxel[i][j][k].PositionX);

						vals[1] = GridVoxel[i][j][k].PositionY + factor * (GridVoxel[i + 1][j][k].PositionY - GridVoxel[i][j][k].PositionY);

						vals[2] = GridVoxel[i][j][k].PositionZ + factor * (GridVoxel[i + 1][j][k].PositionZ - GridVoxel[i][j][k].PositionZ);


						IsoPointMapOriginal[NbPointIsoMap] = vcg::Point3d(vals[0], vals[1], vals[2]);

						// save The reference to this point
						GridVoxel[i][j][k].Edge_Points[0] = NbPointIsoMap;
						GridVoxel[i][j][k].NbEdgePoint += 1;

						// The same Point is used in three other Voxels
						if (j != 0) {
							GridVoxel[i][j - 1][k].Edge_Points[4] = NbPointIsoMap;
							GridVoxel[i][j - 1][k].NbEdgePoint += 1;
						}
						if (k != 0){
							GridVoxel[i][j][k - 1].Edge_Points[2] = NbPointIsoMap;
							GridVoxel[i][j][k - 1].NbEdgePoint += 1;
						}
						if (j != 0 && k != 0) {
							GridVoxel[i][j - 1][k - 1].Edge_Points[6] = NbPointIsoMap;
							GridVoxel[i][j - 1][k - 1].NbEdgePoint += 1;
						}

						if (IsoConditionRequired != 1) WichPointVeryCond[NbPointIsoMap] = 1;
						else (pValParser->Eval(vals) > 0) ? WichPointVeryCond[NbPointIsoMap] = 1 : WichPointVeryCond[NbPointIsoMap] = 0;
						NbPointIsoMap++;


					}
				} /// End of if(i != nb_ligne-1)...

				// Second Case P(i)(j+1)(k)
				if (j != (nb_colon - 1)){
					IsoValue_2 = GridVoxel[i][j + 1][k].Value;
					// Edge Point computation and  save in IsoPointMap
					if (IsoConditionRequired == 1 ? EXPP1 : EXPP) {
						factor = (IsoValue - IsoValue_1) / rapport;
						index = NbPointIsoMap * 3;

						vals[0] = GridVoxel[i][j][k].PositionX + factor * (GridVoxel[i][j + 1][k].PositionX - GridVoxel[i][j][k].PositionX);

						vals[1] = GridVoxel[i][j][k].PositionY + factor * (GridVoxel[i][j + 1][k].PositionY - GridVoxel[i][j][k].PositionY);

						vals[2] = GridVoxel[i][j][k].PositionZ + factor * (GridVoxel[i][j + 1][k].PositionZ - GridVoxel[i][j][k].PositionZ);
						///

						IsoPointMapOriginal[NbPointIsoMap] = vcg::Point3d(vals[0], vals[1], vals[2]);
						// save The reference to this point
						GridVoxel[i][j][k].Edge_Points[8] = NbPointIsoMap;
						GridVoxel[i][j][k].NbEdgePoint += 1;

						// The same Point is used in three other Voxels
						if (i != 0){
							GridVoxel[i - 1][j][k].Edge_Points[9] = NbPointIsoMap;
							GridVoxel[i - 1][j][k].NbEdgePoint += 1;
						}
						if (k != 0){
							GridVoxel[i][j][k - 1].Edge_Points[11] = NbPointIsoMap;
							GridVoxel[i][j][k - 1].NbEdgePoint += 1;
						}
						if (i != 0 && k != 0){
							GridVoxel[i - 1][j][k - 1].Edge_Points[10] = NbPointIsoMap;
							GridVoxel[i - 1][j][k - 1].NbEdgePoint += 1;
						}

						if (IsoConditionRequired != 1) WichPointVeryCond[NbPointIsoMap] = 1;
						else (pValParser->Eval(vals) > 0) ? WichPointVeryCond[NbPointIsoMap] = 1 : WichPointVeryCond[NbPointIsoMap] = 0;
						NbPointIsoMap++;

					}
				} /// End of if( j != (nb_colon -1) )...



			}
	}
};


///+++++++++++++++++++++++++++++++++++++++++++++++++++++///
void Iso3D::SignatureComputation(){

	for (i = 0; i < nb_ligne; i++)
		for (j = 0; j < nb_colon; j++)
			for (k = 0; k < nb_depth; k++)
				/*if (GridVoxel[i][j][k].NbEdgePoint != 0)*/{
					///GridVoxel[i][j][k].Signature =0; /// Done now in
					if (GridVoxel[i][j][k].Value < 0) GridVoxel[i][j][k].Signature += 1;

					if (i != (nb_ligne - 1))
						if (GridVoxel[i + 1][j][k].Value < 0) GridVoxel[i][j][k].Signature += 2;

					if (i != (nb_ligne - 1) && k != (nb_depth - 1))
						if (GridVoxel[i + 1][j][k + 1].Value < 0) GridVoxel[i][j][k].Signature += 4;

					if (k != (nb_depth - 1))
						if (GridVoxel[i][j][k + 1].Value < 0) GridVoxel[i][j][k].Signature += 8;

					if (j != (nb_colon - 1))
						if (GridVoxel[i][j + 1][k].Value < 0) GridVoxel[i][j][k].Signature += 16;

					if (i != (nb_ligne - 1) && j != (nb_colon - 1))
						if (GridVoxel[i + 1][j + 1][k].Value < 0) GridVoxel[i][j][k].Signature += 32;

					if (i != (nb_ligne - 1) && j != (nb_colon - 1) && k != (nb_depth - 1))
						if (GridVoxel[i + 1][j + 1][k + 1].Value < 0) GridVoxel[i][j][k].Signature += 64;

					if (j != (nb_colon - 1) && k != (nb_depth - 1))
						if (GridVoxel[i][j + 1][k + 1].Value < 0) GridVoxel[i][j][k].Signature += 128;
			} // End if(Grid...
}


void Iso3D::SaveIsoMapUnifColor() {
	int ThreeTimesI;
	double pt1_x, pt1_y, pt1_z,
		pt2_x, pt2_y, pt2_z,
		XStep, YStep, ZStep,
		tp1, tp2, tp3,
		X_Val, Y_Val, Z_Val, ray;
	vcg::Point3d temp, vals;


	XStep = fabs((Start[0] - End[0]) / (100 * (nb_ligne - 1)));
	YStep = fabs((Start[1] - End[1]) / (100 * (nb_colon - 1)));
	ZStep = fabs((Start[2] - End[2]) / (100 * (nb_depth - 1)));


	for (i = 0; i < NbPointIsoMap; i++)
	{
		ThreeTimesI = 3 * i;

		/// Normal at this Point :

		X_Val = IsoPointMapOriginal[i].X();
		Y_Val = IsoPointMapOriginal[i].Y();
		Z_Val = IsoPointMapOriginal[i].Z();

		vals[0] = X_Val + XStep;
		vals[1] = Y_Val;
		vals[2] = Z_Val;
		//        if(gsysType == PM3::SYSCYLINDRICAL) {
		//            temp = PM3::car2cyl(vals);
		//            vals = temp;
		//        }
		pt1_x = pValParser->Eval(vals.V());
		vals[0] = X_Val - XStep;
		vals[1] = Y_Val;
		vals[2] = Z_Val;
		//        if(gsysType == PM3::SYSCYLINDRICAL) {
		//            temp = PM3::car2cyl(vals);
		//            vals = temp;
		//        }
		pt2_x = pValParser->Eval(vals.V());
		IsoNormMapOriginal[i].X() = pt1_x - pt2_x;

		vals[0] = X_Val;
		vals[1] = Y_Val + YStep;
		vals[2] = Z_Val;
		//        if(gsysType == PM3::SYSCYLINDRICAL) {
		//            temp = PM3::car2cyl(vals);
		//            vals = temp;
		//        }
		pt1_y = pValParser->Eval(vals.V());
		vals[0] = X_Val;
		vals[1] = Y_Val - YStep;
		vals[2] = Z_Val;
		pt2_y = pValParser->Eval(vals.V());
		IsoNormMapOriginal[i].Y() = pt1_y - pt2_y;

		vals[0] = X_Val;
		vals[1] = Y_Val;
		vals[2] = Z_Val + ZStep;
		//        if(gsysType == PM3::SYSCYLINDRICAL) {
		//            temp = PM3::car2cyl(vals);
		//            vals = temp;
		//        }
		pt1_z = pValParser->Eval(vals.V());
		vals[0] = X_Val;
		vals[1] = Y_Val;
		vals[2] = Z_Val - ZStep;
		//        if(gsysType == PM3::SYSCYLINDRICAL) {
		//            temp = PM3::car2cyl(vals);
		//            vals = temp;
		//        }
		pt2_z = pValParser->Eval(vals.V());
		IsoNormMapOriginal[i].Z() = pt1_z - pt2_z;

		IsoNormMapOriginal[i].Normalize();
	}
}

