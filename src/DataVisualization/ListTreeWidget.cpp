#include"ListTreeWidget.h"
#include <map>
#include <vector>
#include <sstream>
#include "C_encoding.h"
#include <QDebug>
namespace DV {
#ifndef MAX_TYPE_NUMBER
#define  MAX_TYPE_NUMBER 7
#endif
	enum emType
	{
		CONTOUR = 0,
		PHASEPACE,
		RANGE,
		VECTOR,
		STRUCT,
		OBSERVE,
		PLANE,
	};
	//图标：
	QString Treeicon[] = { ":/Tree/TreeFile1.png", ":/Tree/TreeFile2.png" };
	std::string Type[MAX_TYPE_NUMBER] = { "CONTOUR", "PHASESPACE", "RANGE", "VECTOR", "struct" ,"OBSERVE","PLANE" };
	std::string Structdirection[3] = { "Phi-Z",
	"Z-R",
	"R*cos(Phi)-R*sin(Phi)" };
	std::string Structdirection_cartesian[3] = { "X_Y", "Y_Z", "X_Z" };
	/**
	* @brief ListTreeWidget::ListTreeWidget 构造函数
	* @param QWidget* parent
	*/
	ListTreeWidget::ListTreeWidget(QWidget* parent) :QWidget(parent)/*, structHeadCount(0)*/
	{
		//初始化TreeView的风格
		m_TreeView = new QTreeView(this);
		m_TreeView->resize(this->size());
		goodsModel = new QStandardItemModel(m_TreeView);
		goodsModel->setRowCount(0);
		goodsModel->setColumnCount(0);
		//goodsModel->setHorizontalHeaderLabels(QStringList() << (QString::fromLocal8Bit("分类")));
		goodsModel->setHorizontalHeaderLabels(QStringList() << GetEncodingstr("分类", ENCODING_GB2312));
		m_TreeView->setModel(goodsModel);
		m_TreeView->setEditTriggers(QAbstractItemView::NoEditTriggers);
		connect(m_TreeView, SIGNAL(doubleClicked(const QModelIndex&)), this, SLOT(on_doubleclick(const QModelIndex&)));
	}
	/**
	* @brief  ListTreeWidget::~ListTreeWidget 析构
	* @return
	*/
	ListTreeWidget::~ListTreeWidget() {
		//datainfor.clear();
#if MY_DEBUG
		qDebug() << "ListTreeWidget delete";
#endif
	}
	/**
	* @brief ListTreeWidget::loadHdflist 读取hdf文件
	* @param std::vector<Hdf5Data> Hdf5Datalist
	* @return void
	*/
	void ListTreeWidget::loadHdflist(std::vector<Hdf5Data>& Hdf5Datalist)
	{
		//增加清理流程
		clear();
		//获取到全部信息
		std::string varString;
		for (auto index = 0; index < Hdf5Datalist.size(); index++)
		{
#pragma region 处理结构图
			if (Hdf5Datalist[index].name.find("struct") != std::string::npos)
			{
				toStructh5df(Hdf5Datalist[index], index);
				continue;
			}
#pragma endregion
#pragma region
			if (Hdf5Datalist[index].name.find("PLANE") != std::string::npos)
			{
				toPlaneh5df(Hdf5Datalist[index], index);
				continue;
			}
#pragma endregion
#pragma region 其他图
			fromdataManageNewData(Hdf5Datalist[index], index);
#pragma endregion

		}
	}
	/**
	* @brief ListTreeWidget::resizeEvent 窗口大小变化事件
	* @param QResizeEvent * event
	* @return void
	*/
	void ListTreeWidget::resizeEvent(QResizeEvent* event)
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
	void ListTreeWidget::on_doubleclick(const QModelIndex& index)
	{
		/*double_clicked_event(index);*/
		QStandardItem* currenitem = goodsModel->itemFromIndex(index);
		//寻找对应的hdf数据
		auto iter = datainfor.find(currenitem);
		if (iter != datainfor.end())
		{
			//传入hdf5数据
			std::string name = (index.data().toString()).toStdString();
			emit _transfromRenderer(name, iter->second.index);
		}
	}
	/**
	* @brief ListTreeWidget::GetType 获取数据类型
	* @param std::string name
	* @return std::string
	*/
	std::string ListTreeWidget::GetType(std::string name)
	{
		int index = -1;
		for (auto i = 0; i < MAX_TYPE_NUMBER; i++)
		{
			if (name.find(Type[i]) != std::string::npos)
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
		case emType::PLANE:
			return "三维结构图";
		default:
			return "未知图";
		}
	}
	/**
	* @brief  ListTreeWidget::fromdataManageNewData 接收来自manager的信息
	* @param  Hdf5Data & data
	* @param  int index
	* @return void
	*/
	QStandardItem* ListTreeWidget::fromdataManageNewData(Hdf5Data& data, int index) {
		std::string observingstr;
		itemInfo mitemInfo;
		mitemInfo.index = index;
		//获取观测面
		int _type = -1;
		for (auto i = 0; i < MAX_TYPE_NUMBER; i++)
		{
			if (data.name.find(Type[i]) != std::string::npos)
			{
				_type = i;
				break;
			}
		}
		std::stringstream ss;
		std::stringstream subss;
		auto getSStr = [&](std::string str)->std::string {
			std::string res;
			res = str;
			//res.erase(std::remove_if(res.begin(),res.end(),isspace),res.end());
			int pos = res.find("=");
			res.erase(0, pos + 1);
			QString qres = QString::fromStdString(res);
			qres = qres.simplified();
			//qres=qres.replace(" ","_");
			return qres.toStdString();
		};
		auto replaceStr = [&](std::string str)->std::string
		{
			QString qstr = QString::fromStdString(str);
			qstr = qstr.simplified();
			qstr = qstr.replace(QRegExp("\\s{1,}"), "_");
			return qstr.toStdString();
		};
		//字符串拼接
		switch (_type)
		{
		case emType::VECTOR:
		{
			std::string art3 = getSStr(data.headList[2]);
			std::string art14 = getSStr(data.headList[13]);
			std::string art12 = getSStr(data.headList[11]);
			{
				//transform(art12.begin(),art12.end(),art12.begin(),toupper);
				//int pos = 0;
				/*while (std::string::npos != (pos = art12.find("VECTOR"))) art12.erase(pos, 6);
				while (std::string::npos != (pos = art12.find("OF"))) art12.erase(pos, 2);
				while (std::string::npos != (pos = art12.find("PLOT"))) art12.erase(pos, 2);*/
				art12.erase(0, art12.find("("));
				art3.erase(0, art3.find("$") + 1);
				art14.erase(0, art14.find("TIME:") + 5);
			}
			ss << "PLOT" << art12;
			//测试
			//subss << art12 << " ";
			subss << art3 << " " << art14;
			{
				//获取时间
				std::string mt = art14;
				mitemInfo.time = QString::fromStdString(mt.erase(mt.find("SEC"), mt.size())).toDouble();
			}
		}
		break;
		case emType::CONTOUR:
		{
			//等位图
			std::string art3 = getSStr(data.headList[2]);
			//std::string art3=std::remove_space
			ss << art3.substr(0, art3.find("-#"));
			std::string art13 = getSStr(data.headList[12]);
			{
				art3.erase(0, art3.find("$") + 1);
				art13.erase(0, art13.find("TIME") + 4);
			}
			//测试
			//subss << ss.str()<<" ";
			subss << art3 << " " << art13;
			{
				//保存时间
				std::string mt = art13;
				mitemInfo.time = QString::fromStdString(mt.erase(mt.find("SEC"), mt.size())).toDouble();
			}
		}
		break;
		case emType::PHASEPACE:
		{
			//相空间图
			//ss << getSStr(data.headList[2]);
			std::string art3 = getSStr(data.headList[2]);
			art3.erase(art3.find("-#"), art3.size());
			ss << art3;
			//观测类型
			//std::string art14 = data.headList[13];
			//观测对象
			art3 = getSStr(data.headList[2]);
			//观测时刻
			std::string art12 = getSStr(data.headList[11]);
			{
				//获取时间
				std::string mt = art12;
				mt.erase(0, mt.find("TIME:") + 5);
				mt.erase(mt.find("SEC"), mt.size());
				mitemInfo.time = QString::fromStdString(mt).toDouble();
			}
			{
				int pos = art3.find("$");
				art3 = (pos == std::string::npos) ? ("") : (art3.erase(0, art3.find("$") + 1));
				{
					std::stringstream s1;
					s1 << art12.substr(art12.find("OF") + 2, (art12.find("VS") - (art12.find("OF") + 2)))
						<< " " << art12.substr(art12.find("VS") + 2, (art12.find("AT") - (art12.find("VS") + 2)));
					s1 << " " << art12.substr(art12.find("TIME") + 5, (art12.size() - (art12.find("TIME") + 5)));
					art12 = s1.str();
				}
				//art12.erase(0, art12.find("TIME"));
			}
			subss << art3 << " " << art12;
		}
		break;
		case emType::RANGE:
		{
			std::string art3 = getSStr(data.headList[2]);
			art3.erase(art3.find("-#"), art3.size());
			ss << art3;
			//ss << getSStr(data.headList[2]) << getSStr(data.headList[13]);
			//观测类型
			std::string art14 = data.headList[13];
			//观测对象
			art3 = getSStr(data.headList[2]);
			//观测时刻
			std::string art12 = getSStr(data.headList[11]);
			{
				art14.erase(0, art14.find("=") + 1);
				art14.erase(art14.find(" "), art14.size());
				art3.erase(0, art3.find("$") + 1);
				art12.erase(0, art12.find("TIME") + 5);
			}
			subss << art14 << " " << art3 << " " << art12;
			{
				std::string mt = art12;
				mitemInfo.time = QString::fromStdString(mt.erase(mt.find("SEC"), mt.size())).toDouble();
			}
		}
		break;
		/*case emType::VECTOR:
			ss << getSStr(data.headList[2]) << getSStr(data.headList[11]);
			break;*/
		case emType::OBSERVE:
		{
			//ss << getSStr(data.headList[2]) << getSStr(data.headList[13]);
			std::string art3 = getSStr(data.headList[2]);
			art3.erase(art3.find("-#"), art3.size());
			ss << art3;
			std::string art14 = getSStr(data.headList[13]);
			{
				transform(art14.begin(), art14.end(), art14.begin(), toupper);
				//transform(fileFormat.begin(), fileFormat.end(), fileFormat.begin(), tolower);
				int pos = 0;
				while (std::string::npos != (pos = art14.find("MAGINTUDE"))) art14.erase(pos, 9);
				while (std::string::npos != (pos = art14.find("OF"))) art14.erase(pos, 2);
				while (std::string::npos != (pos = art14.find("COMPONENT"))) art14.erase(pos, 9);

				//art14.erase(std::remove_if(art14.begin(), art14.end(), "MAGINTUDE"), art14.end());
				//art14.erase(std::remove_if(art14.begin(), art14.end(), "OF"), art14.end());
				//art14.erase(std::remove_if(art14.begin(), art14.end(), "COMPONENT"), art14.end());
			}
			art3 = getSStr(data.headList[2]);
			art3.erase(0, art3.find("$") + 1);
			subss << art14 << " " << art3;
		}
		break;
		}

		observingstr = replaceStr(ss.str());
		std::stringstream nodeStrStream;
		nodeStrStream << data.name << observingstr;
		auto iter = parentnode.find(nodeStrStream.str());
		QStandardItem* observeItem;
		//没有记录该观测面
		if (iter == parentnode.end())
		{
			//查看是否有上层的分类
			std::string dataType = GetType(data.name);
			//若是未知的图不做处理
			if (dataType.find("未知图") != std::string::npos)
				return nullptr;
			iter = parentnode.find(dataType);
			QStandardItem* parentItem;
			if (iter != parentnode.end())
				parentItem = iter->second;
			else
			{
				parentItem = new QStandardItem(QIcon(Treeicon[0]), GetEncodingstr(dataType.c_str(), ENCODING_GB2312));
				int row = goodsModel->rowCount();
				goodsModel->setItem(row, parentItem);
				parentnode[dataType] = parentItem;
			}
			//新增观测面选项
			observeItem = new QStandardItem(QIcon(Treeicon[0]), GetEncodingstr(observingstr.c_str(), ENCODING_GB2312));
			int row = parentItem->rowCount();
			parentItem->setChild(row, observeItem);
			parentnode[nodeStrStream.str()] = observeItem;
		}
		else
		{
			observeItem = iter->second;
		}
		int row = observeItem->rowCount();
		if (row == 0 || mitemInfo.time < 0.0)
		{
			QStandardItem* childItem = new QStandardItem(QIcon(Treeicon[1]), GetEncodingstr(replaceStr(subss.str()).c_str(), ENCODING_GB2312));
			datainfor[childItem] = mitemInfo;
			observeItem->setChild(row, childItem);
			return childItem;
		}
		else
		{
			//根据时间进行排序
			QStandardItem* childItem = new QStandardItem(QIcon(Treeicon[1]), GetEncodingstr(replaceStr(subss.str()).c_str(), ENCODING_GB2312));
			datainfor[childItem] = mitemInfo;
			int currow = 0;
			for (int rowindex = 0; rowindex < row; rowindex++)
			{
				QStandardItem* item = observeItem->child(rowindex);
				auto iter = datainfor.find(item);
				auto res = (iter->second.time < mitemInfo.time);
				if (res)	currow = rowindex + 1;
			}
			observeItem->insertRow(currow, childItem);
			return childItem;
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

	/**
	* @brief  ListTreeWidget::toStructh5df 传入结构图数据
	* @param  Hdf5Data data
	* @param  int index
	* @return void
	*/
	std::vector<QStandardItem*> ListTreeWidget::toStructh5df(Hdf5Data& data, int index)
	{
		std::vector<QStandardItem*> qstandarditems;
		itemInfo mitemInfo;
		mitemInfo.index = index;
		if (data.name.find("struct") == std::string::npos)
			return qstandarditems;
		std::string dataType = GetType(data.name);
		auto iter = parentnode.find(dataType);
		QStandardItem* item;
		if (iter != parentnode.end())
			item = iter->second;
		else
		{
			item = new QStandardItem(QIcon(Treeicon[0]), GetEncodingstr(dataType.c_str(), ENCODING_GB2312));
			int row = goodsModel->rowCount();
			goodsModel->setItem(row, item);
			parentnode[dataType] = item;
		}
		//判断结构图的是2维的还是3维的
		if (data.listDataSet.size() > 3)
		{
			switch (data.coordinateSystem)
			{
			case Hdf5Data::CARTESIAN:
			{
				for each (std::string var in Structdirection_cartesian)
				{
					int subrow = item->rowCount();
					QStandardItem* subitem = new QStandardItem(QIcon(Treeicon[1]), QString("%1").arg(GetEncodingstr(var.c_str(), ENCODING_GB2312)));
					datainfor[subitem] = mitemInfo;
					item->setChild(subrow, subitem);
					qstandarditems.push_back(subitem);
				}
			}
			break;
			case Hdf5Data::POLAR:
			case Hdf5Data::CYLINDER:
			{
				for each (std::string var in Structdirection)
				{
					int subrow = item->rowCount();
					QStandardItem* subItem = new QStandardItem(QIcon(Treeicon[1]), QString("%1").arg(GetEncodingstr(var.c_str(), ENCODING_GB2312)));
					datainfor[subItem] = mitemInfo;
					item->setChild(subrow, subItem);
					qstandarditems.push_back(subItem);
				}
			}
			break;
			}
		}
		else
		{
			std::string structstr = *(data.headList.begin() + 2);
			structstr.erase(std::remove_if(structstr.begin(), structstr.end(), isspace), structstr.end());
			int _j = structstr.find("=");
			structstr.erase(0, _j + 1);
			int pos1 = structstr.find("$");
			int pos2 = structstr.find("$", pos1 + 1);
			structstr = structstr.substr(pos1 + 1, pos2 - pos1 - 1);
			QStandardItem* subitem = new QStandardItem(QIcon(Treeicon[1]), GetEncodingstr(structstr.c_str(), ENCODING_GB2312));
			int row = item->rowCount();
			item->setChild(row, subitem);
			datainfor[subitem] = mitemInfo;
			qstandarditems.push_back(subitem);
		}
		return qstandarditems;
	}

	/**
	* @brief ListTreeWidget::toPlaneh5df 处理三维结构图
	* @param Hdf5Data & data
	* @param int index
	* @return void
	*/
	void  ListTreeWidget::toPlaneh5df(Hdf5Data& data, int index)
	{
		itemInfo mitemInfo;
		mitemInfo.index = index;
		if (data.name.find("PLANE") == std::string::npos)
			return;
		std::string dataType = GetType(data.name);
		auto iter = parentnode.find(dataType);
		QStandardItem* item;
		if (iter != parentnode.end())
		{
			item = iter->second;
		}
		else
		{
			item = new QStandardItem(QIcon(Treeicon[0]), GetEncodingstr(dataType.c_str(), ENCODING_GB2312));
			int row = goodsModel->rowCount();
			goodsModel->setItem(row, item);
			parentnode[dataType] = item;
		}
		//添加子节点
		int subrow = item->rowCount();
		QStandardItem* subItem = new QStandardItem(QIcon(Treeicon[1]), GetEncodingstr("Group_Plane", ENCODING_GB2312));
		datainfor[subItem] = mitemInfo;
		item->setChild(subrow, subItem);
	}
};
#include "moc_ListTreeWidget.cpp"
