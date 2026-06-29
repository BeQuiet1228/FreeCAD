#include "MultipleTargetGeneticAlgorithmUI.h"
#include "ui_MultipleTargetGeneticAlgorithm.h"
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
#include "OptimizeCurse.h"
#include <QTextCodec>
#include <QScrollBar>
#include <QTextCursor>
#include "MultipleTargetGeneticAlgorithm.h"
#include "TimeTargetItemUI.h"
#include <QListWidgetItem>
#include "DataVisualization/RendererFactory.h"
#include "GeneticAlgorithm.h"
#include "ChartEvent.h"
#include "Event/EventManager.h"
#include "DialogTargetSelect.h"
#include "FrequencyTargetItemUI.h"
#include "PiModeTargetItemUI.h"
MultipleTargetGeneticAlgorithmUI::MultipleTargetGeneticAlgorithmUI(QWidget* parent /*= 0*/)
	:QDialog(parent), ui(new Ui::MultipleTargetGeneticAlgorithmUI)
{
	ui->setupUi(this);

	auto contorlData = SmartContorlData::GetInstance();
	smartContorl = contorlData->smartContorl;
	auto contorlInterface = ContorlInterface::GetInstance();

#ifdef SMART_EXE
	std::string m3dPath = "D:/test/MILO_P.m3d";
	//std::string m3dPath = "D:/test/match.m3d";
	smartContorl->setM3dPath(m3dPath);
	loadParameterXml();
#else
	//smartContorl->setM3dPath(contorlInterface->getDocumentPath());
#endif
	connect(smartContorl, SIGNAL(addDataBar(QListWidgetItem*, QWidget*)), this, SLOT(addListWidgetItem(QListWidgetItem*, QWidget*)));
	connect(smartContorl, SIGNAL(smartContorlLog(std::string)), this, SLOT(pringLuaLog(std::string)));

	this->setModal(true);
	setWindowFlags(Qt::Dialog | Qt::WindowMinimizeButtonHint);

	ui->textEdit->hide();
}

MultipleTargetGeneticAlgorithmUI::~MultipleTargetGeneticAlgorithmUI()
{
	smartContorl->stop();
	auto data = SmartContorlData::GetInstance();
	data->clear();
}

/**
* @brief MultipleTargetGeneticAlgorithmUI::setTextPath 设置优化算法的运行路径
* @param const std::string & path
* @return void
*/
void MultipleTargetGeneticAlgorithmUI::setTextPath(const std::string& path)
{
	smartContorl->setM3dPath(path);
}

void MultipleTargetGeneticAlgorithmUI::on_pushButton_clicked()
{
	auto str = replaceVariate();
	smartContorl->chipicCount = this->ui->spinBoxRunCount->value();
	smartContorl->maxCount = this->ui->spinBoxOptimizeCount->value();
	
	MultipleTargetGeneticAlgorithm* optimize;
	if (GMod)
		optimize = new MultipleTargetGeneticAlgorithmG();
	else
		optimize = new MultipleTargetGeneticAlgorithm();
	//auto optimize = new OptimizeCurseLua();

	//添加变量
	for each (auto var in variateDatas)
	{
		OPtimizeVariate v;
		v.name = var->name;
		v.min = var->mini;
		v.max = var->max;
		optimize->optimizeVariates.push_back(v);
	}
	//添加目标函数
	auto listWidget = ui->listWidgetTarget;
	int targetCount = listWidget->count();
	for (int i = 0; i < targetCount; i++)
	{
		auto item = listWidget->item(i);
		auto widget = listWidget->itemWidget(item);
		TargetItem* targetItem = dynamic_cast<TargetItem*>(widget);
		optimize->addTarget(targetItem->GenerateTarget());
	}
	optimize->setMutationProbability(ui->lineEditMutationProbability->text().toDouble());
	optimize->setMutationProbabilityRange(ui->lineEditMutationProbabilityRange->text().toDouble());
	optimize->luaLoadFromString(str.toStdString());
	smartContorl->setOptimizeCurse(optimize);
	smartContorl->run();
	smartContorl->setRunDataMakeType(SmartContorl::CONBINATION);
	saveParameterXml();
}

