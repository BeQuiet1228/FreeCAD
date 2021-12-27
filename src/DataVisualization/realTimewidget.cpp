#include "realTimewidget.h"
#include "ui_realTimewidget.h"
#include "QHeaderView"
#include "ScalarTableItem.h"
namespace DV
{
	QString compareValToQString(double& val1, double& val2, const double callVal);
	int getBitInt(const double values);
	int getBitDec(const double values);
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
}
DV::realTimewidget::~realTimewidget()
{

}
/**
* @time	2021/12/27
* @brief DV::realTimewidget::loadConfigLevels 读取数据至表中
* @param std::list<double> & leves
* @return void
*/
void DV::realTimewidget::loadConfigLevels(std::list<double>& leves)
{
	leves.sort();
	boolCellChangedConnect(false);
	clearTableItem();
	//min = max = *(leves.begin());
	min = *leves.begin();
	max = *leves.rbegin();
	auto datas = getScalarDatas(leves);
	for (auto iter = datas.begin(); iter != datas.end(); ++iter)
		addTableItem(iter->valStr, iter->value);
	setRangTitle();
	boolCellChangedConnect(true);
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
		ScalarTableItem* scalarItem = dynamic_cast<ScalarTableItem*>(ui->tableWidget->item(i, 0));
		if (scalarItem != nullptr)
			values.push_back(scalarItem->getValue());
	}
	return values;
}


