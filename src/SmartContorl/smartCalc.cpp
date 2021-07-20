#include"smartCalc.h"
#include<QGridLayout>
#include"ui_smartCalc.h"
#include"VariateInputDialog.h"
#include"SmartContorlUI.h"
#include"VariateitemDialog.h"
#include"QMessageBox"
#include"QTextStream"
#include <SmartContorlData.h>
#include <Contorl/ContorlInterface.h>
#include "xml/pugixml.hpp"
#include <QTextCodec>
#include<QListWidgetItem>
#include<QDebug>
#include"VariateitemWidget2.h"
void SplitString(const std::string& s, std::vector<std::string>& v, const std::string& c);
smartCalc::smartCalc(QWidget* parent) :QDialog(parent),ui(new Ui::smartCalc)
{
	ui->setupUi(this);
	initUI();
	//initData();
}
void smartCalc::initUI()
{
//	ui->ObjectName->setText("text");
	//输入模式：
	{
		ui->Mode1->setChecked(true);
		ui->Mode2->setChecked(false);
	}
	//添加变量
	connect(ui->addPushbutton,SIGNAL(clicked(bool)),this,SLOT(BtnClicked(bool)));
	connect(ui->deletePushbutton,SIGNAL(clicked(bool)),this,SLOT(BtnClicked(bool)));
	connect(ui->run,SIGNAL(clicked(bool)),this,SLOT(BtnClicked(bool)));
}
void smartCalc::initData()
{
	auto contorData = SmartContorlData::GetInstance();
	smartContorl = contorData->smartContorl;
	auto contorlInterface = ContorlInterface::GetInstance();
	std::string m3dPath = "D:/wdtProject/test/test.m3d";
	smartContorl->setM3dPath(m3dPath);
	loadParameterXml();
	connect(smartContorl, SIGNAL(addDataBar(QListWidgetItem*, QWidget*)), this, SLOT(addListWidgetItem(QListWidgetItem*, QWidget*)));
	connect(smartContorl, SIGNAL(smartContorlLog(std::string)), this, SLOT(pringLuaLog(std::string)));

	this->setModal(true);
	setWindowFlags(Qt::Dialog | Qt::WindowMinimizeButtonHint);
}
void smartCalc::BtnClicked(bool b)
{
	if (sender() == ui->addPushbutton)
		addButton(b);
	else if (sender() == ui->deletePushbutton)
		deleteButton(b);
	else if(sender()==ui->run)
		run(b);
}
void smartCalc::addButton(bool b)
{
	//qPrint("addbutton");
	//获取输入模式
	if (ui->Mode1->isChecked())
	{
		//模式1,用户添加变量名，输入范围，步长
		VariateInputDialog d;
		d.exec();
		if (d.okClicked)
		{
			auto data = d.getData();
			data->count = this->ui->spinBoxRunCount->value();
			data->Mode = 1;
			data->item = new QListWidgetItem();
			data->widget = new VariateitemDialog();
			data->widget->initUi();
			data->widget->setData(data);
			variateDatas.push_back(data);

			this->ui->listWidgetVariate->addItem(data->item);
			auto size = data->widget->size();
			data->item->setSizeHint(size);
			this->ui->listWidgetVariate->setItemWidget(data->item,data->widget);
		}
		
	}
	else
	{
		//模式2，用户添加变量名，手动输入数值
		VariateitemWidget2 d;
		d.setModal(true);
		d.exec();
		if (d.okClicked)
		{
			std::shared_ptr<VariateData> data(new VariateData);
			data->name =d.getName() ;
			data->stepLength = d.getCount();
			std::vector<double> datas = d.getdatas();
			data->datas = datas;
			data->max = *(datas.end() - 1);
			data->mini = *(datas.begin());
			data->Mode = 2;
			data->item = new QListWidgetItem();
			data->widget = new VariateitemDialog();
			data->widget->initUi();
			data->widget->setData(data);
			variateDatas.push_back(data);
			this->ui->listWidgetVariate->addItem(data->item);
			auto size = data->widget->size();
			data->item->setSizeHint(size);
			this->ui->listWidgetVariate->setItemWidget(data->item, data->widget);
		}


	}
}
void smartCalc::deleteButton(bool b)
{
	//qPrint("deletebutton");
	auto items = this->ui->listWidgetVariate->selectedItems();
	if (items.size() < 1)
		return;
	auto item = items.begin();
	for (auto iter=variateDatas.begin();iter!=variateDatas.end();iter++)
	{
		if ((*iter)->item==*item)
		{
			(*iter)->deleteUI();
			variateDatas.erase(iter);
			return;
		}
	}
}
void smartCalc::run(bool)
{
	auto str = replaceVariate();
	smartContorl->run(str);
	saveParameterXml();
}
void smartCalc::loadParameterXml()
{
	pugi::xml_document document;
	auto path = smartContorl->getM3dPath();
	qPrint(path);
	path = path.left(path.length() - 4) + "_bat.cc";
	auto gbk = QTextCodec::codecForName("gb2312");

	std::string ret = gbk->fromUnicode(path).data();
	auto result = document.load_file(ret.c_str());
	if (!result)
		return;
	auto parNode = document.child("Parameter");
	auto configNode = document.child("Config");
	//ui->spinBoxOptimizeCount->setValue(configNode.attribute("OptimizeCount").as_int());
	//ui->spinBoxRunCount->setValue(configNode.attribute("RunMaxCount").as_int());
	//ui->spinBoxCount->setValue(configNode.attribute("RunCount").as_int());
	//ui->lineEditName->setText(QString::fromStdString(configNode.attribute("ObserveName").as_string()));
	//ui->lineEditMaxTime->setText(QString::number(configNode.attribute("MaxTime").as_int()));
	//ui->lineEditMiniTime->setText(QString::number(configNode.attribute("MiniTime").as_int()));
	//ui->comboBoxF->setCurrentIndex(configNode.attribute("FModIndex").as_int());
	//ui->lineEditMaxF->setText(QString::number(configNode.attribute("F").as_llong()));
	//ui->comboBoxExcpcet->setCurrentIndex(configNode.attribute("ExcpectMod").as_int());
	//ui->lineEditAccuracy->setText(QString::number(configNode.attribute("Accuracy").as_double()));
	//ui->lineEditC1->setText(QString::number(configNode.attribute("C1").as_double()));
	//ui->lineEditC2->setText(QString::number(configNode.attribute("C2").as_double()));
	//ui->lineEditOmega->setText(QString::number(configNode.attribute("Omega").as_double()));

	for (auto iter = parNode.begin(); iter != parNode.end(); iter++)
	{
		std::shared_ptr<VariateData> data;
		data.reset(new VariateData);
		//data->count = configNode.attribute("RunMaxCount").as_int();
		data->name = QString::fromStdString(iter->name());
		data->max = iter->attribute("Max").as_double();
		data->mini = iter->attribute("Mini").as_double();
		//data->stepLength = configNode.attribute("RunMaxCount").as_int();
		data->stepLength = iter->attribute("stepLength").as_int();
		data->Mode = iter->attribute("Mode").as_int();
		if (2==data->Mode)
		{
			std::vector<std::string> v;
			SplitString(iter->attribute("datas").as_string(), v,",");
			std::vector<double> vals;
			for (auto strit=v.begin();strit!=v.end();strit++)
				vals.push_back(atof(strit->c_str()));
			data->datas = vals;
		}
		data->item = new QListWidgetItem();
		data->widget = new VariateitemDialog();
		data->widget->initUi();
		data->widget->setData(data);
		variateDatas.push_back(data);
		this->ui->listWidgetVariate->addItem(data->item);
		auto size = data->widget->size();
		data->item->setSizeHint(size);
		this->ui->listWidgetVariate->setItemWidget(data->item, data->widget);
	}
}
QString smartCalc::replaceVariate()
{
	//添加参数
	int count = this->ui->spinBoxRunCount->value();
	QString vars = "\n";
	QString temp = "";
	for (auto iter = variateDatas.begin(); iter != variateDatas.end(); iter++)
	{
		if (1==(*iter)->Mode)
		{
			temp = QString("addVarMod1(\"%1\",%2,%3,%4);\n").arg((*iter)->name)
				.arg((*iter)->max).arg((*iter)->mini).arg(count);
			vars += temp;
		}
		else if (2==(*iter)->Mode)
		{
			for (auto iter2=(*iter)->datas.begin();iter2!= (*iter)->datas.end();iter2++)
			{
				temp = QString("addVarMod2(\"%1\",%2);\n").arg((*iter)->name).arg(*iter2);
				vars += temp;
			}
		}
	}
	//auto text = this->ui->textEdit->toPlainText();
	//text += vars;
	QString text="";
	//获取全部文本
	//QFile f("C://Users//DELL//Desktop//opt.lua");
	//QFile f("D://wdtProject//FreeCAD//FreeCAD//src//SmartContorl//opt.lua");
	QFile f(scriptPath.c_str());
	if (!f.open(QIODevice::ReadOnly | QIODevice::Text))//打开指定文件
		QMessageBox::about(NULL, "文件", "文件打开失败");
	QTextStream txtInput(&f);
	QString lineStr;
	while (!txtInput.atEnd())
	{
		text += txtInput.readLine();  //读取数据
		text += "\n";
	}
	f.close();
	text += vars;
	//添加配置
	//QString config = "";
	//temp = QString("observeName = \"%1\";\n").arg(this->ui->lineEditName->text());
	//config += temp;
	//temp = QString("maxTime = %1;\n").arg(this->ui->lineEditMaxTime->text().toInt());
	//config += temp;
	//temp = QString("miniTime = %1;\n").arg(this->ui->lineEditMiniTime->text().toInt());
	//config += temp;
	//temp = QString("excpectF = %1;\n").arg(this->ui->lineEditMaxF->text().toLongLong());
	//config += temp;
	//temp = QString("omiga = %1;\n").arg(this->ui->lineEditOmega->text().toDouble());
	//config += temp;
	//temp = QString("c1 = %1;\n").arg(this->ui->lineEditC1->text().toDouble());
	//config += temp;
	//temp = QString("c2 = %1;\n").arg(this->ui->lineEditC2->text().toDouble());
	//config += temp;
	//temp = QString("fmod = %1;\n").arg(this->ui->comboBoxF->currentIndex());
	//config += temp;
	//temp = QString("excpectMod = %1;\n").arg(this->ui->comboBoxExcpcet->currentIndex());
	//config += temp;
	//temp = QString("optimizeMaxCount = %1;\n").arg(this->ui->spinBoxOptimizeCount->value());
	//config += temp;
	//temp = QString("accuracy = %1/100;\n").arg(this->ui->lineEditAccuracy->text());
	//config += temp;
	//text = config + text;

	qPrint(text);
	return text;
}
void smartCalc::saveParameterXml()
{
	pugi::xml_document doc;
	auto parNode = doc.append_child("Parameter");
	auto configNode = doc.append_child("Config");
	//configNode.append_attribute("OptimizeCount") = ui->spinBoxOptimizeCount->value();
	//configNode.append_attribute("RunCount") = ui->spinBoxCount->value();
	configNode.append_attribute("RunMaxCount") = ui->spinBoxRunCount->value();
	//configNode.append_attribute("ObserveName") = ui->lineEditName->text().toStdString().c_str();
	//configNode.append_attribute("MaxTime") = ui->lineEditMaxTime->text().toInt();
	//configNode.append_attribute("MiniTime") = ui->lineEditMiniTime->text().toInt();
	//configNode.append_attribute("FModIndex") = ui->comboBoxF->currentIndex();
	//configNode.append_attribute("F") = ui->lineEditMaxF->text().toLongLong();
	//configNode.append_attribute("ExcpectMod") = ui->comboBoxExcpcet->currentIndex();
	//configNode.append_attribute("Accuracy") = ui->lineEditAccuracy->text().toStdString().c_str();
	//configNode.append_attribute("C1") = ui->lineEditC1->text().toStdString().c_str();
	//configNode.append_attribute("C2") = ui->lineEditC2->text().toStdString().c_str();
	//configNode.append_attribute("Omega") = ui->lineEditOmega->text().toStdString().c_str();
	for (auto i = variateDatas.begin(); i != variateDatas.end(); i++)
	{
		auto node = parNode.append_child((*i)->name.toStdString().c_str());
		std::string max = QString::number((*i)->max).toStdString();
		std::string mini = QString::number((*i)->mini).toStdString();
		std::string steplength = QString::number((*i)->stepLength).toStdString();
		std::string mode = QString::number((*i)->Mode).toStdString();
		node.append_attribute("Mode")=mode.c_str();
		node.append_attribute("Max") = max.c_str();
		node.append_attribute("Mini") = mini.c_str();
		node.append_attribute("stepLength") = steplength.c_str();
		//如果为模式2，需要存下数组队列
		
		if (2==(*i)->Mode){
			QString qdatas = "";
			std::vector<double> vals = (*i)->datas;
			for (auto iter=vals.begin();iter!=vals.end();iter++)
			{
				qdatas += QString::number(*iter);
				qdatas += ",";
			}

			std::string sdatas = qdatas.toStdString();
			sdatas=sdatas.substr(0,sdatas.length()-1);
			node.append_attribute("datas")=sdatas.c_str();
		}
	}
	auto path = smartContorl->getM3dPath();
	path = path.left(path.length() - 4) + "_bat.cc";
	auto gbk = QTextCodec::codecForName("gb2312");

	std::string ret = gbk->fromUnicode(path).data();
	doc.save_file(ret.c_str());
}
void smartCalc::qPrint(QString str)
{
	//ui->plainTextEdit->appendPlainText(str);
}
void smartCalc::qPrint(std::string str)
{
	auto temp = QString::fromStdString(str);
	//ui->plainTextEdit->appendPlainText(temp);
}
void smartCalc::addListWidgetItem(QListWidgetItem* item, QWidget* widget)
{
	ui->listWidget->addItem(item);
	ui->listWidget->setItemWidget(item, widget);
}
void smartCalc::pringLuaLog(std::string str)
{
	qPrint(str);
}

