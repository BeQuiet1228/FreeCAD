#include "HDF5DataItem2DFactory.h"
#include "Transition/transition.h"
#include "sstream"
#include "HDF5DataItem2DDoubleClickEventHander.h"
/**
* @time	2021/12/20
* @brief Gui::HDF5DataItem2DFactory::CreatHDF5Items 创建item
* @param std::vector<Hdf5Data> & datas
* @return Gui::HDF5DataItemFactory::HDF5DataItems
*/
Gui::HDF5DataItemFactory::HDF5DataItems Gui::HDF5DataItem2DFactory::CreatHDF5Items(std::vector<Hdf5Data> datas)
{
	initDoubleClickHanderStructData(datas);

	HDF5DataItemFactory::HDF5DataItems items;
	auto item = CreatStructDataItem(datas);
	if (item)
		items.push_back(item);
	item = CreatContourDataItem(datas);
	if (item)
		items.push_back(item);
	item = CreatPhasespaceDataItem(datas);
	if (item)
		items.push_back(item);
	item = CreatVectorDataItem(datas);
	if (item)
		items.push_back(item);
	item = CreatObserveDataItem(datas);
	if (item)
		items.push_back(item);
	item = CreatRangDataItem(datas);
	if (item)
		items.push_back(item);
	return items;
}


Gui::HDF5DataItem* Gui::HDF5DataItem2DFactory::CreatHDF5Item(Hdf5Data& data)
{
	std::vector<Hdf5Data> datas;
	datas.push_back(data);
	auto its = CreatHDF5Items(datas);
	if (its.size() <= 0)
		return nullptr;
	return *its.begin();
}


/**
* @time	2022/01/06
* @brief Gui::HDF5DataItem2DFactory::CreatRangDataItem 创建空间变化图的节点
* @param Hdf5Data & data
* @param HDF5DataItem * parentItem
* @return Gui::HDF5DataItem*
*/
Gui::HDF5DataItem* Gui::HDF5DataItem2DFactory::CreatRangDataItem(Hdf5Data& data, HDF5DataItem* parentItem /*= nullptr*/)
{
	if (nullptr == parentItem)
	{
		parentItem = new HDF5DataItem("空间变化图");
	}
	std::string typeNode, subNode;
	{
		std::stringstream ss, subss;
		std::string art3 = getEffePartStr(data.headList[2]);
		art3.erase(art3.find("-#"), art3.size());
		ss << art3;
		//观测类型
		std::string art14 = data.headList[13];
		//观测对象
		art3 = getEffePartStr(data.headList[2]);
		//观测时刻
		std::string art12 = getEffePartStr(data.headList[11]);
		{
			art14.erase(0, art14.find("=") + 1);
			art14.erase(art14.find(" "), art14.size());
			art3.erase(0, art3.find("$") + 1);
			art12.erase(0, art12.find("TIME") + 5);
		}
		subss << art14 << " " << art3 << " " << art12;
		typeNode = ss.str();
		subNode = subss.str();
	}
	//创建节点
	auto typeNodeItem = new HDF5DataItem(typeNode.c_str());
	auto subNodeItem = new HDF5DataItem(data, subNode.c_str());
	itemSetHander(subNodeItem);
	subNodeItem = typeNodeItem->addSubItem(subNodeItem);
	typeNodeItem = parentItem->addSubItem(typeNodeItem);
	return parentItem;
}

Gui::HDF5DataItem* Gui::HDF5DataItem2DFactory::CreatRangDataItem(std::vector<Hdf5Data>& datas)
{
	auto item = new HDF5DataItem(gbkStdstringToQstring("空间变化图"));
	for (auto iter = datas.begin(); iter != datas.end();)
	{
		if (iter->name != "RANGE")
		{
			iter++;
			continue;
		}
		auto h5data = *iter;
		iter = datas.erase(iter);
		CreatRangDataItem(h5data, item);
	}
	if (item->rowCount() != 0)
		return item;
	delete item;
	return nullptr;
}

