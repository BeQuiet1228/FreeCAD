#include "PreCompiled.h"
#include "PICRibbon.h"
#include "PICRibbonTabContent.h"
#include "PICRibbonButtonGroup.h"

#include <QApplication>
#include <QStyleOption>
#include <QPainter>
#include "picgui_ribbon/moc_PICRibbon.cpp"
#include <iostream>
#include"darWer.h"
#define WIGET_INTERVAL (30)
Ribbon::Ribbon(QWidget *parent)
	: QTabWidget(parent)
{
	mydarWer.clear();
	setCursor(Qt::ArrowCursor);
}

void Ribbon::addTab(const QString &tabName)
{
  // Note: superclass QTabWidget also has a function addTab()
  PICRibbonTabContent *ribbonTabContent = new PICRibbonTabContent;
  QTabWidget::addTab(ribbonTabContent, tabName);
  this->setAttribute(Qt::WA_StyledBackground);

}
void Ribbon::addTab(const QIcon &tabIcon, const QString &tabName)
{
  // Note: superclass QTabWidget also has a function addTab()
  PICRibbonTabContent *ribbonTabContent = new PICRibbonTabContent;
  QTabWidget::addTab(ribbonTabContent, tabIcon, tabName);
}

void Ribbon::removeTab(const QString &tabName)
{
  // Find ribbon tab
  for (int i = 0; i < count(); i++)
  {
    if (tabText(i).toLower() == tabName.toLower())
    {
      // Remove tab
      QWidget *tab = QTabWidget::widget(i);
      QTabWidget::removeTab(i);
      delete tab;
      break;
    }
  }
}

void Ribbon::addGroup(const QString &tabName, const QString &groupName)
{
  // Find ribbon tab
  QWidget *tab = nullptr;
  for (int i = 0; i < count(); i++)
  {
    if (tabText(i).toLower() == tabName.toLower())
    {
      tab = QTabWidget::widget(i);
      break;
    }
  }

  if (tab != nullptr)
  {
    // Tab found
    // Add ribbon group
    PICRibbonTabContent *ribbonTabContent = static_cast<PICRibbonTabContent*>(tab);
    ribbonTabContent->addGroup(groupName);
  }
  else
  {
    // Tab not found
    // Create tab
    addTab(tabName);

    // Add ribbon group
    addGroup(tabName, groupName);
  }
}

void Ribbon::addButton(const QString &tabName, const QString &groupName, QToolButton *button)
{
  // Find ribbon tab
  QWidget *tab = nullptr;
  for (int i = 0; i < count(); i++)
  {
    if (tabText(i).toLower() == tabName.toLower())
    {
      tab = QTabWidget::widget(i);
      break;
    }
  }

  if (tab != nullptr)
  {
    // Tab found
    // Add ribbon button
    PICRibbonTabContent *ribbonTabContent = static_cast<PICRibbonTabContent*>(tab);
    ribbonTabContent->addButton(groupName, button);
  }
  else
  {
    // Tab not found.
    // Create tab
    addTab(tabName);

    // Add ribbon button
    addButton(tabName, groupName, button);
  }
}

void Ribbon::removeButton(const QString &tabName, const QString &groupName, QToolButton *button)
{
  // Find ribbon tab
  QWidget *tab = nullptr;
  for (int i = 0; i < count(); i++)
  {
    if (tabText(i).toLower() == tabName.toLower())
    {
      tab = QTabWidget::widget(i);
      break;
    }
  }

  if (tab != nullptr)
  {
    // Tab found
    // Remove ribbon button
    PICRibbonTabContent *ribbonTabContent = static_cast<PICRibbonTabContent*>(tab);
    ribbonTabContent->removeButton(groupName, button);

    if (ribbonTabContent->groupCount() == 0)
    {
      removeTab(tabName);
    }
  }
}