void SplitString(const std::string& s, std::vector<std::string>& v, const std::string& c)
{
	std::string::size_type pos1, pos2;
	pos2 = s.find(c);
	pos1 = 0;
	while (std::string::npos != pos2)
	{
		v.push_back(s.substr(pos1, pos2 - pos1));

		pos1 = pos2 + c.size();
		pos2 = s.find(c, pos1);
	}
	if (pos1 != s.length())
		v.push_back(s.substr(pos1));
}
/**
* @brief smartCalc::afferscriptpath 传入脚本路径
* @param std::string path
* @return void
* @Time 2021/7/15
*/
void smartCalc::afferscriptpath(std::string path)
{
	scriptPath = path;
}
/**
* @brief smartCalc::afferm3dpath 传入m3d的路径
* @param std::string path
* @return void
* @Time 2021/7/15
*/
void smartCalc::afferm3dpath(std::string path)
{
	m3dPath = path;
	auto contorData = SmartContorlData::GetInstance();
	smartContorl = contorData->smartContorl;
	auto contorlInterface = ContorlInterface::GetInstance();
	std::string m3dPath = path;
	smartContorl->setM3dPath(m3dPath);
	loadParameterXml();
	connect(smartContorl, SIGNAL(addDataBar(QListWidgetItem*, QWidget*)), this, SLOT(addListWidgetItem(QListWidgetItem*, QWidget*)));
	connect(smartContorl, SIGNAL(smartContorlLog(std::string)), this, SLOT(pringLuaLog(std::string)));

	this->setModal(true);
	setWindowFlags(Qt::Dialog | Qt::WindowMinimizeButtonHint);
}
#include"moc_smartCalc.cpp"