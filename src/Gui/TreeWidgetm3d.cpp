#include "PreCompiled.h"
#include "TreeWidgetm3d.h"
#include "Application.h"
#include <App/Document.h>
#include"Document.h"
#include"Tree.h"
QString treeIcon2[2] = {};
TreeWidgetm3d::TreeWidgetm3d(QWidget* parent) :Gui::TreeWidget(parent)
{
	//2021/6/18 新增信号，用于添加子节点控件
	Gui::Application::Instance->signalAddsubitem.connect(boost::bind(&TreeWidgetm3d::addSubItem, this, _1, _2));
	/*Application::Instance->signalAddsubItem2.connect(boost::bind(&TreeWidget::addSubItem2, this, _1, _2));*/
	Gui::Application::Instance->signalAddsubitem2.connect(boost::bind(&TreeWidgetm3d::addSubItem2, this,
		_1, _2, _3, _4));
	Gui::Application::Instance->signalClearSub.connect(boost::bind(&TreeWidgetm3d::clearsubItem, this, _1));
	treeIcon2[0] = QString::fromUtf8(":/icons/Group.svg");
	treeIcon2[1] = QString::fromUtf8(":/icons/ClassBrowser/member.png");
	//treewidget = new Gui::TreeWidget(parent);
}
TreeWidgetm3d::~TreeWidgetm3d()
{

}
void TreeWidgetm3d::addSubItem(const Gui::Document& doc, const std::string& keyWord){
	auto iter = DocumentMap.find(&doc);
	if (iter != DocumentMap.end())
	{
		Gui::DocumentItem* mItem = dynamic_cast<Gui::DocumentItem*>(iter->second);
		if (!mItem)
		{
			std::cerr << "DocumentItem is nullptr from void TreeWidget::addSubItem(const Gui::Document& doc,const std::string& keyWord)" << std::endl;
			return;
		}
		QTreeWidgetItem* subitem = new QTreeWidgetItem(mItem, Gui::TreeWidget::m3dtextType);
		subitem->setText(0, QString::fromStdString(keyWord));
	}
}
void TreeWidgetm3d::addSubItem2(const Gui::Document& doc, const std::string& GroupName,
	const std::string& KeyName, const int cusline){
	auto iter = DocumentMap.find(&doc);
	if (iter != DocumentMap.end())
	{
		Gui::DocumentItem* mItem = dynamic_cast<Gui::DocumentItem*>(iter->second);
		QTreeWidgetItem* parentItem = dynamic_cast<QTreeWidgetItem*>(mItem);
		if (!parentItem)
		{
			std::cerr << "DocumentItem is nullptr from void TreeWidget::addSubItem(const Gui::Document& doc,const std::string& keyWord)" << std::endl;
			return;
		}
		QTreeWidgetItem* item = nullptr;/* = new QTreeWidgetItem(mItem, TreeWidget::m3dtextType);*/
		//查找组
		auto itergroup = groupItems.find(GroupName);
		if (itergroup != groupItems.end())
		{
			item = itergroup->second;
		}
		else
		{
			item = new QTreeWidgetItem(parentItem,Gui::TreeWidget::m3dtextType);
			item->setText(0, QString::fromStdString(GroupName));
			item->setIcon(0, QIcon(treeIcon2[0]));
			groupItems[GroupName] = item;
		}
		//判断子节点的长度是否过长
		std::string substring = KeyName;
		/*if (KeyName.length() > 15)
		{
		substring = KeyName.substr(0, 15);
		substring = substring + "...";
		}*/
		QTreeWidgetItem* subItems = nullptr;
		subItems = new QTreeWidgetItem(item, Gui::TreeWidget::m3dtextType);
		subItems->setIcon(0, QIcon(treeIcon2[1]));
		subItems->setText(0, QString::fromStdString(substring));
		//item->addChild(subItems);
		itemToLine[subItems] = cusline;
	}
}
void TreeWidgetm3d::clearsubItem(const Gui::Document& doc){
	auto iter = DocumentMap.find(&doc);
	if (iter != DocumentMap.end())
	{
		//清除该节点下的所有节点
		Gui::DocumentItem* mItem = dynamic_cast<Gui::DocumentItem*>(iter->second);
		if (!mItem)
		{
			std::cerr << "DocumentItem is nullptr from void TreeWidget::addSubItem(const Gui::Document& doc,const std::string& keyWord)" << std::endl;
			return;
		}
		//清除该节点下的所有子字节点
		auto childCount = mItem->childCount();
		for (auto index = childCount - 1; index >= 0; index--)
		{
			auto childitem = mItem->child(index);
			auto childitensub = childitem->childCount();
			for (auto subindex = childitensub - 1; subindex >= 0; subindex--)
			{
				childitem->removeChild(childitem->child(subindex));
			}
			mItem->removeChild(mItem->child(index));
		}
		itemToLine.clear();
		groupItems.clear();
	}
}
void TreeWidgetm3d::mouseDoubleClickEvent(QMouseEvent * event)
{
	QTreeWidgetItem* item = itemAt(event->pos());
	//if (!item)
	//	return;
	//Gui::TreeWidget::mouseDoubleClickEvent(event);
	//if (item->type()==TreeWidget::m3dtextType)
	//{
	//	auto iter = itemToLine.find(item);
	//	if (iter != itemToLine.end())
	//	{
	//		//qDebug() << "line:" << iter->second;
	//		Gui::Application::Instance->GoToLine(iter->second);
	//	}
	//}
}

