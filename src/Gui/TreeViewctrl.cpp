#include "PreCompiled.h"
#include"TreeViewctrl.h"
#include "App/Document.h"
#include "App/DocumentDataManager.h"
#include <HDF5Reader/hdf5io.h>
#include "Contorl/ContorlInterface.h"
//
#include "Gui/Document.h"
#include "Application.h"
#include "PlotMDIView.h"
#include"PLaneMDIView.h"
#include "MainWindow.h"
#include"iostream"
#include"VisualizationOf3D/Widget3D.h"
#include "QDebug"
#include"DataVisualization/RendererFactory.h"
#include"TreeNodeManager.h"
#include "DataVisualization/C_encoding.h"
#include "Item3DDoubleClickEvent.h"
namespace Gui {
	//图标：
	QString Treeicon[] = {
		QString::fromStdString(":/Tree/TreeFile1.png"),
		QString::fromStdString(":/Tree/TreeFile2.png")
	};
	TreeViewCtrl::TreeViewCtrl(QWidget* parent) :ListTreeWidget(parent) {
		structIndex = -1;
	}
	TreeViewCtrl::~TreeViewCtrl()
	{
	}
	void TreeViewCtrl::upClear()
	{
		structIndex = -1;
		clear();
		parentNodes.clear();
		hdf5Indexs.clear();
		adapterFunc.clear();
		//获取当前活跃的Document;
		App::Document* doc = App::GetApplication().getActiveDocument();
		DocumentManager* docM = dynamic_cast<DocumentManager*>(doc);
		if (docM)
			docM->dataclear();
	}
	/**
	* @brief Gui::TreeViewCtrl::on_doubleclick 双击事件
	* @param const QModelIndex & index
	* @return void
	*/
	void TreeViewCtrl::on_doubleclick(const QModelIndex& index)
	{
		//寻找对应的hdf数据
		//获取到QStandardItem*
		QStandardItem* currentItem = goodsModel->itemFromIndex(index);
		auto dataItem = hdf5Indexs.find(currentItem);
		if (dataItem == hdf5Indexs.end())
			return;
		App::Document* doc = App::GetApplication().getActiveDocument();
		DocumentManager* docM = dynamic_cast<DocumentManager*>(doc);
		if (!docM)
		{
			std::cerr << "DocumentManager is null from FreeCadGui void TreeViewCtrl::double_clicked_event(const QModelIndex &index)" << std::endl;
			return;
		}
		std::string name = (index.data().toString()).toStdString();
		auto h5d = docM->gethdf5dataList()[dataItem->second];
		auto itemfunc = adapterFunc.find(currentItem);
		if (itemfunc != adapterFunc.end())
		{
			itemfunc->second->doubleEvent(h5d, name);
		}
	}
	void TreeViewCtrl::displayItem(QStandardItem* item, Hdf5Data& data)
	{
		auto dataItem = hdf5Indexs.find(item);
		if (dataItem == hdf5Indexs.end())
			return;
		std::string name = item->text().toStdString();
		auto itemfunc = adapterFunc.find(item);
		if (itemfunc != adapterFunc.end())
		{
			itemfunc->second->doubleEvent(data, name);
		}
	}
	/**
	* @brief Gui::TreeViewCtrl::loadHdflist 读取hdf5数据组，批量生成Item
	* @param std::vector<Hdf5Data> & Hdf5Datalist
	* @return void
	*/

	void TreeViewCtrl::loadHdflist(std::vector<Hdf5Data>& Hdf5Datalist)
	{
		auto index = DV::RendererFactory::findStructDataIndex(Hdf5Datalist);
		if (-1 != index)
		{
			structIndex = index;
		}
		//增加清理流程
		clear();
		for (auto index = 0; index < Hdf5Datalist.size(); index++)
		{
			createIteminfo(Hdf5Datalist[index], index);
		}
	}
	/**
	* @brief Gui::TreeViewCtrl::createIteminfo 根据传入的数据和id生成item，并保存到内部字典
	* @param Hdf5Data & data
	* @param int index
	* @return void
	*/

