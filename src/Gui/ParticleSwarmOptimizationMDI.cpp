#include "ParticleSwarmOptimizationMDI.h"
#include "QHBoxLayout"
#include "SmartContorl/SmartContorlInterface.h"
ParticleSwarmOptimizationMDI::ParticleSwarmOptimizationMDI(Gui::Document* pcDocument, QWidget* parent, Qt::WindowFlags wflags /*= 0*/)
	:MDIView(pcDocument,parent,wflags)
{

}

ParticleSwarmOptimizationMDI::~ParticleSwarmOptimizationMDI()
{

}

void ParticleSwarmOptimizationMDI::init(const std::string& path)
{
	QWidget *w = SmartContorlInterface::creatSmartControlUI(path);
	setCentralWidget(w);
}


