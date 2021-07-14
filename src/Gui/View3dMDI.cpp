#include "View3dMDI.h"
#include "DocumentPic.h"
#include "Contorl/ContorlInterface.h"
View3dMDI::View3dMDI(Gui::Document* pcDocument, QWidget* parent, const QtGLWidget* sharewidget /*= 0*/, Qt::WindowFlags wflags /*= 0*/)
	:View3DInventor(pcDocument,parent,sharewidget,wflags)
{

}

View3dMDI::~View3dMDI()
{

}

bool View3dMDI::onMsg(const char* pMsg, const char** ppReturn)
{
	if (View3DInventor::onMsg(pMsg, ppReturn))
		return true;
	if (onMsgChipic(pMsg, ppReturn, getGuiDocument()))
		return true;

	return false;
}

bool View3dMDI::onHasMsg(const char* pMsg) const
{
	if (View3DInventor::onHasMsg(pMsg))
		return true;
	if (onHasMsgChipic(pMsg))
		return true;
	return false;
}

bool View3dMDI::onMsgChipic(const char* pMsg, const char** ppReturn, Gui::Document* doc)
{
	auto picDoc = dynamic_cast<DocumentPic*>(doc);
	if (!picDoc)
		return false;

	if (strcmp("RunChipic", pMsg) == 0){	
		picDoc->runChipic();
		return true;
	}
	else if (strcmp("StopChipic", pMsg) == 0){
		picDoc->stopChipic();
		return true;
	}else if (strcmp("ParalleRunChipic", pMsg) == 0) {
		picDoc->paralleRunChipic();
		return true;
	}else if (strcmp("showPSOView", pMsg) == 0) {
		picDoc->showParticleSwarmOptimizationView();
		return true;
	}

	return false;
}

bool View3dMDI::onHasMsgChipic(const char* pMsg)
{
	if (strcmp("RunChipic", pMsg) == 0) {
		auto control = ContorlInterface::GetInstance();
		if (control->hasAutoChipicRuning())
			return false;
		return true;
	}else if (strcmp("ParalleRunChipic", pMsg) == 0) {
		auto control = ContorlInterface::GetInstance();
		if (control->hasChipicRuning())
			return false;
		return true;
	}else if (strcmp("showPSOView", pMsg) == 0) {
		auto control = ContorlInterface::GetInstance();
		if (control->hasChipicRuning())
			return false;
		return true;
	}
	return false;
}