//void TreeWidgetm3d::onSelectionChanged(const SelectionChanges& msg)
//{
//	switch (msg.Type)
//	{
//	case SelectionChanges::AddSelection:
//	{
//		Gui::Document* pDoc = Application::Instance->getDocument(msg.pDocName);
//		std::map<const Gui::Document*, DocumentItem*>::iterator it;
//		it = DocumentMap.find(pDoc);
//		bool lock = this->blockConnection(true);
//		if (it != DocumentMap.end())
//		 it->second->setObjectSelected(msg.pObjectName, true);
//		this->blockConnection(lock);
//	}   break;
//	case SelectionChanges::RmvSelection:
//	{
//										   Gui::Document* pDoc = Application::Instance->getDocument(msg.pDocName);
//										   std::map<const Gui::Document*, DocumentItem*>::iterator it;
//										   it = DocumentMap.find(pDoc);
//										   bool lock = this->blockConnection(true);
//										   if (it != DocumentMap.end())
//											   it->second->setObjectSelected(msg.pObjectName, false);
//										   this->blockConnection(lock);
//	}   break;
//	case SelectionChanges::SetSelection:
//	{
//										   Gui::Document* pDoc = Application::Instance->getDocument(msg.pDocName);
//										   std::map<const Gui::Document*, DocumentItem*>::iterator it;
//										   it = DocumentMap.find(pDoc);
//										   // we get notified from the selection and must only update the selection on the tree,
//										   // thus no need to notify again the selection. See also onItemSelectionChanged().
//										   if (it != DocumentMap.end()) {
//											   bool lock = this->blockConnection(true);
//											   it->second->selectItems();
//											   this->blockConnection(lock);
//										   }
//	}   break;
//	case SelectionChanges::ClrSelection:
//	{
//										   // clears the complete selection
//										   if (strcmp(msg.pDocName, "") == 0) {
//											   this->clearSelection();
//										   }
//										   else {
//											   // clears the selection of the given document
//											   Gui::Document* pDoc = Application::Instance->getDocument(msg.pDocName);
//											   std::map<const Gui::Document*, DocumentItem*>::iterator it;
//											   it = DocumentMap.find(pDoc);
//											   if (it != DocumentMap.end()) {
//												   it->second->clearSelection();
//											   }
//										   }
//										   this->update();
//	}   break;
//	case SelectionChanges::SetPreselect:
//	{
//										   Gui::Document* pDoc = Application::Instance->getDocument(msg.pDocName);
//										   std::map<const Gui::Document*, DocumentItem*>::iterator it;
//										   it = DocumentMap.find(pDoc);
//										   if (it != DocumentMap.end())
//											   it->second->setObjectHighlighted(msg.pObjectName, true);
//	}   break;
//	case SelectionChanges::RmvPreselect:
//	{
//										   Gui::Document* pDoc = Application::Instance->getDocument(msg.pDocName);
//										   std::map<const Gui::Document*, DocumentItem*>::iterator it;
//										   it = DocumentMap.find(pDoc);
//										   if (it != DocumentMap.end())
//											   it->second->setObjectHighlighted(msg.pObjectName, false);
//	}   break;
//	default:
//		break;
//	}
//}
	//std::map <QTreeWidgetItem*, int> itemToLine;
	//std::map<std::string, QTreeWidgetItem*> groupItems;

#include "moc_TreeWidgetm3d.cpp"