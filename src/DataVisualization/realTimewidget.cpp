#include "realTimewidget.h"
#include "ui_realTimewidget.h"
#include <QLineEdit>
/**
* @brief  realTimewidget::realTimewidget
* @param  QWidget * parent  
* @return   
*/
realTimewidget::realTimewidget(QWidget* parent) :QDialog(parent), ui(new Ui::realTimewidget)
{
	ui->setupUi(this);
	//curRow = -1;
	//lastRow = -1;
}
/**
* @brief  realTimewidget::~realTimewidget
* @return   
*/
realTimewidget::~realTimewidget()
{

}
/**
* @brief  realTimewidget::closeEvent 关闭事件
* @param  QCloseEvent * event  
* @return void  
*/
void realTimewidget::closeEvent(QCloseEvent *event)
{
	//emit setcoloseEvent(true);
	/*auto row=ui->tableWidget->rowCount();
	std::vector<double> val;
	val.clear();
	for (auto index = 0; index < row; index++)
	{
		double curval = ui->tableWidget->item(index, 0)->text().toDouble();
		if (curval > max || curval<min)
		{
			continue;
		}
		val.push_back(curval);
	}
	std::sort(val.begin(),val.end());
	val.erase(std::unique(val.begin(),val.end()),val.end());
	std::list<double> vallist;
	for (auto iter=val.begin();iter!=val.end();iter++)
	{
		vallist.push_back(*iter);
	}
	emit GetListDouble(vallist);*/
	//disconnect(this, 0);
	QWidget::closeEvent(event);
}
/**
* @brief  realTimewidget::init 初始化
* @param  float min  
* @param  float max  
* @return void  
*/
void realTimewidget::init(float rmin, float rmax)
{
	min = rmin;
	max = rmax;
	this->setWindowTitle(QString("Rang:(%1~%2)").arg(min).arg(max));
	//初始化
	QStringList header;
	header << "value:"<<"Rang:";
	ui->tableWidget->setColumnCount(2);
	ui->tableWidget->setHorizontalHeaderLabels(header);
	ui->tableWidget->setShowGrid(false);
	auto cloumcount = ui->tableWidget->rowCount();
	for (int index = cloumcount; index >= 0;index--)
	{
		ui->tableWidget->removeRow(index);
	}
	//添加第一行
	int rowFirst = ui->tableWidget->rowCount();
	ui->tableWidget->insertRow(rowFirst);
	float curval = (min + max) / 2;
	ui->tableWidget->setItem(rowFirst,0,new QTableWidgetItem(QString("%1").arg(curval,0,'f',GetdecimalBit(curval))));
	QTableWidgetItem* item = new QTableWidgetItem(QString("%1~%2").arg(min, 0, 'f', GetdecimalBit(min)).arg(max, 0, 'f', GetdecimalBit(max)));
	item->setFlags(Qt::ItemIsEditable);
	ui->tableWidget->setItem(rowFirst,1,item);
	ui->tableWidget->resizeColumnsToContents();
	connect(ui->addBtn, SIGNAL(clicked()), this, SLOT(addClicked()));
	connect(ui->deleteBtn, SIGNAL(clicked()), this, SLOT(deleteClicked()));
	connect(ui->tableWidget, SIGNAL(itemClicked(QTableWidgetItem*)), this, SLOT(tableWidgetClicked(QTableWidgetItem*)));
	connect(ui->tableWidget, SIGNAL(itemDoubleClicked(QTableWidgetItem*)), this, SLOT(tableWidgetClicked(QTableWidgetItem*)));
}

/**
* @brief  realTimewidget::addClicked 添加按钮
* @return void  
*/
void realTimewidget::addClicked(){
	int row = ui->tableWidget->rowCount();
	if (row==0)
	{
		ui->tableWidget->insertRow(row);
		float curval = (min + max) / 2;
		ui->tableWidget->setItem(row, 0, new QTableWidgetItem(QString("%1").arg(curval, 0, 'f', GetdecimalBit(curval))));
	}
	else
	{
		ui->tableWidget->insertRow(row);
		float curval = ui->tableWidget->item(row - 1, 0)->text().toFloat();
		ui->tableWidget->setItem(row, 0, new QTableWidgetItem(QString("%1").arg(curval, 0, 'f', GetdecimalBit(curval))));
	}
	QTableWidgetItem* item = new QTableWidgetItem(QString("%1~%2").arg(min,0,'f',GetdecimalBit(min)).arg(max,0,'f',GetdecimalBit(max)));
	item->setFlags(Qt::ItemIsEditable);
	ui->tableWidget->setItem(row, 1, item);
}

/**
* @brief  realTimewidget::deleteClicked 删除按钮
* @return void  
*/
void realTimewidget::deleteClicked(){
	int row = ui->tableWidget->rowCount();
	ui->tableWidget->removeRow(row-1);
}

