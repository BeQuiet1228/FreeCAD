#pragma once
#include "TimeRenderer.h"
#include <memory>
#include "InterSpaceData.h"
namespace DV {
	class InterspaceRender :public TimeRenderer {
	public:
		InterspaceRender(std::shared_ptr<InterspaceData> data);
		~InterspaceRender() = default;

	};
};
