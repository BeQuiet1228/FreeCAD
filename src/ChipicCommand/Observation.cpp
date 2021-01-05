#include "Observation.h"

Observation::Observation()
	:model(nullptr)
{
}

Observation::~Observation()
{
	if (model != nullptr)
		delete model;
}

/**
* @brief Observation::modelsToCommand Éú³ÉmodelµÄm3d
* @return std::string
*/
std::string Observation::modelsToCommand()
{
	std::string cmd;
	
	if (model != nullptr)
		cmd += model->toCommand();

	return cmd;
}