/**
* @brief  realTimewidget::GetdecimalBit 获取小数位数
* @param  double & value  
* @return int  
*/
int realTimewidget::GetdecimalBit(float& value)
{
	int valinter = static_cast<int>(value);
	double fspace = abs(value - static_cast<float>(valinter));
	unsigned __int32 index = 0;
	while (fspace>0.0f)
	{
		index++;
		fspace *= 10;
		valinter = static_cast<int> (fspace);
		fspace = fspace - static_cast<float>(valinter);
	}
	return index;
}
/**
* @brief  realTimewidget::tableWidgetClicked tablewidget点击
* @param  QTableWidgetItem * item  
* @return void  
*/
void realTimewidget::tableWidgetClicked(QTableWidgetItem* item)
{
	curRow = ui->tableWidget->currentRow();
	/*if (0 == curRow)
		return;
	if (lastRow != curRow&&lastRow!=-1)
	{
		float lastvalue = ui->tableWidget->item(lastRow,0)->text().toFloat();
		if (lastvalue>max ||lastvalue<min)
		{
			float tempval = ui->tableWidget->item(lastRow-1,0)->text().toFloat();
			ui->tableWidget->item(lastRow, 0)->setText(QString("%1").arg(tempval,0,'f',GetdecimalBit(tempval)));
		}
	}
	lastRow = curRow;*/
}
/**
* @brief  realTimewidget::insertformatTableItem 插入控件
* @param  int row  
* @return void  
*/
void realTimewidget::insertformatTableItem()
{
	
}
void realTimewidget::BtnClicked()
{
	if (sender()==ui->addBtn)
	{
		addClicked();
	}
	else if (sender()==ui->deleteBtn)
	{
		deleteClicked();
	}
	else if (sender()==ui->saveBtn)
	{
		auto row = ui->tableWidget->rowCount();
		std::vector<double> val;
		val.clear();
		for (auto index = row-1; index >=0 ; index--)
		{
			double curval = ui->tableWidget->item(index, 0)->text().toDouble();
			ui->tableWidget->removeRow(index);
			if (curval > max || curval < min)	continue;
			val.push_back(curval);
		}
		std::sort(val.begin(), val.end());
		val.erase(std::unique(val.begin(), val.end()), val.end());
		std::list<double> vallist;
		for (auto iter = val.begin(); iter != val.end(); iter++) {
			addTableItem(*iter);
			vallist.push_back(*iter);
		}
		emit GetListDouble(vallist);
	}
}
void realTimewidget::init(std::list<double>& leves)
{
	min = max = *leves.begin();
	for (auto iter = leves.begin(); iter != leves.end(); iter++)
	{
		if (min > *iter) min = *iter;
		if (max < *iter) max = *iter;
	}
	this->setWindowTitle(QString("Rang:(%1~%2)").arg(min).arg(max));
	//初始化
	QStringList header;
	header << "levelval:" << "Rang:";
	ui->tableWidget->setColumnCount(1);
	ui->tableWidget->setHorizontalHeaderLabels(header);
	ui->tableWidget->setShowGrid(false);
	ui->tableWidget->horizontalHeader()->setResizeMode(QHeaderView::ResizeMode::Stretch);
	auto cloumcount = ui->tableWidget->rowCount();
	for (int index = cloumcount; index >= 0; index--)	ui->tableWidget->removeRow(index);
	for (auto iter = leves.begin(); iter != leves.end(); iter++)	addTableItem(*iter);
	//添加
	connect(ui->addBtn, SIGNAL(clicked()), this, SLOT(BtnClicked()));
	connect(ui->deleteBtn, SIGNAL(clicked()), this, SLOT(BtnClicked()));
	connect(ui->saveBtn, SIGNAL(clicked()), this, SLOT(BtnClicked()));
	connect(ui->tableWidget, SIGNAL(itemClicked(QTableWidgetItem*)), this, SLOT(tableWidgetClicked(QTableWidgetItem*)));
	connect(ui->tableWidget, SIGNAL(itemDoubleClicked(QTableWidgetItem*)), this, SLOT(tableWidgetClicked(QTableWidgetItem*)));
}
void realTimewidget::addTableItem(double val)
{
	int row = ui->tableWidget->rowCount();
	ui->tableWidget->insertRow(row);
	ui->tableWidget->setItem(row, 0, new QTableWidgetItem(QString("%1").arg(val,0,'f',GetdecimalBit(val))));
}
int realTimewidget::GetdecimalBit(double& value)
{
	__int64 valinter = static_cast<__int64>(value);
	double fspace = abs(value - static_cast<double>(valinter));
	unsigned __int32 index = 0;
	while (fspace > 0.0f)
	{
		index++;
		fspace *= 10;
		valinter = static_cast<__int64> (fspace);
		fspace = fspace - static_cast<double>(valinter);
	}
	return index;
}
#include "moc_realTimewidget.cpp"