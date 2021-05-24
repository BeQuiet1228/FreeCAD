#include "SmartContorlInterface.h"
#include "Contorl\ContorlInterface.h"
#include "SmartContorlUI.h"
void SmartContorlInterface::init(){

	auto contorl = ContorlInterface::GetInstance();
	auto buttonBar = contorl->getContorlButtonBar();
	connect(buttonBar, SIGNAL(buttonClicked(int)), this, SLOT(buttonClicked(int)));
}

void SmartContorlInterface::showSmartControlUI(const std::string& path)
{
	auto contorlUi = new SmartContorlUI();
	contorlUi->setTextPath(path);
	contorlUi->loadParameterXml();
	contorlUi->show();
	contorlUi->setAttribute(Qt::WA_DeleteOnClose);
}

void SmartContorlInterface::buttonClicked(int type){

	if (ContorlButtonBar::ButtonType(type) == ContorlButtonBar::SMART_CONTORL)
	{
		auto contorlUi = new SmartContorlUI();
		contorlUi->show();
		contorlUi->setAttribute(Qt::WA_DeleteOnClose);
	}
}
#include "moc_SmartContorlInterface.cpp"