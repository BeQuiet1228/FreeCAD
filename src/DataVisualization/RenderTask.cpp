#include "RenderTask.h"

namespace DV {
	RenderTask::RenderTask(const std::shared_ptr<Renderer> rder, const TaskType type /*= MAP*/, const unsigned int rank /*= 0*/)
		:renderer(rder)
	{
		this->type = type;
		this->rank = rank;
	}

	RenderTask::~RenderTask()
	{

	}
};


