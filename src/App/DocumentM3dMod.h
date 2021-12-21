#pragma once
//#include "Document.h"
#include "Document.h"
class  DocumentM3dMod :public App::Document{
public:
	DocumentM3dMod();
	~DocumentM3dMod();


	bool save() override;

	bool undo() override;
	bool redo() override;
	

};