#include "ParticleSwarmOptimizationMDI.h"
#include "QHBoxLayout"
#include "SmartContorl/SmartContorlInterface.h"
ParticleSwarmOptimizationMDI::ParticleSwarmOptimizationMDI(DocumentPic* pcDocument, QWidget* parent)
	:MDIViewPIC(pcDocument,parent)
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


ProcessingBatchView::ProcessingBatchView(DocumentPic* pcDocument, QWidget* parent /*= 0*/)
	:MDIViewPIC(pcDocument,parent)
{

}

void ProcessingBatchView::init(const std::string& path)
{
	QWidget* w = SmartContorlInterface::createCalcWidget(path);
	setCentralWidget(w);
}
