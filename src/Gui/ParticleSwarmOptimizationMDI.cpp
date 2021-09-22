#include "ParticleSwarmOptimizationMDI.h"
#include "QHBoxLayout"
#include "SmartContorl/SmartContorlInterface.h"
#include "Transition/transition.h"
ParticleSwarmOptimizationMDI::ParticleSwarmOptimizationMDI(DocumentPic* pcDocument, QWidget* parent)
	:MDIViewPIC(pcDocument,parent)
{
	setWindowTitle(gbkStdstringToQstring("粒子群优化算法"));
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
	setWindowTitle(gbkStdstringToQstring("批处理"));
}

void ProcessingBatchView::init(const std::string& path)
{
	QWidget* w = SmartContorlInterface::createCalcWidget(path);
	setCentralWidget(w);
}
