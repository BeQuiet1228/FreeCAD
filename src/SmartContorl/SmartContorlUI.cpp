#include "SmartContorlUI.h"
#include "ui_SmartContorlUI.h"
#include "iostream"
#include "VariateAnalysis.h"
#include "FileMaker.h"
#include <Contorl/ContorlInterface.h>
#include <contorl/ContorlDataBar.h>
#include <QListWidgetItem>
#include <Contorl/Chipic.h>
#include <SmartContorlData.h>
#include "VariateInputDialog.h"
#include "VariateItemWidget.h"
#include <QVector>
#include "qcustomplot.h"
#include "VariateChart.h"
#include "xml/pugixml.hpp"
#include <QTextCodec>
SmartContorlUI::SmartContorlUI(QWidget * parent /*= 0*/)
	:QDialog(parent), ui(new Ui::SmartContorlUI)
{
	ui->setupUi(this);

	auto contorlData = SmartContorlData::GetInstance();
	smartContorl = contorlData->smartContorl;
	auto contorlInterface = ContorlInterface::GetInstance();

#ifdef SMART_EXE
	std::string m3dPath = "E:/test/test.m3d";
	smartContorl->setM3dPath(m3dPath);
#else
	//smartContorl->setM3dPath(contorlInterface->getDocumentPath());
#endif
	connect(smartContorl, SIGNAL(addDataBar(QListWidgetItem*, QWidget*)), this, SLOT(addListWidgetItem(QListWidgetItem*, QWidget*)));
	connect(smartContorl, SIGNAL(smartContorlLog(std::string)), this, SLOT(pringLuaLog(std::string)));

	this->setModal(true);
	setWindowFlags(Qt::Dialog | Qt::WindowMinimizeButtonHint);

	//隐藏测试控件
	this->ui->pushButton_3->hide();
	this->ui->pushButton_4->hide();
	this->ui->pushButton_5->hide();
	this->ui->pushButton_6->hide();
	this->ui->pushButton_7->hide();
	this->ui->textEdit->hide();

}

SmartContorlUI::~SmartContorlUI()
{
	
}

/**
* @brief SmartContorlUI::setTextPath 设置优化算法的运行路径
* @param const std::string & path
* @return void
*/
void SmartContorlUI::setTextPath(const std::string& path)
{
	smartContorl->setM3dPath(path);
}

void SmartContorlUI::on_pushButton_clicked()
{
	auto str = replaceVariate();
	smartContorl->chipicCount = this->ui->spinBoxRunCount->value();
	smartContorl->run(str);

	saveParameterXml();
}

void SmartContorlUI::on_pushButton_2_clicked()
{
	smartContorl->stop();
	auto data = SmartContorlData::GetInstance();
	data->clear();
}
//载入按钮
void SmartContorlUI::on_pushButton_3_clicked()
{
	auto  str = ui->textEdit->toPlainText();

	smartContorl->luaLoadFromString(str.toStdString());
}
//初始化按钮
void SmartContorlUI::on_pushButton_4_clicked()
{
	smartContorl->luaInit();
}
//数据筛选按钮
void SmartContorlUI::on_pushButton_5_clicked()
{
	smartContorl->luaResultDataFilter();
}
//预期对比按钮
void SmartContorlUI::on_pushButton_6_clicked()
{
	smartContorl->luaResultExpcet();
}
//参数优化
void SmartContorlUI::on_pushButton_7_clicked()
{
	smartContorl->luaOptimize();
}

void SmartContorlUI::on_pushButton_8_clicked()
{

}

void SmartContorlUI::on_pushButtonF_clicked()
{
	auto histroy = SmartContorlData::GetInstance()->smartContorl->getHistoryDatas();
	if (histroy.size() < 1)
		return;
	auto variates = histroy.begin()->variates;
	if (variates.size() < 1)
		return;
	auto valueCount = variates.begin()->values.size();


 
	QVector<QVector<double>> values;
	QVector<double> keys;
	int key = 1;
	for (int i = 0; i < valueCount; i++)
	{
		QVector<double> v;
		values.push_back(v);
	}

	for (auto historyIter = histroy.begin(); historyIter != histroy.end(); historyIter++)
	{
		auto historyValues = historyIter->datas;
		auto vIter = values.begin();
		auto hIter = historyValues.begin();
		for (; vIter != values.end() && hIter != historyValues.end();
			vIter++, hIter++)
		{
			vIter->push_back((*hIter)->resultData->getValue(0));
		}
		keys.push_back(key);
		key++;
	}
	auto chart = new VariateChart;
	chart->setAttribute(Qt::WA_DeleteOnClose);
	chart->clearGraph();
	chart->setDatas(keys, values, "F");
	chart->show();

}

