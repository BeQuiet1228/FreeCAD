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

****************************************************************************/

#include <GL/glew.h>
#include <wrap/gl/space.h>
#include <wrap/gl/picking.h>

#include "rubberband.h"

using namespace vcg;

Rubberband::Rubberband(Color4b c)
:color(c),currentphase(RUBBER_BEGIN),qt_cursor(),
start(0,0,0),end(0,0,0),font()
{
  font.setFamily("Helvetica");
  font.setPixelSize(13);
}

void Rubberband::Render(QGLWidget* gla )
{
	glPushAttrib(GL_ALL_ATTRIB_BITS);
	// enable color tracking
	glEnable(GL_COLOR_MATERIAL);

	glDepthFunc(GL_ALWAYS);
	glEnable(GL_DEPTH_TEST); 
	glDepthMask(GL_FALSE);
	glEnable(GL_BLEND);
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
			

	glEnable(GL_LINES);
	glColor4f(0.1f, 0.8f, 0.2f, 1.0f);

	glLineWidth(1.2);			
	glPointSize(4.5);
	glBegin(GL_LINES);
	glVertex(start);
	glVertex(end);
	glEnd();
	glPopAttrib();

}

void Rubberband::Drag(QPoint p,QGLWidget* gla)
{
	if (RUBBER_DRAGGING)
	{
		qt_cursor = p;
		Point3f pick_point;
		bool picked = Pick(qt_cursor.x(), gla->height() - qt_cursor.y(), pick_point);
		if ( picked)
		{
			start = end;
			end = pick_point;
		}
	}
}

void Rubberband::Pin(QPoint p,QGLWidget* gla)
{
  qt_cursor = p;
  Point3f pick_point;
  bool picked = Pick(qt_cursor.x(), gla->height() - qt_cursor.y(), pick_point);
  if(picked)
  { 
	  switch(currentphase)
	  {
	  case RUBBER_BEGIN:
		  start = end = pick_point;
		  currentphase = RUBBER_DRAGGING;
		  //gla->setMouseTracking(true);
		  break;
	  case RUBBER_DRAGGING:
		  if(pick_point==start)  break;
		  start = end;
		  end = pick_point;
		  //gla->setMouseTracking(false);
		  //currentphase = RUBBER_DRAGGED;
		  break;
	  default:
		  break;
	  }
  }
}

void Rubberband::Reset()
{
  currentphase = RUBBER_BEGIN;
  qt_cursor = QPoint();
  start = Point3f(0,0,0);
  end = Point3f(0,0,0);
 // have_to_pick = false;
}

bool Rubberband::IsReady()
{
	return currentphase==RUBBER_DRAGGED;
}

//void Rubberband::GetPoints(Point3f &s,Point3f &e)
//{
//  assert(IsReady());
//  s=start;
//  e=end;
//}
//
//void Rubberband::RenderLabel(QString text,QGLWidget* gla)
//{
//  if(currentphase==RUBBER_BEGIN) return;
//  
//  int x,y;  
//  if(currentphase==RUBBER_DRAGGING){
//  	x=qt_cursor.x()+16;
//  	y=qt_cursor.y()+16;
//  } else {
//    Point3f qt_start = PixelConvert(start);
//    Point3f qt_end   = PixelConvert(end);
//    if(qt_start[0]>qt_end[0]){
//      x=int(qt_start[0]+5);
//      y=int(qt_start[1]);
//    }else{
//      x=int(qt_end[0]+5);
//      y=int(qt_end[1]);
//    }
//  }
//
//  QFontMetrics fm(font);
//  QRect brec=fm.boundingRect(text);
//  glPushAttrib(GL_CURRENT_BIT | GL_DEPTH_BUFFER_BIT | GL_ENABLE_BIT | GL_LINE_BIT );
//  glDisable(GL_LIGHTING);
//  glDisable(GL_TEXTURE_2D);
//  glDisable(GL_DEPTH_TEST);
//  glEnable(GL_BLEND);
//  glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA);
//
//  glMatrixMode(GL_PROJECTION);
//  glPushMatrix();
//  glLoadIdentity();
//  gluOrtho2D(0,gla->width(),gla->height(),0);
//  glMatrixMode(GL_MODELVIEW);
//  glPushMatrix();
//  glLoadIdentity();
//  glColor4f(0,0,0,0.5);
//  glBegin(GL_QUADS);
//    glVertex2f(x+brec.left(),y+brec.bottom());
//    glVertex2f(x+brec.right(),y+brec.bottom());
//    glVertex2f(x+brec.right(),y+brec.top());
//    glVertex2f(x+brec.left(),y+brec.top());
//  glEnd();
//  int offset=2;
//  glColor4f(0,0,0,0.2);
//  glBegin(GL_QUADS);
//    glVertex2f(x+brec.left()-offset,y+brec.bottom()+offset);
//    glVertex2f(x+brec.right()+offset,y+brec.bottom()+offset);
//    glVertex2f(x+brec.right()+offset,y+brec.top()-offset);
//    glVertex2f(x+brec.left()-offset,y+brec.top()-offset);
//  glEnd();
//  glColor3f(1,1,1);
//  gla->renderText(x,y,0.99f,text,font);
//  glGetError();//Due to buggy glrenderText()
//  glMatrixMode(GL_PROJECTION);
//  glPopMatrix();
//  glMatrixMode(GL_MODELVIEW);
//  glPopMatrix();
//  glPopAttrib();
//}
//
//Point3f Rubberband::PixelConvert(const Point3f p)
//{
//  GLint vm[4];
//  GLdouble mm[16];
//  GLdouble pm[16];
//  glGetIntegerv(GL_VIEWPORT, vm);
//  glGetDoublev(GL_MODELVIEW_MATRIX, mm);
//  glGetDoublev(GL_PROJECTION_MATRIX, pm);
//  GLdouble wx,wy,wz;
//  gluProject(p[0], p[1], p[2], mm, pm, vm, &wx, &wy, &wz);
//  return Point3f(wx,vm[3]-wy,wz);
//}
