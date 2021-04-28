#pragma once
#include "Plot.h"
#include <memory>
#include "exportConfig.hpp"
class ContourRender;
class DATA_VISUALIZATION_EXPORT ContourRenderStateGetter {
public:
	enum DisplayMod {
		NONE = 0,
		IMAGE = 1,			//渲染图片
		CONTOUR = 2,		//渲染等值线
		IMAGE_AND_CONTOUR = IMAGE | CONTOUR //等值线跟图片都渲染
	};

public:
	ContourRenderStateGetter(Plot* p);
	~ContourRenderStateGetter() = default;

public:
	//是否可用
	bool enabled();
	//获取渲染状态
	DisplayMod getDisplayMod();
	void setDisplayMode(const DisplayMod& mod);

private:
	Plot* plot;

private:
	std::shared_ptr<ContourRender> getContourRender();
};