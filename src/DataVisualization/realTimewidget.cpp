#include "realTimewidget.h"
#include "ui_realTimewidget.h"
#include "QHeaderView"
#include "ScalarTableItem.h"
namespace DV
{
	const long long max64 = 0x7fffffffffffffff;
	int GetdecimalBit(double& value);
	QString valToQString(double val, int bit);
};
DV::realTimewidget::realTimewidget(QWidget* parent/*=nullptr*/) :
	QDialog(parent),
	ui(new Ui::realTimewidget)
{
	ui->setupUi(this);
	//初始化ui
	QStringList header;
	header << "levelval:";
	//设置表头目
	ui->tableWidget->setColumnCount(1);
	ui->tableWidget->setHorizontalHeaderLabels(header);
	ui->tableWidget->horizontalHeader()->setResizeMode(QHeaderView::ResizeMode::Stretch);
	//
	connect(ui->addBtn, SIGNAL(clicked()), this, SLOT(btnClicked()));
	connect(ui->saveBtn, SIGNAL(clicked()), this, SLOT(btnClicked()));
	connect(ui->deleteBtn, SIGNAL(clicked()), this, SLOT(btnClicked()));
	connect(ui->tableWidget,SIGNAL(cellChanged(int,int)),this,SLOT(slotCellChange(int,int)));
}

DV::realTimewidget::~realTimewidget()
{

}


void DV::realTimewidget::loadConfigLevels(std::list<double>& leves)
{
	leves.sort();
	clearTableItem();
	min = max = *leves.begin();
	for (auto iter = leves.begin(); iter != leves.end(); iter++)
	{
		if (min > *iter) min = *iter;
		if (max < *iter) max = *iter;
		addTableItem(*iter);
	}
	setRangTitle();
}


/**
* @time	2021/12/24
* @brief DV::realTimewidget::getConfigLevels 获取等值线等级
* @return std::list<double>
*/

std::list<double> DV::realTimewidget::getConfigLevels()
{
	int rowCount = ui->tableWidget->rowCount();
	std::list<double> values;
	for (int i = 0; i < rowCount; ++i)
	{
		 ScalarTableItem* scalarItem=dynamic_cast<ScalarTableItem*>(ui->tableWidget->item(i,0));
		 if (scalarItem != nullptr)
			 values.push_back(scalarItem->getValue());
	}
	return values;
}

/**
* @time	2021/12/24
* @brief DV::realTimewidget::addTableItem 添加item
* @param double val
* @return void
*/
void DV::realTimewidget::addTableItem(double val)
{
	int row = ui->tableWidget->rowCount();
	ui->tableWidget->insertRow(row);
	/*ui->tableWidget->setItem(row, 0,
		new QTableWidgetItem(QString("%1").arg(val)));*/
	ScalarTableItem* item = new ScalarTableItem(QString("%1").arg(val),val);
	ui->tableWidget->setItem(row, 0, item);
}


void DV::realTimewidget::setRangTitle()
{
	this->setWindowTitle(QString("Rang:(%1-%2)").arg(min).arg(max));
}


/**
* @time	2021/12/24
* @brief DV::realTimewidget::clearTableItem 清空表格的内容
* @return void
*/
void DV::realTimewidget::clearTableItem()
{
	auto row = ui->tableWidget->rowCount();
	for (int i = row - 1; i >= 0; --i)
		ui->tableWidget->removeRow(i);
}
/**
* @time	2021/12/24
* @brief DV::realTimewidget::btnClicked 按钮点击事件
* @return void
*/
void DV::realTimewidget::btnClicked()
{
	if (sender() == ui->saveBtn)
	{
		saveClicked();
	}
	else if (sender() == ui->addBtn)
	{
		addClicked();
	}
	else if (sender() == ui->deleteBtn)
	{
		deleteClicked();
	}
}


/**
* @time	2021/12/24
* @brief DV::realTimewidget::addClicked 增加条目
* @return void
*/
void DV::realTimewidget::addClicked()
{
	int row = ui->tableWidget->rowCount();
	addTableItem(0.0f);
}


/**
* @time	2021/12/24
* @brief DV::realTimewidget::deleteClicked 删除条目
* @return void
*/
void DV::realTimewidget::deleteClicked()
{
	int currentRow = ui->tableWidget->currentRow();
	int row = ui->tableWidget->rowCount();
	if (currentRow<0 || currentRow>row - 1)
		ui->tableWidget->removeRow(row - 1);
	else
		ui->tableWidget->removeRow(currentRow);
}


/**
* @time	2021/12/24
* @brief DV::realTimewidget::saveClicked 将数据进行整理，并触发信号
* @return void
*/
void DV::realTimewidget::saveClicked()
{
	//取出数据
	auto dataList = getConfigLevels();
	loadConfigLevels(dataList);
	emit sendConfigLevels(dataList);
}

QString DV::valToQString(double val, int bit)
{
	QString temp;
	if (-1 == bit)
		temp = QString("%1").arg(val);
	else
		temp = QString("%1").arg(val, 0, 'f', bit);
	return temp;
}

int DV::GetdecimalBit(double& value)
{
	double absvalue = abs(value);
	double maxdouble = static_cast<double>(max64);
	if (absvalue > maxdouble)return -1;
	unsigned __int64 valinter = static_cast<unsigned __int64>(absvalue);
	/*static_cast<unsigned __int64>(absvalue);*/
	double fspace = abs(absvalue - static_cast<double>(valinter));
	unsigned __int32 index = 0;
	while (fspace > 0.0f)
	{
		index++;
		fspace *= 10;
		valinter = static_cast<unsigned __int64> (fspace);
		fspace = fspace - static_cast<double>(valinter);
	}
	return index;
}

/**
* @time	2021/12/27
* @brief DV::realTimewidget::slotCellChange 
* @param int r
* @param int c
* @return void
*/
void DV::realTimewidget::slotCellChange(int r, int c)
{
	ScalarTableItem* item=dynamic_cast<ScalarTableItem*>(ui->tableWidget->item(r, c));
	if (item == nullptr)
		return;
	double val = item->text().toDouble();
	item->setValue(val);
}
#include "moc_realTimewidget.cpp"