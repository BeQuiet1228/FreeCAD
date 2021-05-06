#include"ListTreeWidget.h"
#include <map>
#include <vector>
#include "Dataresource.h"
#include "C_encoding.h"
#define  MAX_TYPE_NUMBER 6
enum emType
{
	CONTOUR=0,
	PHASEPACE,
	RANGE,
	VECTOR,
	STRUCT,
	OBSERVE,
};
//图标：
QString Treeicon[] = { ":/Tree/TreeFile1.png", ":/Tree/TreeFile2.png" };
std::string Type[MAX_TYPE_NUMBER] = { "CONTOUR", "PHASESPACE", "RANGE", "VECTOR", "struct" ,"OBSERVE"};
std::string Structdirection[3] = { "Phi-Z",
"Z-R",
"R*cos(Phi)-R*sin(Phi)" };
std::string Structdirection_cartesian[3] = { "X_Y", "Y_Z", "X_Z" };
/**
* @brief ListTreeWidget::ListTreeWidget 构造函数
* @param QWidget* parent
*/
ListTreeWidget::ListTreeWidget(QWidget* parent) :QWidget(parent)
{
	//初始化TreeView的风格
	m_TreeView = new QTreeView(this);
	m_TreeView->resize(this->size());
	goodsModel = new QStandardItemModel(m_TreeView);
	goodsModel->setRowCount(0);
	goodsModel->setColumnCount(0);
	//goodsModel->setHorizontalHeaderLabels(QStringList() << (QString::fromLocal8Bit("分类")));
	goodsModel->setHorizontalHeaderLabels(QStringList() << GetEncodingstr("分类",ENCODING_GB2312));
	m_TreeView->setModel(goodsModel);
	m_TreeView->setEditTriggers(QAbstractItemView::NoEditTriggers);
	connect(m_TreeView, SIGNAL(doubleClicked(const QModelIndex &)), this, SLOT(on_doubleclick(const QModelIndex&)));
}
/**
* @brief  ListTreeWidget::~ListTreeWidget 析构
* @return   
*/
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
				std::string coord_type = *(Hdf5Datalist[i].headList.end() - 1);
				if (coord_type.find("cartesian") != std::string::npos)
				{
					for each (std::string var in Structdirection_cartesian)
					{
						itemlist[_str].push_back(var);
						datalist[_str][var] = i;
					}
				}
				else
				{
					for each (std::string var in Structdirection)
					{
						itemlist[_str].push_back(var);
						datalist[_str][var] = i;
					}
				}
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
		//查找父节点
		auto iterparent=parentnode.find(iter->first);
		QStandardItem* item;
		int row = goodsModel->rowCount();
		if (iterparent != parentnode.end()){
			item = iterparent->second;
		}	
		else { 
			item = new QStandardItem(QIcon(Treeicon[0]), GetEncodingstr((iter->first).c_str(), ENCODING_GB2312));
			parentnode[iter->first] = item;
			goodsModel->setItem(row, item);
		}
		//添加子节点
		for (auto subiter = iter->second.begin(); subiter != iter->second.end();subiter++)
		{
			int subrow = item->rowCount();
			QStandardItem* subitem = new QStandardItem(QIcon(Treeicon[1]), QString::fromStdString(*subiter));
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
	double_clicked_event(index);
}
/**
* @brief ListTreeWidget::GetType 获取数据类型
* @param std::string name 
* @return std::string
*/
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
	case emType::OBSERVE:
		return "时间图";
	default:
		return "未知图";
	}
}
/**
* @brief ListTreeWidget::double_clicked_event 树控件双击事件(可重写)
* @param const QModelIndex &index
* @return void
*/
void ListTreeWidget::double_clicked_event(const QModelIndex &index)
{
	QStandardItem* currenitem = goodsModel->itemFromIndex(index);
	//寻找对应的hdf数据
	auto iter = datainfor.find(currenitem);
	if (iter != datainfor.end())
	{
		//传入hdf5数据
		std::string name = (index.data().toString()).toStdString();
		printf("%s", name.c_str());
		emit _transfromRenderer(name, iter->second);
	}
}
/**
* @brief  ListTreeWidget::fromdataManageNewData 接收来自manager的信息
* @param  Hdf5Data & data  
* @param  int index  
* @return void  
*/
void ListTreeWidget::fromdataManageNewData(Hdf5Data& data, int index){
#ifdef MY_DEBUG
	printf("fromdataManageNewData-index:%d\n",index);
#endif
	//开始做处理
	std::string daTaType = GetType(data.name);
	auto iter = parentnode.find(daTaType);
	QStandardItem* item;
	if (iter!=parentnode.end())
		item = iter->second;
	else
	{
		item = new QStandardItem(QIcon(Treeicon[0]),GetEncodingstr(daTaType.c_str(), ENCODING_GB2312));
		int row = goodsModel->rowCount();
		goodsModel->setItem(row, item);
		parentnode[daTaType] = item;
	}
	//添加子节点
	if (data.name.find("struct")==std::string::npos)
	{
		int subrow = item->rowCount();
		QStandardItem* subitem = new QStandardItem(QIcon(Treeicon[1]),QString("save_%1_%2").arg(GetEncodingstr(daTaType.c_str(), ENCODING_GB2312)).arg(subrow));
		datainfor[subitem] = index;
		item->setChild(subrow, subitem);
	}
	else
	{
		switch (data.coordinateSystem)
		{
		case Hdf5Data::CARTESIAN:
		{
			for each (std::string var in Structdirection_cartesian)
			{
				int subrow = item->rowCount();
				QStandardItem* subitem = new QStandardItem(QIcon(Treeicon[1]),QString("%1").arg(GetEncodingstr(var.c_str(), ENCODING_GB2312)));
				datainfor[subitem] = index;
				item->setChild(subrow, subitem);
			}
		}
			break;
		case Hdf5Data::POLAR:
		case Hdf5Data::CYLINDER:
		{
			for each(std::string var in Structdirection)
			{
				int subrow = item->rowCount();
				QStandardItem* subItem = new QStandardItem(QIcon(Treeicon[1]), QString("%1").arg(GetEncodingstr(var.c_str(),ENCODING_GB2312)));
				/*QStandardItem* subitem = new QStandardItem(QIcon(Treeicon[1])),QString("%1").arg(GetEncodingstr(var.c_str(), ENCODING_GB2312)))*/;
				datainfor[subItem] = index;
				item->setChild(subrow, subItem);
			}
		}
			break;
		}
	}
}
/**
* @brief  ListTreeWidget::clear 清除树控件
* @return void  
*/
void ListTreeWidget::clear()
{
	if (goodsModel->hasChildren() > 0)
	{
		goodsModel->removeRows(0, goodsModel->rowCount());
	}
	datainfor.clear();
	parentnode.clear();
}
#include "moc_ListTreeWidget.cpp"