void MultipleTargetGeneticAlgorithmUI::on_pushButton_2_clicked()
{
	smartContorl->stop();
	auto data = SmartContorlData::GetInstance();
	data->clear();
}

void MultipleTargetGeneticAlgorithmUI::on_pushButtonF_clicked()
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

void MultipleTargetGeneticAlgorithmUI::on_pushButtonAddVariate_clicked()
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

void MultipleTargetGeneticAlgorithmUI::on_pushButtonDeleteVariate_clicked()
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

void MultipleTargetGeneticAlgorithmUI::on_pushButtonAddTarget_clicked()
{
	DialogTargetSelect diaglog;
	diaglog.exec(); 
	auto listWidget = ui->listWidgetTarget;
	QWidget* widget;
	if (diaglog.index == -1)
		return;
	if (diaglog.index == 0)
	{
		auto t = new TimeTargetItemUI(listWidget);
		if (this->GMod)
			t->showG();
		widget = t;
	}
	else if(diaglog.index == 1) {
		auto t = new FrequencyTargetItemUI(listWidget);
		if (this->GMod)
			t->showG();
		widget = t;
	}
	// 2: 多时间观测 (TimeDouble)
	else if (diaglog.index == 2) {
		auto t = new TimeDoubleTargetItemUI(listWidget);
		if (this->GMod) t->showG();
		widget = t;
	}
	// 【新增】3: π模识别 (PiMode)
	else if (diaglog.index == 3) {
		auto t = new PiModeTargetItemUI(listWidget); // 创建我们的新类
		if (this->GMod) t->showG();
		widget = t;
	}

	if (widget) { // 确保 widget 不为空再添加
		QListWidgetItem *item = new QListWidgetItem(listWidget);
		item->setSizeHint(widget->size());
		listWidget->setItemWidget(item, widget);
	}
}

void MultipleTargetGeneticAlgorithmUI::on_pushButtonDeleteTarget_clicked()
{
	auto listWidget = ui->listWidgetTarget;
	auto items = listWidget->selectedItems();
	for (auto iter = items.begin(); iter != items.end(); iter++)
	{
		int index = listWidget->row(*iter);
		auto widget = listWidget->itemWidget(*iter);
		auto item = listWidget->takeItem(index);

		delete widget;
		delete item;
	}
}

void MultipleTargetGeneticAlgorithmUI::on_pushButtonTargetChart_clicked()
{
	//获取被选中的目标索引
	int selectIndex = 0;
	int targetCount = 0;
	{
		targetCount = this->ui->listWidgetTarget->count();
		auto indexs = this->ui->listWidgetTarget->selectionModel()->selectedIndexes();
		if (indexs.size() != 0)
			selectIndex = indexs.begin()->row();
	}

	auto histroy = SmartContorlData::GetInstance()->smartContorl->getHistoryDatas();
	if (histroy.size() < 1)
		return;
	auto variates = histroy.begin()->variates;
	if (variates.size() < 1)
		return;
	auto valueCount = histroy.begin()->datas.size();


	std::vector<DV::Data::ValuesPtr> listValues;
	listValues.reserve(valueCount);

	for (int i = 0; i < valueCount; i++)
	{
		DV::Data::ValuesPtr valuePtr(new DV::Data::Values());
		listValues.push_back(valuePtr);
	}

	std::vector<std::map<QString, std::vector<float>>> parValues;
	for (int i = 0; i < valueCount; i++)
	{
		std::map<QString, std::vector<float>> parValue;
		for (auto iter = histroy.begin()->variates.begin(); iter != histroy.begin()->variates.end(); iter++)
		{
			parValue[iter->name] = std::vector<float>();
		}

		for (int t = 0; t < targetCount; t++)
		{
			parValue[QString("F%1").arg(t)] = std::vector<float>();
		}

		parValues.push_back(parValue);
	}


	int temp = 1;
	for (auto historyIter = histroy.begin(); historyIter != histroy.end(); historyIter++)
	{
		auto datas = historyIter->datas;
		for (int i = 0; i < datas.size(); i++)
		{
			auto f = datas[i]->resultData->getValue(selectIndex);
			listValues[i]->push_back(temp);
			listValues[i]->push_back(f);

			for (int t = 0; t < targetCount; t++)
			{
				parValues[i][QString("F%1").arg(t)].push_back(datas[i]->resultData->getValue(t));
			}
		}
		auto varuates = historyIter->variates;
		for (auto iter = varuates.begin(); iter != varuates.end(); iter++)
		{
			int count = iter->values.size();
			for (int i = 0; i < count; i++)
			{
				parValues[i][iter->name].push_back(iter->values[i]);
			}
		}

		temp++;
	}

	std::list<std::shared_ptr<DV::CurveData>> dataList;
	for (int i = 0; i < valueCount; i++)
	{
		auto curveData = DV::RendererFactory::creatCurveData(listValues[i], parValues[i]);
		dataList.push_back(curveData);
	}

	auto renderers = DV::RendererFactory::creatMultipleCurveRenderers(dataList);
	auto adapter = DV::RendererFactory::creatMultipleTimeAdapter(renderers);

	ChartEvent* event = new ChartEvent();
	event->setAdapter(adapter);
	EV::EventManager::postEvent(event);
}

