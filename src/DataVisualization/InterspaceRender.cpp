#include "InterspaceRender.h"

InterspaceRender::InterspaceRender(std::shared_ptr<InterspaceData> data)
	:TimeRenderer(std::dynamic_pointer_cast<TimeData>(data))
{

}