QList<PICRibbonTabContent *> Ribbon::get_tab_all()
{
	QList<PICRibbonTabContent *> list;
	for (int i = 0; i < count(); i++)
	{
		QWidget *tab = QTabWidget::widget(i);
		PICRibbonTabContent *ribbonTabContent = static_cast<PICRibbonTabContent*>(tab);
		list.append(ribbonTabContent);
	}
	return list;
}

PICRibbonTabContent *Ribbon::get_tab_by_name(QString &name)
{
	QWidget *tab = nullptr;
	for (int i = 0; i < count(); i++)
	{
		if (tabText(i) == name)
		{
			tab = QTabWidget::widget(i);
			break;
		}
	}
	PICRibbonTabContent *ribbonTabContent = static_cast<PICRibbonTabContent*>(tab);
	return ribbonTabContent;
}









/**
* @brief  Ribbon::addAction
* @param  const QString & tabName  
* @param  const QString & groupName  
* @param  QAction * action  
* @return void  
*/
void Ribbon::addAction(const QString &tabName, const QString &groupName, QAction *action)
{
	QToolButton *b = new QToolButton;
	b->setDefaultAction(action);
	this->addButton(tabName, groupName, b);
}

/**
* @brief  Ribbon::clearAllAction
* @return void  
*/
void Ribbon::clearAllAction()
{
	this->clear();
}

void Ribbon::clearTab(const QString &tabName)
{
	QString name_t = tabName;
	PICRibbonTabContent * t = get_tab_by_name(name_t);
	QList<QString> list_g_name = this->getGroup(name_t);
	for (int i = 0; i<list_g_name.count(); i++) {
		t->removeGroup(list_g_name.at(i));
	}

}

void Ribbon::clearGoup(const QString &groupName)
{
	PICRibbonButtonGroup * g = nullptr;
	QList<PICRibbonTabContent *> list_t = get_tab_all();
	QList<QAction*> list;
	for (int i = 0; i<list_t.count(); i++) {
		PICRibbonTabContent * t = list_t.at(i);

		QList<PICRibbonButtonGroup *> list_g = t->get_group_all();
		for (int j = 0; j<list_g.count(); j++) {
			QString name = list_g.at(j)->title();
			if (name == groupName){
				t->removeGroup(name);
				break;
			}
		}
	}
	//    QList<QToolButton*> list_b= this->findChildren<QToolButton*>();
	//    QToolButton* b=nullptr;
	//    for (int i;i<list_b.count();i++) {
	//        b=list_b.at(i);
	//        g->removeButton(b);
	//        delete b;
	//    }
}

/**
* @brief  Ribbon::getTabs
* @return QT_NAMESPACE::QList<QT_NAMESPACE::QString>  
*/
QList<QString> Ribbon::getTabs()
{
	QList<QString> list;
	for (int i = 0; i < count(); i++)
	{
		QString name = tabText(i);
		list.append(name);

	}
	return list;
}

/**
* @brief  Ribbon::getGroups 获取组
* @return QT_NAMESPACE::QList<QT_NAMESPACE::QString>  
*/
QList<QString> Ribbon::getGroups()
{
	QList<PICRibbonTabContent *> list_t = get_tab_all();
	QList<QString> list;
	for (int i = 0; i<list_t.count(); i++) {
		PICRibbonTabContent * t = list_t.at(i);
		QList<PICRibbonButtonGroup *> list_g = t->get_group_all();
		for (int j = 0; j<list_g.count(); j++) {
			QString name = list_g.at(j)->title();
			list.append(name);
		}
	}
	return list;
}

/**
* @brief  Ribbon::getGroup
* @param  const QString & tabName  
* @return QT_NAMESPACE::QList<QT_NAMESPACE::QString>  
*/
QList<QString> Ribbon::getGroup(const QString &tabName)
{
	QString name_t = tabName;
	QList<QString> list;
	PICRibbonTabContent * t = get_tab_by_name(name_t);
	QList<PICRibbonButtonGroup *> list_g = t->get_group_all();
	for (int j = 0; j<list_g.count(); j++) {
		QString name = list_g.at(j)->title();
		list.append(name);
	}
	return list;
}