/**
* @time	2021/12/20
* @brief Gui::HDF5DataItem2DFactory::setStructData 设置结构体数据
* @param Hdf5Data data
* @return void
*/
void Gui::HDF5DataItem2DFactory::setStructData(Hdf5Data data)
{
	auto hand=getEventHander();
	std::shared_ptr<HDF5DataItem2DDoubleClickEventHander> handPtr = std::dynamic_pointer_cast<HDF5DataItem2DDoubleClickEventHander>(hand);
	if (nullptr == handPtr)
		return;
	handPtr->setStructData(data);
}

bool Gui::HDF5DataItem2DFactory::initDoubleClickHanderStructData(Hdf5Data& data)
{
	if (data.name != "struct" && data.name!="struct2d")
		return false;
	auto hander = getEventHander();
	auto hander2d = std::dynamic_pointer_cast<HDF5DataItem2DDoubleClickEventHander>(hander);
	if (!hander2d)
		return false;
	hander2d->setStructData(data);

	return true;
}

bool Gui::HDF5DataItem2DFactory::initDoubleClickHanderStructData(std::vector<Hdf5Data>& datas)
{
	for (auto iter = datas.begin(); iter != datas.end(); iter++)
	{
		if (initDoubleClickHanderStructData(*iter))
			return true;
	}
	return false;
}

/**
* @time	2021/12/20
* @brief Gui::HDF5DataItem2DFactory::CreatStructDataItem 创建结构图数据
* @param Hdf5Data & data
* @param HDF5DataItem * parentItem
* @return Gui::HDF5DataItem*
*/
Gui::HDF5DataItem* Gui::HDF5DataItem2DFactory::CreatStructDataItem(Hdf5Data& data, HDF5DataItem* parentItem)
{
	if (nullptr == parentItem)
	{
		parentItem = new HDF5DataItem(gbkStdstringToQstring("结构图"));
	}
	//判断是2维还是3维的
	if (data.listDataSet.size()<4)
	{
		//提取名称
		std::string structstr = *(data.headList.begin() + 2);
		structstr.erase(std::remove_if(structstr.begin(), structstr.end(), isspace), structstr.end());
		int _j = structstr.find("=");
		structstr.erase(0, _j + 1);
		int pos1 = structstr.find("$");
		int pos2 = structstr.find("$", pos1 + 1);
		structstr = structstr.substr(pos1 + 1, pos2 - pos1 - 1);
		auto structItem = new HDF5DataItem(data, structstr.c_str());
		itemSetHander(structItem);
		parentItem->addSubItem(structItem);
		return parentItem;
	}
	//3维
	switch (data.coordinateSystem)
	{
	case Hdf5Data::CARTESIAN:
	{
		//"X_Y", "Y_Z", "X_Z";
		auto structItem1 = new HDF5DataItem(data, "X_Y");
		itemSetHander(structItem1);
		parentItem->addSubItem(structItem1);
		auto structItem2 = new HDF5DataItem(data, "Y_Z");
		itemSetHander(structItem2);
		parentItem->addSubItem(structItem2);
		auto structItem3 = new HDF5DataItem(data, "X_Z");
		itemSetHander(structItem3);
		parentItem->addSubItem(structItem3);
	}
	break;
	case Hdf5Data::POLAR:
	case Hdf5Data::CYLINDER:
	{
		//"Phi-Z",
		//"Z-R",
		//"R*cos(Phi)-R*sin(Phi)"
		auto structItem1 = new HDF5DataItem(data, "Phi-Z");
		itemSetHander(structItem1);
		parentItem->addSubItem(structItem1);
		auto structItem2 = new HDF5DataItem(data, "Z-R");
		itemSetHander(structItem2);
		parentItem->addSubItem(structItem2);
		auto structItem3 = new HDF5DataItem(data, "R*cos(Phi)-R*sin(Phi)");
		itemSetHander(structItem3);
		parentItem->addSubItem(structItem3);
	}
	break;
	}
	//传入结构图数据
	setStructData(data);
	return parentItem;
}

