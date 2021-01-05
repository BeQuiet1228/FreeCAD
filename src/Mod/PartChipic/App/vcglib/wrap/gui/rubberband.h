/****************************************************************************
 * MeshLab                                                           o o     *
 * A versatile mesh processing toolbox                             o     o   *
 *                                                                _   O  _   *
 * Copyright(C) 2008                                                \/)\/    *
 * Visual Computing Lab                                            /\/|      *
 * ISTI - Italian National Research Council                           |      *
 *                                                                    \      *
 * All rights reserved.                                                      *
 *                                                                           *
 * This program is free software; you can redistribute it and/or modify      *
 * it under the terms of the GNU General Public License as published by      *
 * the Free Software Foundation; either version 2 of the License, or         *
 * (at your option) any later version.                                       *
 *                                                                           *
 * This program is distributed in the hope that it will be useful,           *
 * but WITHOUT ANY WARRANTY; without even the implied warranty of            *
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             *
 * GNU General Public License (http://www.gnu.org/licenses/gpl.txt)          *
 * for more details.                                                         *
 *                                                                           *
 ****************************************************************************/
/****************************************************************************
  History
$Log: not supported by cvs2svn $
Revision 1.1  2008/02/16 12:00:34  benedetti
first version, adapted from meshlab's editmeasure plugin


****************************************************************************/
#ifndef RUBBERBAND_H
#define RUBBERBAND_H

#include <vcg/space/color4.h>
#include <QGLWidget>

namespace vcg {

/*!
  @brief The Rubberband class.

  This class is useful for interactively draw a straight line between 2 pickable points in a GL widget.
*/
class Rubberband
{
public:
  //data:
  
  /// The color of the rubberband
  Color4b color;
  
  // functions:
  
  Rubberband(Color4b);
  

  virtual ~Rubberband() {}
  

  void Render(QGLWidget* gla);
  

  void Drag(QPoint p,QGLWidget* gla);
  

  void Pin(QPoint cursor,QGLWidget* gla);
  

  void Reset();
  

  bool IsReady();  
  
  
  //void GetPoints(Point3f &startpoint,Point3f &endpoint);
  
 
  //void RenderLabel(QString text,QGLWidget* glw);

private:
  // types:
  typedef enum { RUBBER_BEGIN = 0,
	             RUBBER_DRAGGING = 1,
	             RUBBER_DRAGGED = 2,
	           } RubberPhase;
  // data:  
  RubberPhase currentphase;
  QPoint qt_cursor;
  Point3f start, end;
  QFont font;
  // functions:
  //Point3f PixelConvert(const Point3f);
  
};

}//namespace

#endif /*RUBBERBAND_H*/