/**
* @time	2021/12/27
* @brief DV::realTimewidget::getScalarDatas 获取标尺数据类型
* @param std::list<double> & value
* @return std::list<DV::realTimewidget::ScalarItemData>
*/
std::list<DV::realTimewidget::ScalarItemData> DV::realTimewidget::getScalarDatas(std::list<double>& value)
{
	/*
		将数据转换成字符串和数值，字符串用于展示，数值为实际数值
	*/
	std::list<ScalarItemData> datas;
	value.sort();
#if 1
	auto iterLast = value.rbegin(); iterLast++;
	double firstVal = 0.0f, secondVal = 0.0f;
	//逆向比较数值
	for (auto iter = value.rbegin(); iter != value.rend(); ++iter, ++iterLast)
	{
		if (iterLast == value.rend())
			break;
		ScalarItemData data;
		/*
		 有一种特殊情况，当正负两个数值比较大小时，无法获取到精确的有效位，因为始终满足非负>负数的情况
		*/
		if ((*iterLast) * (*iter) < 0.0f && *iter < secondVal)
			data.valStr = compareValToQString(*iter, secondVal, *iter);
		else
			data.valStr = compareValToQString(*iterLast, *iter, *iter);
		data.value = *iter;
		datas.push_back(data);
		firstVal = *iterLast;
		secondVal = *iter;
	}
	//装入最后一个点
	{
		ScalarItemData data;
		data.valStr = compareValToQString(firstVal, secondVal, firstVal);
		data.value = firstVal;
		datas.push_back(data);
	}
	datas.sort();
#endif
#if 0
	auto iterNext = value.begin(); iterNext++;
	double endVal, lastVal;
	for (auto iter = value.begin(); iter != value.end(); ++iter, ++iterNext)
	{
		if (iterNext == value.end())
			break;
		ScalarItemData data;
		data.valStr = compareValToQString(*iter, *iterNext, *iter);
		data.value = *iter;
		datas.push_back(data);
		endVal = *iterNext;
		lastVal = *iter;
	}
	//装入最后一个点
	{
		ScalarItemData data;
		data.valStr = compareValToQString(endVal, lastVal, endVal);
		data.value = endVal;
		datas.push_back(data);
}
#endif
	return datas;
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
	ScalarTableItem* item = new ScalarTableItem(QString("%1").arg(val), val);
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
* @time	2021/12/27
* @brief DV::realTimewidget::boolCellChangedConnect 用于开启和关闭条目改变时是否需要关联到槽
* @param bool
* @return void
*/
void DV::realTimewidget::boolCellChangedConnect(bool b)
{
	/*
		用于防止读取数据列表时，字符串信息，改变时调用单元改变时的槽函数，频繁修改val的值。
	*/
	(b) ?
		(connect(ui->tableWidget, SIGNAL(cellChanged(int, int)), this, SLOT(slotCellChange(int, int)))) :
		(disconnect(ui->tableWidget, SIGNAL(cellChanged(int, int)), this, SLOT(slotCellChange(int, int))));
}


/**
* @time	2021/12/27
* @brief DV::realTimewidget::addTableItem 添加item
* @param QString
* @param double
* @return void
*/
void DV::realTimewidget::addTableItem(QString str, double val)
{
	int row = ui->tableWidget->rowCount();
	ui->tableWidget->insertRow(row);
	ScalarTableItem* item = new ScalarTableItem(str, val);
	ui->tableWidget->setItem(row, 0, item);
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

/**
* @time	2021/12/27
* @brief DV::realTimewidget::slotCellChange
* @param int r
* @param int c
* @return void
*/
void DV::realTimewidget::slotCellChange(int r, int c)
{
	ScalarTableItem* item = dynamic_cast<ScalarTableItem*>(ui->tableWidget->item(r, c));
	if (item == nullptr)
		return;
	double val = item->text().toDouble();
	item->setValue(val);
}
bool DV::realTimewidget::ScalarItemData::operator<(const ScalarItemData& that) const
{
	if (this->value < that.value)
		return true;
	return false;
}

/**
* @time	2021/12/27
* @brief DV::compareValToQString 比较浮点数获取有效位，并将callVal转换成字符串
* @param double & val1 比较的数值
* @param double & val2
* @param const double callVal 需要转换的数值
* @return QString
*/
QString DV::compareValToQString(double& val1, double& val2, const double callVal)
{
	double intervalVal = abs(val1 - val2);
	if (0.0f == intervalVal)
		return QString("%1").arg(callVal);
	double* maxVal, * minVal;
	if (val2 > val1) {
		maxVal = &val2;
		minVal = &val1;
	}
	else {
		maxVal = &val1;
		minVal = &val2;
	}
	//若插值大于1
	if (intervalVal >= 1.0f)
	{
		//获取最大的位数
		double intervalValDouble = intervalVal;
		int index = getBitInt(intervalValDouble);
		//获取整数部分的位数
		int bitInt = getBitInt(callVal);
		int keepBit = (bitInt - index > 0) ? (bitInt - index) : (1);
		QString qstr = QString::number(callVal, 'E', keepBit);
		std::string str = qstr.toStdString();
		return qstr;
	}
	else
	{
		//获取最大位数
		double intervalValDouble = intervalVal;
		int intervalBit = getBitDec(intervalValDouble);
		int valBit = getBitDec(callVal);
		QString qstr = (
			(abs(callVal) < 1.0f) ?
			(QString::number(callVal, 'E', abs(intervalBit - valBit))) :
			(QString::number(callVal, 'F', abs(intervalBit - valBit)))
			);
		std::string str = qstr.toStdString();
		return qstr;
	}
}
int DV::getBitInt(const double value)
{
	int index = 0;
	//获取整数部分
	double valuesInt = floor(abs(value));
	while (valuesInt > 1.0f)
	{
		valuesInt = valuesInt / 10.0f;
		index++;
	}
	return index;
}

/**
* @time	2021/12/27
* @brief DV::getBitDec 获取小数点后的非0位数
* @param const double value
* @return int
*/
int DV::getBitDec(const double value)
{
	int index = 0;
	//获取小鼠部分
	double valueDec = abs(value);
	while (valueDec < 1.0f)
	{
		valueDec = valueDec * 10.0f;
		index++;
	}
	return index;
}
#include "moc_realTimewidget.cpp"