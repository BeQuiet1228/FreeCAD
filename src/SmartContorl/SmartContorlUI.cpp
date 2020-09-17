#include "SmartContorlUI.h"
#include "ui_SmartContorlUI.h"
#include "iostream"
#include "VariateAnalysis.h"
#include "FileMaker.h"
#include <Contorl/ContorlInterface.h>
#include <contorl/ContorlDataBar.h>
#include <QListWidgetItem>
SmartContorlUI::SmartContorlUI(QWidget * parent /*= 0*/)
	:QWidget(parent), ui(new Ui::SmartContorlUI)
{
	ui->setupUi(this);
	auto contorl = ContorlInterface::GetInstance();
	auto chipicManger = contorl->getChipicManager();
	chipicManger->setRunType(ChipicManager::AUTO);

	connect(chipicManger, SIGNAL(chipicStartFinished(unsigned long)), this, SLOT(chipicStartFinished(unsigned long)));
}

SmartContorlUI::~SmartContorlUI()
{

}

void SmartContorlUI::on_pushButton_clicked()
{
	VariateAnalysis var;
	auto tt = var.analysisTextToVariate(ui->textEdit->toPlainText());

	auto str = Variate::makeStringForVariates(tt);
	for (auto i = str.begin(); i != str.end(); i++)
	{
		std::cerr << "string:/n" << std::endl;
		std::cerr << (*i).toStdString() << std::endl;
	}
	FileMaker maker;
	maker.setM3dPath("E:/lingshiwenjianjia/MILO_C/MILO_C.m3d");
	m3dDatas = maker.makeFile(str);

	auto contorl = ContorlInterface::GetInstance();
	auto chipicManger = contorl->getChipicManager();
	auto data = m3dDatas.front();
	chipicManger->sendStartChipicMessage(data.m3dPath.toStdString(), 1);
}

void SmartContorlUI::chipicStartFinished(unsigned long threadID)
{
	m3dDatas.pop_front();
	
	auto contorl = ContorlInterface::GetInstance();
	auto manager = contorl->getChipicManager();

	auto chipicUI = manager->ChipicUIMap.find(threadID);
	if (chipicUI != manager->ChipicUIMap.end())
	{
		auto item = new QListWidgetItem(ui->listWidget);
		item->setSizeHint(chipicUI->second.dataBar->size());
		ui->listWidget->setItemWidget(item,chipicUI->second.dataBar);
	}

	if (manager->chipicMap.size() < 8)
	{
		auto data = m3dDatas.front();
		manager->sendStartChipicMessage(data.m3dPath.toStdString(), 1);
	}

}

#include "moc_SmartContorlUI.cpp"