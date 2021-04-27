#include "ConfigWidget.h"
#include "ui_ConfigWidget.h"
#include "C_encoding.h"
#include <QDebug>
ConfigWidget::ConfigWidget(QWidget* panter) :QWidget(panter), ui(new Ui::ConfigWidget)
{
	ui->setupUi(this);
	initUI();
}
ConfigWidget::~ConfigWidget(){

}
void ConfigWidget::on_doubleclick(const QModelIndex& modindex){
	QStandardItem* currenitem = goodsModel->itemFromIndex(modindex);
	auto it = mapview.find(currenitem);
	if (it!=mapview.end())
	{
		printf("图标设置\n");
	}
}
void ConfigWidget::initUI()
{
	mapview.clear();
	//初始化TreeView风格
	goodsModel = new QStandardItemModel(ui->treeView);
	goodsModel->setRowCount(0);
	goodsModel->setColumnCount(0);
	goodsModel->setHorizontalHeaderLabels(QStringList() << GetEncodingstr("配置", ENCODING_GB2312));
	ui->treeView->setModel(goodsModel);
	ui->treeView->setEditTriggers(QAbstractItemView::NoEditTriggers);
	connect(ui->treeView, SIGNAL(doubleClicked(const QModelIndex &)), this, SLOT(on_doubleclick(const QModelIndex&)));
	//暂时先这样写---后续通过列表初始化
	QStandardItem* item = new QStandardItem(GetEncodingstr("图表设置", ENCODING_GB2312));
	int row = goodsModel->rowCount();
	goodsModel->setItem(row, item);
	mapview[item] = 1;
}
#include "moc_ConfigWidget.cpp"