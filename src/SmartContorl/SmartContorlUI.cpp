#include "SmartContorlUI.h"
#include "ui_SmartContorlUI.h"
#include "iostream"
#include "VariateAnalysis.h"
#include "FileMaker.h"
#include <Contorl/ContorlInterface.h>
#include <contorl/ContorlDataBar.h>
#include <QListWidgetItem>
#include <Contorl/Chipic.h>
SmartContorlUI::SmartContorlUI(QWidget * parent /*= 0*/)
	:QWidget(parent), ui(new Ui::SmartContorlUI)
{
	ui->setupUi(this);
	auto contorl = ContorlInterface::GetInstance();
	auto chipicManger = contorl->getChipicManager();
	chipicManger->setRunType(ChipicManager::AUTO);

	connect(chipicManger, SIGNAL(chipicStartFinished(unsigned long)), this, SLOT(chipicStartFinished(unsigned long)));
	connect(chipicManger, SIGNAL(finishChipicM3dPath(unsigned long)), this, SLOT(chipicWorkFinished(unsigned long)));

	fileMaker.setM3dPath("E:/lingshiwenjianjia/MILO_C/MILO_C.m3d");
}

SmartContorlUI::~SmartContorlUI()
{

}

void SmartContorlUI::on_pushButton_clicked()
{
/*	VariateAnalysis var;
	auto tt = var.analysisTextToVariate(ui->textEdit->toPlainText());

	auto str = Variate::makeStringForVariates(tt);
	for (auto i = str.begin(); i != str.end(); i++)
	{
		std::cerr << "string:/n" << std::endl;
		std::cerr << (*i).toStdString() << std::endl;
	}
	m3dDatas = fileMaker.makeFile(str);

	auto contorl = ContorlInterface::GetInstance();
	auto chipicManger = contorl->getChipicManager();
	if (m3dDatas.size() == 0)
		return;
	auto data = m3dDatas.front();
	m3dDatas.pop_front();
	chipicManger->sendStartChipicMessage(data.m3dPath.toStdString(), 1);*/
}
//载入按钮
void SmartContorlUI::on_pushButton_3_clicked()
{
	auto  str = ui->textEdit->toPlainText();

	smartContorl.luaLoadFromString(str.toStdString());
}
//初始化按钮
void SmartContorlUI::on_pushButton_4_clicked()
{
	smartContorl.luaInit();
}
//数据筛选按钮
void SmartContorlUI::on_pushButton_5_clicked()
{
	smartContorl.luaResultDataFilter();
}
//预期对比按钮
void SmartContorlUI::on_pushButton_6_clicked()
{
	smartContorl.luaResultExpcet();
}
//参数优化
void SmartContorlUI::on_pushButton_7_clicked()
{
	smartContorl.luaOptimize();
}

void SmartContorlUI::chipicStartFinished(unsigned long threadID)
{
	auto contorl = ContorlInterface::GetInstance();
	auto manager = contorl->getChipicManager();

	auto item = new QListWidgetItem(ui->listWidget);
	auto dataBar = new ContorlDataBar;
	item->setSizeHint(dataBar->size());
	ui->listWidget->setItemWidget(item, dataBar);

	auto chipic = manager->chipicMap.find(threadID);
	if (chipic != manager->chipicMap.end())
		dataBar->setChipicData(chipic->second);

	itemMap.insert(std::map<unsigned long, QListWidgetItem*>::value_type(threadID, item));

	auto m3dPath = manager->getM3dpathForThreadID(threadID);
	pathMap.insert(std::map<unsigned long, QString>::value_type(threadID, m3dPath));

	if (manager->chipicMap.size() < 8)
	{
		if (m3dDatas.size() <= 0)
			return;
		auto data = m3dDatas.front();
		m3dDatas.pop_front();
		manager->sendStartChipicMessage(data.m3dPath.toStdString(), 1);
	}


}

void SmartContorlUI::chipicWorkFinished(unsigned long threadID)
{
	//寻找到对应的ui 然后释放掉
	auto iter = itemMap.find(threadID);
	if (iter != itemMap.end())
	{
		auto databar = ui->listWidget->itemWidget(iter->second);
		delete iter->second;
		delete databar;
	}

	auto contorl = ContorlInterface::GetInstance();
	auto manager = contorl->getChipicManager();

	//剪切文件
	auto it = pathMap.find(threadID);
	if (it != pathMap.end())
	{
		auto m3dpath = it->second;
		m3dpath = m3dpath.left(m3dpath.length() - 4) + ".h5";
		fileMaker.cutFile(m3dpath, fileMaker.filePath);
	}

	if (manager->chipicMap.size() < 8)
	{
		if (m3dDatas.size() <= 0)
			return;
		auto data = m3dDatas.front();
		m3dDatas.pop_front();
		manager->sendStartChipicMessage(data.m3dPath.toStdString(), 1);
	}

}

#include "moc_SmartContorlUI.cpp"