void MultipleTargetGeneticAlgorithmUI::chipicStartFinished(unsigned long threadID)
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

void MultipleTargetGeneticAlgorithmUI::chipicWorkFinished(unsigned long threadID)
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

void MultipleTargetGeneticAlgorithmUI::addListWidgetItem(QListWidgetItem* item, QWidget* widget)
{
	ui->listWidget->addItem(item);
	ui->listWidget->setItemWidget(item, widget);
}

void MultipleTargetGeneticAlgorithmUI::pringLuaLog(std::string str)
{
	auto temp = QString::fromUtf8(str.c_str());
	auto text = this->ui->plainTextEdit->toPlainText();
	text += temp;
	this->ui->plainTextEdit->setPlainText(text);
	ui->plainTextEdit->moveCursor(QTextCursor::End);
}

void MultipleTargetGeneticAlgorithmUI::on_pushButtonVariateMax_clicked()
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

#if 0
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
#else
	std::vector<DV::Data::ValuesPtr> listValues;
	listValues.reserve(valueCount);

	for (int i = 0; i < valueCount; i++)
	{
		DV::Data::ValuesPtr valuePtr(new DV::Data::Values());
		listValues.push_back(valuePtr);
	}

	std::vector<std::map<QString, std::vector<float>>> parValues;
	for (int i = 0; i < valueCount; i++)
	{
		auto parV = std::map<QString, std::vector<float>>();
		for (int j = 0; j < variates.size(); j++)
		{
			if (j == selectIndex)
				continue;
			parV[variates[j].name] = std::vector<float>();
		}
		parV["F"] = std::vector<float>();
		parValues.push_back(parV);
	}
	int temp = 1;
	for (auto historyIter = histroy.begin(); historyIter != histroy.end(); historyIter++)
	{
		auto historyValues = historyIter->variates.at(selectIndex).values;
		for (int i = 0; i < historyValues.size(); i++)
		{
			listValues[i]->push_back(temp);
			listValues[i]->push_back(historyValues[i]);
		}
		temp++;
		for (int index = 0; index < historyIter->variates.size(); index++)
		{
			if (index == selectIndex)
				continue;
			auto values = historyIter->variates.at(index).values;
			for (int i = 0; i < values.size(); i++)
			{
				parValues[i][historyIter->variates[index].name].push_back(values.at(i));
			}
		}

		for (int index = 0; index < historyIter->datas.size(); index++)
		{
			parValues[index]["F"].push_back(historyIter->datas[index]->resultData->getValue(0));
		}
	}

	std::list<std::shared_ptr<DV::CurveData>> dataList;
	for (int i = 0; i < listValues.size(); i++)
	{
		auto curveData = DV::RendererFactory::creatCurveData(listValues[i], parValues[i]);
		dataList.push_back(curveData);
	}

	auto renderers = DV::RendererFactory::creatMultipleCurveRenderers(dataList);
	auto adapter = DV::RendererFactory::creatMultipleTimeAdapter(renderers);

	ChartEvent* event = new ChartEvent();
	event->setAdapter(adapter);
	EV::EventManager::postEvent(event);
