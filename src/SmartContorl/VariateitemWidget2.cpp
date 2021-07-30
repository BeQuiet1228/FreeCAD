#include"VariateitemWidget2.h"
#include<QTableWidget>
#include<QPushButton>
#include<QGridLayout>
#include<QLineEdit>
#include<QLabel>
#include<QHeaderView>
#include<QTableWidgetItem>
VariateitemWidget2::VariateitemWidget2(QWidget* parent):QDialog(parent),currow(-1)
{
	initUI();
}
VariateitemWidget2::~VariateitemWidget2()
{

}
void VariateitemWidget2::initUI()
{
	mtablewidget = new QTableWidget(this);
	mtablewidget->setColumnCount(1);
	addBtn=new QPushButton(this);
	deleteBtn=new QPushButton(this);
	okBtn = new QPushButton(this);
	layout=new QGridLayout;
	layout->setSpacing(0);
	mLineEdit=new QLineEdit(this);
	QLabel* label = new QLabel(this);
	/*********************************/
	this->setLayout(layout);
	layout->addWidget(label,0,0,1,1);
	layout->addWidget(mLineEdit, 0, 1, 1, 1);
	layout->addWidget(mtablewidget,1,0,1,3);
	layout->addWidget(addBtn,2,0,1,1);
	layout->addWidget(okBtn, 2, 1, 1, 1);
	layout->addWidget(deleteBtn, 2, 2, 1, 1);
	//
	addBtn->setText("add");
	deleteBtn->setText("delete");
	okBtn->setText("ok");
	label->setText("name");
	QStringList header;
	header << "DATA:";
	mtablewidget->setHorizontalHeaderLabels(header);
	mtablewidget->horizontalHeader()->setResizeMode(QHeaderView::ResizeMode::Stretch);
	//信号连接
	connect(addBtn,SIGNAL(clicked(bool)),this,SLOT(BtnClicked(bool))); 
	connect(deleteBtn,SIGNAL(clicked(bool)),this,SLOT(BtnClicked(bool))); 
	connect(okBtn,SIGNAL(clicked(bool)),this,SLOT(BtnClicked(bool))); 
	connect(mtablewidget,SIGNAL(itemClicked(QTableWidgetItem*)),this,SLOT(tableWidgetClicked(QTableWidgetItem*)));
}
void VariateitemWidget2::BtnClicked(bool b)
{
	if (sender() == addBtn)
	{
		//添加
		addtablewidget();
	}
	else if (sender() == deleteBtn)
	{
		//删除
		deletetablewidget();
	}
	else if (sender() == okBtn)
	{
		//确定
		OKClicked();
	}
}
void VariateitemWidget2::addtablewidget()
{
	int row = mtablewidget->rowCount();
	mtablewidget->insertRow(row);
	mtablewidget->setItem(row,0,new QTableWidgetItem(QString("")));
	currow = -1;
}
void VariateitemWidget2::deletetablewidget()
{
	int row = mtablewidget->rowCount();
	if (0 == row)
		return;
	if (currow!=-1)
		mtablewidget->removeRow(currow);
	else
		mtablewidget->removeRow(row-1);
	currow = -1;
}
void VariateitemWidget2::OKClicked()
{
	//获取数据
	int rowcount = mtablewidget->rowCount();
	if (0 == rowcount)
		return;
	name = mLineEdit->text();
	if (name == QString(""))
		return;
	std::vector<double> vals;
	for (int i=0;i<rowcount;i++)
	{
		vals.push_back(mtablewidget->item(i,0)->text().toDouble());
	}
	//传入完成后进行排序
	std::sort(vals.begin(), vals.end());
	vals.erase(std::unique(vals.begin(), vals.end()), vals.end());
	Count = vals.size();
	datas.swap(vals);
	this->close();
	okClicked = true;
	
}
void VariateitemWidget2::tableWidgetClicked(QTableWidgetItem*)
{
	currow = mtablewidget->currentRow();
}
#include"moc_VariateitemWidget2.cpp"