Gui::HDF5DataItem* Gui::HDF5DataItem2DFactory::CreatContourDataItem(std::vector<Hdf5Data>& datas)
{
	HDF5DataItem* item = new HDF5DataItem(gbkStdstringToQstring("等位图"));
	for (auto iter=datas.begin();iter!=datas.end();)
	{
		if (iter->name != "CONTOUR")
		{
			iter++;
			continue;
		}
		auto h5ddata = *iter;
		iter = datas.erase(iter);
		CreatContourDataItem(h5ddata,item);
	}
	if (item->rowCount() != 0)
		return item;
	delete item;
	return nullptr;
}




/**
* @time	2021/12/20
* @brief Gui::HDF5DataItem2DFactory::CreatPhasespaceDataItem 创建相空间图节点
* @param std::vector<Hdf5Data> & datas
* @return Gui::HDF5DataItem*
*/
Gui::HDF5DataItem* Gui::HDF5DataItem2DFactory::CreatPhasespaceDataItem(std::vector<Hdf5Data>& datas)
{
	HDF5DataItem* item = new HDF5DataItem(gbkStdstringToQstring("相空间图"));
	for (auto iter=datas.begin();iter!=datas.end();)
	{
		if (iter->name != "PHASESPACE")
		{
			iter++;
			continue;
		}
		auto h5data = *iter;
		iter = datas.erase(iter);
		CreatPhasespaceDataItem(h5data, item);
	}
	if (item->rowCount() != 0)
		return item;
	delete item;
	return nullptr;
}


/**
* @time	2021/12/20
* @brief Gui::HDF5DataItem2DFactory::CreatVectorDataItem 创建矢量图节点
* @param std::vector<Hdf5Data> & datas
* @return Gui::HDF5DataItem*
*/
Gui::HDF5DataItem* Gui::HDF5DataItem2DFactory::CreatVectorDataItem(std::vector<Hdf5Data>& datas)
{
	HDF5DataItem* item = new HDF5DataItem(gbkStdstringToQstring("矢量图"));
	for (auto iter=datas.begin();iter!=datas.end();)
	{
		if (iter->name != "VECTOR")
		{
			iter++;
			continue;
		}
		auto h5data = *iter;
		iter = datas.erase(iter);
		CreatVectorDataItem(h5data,item);
	}
	if (item->rowCount() != 0)
		return item;
	delete item;
	return nullptr;
}


/**
* @time	2021/12/20
* @brief Gui::HDF5DataItem2DFactory::CreatObserveDataItem 创建时间图节点
* @param std::vector<Hdf5Data> & datas
* @return Gui::HDF5DataItem*
*/
Gui::HDF5DataItem* Gui::HDF5DataItem2DFactory::CreatObserveDataItem(std::vector<Hdf5Data>& datas)
{
	auto item = new HDF5DataItem(gbkStdstringToQstring("时间图"));
	for (auto iter=datas.begin();iter!=datas.end();)
	{
		if (iter->name != "OBSERVE")
		{
			iter++;
			continue;
		}
		auto h5data = *iter;
		iter = datas.erase(iter);
		CreatObserveDataItem(h5data, item);
	}
	if (item->rowCount() != 0)
		return item;
	delete item;
	return nullptr;
}

