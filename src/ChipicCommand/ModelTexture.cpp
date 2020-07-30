#include "ModelTexture.h"
ModelTexture::ModelTexture()
{
	name = "";
}

ModelTexture::~ModelTexture()
{
}

std::string ModelTexture::toCommand()
{
	if (notOutputCommand || name == "")
		return "";

	std::string cmd = "";
	switch (type)
	{
	case UNDEFINED:
		break;
	case CONDUCTOR:
		cmd = "CONDUCTOR " + name + ";\n";
		break;
	case VACUO:
		cmd = "VOID " + name + ";\n";
		break;
	case DEFINED:
		break;
	default:
		break;
	}
	return cmd;
}

bool ModelTexture::fromCommand(const std::string& command)
{
	return false;
}
