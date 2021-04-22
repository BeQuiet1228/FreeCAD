#pragma once
//#include "Document.h"
#include "DocumentDataManager.h"

class DocumentM2dMod :public DocumentManager{
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