/**
* @brief  Ribbon::getActions
* @return QT_NAMESPACE::QList<QAction *>  
*/
QList<QAction *> Ribbon::getActions()
{
	QList<PICRibbonTabContent *> list_t = get_tab_all();
	QList<QAction*> list;
	for (int i = 0; i<list_t.count(); i++) {
		PICRibbonTabContent * t = list_t.at(i);
		QList<PICRibbonButtonGroup *> list_g = t->get_group_all();
		for (int j = 0; j<list_g.count(); j++) {
			list.append(list_g.at(j)->get_action_all());
		}
	}
	return list;
}

/**
* @brief  Ribbon::getTabActions
* @param  const QString & tabName  
* @return QT_NAMESPACE::QList<QAction *>  
*/
QList<QAction *> Ribbon::getTabActions(const QString &tabName)
{

	QString name_t = tabName;
	QList<QAction*> list;
	PICRibbonTabContent * t = get_tab_by_name(name_t);
	QList<PICRibbonButtonGroup *> list_g = t->get_group_all();
	for (int j = 0; j<list_g.count(); j++) {
		list.append(list_g.at(j)->get_action_all());
	}
	return list;
}

/**
* @brief  Ribbon::getGroupActions 获取对应的内容
* @param  const QString & groupName  
* @return QT_NAMESPACE::QList<QAction *>  
*/
QList<QAction *> Ribbon::getGroupActions(const QString &groupName)
{
	PICRibbonButtonGroup * g;
	QList<PICRibbonTabContent *> list_t = get_tab_all();
	QList<QAction*> list;
	for (int i = 0; i<list_t.count(); i++) {
		PICRibbonTabContent * t = list_t.at(i);
		QList<PICRibbonButtonGroup *> list_g = t->get_group_all();
		for (int j = 0; j<list_g.count(); j++) {
			QString name = list_g.at(j)->title();
			if (name == groupName){
				list.append(list_g.at(j)->get_action_all());
			}
		}
	}
	return list;

}


/**
* @brief  Ribbon::setTabOlder
* @param  const QString & tabName  
* @param  const int older  
* @return void  
*/
void Ribbon::setTabOlder(const QString &tabName, const int older)
{
	QString name_t = tabName;
	PICRibbonTabContent * t = get_tab_by_name(name_t);
	QTabWidget::insertTab(older, t, name_t);
}

/**
* @brief  Ribbon::hasAction
* @param  const QAction * action  
* @return bool  
*/
bool Ribbon::hasAction(const QAction *action)
{
	QList<QAction*> list = this->getActions();
	for (int i = 0; i<list.count(); i++) {
		if (list.at(i)->text() == action->text()){
			return true;
		}
	}
	return false;
}

//1.15 WDT_QL新增接口
//改变一个分组位置,sequence参数为新的位置,最小为0
void Ribbon::setGroupSequence(const QString &tabName, const QString &groupName, int sequence)
{
	//新序号必须大于等于0
	if (sequence >= 0)
	{
		QString name_t = tabName;
		PICRibbonTabContent * t = get_tab_by_name(name_t);
		QList<PICRibbonButtonGroup *> groupList = t->get_group_all();
		int originalSequence = -1;
		PICRibbonButtonGroup * originalGroup = nullptr;
		for (int i = 0; i < groupList.count(); i++)
		{
			if (groupName == groupList.at(i)->title())
			{
				originalSequence = i;
				originalGroup = groupList.at(i);
				groupList.removeAt(i);
				i--;
				break;
			}
		}

		if (originalSequence >= 0)
		{
			QList<PICRibbonButtonGroup *> newGroupList;
			bool flag = false;
			for (int i = 0; i < groupList.count(); i++)
			{
				if (i == sequence)
				{
					if (!flag)
					{
						newGroupList.append(originalGroup);
						i--;
						flag = true;
						continue;
					}
				}
				newGroupList.append(groupList.at(i));
			}

			t->clearGroups();
			for (int i = 0; i < newGroupList.count(); i++)
			{
				t->addGroup(newGroupList.at(i));
			}

		}
	}
}

