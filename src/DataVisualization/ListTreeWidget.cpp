#include"ListTreeWidget.h"
#include <map>
#include <vector>
#include "Dataresource.h"
ListTreeWidget::ListTreeWidget(QWidget* parent) :QWidget(parent)
{
	//初始化TreeView的风格
	m_TreeView = new QTreeView(this);
	m_TreeView->resize(this->size());
	goodsModel = new QStandardItemModel(m_TreeView);
	goodsModel->setRowCount(0);
	goodsModel->setColumnCount(0);
	//goodsModel->setHeaderData(0, Qt::Horizontal, QString::fromLocal8Bit("分类:"));
	goodsModel->setHorizontalHeaderLabels(QStringList() << (QString::fromLocal8Bit("项目名")));
	m_TreeView->setModel(goodsModel);
	m_TreeView->setEditTriggers(QAbstractItemView::NoEditTriggers);
	connect(m_TreeView, SIGNAL(doubleClicked(const QModelIndex &)), this, SLOT(on_doubleclick(const QModelIndex&)));
}
ListTreeWidget::~ListTreeWidget(){
	//datainfor.clear();
}
/**
* @brief ListTreeWidget::loadHdflist 读取hdf文件
* @param std::vector<Hdf5Data> Hdf5Datalist
* @return void
*/
void ListTreeWidget::loadHdflist(std::vector<Hdf5Data>& Hdf5Datalist)
{
	DataSourceManage::Getinstance()->clearMap();
	//需要清空所有节点信息
	if (goodsModel->hasChildren()>0)
	{
		goodsModel->removeRows(0, goodsModel->rowCount());
	}
	//开始实现
	std::map<std::string, std::vector<std::string>> itemlist;
	std::map<std::string, std::map<std::string, int>> datalist;
	itemlist.clear();
	//for each (Hdf5Data var in Hdf5Datalist)
	//for (auto var = Hdf5Datalist.begin(); var != Hdf5Datalist.end();var++)
	for (auto i = 0; i < Hdf5Datalist.size();i++)
	{
		auto iter=itemlist.find(Hdf5Datalist[i].name);
		if (iter!=itemlist.end())
		{
			std::string str = Hdf5Datalist[i].name+"_"+std::to_string(itemlist[Hdf5Datalist[i].name].size());
			itemlist[Hdf5Datalist[i].name].push_back(str);
			datalist[Hdf5Datalist[i].name][str]=i;
		}
		else
		{
			std::string str = Hdf5Datalist[i].name + "_0";
			itemlist[Hdf5Datalist[i].name].push_back(str);
			datalist[Hdf5Datalist[i].name][str] =i;
		}
	}

	//开始创建树控件
	std::map<QStandardItem*, int> _datainfo;
	for (auto iter = itemlist.begin(); iter != itemlist.end();iter++)
	{
		//添加完父节点
		QStandardItem* item = new QStandardItem(QString::fromStdString(iter->first));
		int row = goodsModel->rowCount();
		goodsModel->setItem(row,item);
		//添加子节点
		for (auto subiter = iter->second.begin(); subiter != iter->second.end();subiter++)
		{
			int subrow = item->rowCount();
			QStandardItem* subitem = new QStandardItem(QString::fromStdString(*subiter));
			_datainfo[subitem] = datalist[iter->first][*subiter];
			item->setChild(subrow, subitem);
		}
	}
	datainfor.swap(_datainfo);
}
/**
* @brief ListTreeWidget::resizeEvent 窗口大小变化事件
* @param QResizeEvent * event
* @return void
*/
void ListTreeWidget::resizeEvent(QResizeEvent * event)
{
	if (m_TreeView)
	{
		m_TreeView->resize(this->size());
	}
}
/**
* @biref ListTreeWidget::on_doubleclick 双击事件
* @param const QModelIndex &index
* @return void
*/
#include <QDebug>
void ListTreeWidget::on_doubleclick(const QModelIndex &index)
{
	//qDebug() << index;
	//获取到对应的控件
	//通过QStandardItemModel的itemFromIndex函数即可得到QModelIndex对应的QStandardItem。
	QStandardItem* currenitem = goodsModel->itemFromIndex(index);
	//寻找对应的hdf数据
	auto iter = datainfor.find(currenitem);
	if (iter!=datainfor.end())
	{
		//传入hdf5数据
		std::string name = (index.data().toString()).toStdString();
		printf("%s",name.c_str());
		//std::shared_ptr<Hdf5Data> data =iter->second;
		//DataSourceManage::Getinstance()->tranfromRenderer(name, data);
		emit _transfromRenderer(name, iter->second);
	}
}
#include "moc_ListTreeWidget.cpp"