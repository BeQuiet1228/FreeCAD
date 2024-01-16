#include "ParticleSwarmOptimizationMDI.h"
#include "QHBoxLayout"
#include "SmartContorl/SmartContorlInterface.h"
#include "Transition/transition.h"
//#include "SmartContorl/smartCalc.h"
//#include "SmartContorl/SmartContorl.h"
#include "SmartContorl/SmartContorlUI.h"
#include "SmartContorl/smartCalc.h"
ParticleSwarmOptimizationMDI::ParticleSwarmOptimizationMDI(DocumentPic* pcDocument, QWidget* parent)
	:AlgorMDIInter(pcDocument,parent), smartControlWidget(nullptr)
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
	if (nullptr != w)
	{
		smartControlWidget = w;
	}
}
bool ParticleSwarmOptimizationMDI::isClose()
{
	SmartContorlUI* saveWidget = dynamic_cast<SmartContorlUI*>(smartControlWidget);
	if (nullptr == saveWidget)
		return true;
	bool ok = saveWidget->getRunning();
	return (!ok);
}

ProcessingBatchView::ProcessingBatchView(DocumentPic* pcDocument, QWidget* parent /*= 0*/)
	:AlgorMDIInter(pcDocument,parent)
{
	setWindowTitle(gbkStdstringToQstring("批处理"));
}

void ProcessingBatchView::init(const std::string& path)
{
	QWidget* w = SmartContorlInterface::createCalcWidget(path);
	setCentralWidget(w);
	if (nullptr != w)
	{
		calcWidget = w;
	}
}
bool ProcessingBatchView::isClose()
{
	smartCalc* saveWidget = dynamic_cast<smartCalc*>(calcWidget);
	if (nullptr == saveWidget)
		return true;
	bool ok = saveWidget->getRunning();
	return (!ok);
}


GeneticAlgorithmView::GeneticAlgorithmView(DocumentPic* pcDocument, QWidget* parent /*= 0*/)
	: ParticleSwarmOptimizationMDI(pcDocument, parent)
{
	setWindowTitle(gbkStdstringToQstring("遗传算法"));
}

GeneticAlgorithmView::~GeneticAlgorithmView()
{

}

void GeneticAlgorithmView::init(const std::string& path)
{
	QWidget* w = SmartContorlInterface::creatGeneticAlgorithmUI(path);
	setCentralWidget(w);
	if (nullptr != w)
	{
		smartControlWidget = w;
	}
}

MultipleTargetGeneticAlgorithmView::MultipleTargetGeneticAlgorithmView(DocumentPic* pcDocument, QWidget* parent /*= 0*/)
	: ParticleSwarmOptimizationMDI(pcDocument, parent)
{
	setWindowTitle(gbkStdstringToQstring("多目标遗传算法"));
}

MultipleTargetGeneticAlgorithmView::~MultipleTargetGeneticAlgorithmView()
{
	
}

void MultipleTargetGeneticAlgorithmView::init(const std::string& path)
{
	QWidget* w = SmartContorlInterface::creatMultipleGeneticAlgorithmUI(path);
	setCentralWidget(w);
	if (nullptr != w)
	{
		smartControlWidget = w;
	}
}

MultipleTargetGeneticAlgorithmGView::MultipleTargetGeneticAlgorithmGView(DocumentPic* pcDocument, QWidget* parent /*= 0*/)
	: ParticleSwarmOptimizationMDI(pcDocument, parent)
{
	setWindowTitle(gbkStdstringToQstring("G占优多目标遗传算法"));
}

MultipleTargetGeneticAlgorithmGView::~MultipleTargetGeneticAlgorithmGView()
{

}

void MultipleTargetGeneticAlgorithmGView::init(const std::string& path)
{
	QWidget* w = SmartContorlInterface::creatMultipleGeneticAlgorithmGUI(path);
	setCentralWidget(w);
	if (nullptr != w)
	{
		smartControlWidget = w;
	}
}