/**
* @brief  Ribbon::getunfoldMinSize 获取扩展大小门限
* @return QT_NAMESPACE::QSize  
*/
QSize Ribbon:: getunfoldMinSize() {
	QSize size;
	QWidget* tab = nullptr;
	unsigned int widgetMax = 0;
	unsigned int widgetMaxHeight = 0;
	for (auto index = 0; index < count();index++)
	{
		tab = QTabWidget::widget(index);
		PICRibbonTabContent* picribbontabcontent = dynamic_cast<PICRibbonTabContent*>(tab);
		unsigned int curallwidth = 0;
		unsigned int curallheight = 0;
		for (auto index2 = 0; index2 < picribbontabcontent->contentLayout->count();index2++)
		{
			PICRibbonButtonGroup* group = dynamic_cast<PICRibbonButtonGroup*>(picribbontabcontent->contentLayout->itemAt(index2)->widget());
			curallwidth += group->size().width();
			curallheight = (curallheight<group->size().height()?group->size().height():curallheight);
		}
		if (curallwidth>widgetMax)
		{
			widgetMax = curallwidth;
		}
		if (curallheight>widgetMaxHeight)
		{
			widgetMaxHeight = curallheight;
		}
	}
	size.setWidth(widgetMax);
	size.setHeight(widgetMaxHeight);
	return size;
}
/**
* @brief  Ribbon::getcurMinSize 获取当前最小大小
* @return QT_NAMESPACE::QSize  
*/
QSize Ribbon:: getcurMinSize() {
	QSize size;
	{

	}
	return size;
}

/**
* @brief Ribbon::setScale
* @param QSize & size
* @param bool state
* @return void
*/
void Ribbon::setScale(QSize& size, bool state) {
	int curindex = QTabWidget::currentIndex();
	if (state)
	{
		for (auto index = 0; index < count(); index++)
			unFold(index, size);
	}
	else
	{
		for (auto index = 0; index < count(); index++)
			toScale(index, size);
	}
	QTabWidget::setCurrentIndex(curindex);
}
/**
* @brief  Ribbon::toScale 具体缩放
* @param  unsigned int index  
* @param  QSize & size  
* @return bool  
*/
bool Ribbon::toScale(unsigned int index,QSize& size)
{
	QTabWidget::setCurrentIndex(index);
	//收缩
	//step1:获取tab页
	QWidget* tab = QTabWidget::widget(index);
	//step2:获取各组件的大小
	PICRibbonTabContent* mtab = dynamic_cast<PICRibbonTabContent*>(tab);
	float widthmax = 0;
	std::vector<PICRibbonButtonGroup*> groups;
	for (auto groupindex=0;groupindex<mtab->contentLayout->count();groupindex++)
	{
		PICRibbonButtonGroup* groupbutton = dynamic_cast<PICRibbonButtonGroup*>
			(mtab->contentLayout->itemAt(groupindex)->widget());
		groups.push_back(groupbutton);
		qDebug() << groupbutton->size().width();
		widthmax += groupbutton->size().width();
	}
	//step3:检查大小差,判断是否需要收进抽屉
	if (size.width() - widthmax > 24)
		return false;
	//step4:开始收进抽屉
	for(int groupindex=groups.size()-1; groupindex >=0; groupindex--)
	{
		auto iter = mydarWer.find(groups[groupindex]->title());
		if (iter==mydarWer.end())
		{
			//step5:可以缩放
			QWidget* parent = reinterpret_cast<QWidget*>(MaindefStie);
			std::list<QAction*> mActions = groups[groupindex]->get_action_all().toStdList();
			//QList<QAction*> mActions = groups[groupindex]->get_action_all();
			PICRibbonButtonGroup* newgroup = new PICRibbonButtonGroup(parent);
			for (auto iteraction = mActions.begin(); iteraction != mActions.end(); iteraction++)
			{
				QToolButton* b = new QToolButton;
				b->setDefaultAction(*iteraction);
				newgroup->addButton(b);
			}
			newgroup->setMaximumSize(groups[groupindex]->size());
			newgroup->setTitle(groups[groupindex]->title());
			//step6:放入用来存储抽屉的表中
			mydarWer.insert(std::pair<QString,QWidget*>(groups[groupindex]->title(),newgroup));
			//step7:清除
			groups[groupindex]->removeButtons();
			//step8:插入抽屉按钮
			{
				QToolButton* darwerbutton = new QToolButton();
				QIcon icon(QString::fromUtf8(":/drawer/icons/darwer.svg"));
				QSize sizeicon(32,32);
				darwerbutton->setIcon(icon);
				darwerbutton->setMaximumSize(sizeicon);
				groups[groupindex]->addButton(darwerbutton);
				groups[groupindex]->setMaximumWidth(118);
				QObject::connect(darwerbutton,SIGNAL(clicked()),this,SLOT(buttomclicked()));
			}
			toScale(index,size);
			break;
		}
	}
	return true;
}


