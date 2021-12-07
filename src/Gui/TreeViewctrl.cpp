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
#include "TreeNodeFactor.h"
#include "TreeNode.h"
#include "DataVisualization/C_encoding.h"
namespace Gui{
	TreeViewCtrl::TreeViewCtrl(QWidget* parent):ListTreeWidget(parent){
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
		App::Document *doc = App::GetApplication().getActiveDocument();
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
		auto dataItem= hdf5Indexs.find(currentItem);
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
	void TreeViewCtrl::displayItem(QStandardItem* item,Hdf5Data& data)
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
		auto index=DV::RendererFactory::findStructDataIndex(Hdf5Datalist);
		if (-1 != index)
		{
			structIndex = index;
		}
		//增加清理流程
		clear();
		for (auto index=0;index<Hdf5Datalist.size();index++)
		{
			createIteminfo(Hdf5Datalist[index],index);
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
		auto node2D = TreeNodeFactor::GetInstance()->createTreeNode2D(data, index);
		creatItem(node2D,2);//2维
		delete node2D;

		auto node3D = TreeNodeFactor::GetInstance()->createTreeNode3D(data, index);
		creatItem(node3D, 3);//3维
		delete node3D;
	}
	void TreeViewCtrl::creatItem(TreeNode* node,int type)
	{
		if (nullptr == node)
			return;
		if (parentNodes.find(node->nodeStr) == parentNodes.end())
		{
			QStandardItem* parentItem = new QStandardItem(DV::GetEncodingstr(node->nodeStr.c_str(), ENCODING_GB2312));
			int row = goodsModel->rowCount();
			goodsModel->setItem(row,parentItem);
			parentNodes[node->nodeStr] = parentItem;
			addItem(parentItem, node, type);
		}
		else
		{
			auto parentItem = parentNodes.find(node->nodeStr);
			addItem(parentItem->second,node,type);
		}
		return;
	}
	void TreeViewCtrl::addItem(QStandardItem* item, TreeNode*node,int type)
	{
		if (0 == node->getChilds())
			return;
		for (auto i = 0; i < node->getChilds(); ++i)
		{
			bool isBreak=false;
			int row = item->rowCount();
			for (auto j=0;j<row;++j)
			{
				auto subitem = item->child(j);
				auto res = subitem->text().toStdString()==(node->Childs()[i]->nodeStr);
				if (1==res)
				{
					addItem(subitem,node->Childs()[i],type);
					isBreak = true;
					break;
				}
			}
			if (!isBreak)
			{
				
				QStandardItem* subitem = new QStandardItem(DV::GetEncodingstr(node->Childs()[i]->nodeStr.c_str(), ENCODING_GB2312));
				if (node->Childs()[i]->mTreeNodeType == TreeNodeType::TREENODE_FILE)
				{
					if (type == 2)
					{
						std::shared_ptr<PlotAdapterBase> funcPtr = std::shared_ptr<PlotAdapterBase>(new PlotAdapter2D());
						if (-1 != structIndex)
						{
							App::Document* doc = App::GetApplication().getActiveDocument();
							DocumentManager* docM = dynamic_cast<DocumentManager*>(doc);
							if (nullptr != docM)
							{
								auto h5dStruct = docM->gethdf5dataList()[structIndex];
								funcPtr->setStructData(h5dStruct);
							}
						}
						adapterFunc[subitem] = funcPtr;
						hdf5Indexs[subitem] = node->Childs()[i]->index;
					}
					
				}
				else
				{
					addItem(subitem, node->Childs()[i], type);
				}
				int row = item->rowCount();
				if (row == 0 || node->Childs()[i]->nodeInfo.time < 0.0)
				{
					item->setChild(row, subitem);
				}
				else
				{
					//排序
					int currow = 0;
					for (int rowindex=0;rowindex<row;rowindex++)
					{
						auto currentItem = item->child(rowindex);
						std::string currentItemstr = currentItem->text().toStdString();
						int res = strcmp(currentItemstr.c_str(), node->Childs()[i]->nodeStr.c_str());
						if (res<0)
							currow = rowindex + 1;
					}
					item->insertRow(currow, subitem);
				}
				//item->setChild(row, subitem);
				
			}
		}
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
		createIteminfo(data,index);
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