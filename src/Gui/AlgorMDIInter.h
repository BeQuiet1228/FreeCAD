#pragma once
#ifndef _ALGORMDIINTER_H_
#define _ALGORMDIINTER_H_
#include "MDIEditView.h"
class AlgorMDIInter :public MDIViewPIC
{
public :
	AlgorMDIInter(DocumentPic* pcDocument, QWidget* parent = 0);
	virtual ~AlgorMDIInter();
	virtual bool isClose();
protected:
	void closeEvent(QCloseEvent* e);
};
#endif