#include"smartCalc.h"
#include<QGridLayout>
#include"ui_smartCalc.h"
#include"VariateInputDialog.h"
#include"SmartContorlUI.h"
#include"VariateItemWidget.h"
smartCalc::smartCalc(QWidget* parent) :QWidget(parent),ui(new Ui::smartCalc)
{
	ui->setupUi(this);
	initUI();
}
void smartCalc::initUI()
{
	ui->ObjectName->setText("text");
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
	qPrint("addbutton");
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
			data->item = new QListWidgetItem();
			data->widget = new VariateItemWidget();
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
	}
}
void smartCalc::deleteButton(bool b)
{
	qPrint("deletebutton");
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
	//auto str = replaceVariate();
	//C:\Users\DELL\Desktop\opt.lua
}
void smartCalc::qPrint(std::string str)
{
	/*auto temp = QString::fromStdString(str);
	ui->plainTextEdit->appendPlainText(temp);*/
}
#include"moc_smartCalc.cpp"