#endif
}


//暂时全写再这儿 日后再改
QString MultipleTargetGeneticAlgorithmUI::replaceVariate()
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
	QString text;
#if 1
	{
		QFile file(QString::fromLocal8Bit("://script/script.lua"));
		file.open(QIODevice::ReadOnly);
		text = QString::fromUtf8(file.readAll());
		file.close();
	}
#else
	text = this->ui->textEdit->toPlainText();
#endif // SMART_EXE


	text += vars;

	//添加配置
	QString config = "";
	temp = QString("observeName = \"%1\";\n").arg("test");
	config += temp;
	temp = QString("maxTime = %1;\n").arg(0);
	config += temp;
	temp = QString("miniTime = %1;\n").arg(0);
	config += temp;
	temp = QString("excpectF = %1;\n").arg(0);
	config += temp;
	temp = QString("omiga = %1;\n").arg(0.0);
	config += temp;
	temp = QString("c1 = %1;\n").arg(0.0);
	config += temp;
	temp = QString("c2 = %1;\n").arg(0.0);
	config += temp;
	temp = QString("fmod = %1;\n").arg(0);
	config += temp;
	temp = QString("excpectMod = %1;\n").arg(0);
	config += temp;
	temp = QString("optimizeMaxCount = %1;\n").arg(0);
	config += temp;
	temp = QString("accuracy = %1/100;\n").arg(0);
	config += temp;

	//是否按照上次优化数据计息
	config += "continue = false;\n";

	text = config + text;

#ifdef SMART_EXE //输出拼接之后的脚本
	{
		QFile file(QString::fromLocal8Bit("./SmartControl.lua"));
		file.open(QIODevice::ReadWrite);
		file.write(text.toUtf8());
		file.close();
	}
#endif // SMART_EXE
	return text;
}

void MultipleTargetGeneticAlgorithmUI::saveParameterXml()
{
	pugi::xml_document doc;
	auto path = smartContorl->getM3dPath();
	path = path.left(path.length() - 4) + ".cc";
	auto gbk = QTextCodec::codecForName("gb2312");

	std::string ret = gbk->fromUnicode(path).data();
	auto result = doc.load_file(ret.c_str());
	pugi::xml_node root;
	if (!result)
	{
		doc.reset();
		if (!GMod)
			root = doc.append_child("MultipleTargetGeneticAlgorithm");
		else
			root = doc.append_child("MultipleTargetGeneticAlgorithmGMod");
	}
	else {
		if (!GMod)
		{
			doc.remove_child("MultipleTargetGeneticAlgorithm");
			root = doc.append_child("MultipleTargetGeneticAlgorithm");
		}
		else
		{
			doc.remove_child("MultipleTargetGeneticAlgorithmGMod");
			root = doc.append_child("MultipleTargetGeneticAlgorithmGMod");
		}
	}


	auto parNode = root.append_child("Parameter");
	auto configNode = root.append_child("Config");
	auto targetNode = root.append_child("Target");
 	configNode.append_attribute("OptimizeCount") = ui->spinBoxOptimizeCount->value();
	configNode.append_attribute("RunCount") = ui->spinBoxCount->value();
	configNode.append_attribute("RunMaxCount") = ui->spinBoxRunCount->value();

	auto listWidget = ui->listWidgetTarget;
	int itemsCount =listWidget->count();
	for (int i = 0; i < itemsCount; i++)
	{
		QString name = QString("Target%1").arg(i);
		auto node = targetNode.append_child(name.toStdString().c_str());
		auto item = listWidget->item(i);
		auto widget = listWidget->itemWidget(item);
		
		TargetItem* targetItem = dynamic_cast<TargetItem*>(widget);
		targetItem->saveXml(node);
	}

	for (auto i = variateDatas.begin(); i != variateDatas.end(); i++)
	{
		auto node = parNode.append_child((*i)->name.toStdString().c_str());
		std::string max = QString::number((*i)->max).toStdString();
		std::string mini = QString::number((*i)->mini).toStdString();
		node.append_attribute("Max") = max.c_str();
		node.append_attribute("Mini") = mini.c_str();
	}

	doc.save_file(ret.c_str());
}

