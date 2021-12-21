#pragma once
//#include "Document.h"
#include "Document.h"

class DocumentM2dMod :public App::Document{
public:
	DocumentM2dMod(){
		classID = 3;
	};
	~DocumentM2dMod(){};

public:
	bool save() override;
	bool undo() override;
	bool redo() override;
};