/**
* @brief Ribbon::unFold 展开
* @param unsigned int index tab页序号
* @param QSize & size 大小
* @return bool
*/
bool Ribbon::unFold(unsigned int index, QSize& size)
{
#if 0
	if (mydarWer.empty())
		return false;
	QWidget* tabwidget = QTabWidget::widget(index);
	PICRibbonTabContent* tabContent = dynamic_cast<PICRibbonTabContent*>(tabwidget);
#if 1
	PICRibbonButtonGroup* scaleWidget = nullptr;
	int allWidth = 0;
	bool istrue = false;
	for (int index = 0; index < tabContent->contentLayout->count(); index++)
	{
		PICRibbonButtonGroup* tempGroup = dynamic_cast<PICRibbonButtonGroup*>(
			tabContent->contentLayout->itemAt(index)->widget());
		auto iter= mydarWer.find(tempGroup->title());
		allWidth += tempGroup->width();
		if (iter!=mydarWer.end()&& !istrue)
		{
			scaleWidget = tempGroup;
			istrue = true;
		}
	}
	if (!scaleWidget)
		return false;
	allWidth -= scaleWidget->width();
	auto iter = mydarWer.find(scaleWidget->title());
	PICRibbonButtonGroup* mydarWerGroup = dynamic_cast<PICRibbonButtonGroup*>(iter->second);
	allWidth += mydarWerGroup->width();
	int distance = size.width() - allWidth;
	if (WIGET_INTERVAL * 2 >= distance)
		return false;
	int indexes= tabContent->getGroupIndex(mydarWerGroup);
	PICRibbonButtonGroup* newGroup = new PICRibbonButtonGroup;
	newGroup->setTitle(mydarWerGroup->title());
	std::list<QAction*> list = mydarWerGroup->get_action_all().toStdList();
	for (auto iteraction = list.begin(); iteraction != list.end();iteraction++)
	{
		QToolButton *b = new QToolButton;
		b->setDefaultAction(*iteraction);
		newGroup->addButton(b);
	}
	tabContent->SlotOnGroup(newGroup, indexes);
	mydarWer.erase(iter);
	return unFold(index,size);
#else 
	/********************************************************************************/
	//展开的组
	std::map<QString, PICRibbonButtonGroup*> groupsunfold;
	//存储的组
	std::map<QString, PICRibbonButtonGroup*>groupsstored;
	//开始遍历对应的group
	int allwidth = 0;
	for (auto index = 0; index < tabContent->contentLayout->count(); index++)
	{
		PICRibbonButtonGroup* group = dynamic_cast<PICRibbonButtonGroup*>(
			tabContent->contentLayout->itemAt(index)->widget());
		if (mydarWer.find(group->title()) != mydarWer.end())
		{
			groupsstored.insert(std::pair<QString, PICRibbonButtonGroup*>(group->title(), group));
		}
		else
		{
			groupsunfold.insert(std::pair<QString, PICRibbonButtonGroup*>(group->title(), group));
			allwidth += group->width();
		}
	}
	//展开的实现
	if (groupsstored.empty())
		return false;
	int stroedwidth = (groupsstored.begin())->second->width();
	int stroedCount = groupsstored.size() - 1;
	for (auto storediter = groupsstored.begin(); storediter != groupsstored.end(); storediter++)
	{
		//获取当前的折叠总大小
		int tabwidth = allwidth + stroedwidth*stroedCount;
		//获取当前被隐藏的组的大小并替换调当前被折叠组
		tabwidth += (mydarWer.find(storediter->first)->second->width());
		int distance = size.width() - tabwidth;
		if (WIGET_INTERVAL * 2 >= distance)
			continue;
		//这里开始替换
		PICRibbonButtonGroup* mydarwer1 = dynamic_cast<PICRibbonButtonGroup*>(mydarWer.find(storediter->first)->second);
		std::list<QAction*> actionlist = mydarwer1->get_action_all().toStdList();
		tabContent->removeGroup(storediter->first);
		for (auto iteraction = actionlist.begin(); iteraction != actionlist.end(); iteraction++)
		{
			QToolButton* b = new QToolButton;
			b->setDefaultAction(*iteraction);
			tabContent->addButton(storediter->first, b);
		}
		allwidth += mydarwer1->width();
		mydarWer.erase(mydarWer.find(storediter->first));
		stroedCount--;
	}
#endif
	return  true;
#endif
	//展开
	//step0:
	if (mydarWer.empty()) return true;
	//step1:设置当前页面
	QTabWidget::setCurrentIndex(index);
	//step2:获取tab页
	QWidget* tab = QTabWidget::widget(index);
	//step3:获取个组件的大小
	PICRibbonTabContent* mtab = dynamic_cast<PICRibbonTabContent*>(tab);
	std::vector<PICRibbonButtonGroup*> groups;
	float widthmax = 0;
	for (auto groupindex=0;groupindex<mtab->contentLayout->count();groupindex++)
	{
		PICRibbonButtonGroup* groupbutton = dynamic_cast<PICRibbonButtonGroup*>
			(mtab->contentLayout->itemAt(groupindex)->widget());
		groups.push_back(groupbutton);
		widthmax += groupbutton->size().width();
	}
	//step4:检查恢复控件后的大小
	for(auto iter=0;iter<groups.size();iter++)
	{
		auto iterdar = mydarWer.find(groups[iter]->title());
		if (iterdar!=mydarWer.end())
		{
			//step5:按顺序展开
			widthmax -= groups[iter]->size().width();
			PICRibbonButtonGroup* curgroup = dynamic_cast<PICRibbonButtonGroup*>(iterdar->second);
			widthmax += curgroup->size().width();
			if (widthmax<size.width())
			{
				groups[iter]->removeButtons();
				std::list<QAction*> actions = curgroup->get_action_all().toStdList();
				for (auto iteraction=actions.begin();iteraction!=actions.end();iteraction++)
				{
					QToolButton* b = new QToolButton();
					b->setDefaultAction(*iteraction);
					groups[iter]->addButton(b);
				}
				groups[iter]->setMaximumSize(iterdar->second->size());
				mydarWer.erase(iterdar);
				QWidget* mainwidget = reinterpret_cast<QWidget*>(MaindefStie);
				//mainwidget->setMaximumWidth(size.width()+24);
				unFold(index, size);
			}
			
			break;
		}
	}
	return true;
}
/**
* @brief  Ribbon::buttomclicked 按钮事件
* @return void  
*/
void Ribbon::buttomclicked()
{
	QToolButton* qtoolbutton = static_cast<QToolButton*>(QObject::sender());
	for (auto index = 0; index < count();index++)
	{
		QWidget* tab = QTabWidget::widget(index);
		PICRibbonTabContent* picribbontabcontent = dynamic_cast<PICRibbonTabContent*>(tab);
		for (auto subindex = 0; subindex < picribbontabcontent->contentLayout->count();subindex++)
		{
			PICRibbonButtonGroup* group = dynamic_cast<PICRibbonButtonGroup*>(picribbontabcontent->contentLayout->itemAt(subindex)->widget());
			auto btnCount = group->buttonCount();
			if (btnCount<=1)
			{
				if (QObject::sender()==group->gridLayout_btn->itemAt(0)->widget())
				{
					showdrawerGroup(group->title(),qtoolbutton);
					return;
				}
			}
		}
	}
}