void MultipleTargetGeneticAlgorithmUI::loadParameterXml()
{
	pugi::xml_document document;
	auto path = smartContorl->getM3dPath();
	path = path.left(path.length() - 4) + ".cc";
	auto gbk = QTextCodec::codecForName("gb2312");

	std::string ret = gbk->fromUnicode(path).data();
	auto result = document.load_file(ret.c_str());
	if (!result)
		return;
	pugi::xml_node root;
	if(!GMod)
		root = document.child("MultipleTargetGeneticAlgorithm");
	else
		root = document.child("MultipleTargetGeneticAlgorithmGMod");
	if (root.empty())
		return;

	auto parNode = root.child("Parameter");
	auto configNode = root.child("Config");
	auto targetNode = root.child("Target");

	auto listWidget = ui->listWidgetTarget;
	for (auto iter = targetNode.begin(); iter != targetNode.end(); iter++)
	{
		std::string id = iter->attribute("ID").as_string();
		TargetItem* targetItem;
		if (id == "TimeTarget")
		{
			auto t = new TimeTargetItemUI(listWidget);
			if (GMod)
				t->showG();
			targetItem = t;
		}
		else if (id == "TimeTargetDouble")
		{
			auto t = new TimeDoubleTargetItemUI(listWidget);
			if (GMod)
				t->showG();
			targetItem = t;
		}
		//新增处理PiModeTarget
		else if (id == "PiModeTarget")
		{
			auto t = new PiModeTargetItemUI(listWidget);
			if (GMod) t->showG();
			targetItem = t;
		}
		else
		{
			auto t = new FrequencyTargetItemUI(listWidget);
			if (GMod)
				t->showG();
			targetItem = t;
		}
			
		targetItem->loadXml(*iter);

		auto widget = dynamic_cast<QWidget*>(targetItem);
		if (!widget)
		{
			delete targetItem;
			continue;
		}
		QListWidgetItem* item = new QListWidgetItem(listWidget);
		item->setSizeHint(widget->size());
		listWidget->setItemWidget(item, widget);
	}


// 
 	ui->spinBoxOptimizeCount->setValue(configNode.attribute("OptimizeCount").as_int());
	ui->spinBoxRunCount->setValue(configNode.attribute("RunMaxCount").as_int());
	ui->spinBoxCount->setValue(configNode.attribute("RunCount").as_int());


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
		data->widget->initUi();
		data->widget->setData(data);
		variateDatas.push_back(data);

		this->ui->listWidgetVariate->addItem(data->item);
		auto size = data->widget->size();
		data->item->setSizeHint(size);
		this->ui->listWidgetVariate->setItemWidget(data->item, data->widget);
	}
}

void MultipleTargetGeneticAlgorithmUI::closeEvent(QCloseEvent* event)
{
	smartContorl->stop();
	auto data = SmartContorlData::GetInstance();
	data->clear();
	QDialog::closeEvent(event);
}
bool MultipleTargetGeneticAlgorithmUI::getRunning()
{
	return smartContorl->runing;
}

void MultipleTargetGeneticAlgorithmUI::setGMod(const bool& b)
{
	GMod = b;
}

#include "moc_MultipleTargetGeneticAlgorithmUI.cpp"