	void TreeViewCtrl::createIteminfo(Hdf5Data& data, int index)
	{
		if (data.name.find("struct") != std::string::npos)
		{
			structIndex = index;
		}
		creatItem(TreeNodeManager::GetInstance()->createNodeInfo2D(data, index), 2);//2维
		creatItem(TreeNodeManager::GetInstance()->createNodeInfo3D(data, index), 3);//3维
	}
	void TreeViewCtrl::creatItem(TreeNode& node, int type)
	{
		//节点为空
		if (TreeNodeType::TREENODE_NULL == node.mTreeNodeType)
			return;
		QStandardItem* parentItem = nullptr;
		auto iter = parentNodes.find(node.nodeStr);
		if (iter == parentNodes.end())
		{
			//没有该节点，新建一个
			parentItem = new QStandardItem(QIcon(Treeicon[0]), DV::GetEncodingstr(node.nodeStr.c_str(), ENCODING_GB2312));
			int row = goodsModel->rowCount();
			goodsModel->setItem(row, parentItem);
			parentNodes[node.nodeStr] = parentItem;
		}
		else
		{
			parentItem = iter->second;
		}
		//添加节点
		addItem(parentItem, node, type);
		return;
	}
	/**
	* @brief Gui::TreeViewCtrl::judgeNewNode 判断是否为新的节点
	* @param QStandardItem * item
	* @param TreeNode & node
	* @param int type
	* @return int 如果是新节点，返回-1，不是，则返回节点的索引值。
	* @time	2021/12/07
	*/
	int TreeViewCtrl::judgeNewNode(QStandardItem* item, TreeNode& node, int type)
	{
		int breakIndex = -1;
		int row = item->rowCount();
		for (auto j = 0; j < row; ++j)
		{
			auto subitem = item->child(j);
			auto res = subitem->text().toStdString() == (node.nodeStr);
			if (1 == res)
			{
				breakIndex = j;
				break;
			}
		}
		return breakIndex;
	}
	/**
	* @brief Gui::TreeViewCtrl::creatNewNode 创建新的节点
	* @param TreeNode & node
	* @return QT_NAMESPACE::QStandardItem*
	* @time	2021/12/07
	*/
	QStandardItem* TreeViewCtrl::creatNewNode(TreeNode& node)
	{
		QStandardItem* subitem = nullptr;
		switch (node.mTreeNodeType)
		{
		case TreeNodeType::TREENODE_FILE:
		{
			//文件节点
			subitem = new QStandardItem(QIcon(Treeicon[1]), DV::GetEncodingstr(node.nodeStr.c_str(), ENCODING_GB2312));
		}
		break;
		case TreeNodeType::TREENODE_FOLDER:
		{
			//文件夹节点
			subitem = new QStandardItem(QIcon(Treeicon[0]), DV::GetEncodingstr(node.nodeStr.c_str(), ENCODING_GB2312));
		}
		break;
		}
		return subitem;
	}
	/**
	* @brief Gui::TreeViewCtrl::addMap 装入字典，关联item与事件,和hdf5data的索引
	* @param QStandardItem * item
	* @param TreeNode & node
	* @param int type
	* @return void
	* @time	2021/12/07
	*/
	void TreeViewCtrl::addMap(QStandardItem* item, TreeNode& node, int type)
	{
		std::shared_ptr<PlotAdapterBase> funcPtr = nullptr;
		if (2 == type)
		{
			//2维
			funcPtr = std::shared_ptr<PlotAdapterBase>(new PlotAdapter2D());

		}
		else if (3 == type)
		{
			//3维
			funcPtr.reset(new Item3DDoubleClickEvent());
		}
		adapterFunc[item] = funcPtr;
		hdf5Indexs[item] = node.index;
		App::Document* doc = App::GetApplication().getActiveDocument();
		DocumentManager* docM = dynamic_cast<DocumentManager*>(doc);
		if (nullptr != docM && structIndex!=-1)
		{
			auto h5dStruct = docM->gethdf5dataList()[structIndex];
			funcPtr->setStructData(h5dStruct);
		}
	}
	/**
	* @brief Gui::TreeViewCtrl::addItem 添加树节点
	* @param QStandardItem * item
	* @param TreeNode & node
	* @param int type
	* @return void
	* @time	2021/12/07
	*/
	void TreeViewCtrl::addItem(QStandardItem* item, TreeNode& node, int type)
	{
		//该节点为空或没有子节点直接返回
		if (TreeNodeType::TREENODE_NULL == node.mTreeNodeType || 0 == node.childNode.size())
			return;
		for (auto i = 0; i < node.childNode.size(); ++i)
		{
			int index = judgeNewNode(item, node.childNode[i], type);
			if (-1 != index)
			{
				//不是新节点,往下一层继续执行
				addItem(item->child(index), node.childNode[i],type);
				continue;
			}
			auto subitem = creatNewNode(node.childNode[i]);
			if (node.childNode[i].mTreeNodeType == TreeNodeType::TREENODE_FILE)
			{
				//关联相关方法，和数据
				addMap(subitem, node.childNode[i], type);
			}
			else
			{
				addItem(subitem, node.childNode[i], type);
			}
			//排序
			sortNode(item, subitem);
		}
	}
	/**
	* @brief Gui::TreeViewCtrl::sortNode 节点排序
	* @param QStandardItem * item
	* @param QStandardItem * subitem
	* @return void
	* @time	2021/12/07
	*/
	void TreeViewCtrl::sortNode(QStandardItem* item, QStandardItem* subitem)
	{
		int row = item->rowCount();
		//排序
		int currow = 0;
		for (int rowindex = 0; rowindex < row; rowindex++)
		{
			auto currentItem = item->child(rowindex);
			std::string currentItemstr = currentItem->text().toStdString();
			std::string subItemstr = subitem->text().toStdString();
			int res = strcmp(currentItemstr.c_str(), subItemstr.c_str());
			if (res < 0)
				currow = rowindex + 1;
		}
		item->insertRow(currow, subitem);
	}
	/**
	* @brief Gui::TreeViewCtrl::showPlotfromData 用于直接传入hdf5data数据和类型时显示
	* @param Hdf5Data data
	* @param int _type
	* @return void
	* @time	2021/12/02
	*/
	void TreeViewCtrl::showPlotfromData(Hdf5Data data, int index)
	{
		createIteminfo(data, index);
		//单独显示
		std::vector<QStandardItem*> items;
		for (auto iter = hdf5Indexs.begin(); iter != hdf5Indexs.end(); iter++)
		{
			if (iter->second == index)
			{
				items.push_back(iter->first);
			}
		}
		if (1 == items.size())
		{
			auto index = items[0]->index();
			on_doubleclick(index);
		}
	}
};

#include"moc_TreeViewctrl.cpp"