/**
* @brief  Ribbon::showdrawerGroup
* @param  QString GroupName  
* @return void  
*/
void Ribbon::showdrawerGroup(QString GroupName,QToolButton* buttom)
{
	auto iter = mydarWer.find(GroupName);
	if (iter!=mydarWer.end())
	{
		PICRibbonButtonGroup* newGroup = dynamic_cast<PICRibbonButtonGroup*>(iter->second);
		if (newGroup->isVisible())
		{
			newGroup->hide();
		}
		else
		{
			newGroup->setWindowFlags(Qt::FramelessWindowHint);
			QPalette pal = newGroup->palette();
			pal.setColor(QPalette::Background, Qt::white);
			newGroup->setAutoFillBackground(true);
			newGroup->setPalette(pal);
			//移动
			{
				
				PICRibbonButtonGroup* group = dynamic_cast<PICRibbonButtonGroup*>(buttom->parent());
				if (!group)
				{
					std::cerr << "group is nullptr from void Ribbon::showdrawerGroup(QString GroupName,QToolButton* buttom)" << std::endl;
					return;
				}
				QWidget* mainWiget = reinterpret_cast<QWidget*>(MaindefStie);
				QPoint widgetPos = mainWiget->mapFromGlobal(mapToGlobal(group->pos()));
				QSize groupSize = group->size();
				QRect groupRect;
				groupRect.setLeft(widgetPos.x());
				groupRect.setTop(widgetPos.y());
				groupRect.setWidth(groupSize.width());
				groupRect.setHeight(groupSize.height());
				if (groupRect.center().x()+newGroup->size().width()>mainWiget->width())
				{
					QPoint centerPos;
					centerPos.setY(groupRect.center().y()+newGroup->size().height()/2);
					int distance = mainWiget->width() - (groupRect.center().x() + newGroup->size().width()) - WIGET_INTERVAL;
					centerPos.setX(groupRect.center().x()+distance);
					newGroup->move(centerPos);
				}
				else
				{
					QPoint centerPos;
					centerPos.setX(groupRect.center().x());
					centerPos.setY(groupRect.center().y() + newGroup->size().height() / 2);
					newGroup->move(centerPos);
				}
				QSize widgetSize = mainWiget->size();

			}
			newGroup->show();
		}
	}
	for (auto index = mydarWer.begin(); index != mydarWer.end(); index++)
	{
		PICRibbonButtonGroup* newGroup = dynamic_cast<PICRibbonButtonGroup*>(index->second);
		if (newGroup&&newGroup->isVisible()&&index!=iter)
		{
			newGroup->hide();
		}
	}
}

/**
* @brief Ribbon::setParentWidget
* @param MainWindowDef * parent
* @return void
*/
void Ribbon::setParentWidget(MainWindowDef* parent)
{
	MaindefStie = reinterpret_cast<unsigned __int64>(parent);
}