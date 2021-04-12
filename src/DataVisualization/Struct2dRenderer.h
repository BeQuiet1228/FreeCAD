#pragma once
#ifndef _STRUCT_2D_RENDERER_H_
#define _STRUCT_2D_RENDERER_H_
#include "Renderer.h"
#include "Struct2dData.h"
class Struct2DRenderer :public Renderer
{
public:
	Struct2DRenderer(std::shared_ptr<Struct2dData> data);
	~Struct2DRenderer();
private:
	Data::Rang xRang, yRang;
	std::mutex xRangMutex, yRangMutex;
public:
	virtual bool drawImage() override;
	virtual bool addListRang(std::list<Data::Rang> listRang) override;
	virtual bool drawPointImage() override;
	virtual bool setDefaultRang() override;
	virtual void dataInit() override;
private:

};
#endif