#pragma once
//#include "Document.h"
#include "DocumentDataManager.h"
class DocumentM3dMod :public DocumentManager{
public:
	DocumentM3dMod();
	~DocumentM3dMod();


	bool save() override;

	bool undo() override;
	bool redo() override;
	

};