void SmartContorlUI::on_pushButtonAddVariate_clicked()
{
	std::cout << "add" << std::endl;
	VariateInputDialog d;
	d.exec();

	if (d.okClicked)
	{
		auto data = d.getData();
		data->count = this->ui->spinBoxCount->value();
		data->item = new QListWidgetItem();
		data->widget = new VariateItemWidget();
		data->widget->setData(data);
		variateDatas.push_back(data);
		
		this->ui->listWidgetVariate->addItem(data->item);
		auto size = data->widget->size();
		data->item->setSizeHint(size);
		this->ui->listWidgetVariate->setItemWidget(data->item, data->widget);
	}
}

void SmartContorlUI::on_pushButtonDeleteVariate_clicked()
{
	auto items = this->ui->listWidgetVariate->selectedItems();
	if (items.size() < 1)
		return;
	auto item = items.begin();

	for (auto iter = variateDatas.begin(); iter != variateDatas.end(); iter++)
	{
		if ((*iter)->item == *item)
		{
			(*iter)->deleteUI();
			variateDatas.erase(iter);
			return;
		}
	}
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

void SmartContorlUI::addListWidgetItem(QListWidgetItem *item, QWidget *widget)
{
	ui->listWidget->addItem(item);
	ui->listWidget->setItemWidget(item, widget);
}

void SmartContorlUI::pringLuaLog(std::string str)
{
	auto temp = QString::fromStdString(str);
	auto text = this->ui->plainTextEdit->toPlainText();
	text += temp;
	this->ui->plainTextEdit->setPlainText(text);
}

void SmartContorlUI::on_pushButtonVariateMax_clicked()
{
	auto histroy = SmartContorlData::GetInstance()->smartContorl->getHistoryDatas();
	if (histroy.size() < 1)
		return;
	auto variates = histroy.begin()->variates;
	if (variates.size() < 1)
		return;
	auto valueCount = variates.begin()->values.size();

	//获取选中项索引
	int selectIndex = 0;
	{
		auto indexs = this->ui->listWidgetVariate->selectionModel()->selectedIndexes();
		if (indexs.size() != 0)
			selectIndex = indexs.begin()->row();
	}


	QVector<QVector<double>> values;
	QVector<double> keys;
	int key = 1;
	for (int i = 0; i < valueCount; i++)
	{
		QVector<double> v;
		values.push_back(v);
	}

	for (auto historyIter = histroy.begin(); historyIter != histroy.end(); historyIter++)
	{
		auto historyValues = historyIter->variates.at(selectIndex).values;
		auto vIter = values.begin();
		auto hIter = historyValues.begin();
		for (; vIter != values.end() && hIter != historyValues.end();
			vIter++, hIter++)
		{
			vIter->push_back(*hIter);
		}
		keys.push_back(key);
		key++;
	}
	auto chart = new VariateChart;
	chart->clearGraph();
	chart->setDatas(keys, values, variates.begin()->name);
	chart->show();
	chart->setAttribute(Qt::WA_DeleteOnClose);
}

void SmartContorlUI::on_comboBoxExcpcet_currentIndexChanged(int index)
{
	if (index == 0)
		this->ui->widgetAccuracy->show();
	else{
		this->ui->widgetAccuracy->hide();
	}
}

//暂时全写再这儿 日后再改
QString SmartContorlUI::replaceVariate()
{
	//添加参数
	int count = this->ui->spinBoxCount->value();
	QString vars = "\n";
	QString temp = "";
	for (auto iter = variateDatas.begin(); iter != variateDatas.end(); iter++)
	{
		temp = QString("addVar(\"%1\",%2,%3,%4);\n").arg((*iter)->name)
			.arg((*iter)->max).arg((*iter)->mini).arg(count);
		vars += temp;
	}
	auto text = this->ui->textEdit->toPlainText();
	text += vars;

	//添加配置
	QString config = "";
	temp = QString("observeName = \"%1\";\n").arg(this->ui->lineEditName->text());
	config += temp;
	temp = QString("maxTime = %1;\n").arg(this->ui->lineEditMaxTime->text().toInt());
	config += temp;
	temp = QString("miniTime = %1;\n").arg(this->ui->lineEditMiniTime->text().toInt());
	config += temp;
	temp = QString("excpectF = %1;\n").arg(this->ui->lineEditMaxF->text().toLongLong());
	config += temp;
	temp = QString("omiga = %1;\n").arg(this->ui->lineEditOmega->text().toDouble());
	config += temp;
	temp = QString("c1 = %1;\n").arg(this->ui->lineEditC1->text().toDouble());
	config += temp;
	temp = QString("c2 = %1;\n").arg(this->ui->lineEditC2->text().toDouble());
	config += temp;
	temp = QString("fmod = %1;\n").arg(this->ui->comboBoxF->currentIndex());
	config += temp;
	temp = QString("excpectMod = %1;\n").arg(this->ui->comboBoxExcpcet->currentIndex());
	config += temp;
	temp = QString("optimizeMaxCount = %1;\n").arg(this->ui->spinBoxOptimizeCount->value());
	config += temp;
	temp = QString("accuracy = %1/100;\n").arg(this->ui->lineEditAccuracy->text());
	config += temp;
	text = config + text;
	return text;
}

void SmartContorlUI::saveParameterXml()
{
	pugi::xml_document doc;
	auto parNode = doc.append_child("Parameter");
	auto configNode = doc.append_child("Config");
	configNode.append_attribute("OptimizeCount") = ui->spinBoxOptimizeCount->value();
	configNode.append_attribute("RunCount") = ui->spinBoxCount->value();
	configNode.append_attribute("RunMaxCount") = ui->spinBoxRunCount->value();
	configNode.append_attribute("ObserveName") = ui->lineEditName->text().toStdString().c_str();
	configNode.append_attribute("MaxTime") = ui->lineEditMaxTime->text().toInt();
	configNode.append_attribute("MiniTime") = ui->lineEditMiniTime->text().toInt();
	configNode.append_attribute("FModIndex") = ui->comboBoxF->currentIndex();
	configNode.append_attribute("F") = ui->lineEditMaxF->text().toLongLong();
	configNode.append_attribute("ExcpectMod") = ui->comboBoxExcpcet->currentIndex();
	configNode.append_attribute("Accuracy") = ui->lineEditAccuracy->text().toStdString().c_str();
	configNode.append_attribute("C1") = ui->lineEditC1->text().toStdString().c_str();
	configNode.append_attribute("C2") = ui->lineEditC2->text().toStdString().c_str();
	configNode.append_attribute("Omega") = ui->lineEditOmega->text().toStdString().c_str();

	for (auto i = variateDatas.begin(); i != variateDatas.end(); i++)
	{
		auto node = parNode.append_child((*i)->name.toStdString().c_str());
		std::string max = QString::number((*i)->max).toStdString();
		std::string mini = QString::number((*i)->mini).toStdString();
		node.append_attribute("Max") = max.c_str();
		node.append_attribute("Mini") = mini.c_str();
	}
	auto path = smartContorl->getM3dPath();
	path = path.left(path.length() - 4) + ".cc";
	auto gbk = QTextCodec::codecForName("gb2312");

	std::string ret = gbk->fromUnicode(path).data();
	doc.save_file(ret.c_str());

	
}

void SmartContorlUI::loadParameterXml()
{
	pugi::xml_document document;
	auto path = smartContorl->getM3dPath();
	path = path.left(path.length() - 4) + ".cc";
	auto gbk = QTextCodec::codecForName("gb2312");

	std::string ret = gbk->fromUnicode(path).data();
	auto result = document.load_file(ret.c_str());
	if (!result)
		return;
	auto parNode = document.child("Parameter");
	auto configNode = document.child("Config");


	ui->spinBoxOptimizeCount->setValue(configNode.attribute("OptimizeCount").as_int());
	ui->spinBoxRunCount->setValue(configNode.attribute("RunMaxCount").as_int());
	ui->spinBoxCount->setValue(configNode.attribute("RunCount").as_int());
	ui->lineEditName->setText(QString::fromStdString(configNode.attribute("ObserveName").as_string()));
	ui->lineEditMaxTime->setText(QString::number(configNode.attribute("MaxTime").as_int()));
	ui->lineEditMiniTime->setText(QString::number(configNode.attribute("MiniTime").as_int()));
	ui->comboBoxF->setCurrentIndex(configNode.attribute("FModIndex").as_int());
	ui->lineEditMaxF->setText(QString::number(configNode.attribute("F").as_llong()));
	ui->comboBoxExcpcet->setCurrentIndex(configNode.attribute("ExcpectMod").as_int());
	ui->lineEditAccuracy->setText(QString::number(configNode.attribute("Accuracy").as_double()));
	ui->lineEditC1->setText(QString::number(configNode.attribute("C1").as_double()));
	ui->lineEditC2->setText(QString::number(configNode.attribute("C2").as_double()));
	ui->lineEditOmega->setText(QString::number(configNode.attribute("Omega").as_double()));

	for (auto iter = parNode.begin(); iter != parNode.end(); iter++)
	{
		std::shared_ptr<VariateData> data;
		data.reset(new VariateData);
		data->count = this->ui->spinBoxCount->value();
		data->name = QString::fromStdString(iter->name());
		data->max = iter->attribute("Max").as_double();
		data->mini = iter->attribute("Mini").as_double();
		data->item = new QListWidgetItem();
		data->widget = new VariateItemWidget();
		data->widget->setData(data);
		variateDatas.push_back(data);

		this->ui->listWidgetVariate->addItem(data->item);
		auto size = data->widget->size();
		data->item->setSizeHint(size);
		this->ui->listWidgetVariate->setItemWidget(data->item, data->widget);
	}
}

void SmartContorlUI::closeEvent(QCloseEvent *event)
{
	smartContorl->stop();
	auto data = SmartContorlData::GetInstance();
	data->clear();
	QDialog::closeEvent(event);
}

#include "moc_SmartContorlUI.cpp"