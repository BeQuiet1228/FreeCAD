#include"ListTreeWidget.h"
#include <map>
#include <vector>
#include "Dataresource.h"
#define  MAX_TYPE_NUMBER 5
enum emType
{
	CONTOUR=0,
	PHASEPACE,
	RANGE,
	VECTOR,
	STRUCT,
};
std::string Type[MAX_TYPE_NUMBER] = { "CONTOUR", "PHASESPACE", "RANGE", "VECTOR", "struct" };
std::string Structdirection[3] = { "Phi-Z",
"Z-R",
"R*cos(Phi)-R*sin(Phi)" };
ListTreeWidget::ListTreeWidget(QWidget* parent) :QWidget(parent)
{
	//初始化TreeView的风格
	m_TreeView = new QTreeView(this);
	m_TreeView->resize(this->size());
	goodsModel = new QStandardItemModel(m_TreeView);
	goodsModel->setRowCount(0);
	goodsModel->setColumnCount(0);
	//goodsModel->setHeaderData(0, Qt::Horizontal, QString::fromLocal8Bit("分类:"));
	goodsModel->setHorizontalHeaderLabels(QStringList() << (QString::fromLocal8Bit("分类")));
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
	//需要清空所有节点信息
	if (goodsModel->hasChildren()>0)
	{
		goodsModel->removeRows(0, goodsModel->rowCount());
	}
	//开始实现
	std::map<std::string, std::vector<std::string>> itemlist;
	std::map<std::string, std::map<std::string, int>> datalist;
	itemlist.clear();
	for (auto i = 0; i < Hdf5Datalist.size();i++)
	{
		std::string _str = GetType(Hdf5Datalist[i].name);
		auto iter=itemlist.find(_str);
		if (iter!=itemlist.end())
		{
			std::string str = Hdf5Datalist[i].name+"_"+std::to_string(itemlist[_str].size());
			itemlist[_str].push_back(str);
			datalist[_str][str]=i;
		}
		else
		{
			//当获取到图表信息是结构图时
			if (Hdf5Datalist[i].name.find("struct")!=std::string::npos)
			{
				for each (std::string var in Structdirection)
				{
					itemlist[_str].push_back(var);
					datalist[_str][var] = i;
				}
				//std::string str1 = "Phi-Z";
				//std::string str2 = "Z-R";
				//std::string str3 = "R*cos(Phi)-R*sin(Phi)";
				//itemlist[_str].push_back(str1);
				//itemlist[_str].push_back(str2);
				//itemlist[_str].push_back(str3);
				//datalist[_str][str1] = i;
				//datalist[_str][str2] = i;
				//datalist[_str][str3] = i;
				continue;
			}
			std::string str = Hdf5Datalist[i].name + "_0";
			itemlist[_str].push_back(str);
			datalist[_str][str] =i;
		}
	}

	//开始创建树控件
	std::map<QStandardItem*, int> _datainfo;
	for (auto iter = itemlist.begin(); iter != itemlist.end();iter++)
	{
		//添加完父节点
		//QString str = QString::fromStdString(iter->first);
		QStandardItem* item = new QStandardItem(QString::fromLocal8Bit((iter->first).c_str()));
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
void ListTreeWidget::on_doubleclick(const QModelIndex &index)
{
	//qDebug() << index;
	//获取到对应的控件
	//通过QStandardItemModel的itemFromIndex函数即可得到QModelIndex对应的QStandardItem。
	QStandardItem* currenitem = goodsModel->itemFromIndex(index);
	//寻找对应的hdf数据
	auto iter = datainfor.find(currenitem);
	//QModelIndex _parent=index.parent();//获取父节点
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
std::string ListTreeWidget::GetType(std::string name)
{
	int index = -1;
	for (auto i = 0; i <MAX_TYPE_NUMBER;i++)
	{
		if (name.find(Type[i])!=std::string::npos)
		{
			index = i;
			break;
		}
	}
	switch (index)
	{
	case emType::CONTOUR:
		return "等位图";
	case emType::PHASEPACE:
		return "相空间图";
	case emType::RANGE:
		return "空间变化图";
	case emType::STRUCT:
		return "结构图";
	case emType::VECTOR:
		return "矢量图";
	default:
		return "未知图";
	}
}
#include "moc_ListTreeWidget.cpp"
