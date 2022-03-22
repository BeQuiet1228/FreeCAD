#include "ConfigFactory.h"
#include "AxisConfigWidget.h"
#include "ContourConfigWidget.h"
#include "ParticleConfigWidget.h"
#include "RangConfigWidget.h"
#include "StructConfigWidget.h"
#include "VectorConfigWidget.h"
std::vector<QWidget*> DV::ConfigPageFactory::CreateConfigWidget()
{
	std::vector<QWidget*> widgets;
	widgets.push_back(new AxisConfigWidget);
	widgets.push_back(new ContourConfigWidget);
	widgets.push_back(new ParticleConfigWidget);
	widgets.push_back(new StructConfigWidget);
	widgets.push_back(new VectorConfigWidget);
	return widgets;
}