Gui::HDF5DataItem* Gui::HDF5DataItem2DFactory::CreatObserveDataItem(Hdf5Data& data, HDF5DataItem* parentItem /*= nullptr*/)
{
	if (nullptr == parentItem)
	{
		parentItem = new HDF5DataItem("时间图");
	}
	std::string typeNode,subNode;
	{
		std::stringstream ss, subss;
		std::string art3 = getEffePartStr(data.headList[2]);
		art3.erase(art3.find("-#"), art3.size());
		ss << art3;
		std::string art14 = getEffePartStr(data.headList[13]);
		{
			transform(art14.begin(), art14.end(), art14.begin(), toupper);
			int pos = 0;
			while (std::string::npos != (pos = art14.find("MAGINTUDE"))) art14.erase(pos, 9);
			while (std::string::npos != (pos = art14.find("OF"))) art14.erase(pos, 2);
			while (std::string::npos != (pos = art14.find("COMPONENT"))) art14.erase(pos, 9);

		}
		art3 = getEffePartStr(data.headList[2]);
		art3.erase(0, art3.find("$") + 1);
		subss << art14 << " " << art3;
		typeNode = ss.str();
		subNode = subss.str();
	}
	//创建节点
	//auto typeNodeItem = findTypeItem(parentItem,typeNode);
	auto typeNodeItem=new HDF5DataItem(typeNode.c_str());
	auto subNodeItem = new HDF5DataItem(data,subNode.c_str());
	itemSetHander(subNodeItem);
	subNodeItem = typeNodeItem->addSubItem(subNodeItem);
	typeNodeItem = parentItem->addSubItem(typeNodeItem);

	return parentItem;
}

Gui::HDF5DataItem* Gui::HDF5DataItem2DFactory::CreatVectorDataItem(Hdf5Data& data, HDF5DataItem* parentItem /*= nullptr*/)
{
	if (nullptr == parentItem)
	{
		parentItem = new HDF5DataItem(gbkStdstringToQstring("矢量图"));
	}
	std::string typeNode;
	std::string subNode;
	{
		auto art3=getEffePartStr(data.headList[2]);
		auto art14=getEffePartStr(data.headList[13]);
		auto art12 = getEffePartStr(data.headList[11]);
		std::stringstream ss, subs;
		art12.erase(0, art12.find("("));
		art3.erase(0, art3.find("$") + 1);
		art14.erase(0,art14.find("TIME:")+5);
		ss << "PLOT" << art12;
		subs << art3 << " " << art14;
		typeNode = ss.str();
		subNode = subs.str();
	}
	//创建节点
	//auto typeNodeItem = findTypeItem(parentItem, typeNode);
	auto typeNodeItem=new HDF5DataItem(typeNode.c_str());
	auto subNodeItem = new HDF5DataItem(data,subNode.c_str());
	itemSetHander(subNodeItem);
	subNodeItem = typeNodeItem->addSubItem(subNodeItem);
	typeNodeItem = parentItem->addSubItem(typeNodeItem);
	
	return parentItem;
}

Gui::HDF5DataItem* Gui::HDF5DataItem2DFactory::CreatPhasespaceDataItem(Hdf5Data& data, HDF5DataItem* parentItem /*= nullptr*/)
{
	if (nullptr == parentItem)
	{
		parentItem = new HDF5DataItem(gbkStdstringToQstring("相空间图"));
	}
	std::string typeNode;
	std::string subNode;
	{
		auto art3 = getEffePartStr(data.headList[2]);
		typeNode = art3.substr(0,art3.find("-#"));
		auto art12 = getEffePartStr(data.headList[11]);
		int pos = art3.find("$");
		art3 = (pos == std::string::npos) ? ("") : art3.erase(0,art3.find("$")+1);
		{
			std::stringstream s1;
			s1 << art12.substr(art12.find("OF") + 2, (art12.find("VS") - (art12.find("OF") + 2)))
				<< " " << art12.substr(art12.find("VS") + 2, (art12.find("AT") - (art12.find("VS") + 2)));
			s1 << " " << art12.substr(art12.find("TIME") + 5, (art12.size() - (art12.find("TIME") + 5)));
			art12 = s1.str();
		}
		std::stringstream subss;
		subss << art3 << " " << art12;
		subNode = subss.str();
	}
	//创建树控件节点
	//auto typeNodeItem = findTypeItem(parentItem, typeNode);
	auto typeNodeItem=new HDF5DataItem(typeNode.c_str());
	auto subNodeItem = new HDF5DataItem(data,subNode.c_str());
	itemSetHander(subNodeItem);
	subNodeItem = typeNodeItem->addSubItem(subNodeItem);
	typeNodeItem = parentItem->addSubItem(typeNodeItem);
	
	return parentItem;
}

