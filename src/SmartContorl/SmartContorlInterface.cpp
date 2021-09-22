#include "SmartContorlInterface.h"
#include "Contorl\ContorlInterface.h"
#include "SmartContorlUI.h"
#include "smartCalc.h"
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

QWidget* SmartContorlInterface::creatSmartControlUI(const std::string& path)
{
	auto contorlUi = new SmartContorlUI();
	contorlUi->setTextPath(path);
	contorlUi->loadParameterXml();
	return contorlUi;
}

void SmartContorlInterface::buttonClicked(int type){

	if (ContorlButtonBar::ButtonType(type) == ContorlButtonBar::SMART_CONTORL)
	{
		auto contorlUi = new SmartContorlUI();
		contorlUi->show();
		contorlUi->setAttribute(Qt::WA_DeleteOnClose);
	}
}

void SmartContorlInterface::showSmartCalc(const std::string& path)
{
	auto calc =new smartCalc();
	calc->afferm3dpath(path);
	calc->afferscriptpath("./opt.lua");
	calc->show();
	calc->setAttribute(Qt::WA_DeleteOnClose);
	//calc->setTextPath();
}

QWidget* SmartContorlInterface::createCalcWidget(const std::string& path)
{
	auto calc = new smartCalc();
	calc->afferm3dpath(path);
	calc->afferscriptpath("./opt.lua");
	calc->show();
	calc->setAttribute(Qt::WA_DeleteOnClose);
	return calc;
}

#include "moc_SmartContorlInterface.cpp"