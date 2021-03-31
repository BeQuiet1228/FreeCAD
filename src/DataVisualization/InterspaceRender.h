#pragma once
#include "TimeRenderer.h"
#include <memory>
#include "InterSpaceData.h"
class InterspaceRender :public TimeRenderer{
public:
	InterspaceRender(std::shared_ptr<InterspaceData> data);
	~InterspaceRender() = default;

};