/**
* @time	2021/12/20
* @brief Gui::HDF5DataItem2DFactory::getEffePartStr 获取头部信息的有效部分，取=右侧信息，以及去掉两端的空格
* @param std::string str
* @return std::string
*/
std::string Gui::HDF5DataItem2DFactory::getEffePartStr(std::string str)
{
	int pos = str.find("=");
	str.erase(0,pos+1);
	QString qres = QString::fromStdString(str);
	qres = qres.simplified();
	return qres.toStdString();
}


/**
* @time	2021/12/20
* @brief Gui::HDF5DataItem2DFactory::findTypeItem 寻找分类节点
* @param HDF5DataItem * parentItem
* @param std::string typeNodestr
* @return Gui::HDF5DataItem*
*/
Gui::HDF5DataItem* Gui::HDF5DataItem2DFactory::findTypeItem(HDF5DataItem* parentItem, std::string typeNodestr)
{
	int rowCount = parentItem->rowCount();
	for (auto row=0;row<parentItem->rowCount();++row)
	{
		auto item = parentItem->child(row);
		if(item->text().toStdString() != typeNodestr)
			continue;
		HDF5DataItem* hdf5Dataitem = dynamic_cast<HDF5DataItem*>(item);
		return hdf5Dataitem;
	}
	auto typeNodeItem = new HDF5DataItem(typeNodestr.c_str());
	parentItem->addSubItem(typeNodeItem);
	return typeNodeItem;
}

/**
* @time	2021/12/20
* @brief Gui::HDF5DataItem2DFactory::CreatContourDataItem 创建等位图
* @param Hdf5Data & data
* @param HDF5DataItem * parentItem
* @return Gui::HDF5DataItem*
*/
Gui::HDF5DataItem* Gui::HDF5DataItem2DFactory::CreatContourDataItem(Hdf5Data& data, HDF5DataItem* parentItem /*= nullptr*/)
{
	//等位图
	if (nullptr == parentItem)
	{
		parentItem = new HDF5DataItem(gbkStdstringToQstring("2D等位图"));
	}
	std::string typeNode;//分类
	std::string subNode;//
	{
		std::string art3 = getEffePartStr(data.headList[2]);
		typeNode = art3.substr(0, art3.find("-#"));
		std::string art13 = getEffePartStr(data.headList[12]);
		art3.erase(0, art3.find("$") + 1);
		art13.erase(0, art13.find("TIME"));
		std::stringstream subss;
		subss << art3 << " " << art13;
		subNode = subss.str();
	}
	//查找是否已经创建过了
	//auto typeNodeItem = findTypeItem(parentItem, typeNode);
	auto typeNodeItem=new HDF5DataItem(typeNode.c_str());
	auto subNodeItem = new HDF5DataItem(data,subNode.c_str());
	itemSetHander(subNodeItem);
	subNodeItem = typeNodeItem->addSubItem(subNodeItem);
	typeNodeItem = parentItem->addSubItem(typeNodeItem);
	
	return parentItem;
}

/**
* @time	2021/12/20
* @brief Gui::HDF5DataItem2DFactory::CreatStructDataItem 创建结构图数据
* @param std::vector<Hdf5Data> & datas
* @return Gui::HDF5DataItem*
*/
Gui::HDF5DataItem* Gui::HDF5DataItem2DFactory::CreatStructDataItem(std::vector<Hdf5Data>& datas)
{
	HDF5DataItem* item = nullptr;
	for (auto iter=datas.begin();iter!=datas.end();iter++)
	{
		if(iter->name!="struct" && iter->name!="struct2d")
			continue;
		auto h5data = *iter;
		iter = datas.erase(iter);
		item = CreatStructDataItem(h5data);
		break;
	}
	return item;
}