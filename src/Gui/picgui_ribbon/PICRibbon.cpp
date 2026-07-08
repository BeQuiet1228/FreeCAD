#include "PreCompiled.h"
#include "PICRibbon.h"
#include "PICRibbonTabContent.h"
#include "PICRibbonButtonGroup.h"

#include <QApplication>
#include <QStyleOption>
#include <QPainter>
#include "picgui_ribbon/moc_PICRibbon.cpp"
#include <iostream>
#include <QMenu>
#include"darWer.h"
#define DEBUGINNG 0
#ifndef WIGET_INTERVAL
#define WIGET_INTERVAL (30)
#endif
#ifndef NO_INSTANCE
#define NO_INSTANCE (386)
#endif
#ifndef DARWER_SIZE
#define DARWER_SIZE (118)
#endif
#ifndef TIME_OUT
#define TIME_OUT (200)
#endif

Ribbon::Ribbon(QWidget *parent)
  : QTabWidget(parent)
{
	setCursor(Qt::ArrowCursor);
	QTabWidget* widget = dynamic_cast<QTabWidget*>(this);
	QObject::connect(widget, SIGNAL(currentChanged(int)), this, SLOT(SlotcurrentChanged(int)));
	timer = new QTimer(this);
	QObject::connect(timer,SIGNAL(timeout()),this,SLOT(slotTimerOut()));
	timer->start(TIME_OUT);
}

/**
* @brief Ribbon::addTab 添加Tab页
* @param const QString & tabName 
* @return void
*/
void Ribbon::addTab(const QString &tabName)
{
  // Note: superclass QTabWidget also has a function addTab()
#if DEBUGINNG
  PICRibbonTabContent *ribbonTabContent = new PICRibbonTabContent;
  QTabWidget::addTab(ribbonTabContent, tabName);
  this->setAttribute(Qt::WA_StyledBackground);
#else
//step1:创建窗口
	PICRibbonTabContent* ribbonTabContent = new PICRibbonTabContent;
	mTabWidget.insert(std::pair<QString, QWidget*>(tabName,ribbonTabContent));
	int mcount = count();
	QTabWidget::addTab(new QWidget(),tabName);
	//qDebug()<<tabName;
	mcount = count();
	this->setAttribute(Qt::WA_StyledBackground);
#endif
}

/**
* @brief Ribbon::addTab
* @param const QIcon & tabIcon
* @param const QString & tabName
* @return void
*/
void Ribbon::addTab(const QIcon &tabIcon, const QString &tabName)
{
  //Note: superclass QTabWidget also has a function addTab()
  
#if DEBUGINNG
  PICRibbonTabContent *ribbonTabContent = new PICRibbonTabContent;
  QTabWidget::addTab(ribbonTabContent, tabIcon, tabName);
#else
  //step1:创建窗口
	PICRibbonTabContent* ribbonTabContent = new PICRibbonTabContent;
	mTabWidget.insert(std::pair<QString, QWidget*>(tabName,ribbonTabContent));
	QTabWidget::addTab(new QWidget, tabIcon, tabName);
#endif
}

/**
* @brief Ribbon::removeTab 移除tab页
* @param const QString & tabName
* @return void
*/
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

/**
* @brief Ribbon::addGroup 添加组
* @param const QString & tabName
* @param const QString & groupName
* @return void
*/
void Ribbon::addGroup(const QString &tabName, const QString &groupName)
{
  // Find ribbon tab

	QWidget* tab = nullptr;
	auto iter = mTabWidget.find(tabName);
	if (iter!=mTabWidget.end())
		tab = iter->second;
	if (tab!=nullptr)
	{
		PICRibbonTabContent* ribbonTabContent = dynamic_cast<PICRibbonTabContent*>(tab);
		ribbonTabContent->addGroup(groupName);
	}
	else
	{
		addTab(tabName);
		addGroup(tabName,groupName);
	}
}

/**
* @brief Ribbon::addButton 添加按钮
* @param const QString & tabName
* @param const QString & groupName
* @param QToolButton * button
* @return void
*/
void Ribbon::addButton(const QString &tabName, const QString &groupName, QToolButton *button)
{
	//先全部展开
	timer->stop();
	//Find ribbon tab
	bool isbreak = false;
	for (int i = 0; i < count(); i++)
	{
		if (tabText(i).toLower() == tabName.toLower())
		{
			isbreak = true;
			break;
		}
	}
	QWidget* tab = nullptr;
	auto iter = mTabWidget.find(tabName);
	if (iter!=mTabWidget.end())
		tab = iter->second;
	if (tab!=nullptr && isbreak)
	{ 
		PICRibbonTabContent* ribbonTabContent = dynamic_cast<PICRibbonTabContent*>(tab);
		ribbonTabContent->addButton(groupName, button);
		timer->start(TIME_OUT);
	}
	else if (tab!=nullptr && !isbreak)
	{
		delete tab;
		mTabWidget.erase(iter);
		auto iterDarwer = mMyDarWer.find(tabName);
		if (iterDarwer != mMyDarWer.end())
		{
			mMyDarWer.erase(mMyDarWer.find(tabName));
			qToolButtons.erase(qToolButtons.find(tabName));
		}
		tab = nullptr;
		addTab(tabName);
		addButton(tabName, groupName, button);
	}
	else
	{
		addTab(tabName);
		addButton(tabName, groupName, button);
	}
}

/**
* @brief Ribbon::removeButton 移除按钮
* @param const QString & tabName
* @param const QString & groupName
* @param QToolButton * button
* @return void
*/
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


/**
* @brief Ribbon::get_tab_all 获取tab列表
* @return QT_NAMESPACE::QList<PICRibbonTabContent *>
*/
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

/**
* @brief Ribbon::get_tab_by_name 通过title查询tab页
* @param QString & name
* @return PICRibbonTabContent *
*/
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
* @brief Ribbon::addAction
* @param const QString & tabName
* @param const QString & groupName
* @param QAction * action
* @return void
*/
void Ribbon::addAction(const QString &tabName, const QString &groupName, QAction *action)
{
	QToolButton *b = new QToolButton;
	if (action->menu()) {
		b->setText(action->text());
		b->setIcon(action->icon());
		b->setToolTip(action->toolTip());
		b->setStatusTip(action->statusTip());
		b->setMenu(action->menu());
		b->setPopupMode(QToolButton::InstantPopup);
		b->setProperty("RibbonButtonSize", action->property("RibbonButtonSize"));
	}
	else {
		b->setDefaultAction(action);
		b->setProperty("RibbonButtonSize", action->property("RibbonButtonSize"));
	}
	this->addButton(tabName, groupName, b);
}
/**
* @brief Ribbon::clearAllAction 清除所有行动
* @return void
*/
void Ribbon::clearAllAction()
{
	this->clear();
}
/**
* @brief Ribbon::clearTab
* @param const QString & tabName
* @return void
*/
void Ribbon::clearTab(const QString &tabName)
{
	QString name_t = tabName;
	PICRibbonTabContent * t = get_tab_by_name(name_t);
	QList<QString> list_g_name = this->getGroup(name_t);
	for (int i = 0; i<list_g_name.count(); i++) {
		t->removeGroup(list_g_name.at(i));
	}
}
/**
* @brief Ribbon::clearGoup
* @param const QString & groupName
* @return void
*/
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
}
/**
* @brief Ribbon::getTabs
* @return QT_NAMESPACE::QList<QString>
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
* @brief Ribbon::getGroups
* @return QT_NAMESPACE::QList<QString>
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
* @brief Ribbon::getGroup
* @param const QString & tabName
* @return QT_NAMESPACE::QList<QString>
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
* @brief Ribbon::getActions
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
* @brief Ribbon::getTabActions
* @param const QString & tabName
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
* @brief Ribbon::setTabOlder
* @param const QString & tabName
* @param const int older
* @return void
*/
void Ribbon::setTabOlder(const QString &tabName, const int older)
{
	QString name_t = tabName;
	PICRibbonTabContent * t = get_tab_by_name(name_t);
	QTabWidget::insertTab(older, t, name_t);
}

/**
* @brief Ribbon::hasAction
* @param const QAction * action
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
* @brief  Ribbon::buttomclicked 按钮事件
* @return void  
*/
void Ribbon::buttomclicked()
{
	//HidemyDar();
	hidebtn();
	QToolButton* qtoolbutton = static_cast<QToolButton*>(QObject::sender());
	for(auto index=qToolButtons.begin();index!=qToolButtons.end();index++)
		for (auto subIndex = index->second.begin(); subIndex != index->second.end(); subIndex++)
		{
			if (subIndex->second == qtoolbutton)
			{
				showdrawerGroup(subIndex->first,subIndex->second);
				return;
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
	//auto iter = mydarWer.find(GroupName);
	QString tabName = QTabWidget::tabText(QTabWidget::currentIndex());
	auto iter = mMyDarWer[tabName].find(GroupName);
	if (iter!=mMyDarWer[tabName].end())
	{
		//PICRibbonButtonGroup* newGroup = dynamic_cast<PICRibbonButtonGroup*>(iter->second);
		darWer* newGroup = dynamic_cast<darWer*>(iter->second);
		if (newGroup->isVisible())
		{
			newGroup->hide();
		}
		else
		{
			QIcon icon(QString::fromUtf8(":/drawer/icons/zhankai.svg"));
			buttom->setIcon(icon);
			//newGroup->setWindowFlags(Qt::FramelessWindowHint);
			//QPalette pal = newGroup->palette();
			//pal.setColor(QPalette::Background, QColor(189,193,190,250));
			newGroup->setAutoFillBackground(true);
			//newGroup->setPalette(pal);
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
					centerPos.setY(groupRect.center().y()+buttom->size().height()*2);
					//int distance = mainWiget->width() - (groupRect.center().x() + newGroup->size().width()) - WIGET_INTERVAL;
					//centerPos.setX(groupRect.center().x()+distance);
					centerPos.setX(mainWiget->width()-newGroup->width());
					newGroup->move(centerPos);
				}
				else
				{
					QPoint groupCenterPos = groupRect.center();
					QPoint centerPos;
					centerPos.setX(groupRect.center().x());
					//centerPos.setY(groupRect.center().y() + newGroup->size().height() / 2);
					centerPos.setY(groupRect.center().y()+buttom->size().height()*2);
					newGroup->move(centerPos);
				}
				QSize widgetSize = mainWiget->size();

			}
			newGroup->show();
		}
	}
	for (auto index = mMyDarWer[tabName].begin(); index != mMyDarWer[tabName].end(); index++)
	{
		//PICRibbonButtonGroup* newGroup = dynamic_cast<PICRibbonButtonGroup*>(index->second);
		darWer* newGroup = dynamic_cast<darWer*>(index->second);
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

/**
* @brief Ribbon::SlotcurrentChanged tab切换页面的槽函数
* @param int index
* @return void
* @Time 2021/7/29
*/
void Ribbon::SlotcurrentChanged(int index)
{
	HidemyDar();
	//step1:切换窗口，将对应的窗口装入tab
	QString tabName = QTabWidget::tabText(index);
	auto iter = mTabWidget.find(tabName);
	if (iter == mTabWidget.end())	return;
	PICRibbonTabContent* tab = dynamic_cast<PICRibbonTabContent*>(iter->second);
	QTabWidget* mtabwidget = dynamic_cast<QTabWidget*>(this);
	QWidget* mwidget = mtabwidget->widget(index);
	tab->setParent(mwidget);
	tab->show();
	tab->resize(QSize(167255,101));
}
/**
* @brief Ribbon::HidemyDar 隐藏抽屉
* @return void
* @Time 2021/7/29
*/
void Ribbon::HidemyDar()
{
	hideDar();
	hidebtn();
}
/**
* @brief Ribbon::slotTimerOut 定时触发函数,用于实现抽屉功能
* @return void
*/
void Ribbon::slotTimerOut()
{
	if (QObject::sender() == timer)
	{
		QWidget* parent = reinterpret_cast<QWidget*>(MaindefStie);
		QSize parentSize = parent->size();
		//step1:获取当前tab页
		int index = QTabWidget::currentIndex();
		QString tabName = QTabWidget::tabText(QTabWidget::currentIndex());
		auto itTab = mTabWidget.find(tabName);
		if (itTab == mTabWidget.end())return;
		PICRibbonTabContent* mTab = dynamic_cast<PICRibbonTabContent*>(itTab->second);
		if (nullptr == mTab)
			return;
		//step2:获取当前tab的大小
		float mtabItemSize = 0.0f;
		std::vector<PICRibbonButtonGroup*> groups;
		for (auto groupIndex=0;groupIndex<mTab->contentLayout->count();groupIndex++)
		{
			PICRibbonButtonGroup* groupButton = dynamic_cast<PICRibbonButtonGroup*>
				(mTab->contentLayout->itemAt(groupIndex)->widget());
			groups.push_back(groupButton);
			if (NO_INSTANCE == groupButton->size().width())
				return;
			mtabItemSize += groupButton->size().width();
		}
		//step3:检查大小差值
		if (parentSize.width() > mtabItemSize)
		{
			bool isreturn = false;
			auto itDar = mMyDarWer.find(tabName);
			if (itDar == mMyDarWer.end())return;
			for(auto iterItem=groups.begin();iterItem!=groups.end();iterItem++)
			{
				auto itdarwer=mMyDarWer[tabName].find((*iterItem)->title());
				auto itBtn = qToolButtons[tabName].find((*iterItem)->title());
				if (itdarwer != mMyDarWer[tabName].end())
				{
					mtabItemSize = mtabItemSize - (*iterItem)->size().width();
					darWer* mDarWer = dynamic_cast<darWer*>(itdarwer->second);
					mtabItemSize = mtabItemSize + mDarWer->getSize().width();
					if (parentSize.width() > mtabItemSize)
					{
						isreturn = true;
						hideDar();
						qToolButtons[tabName].erase(itBtn);
						(*iterItem)->removeButtons();
						std::list<QAction*> mActions = mDarWer->get_action_all().toStdList();
						for (auto itAction=mActions.begin();itAction!=mActions.end();itAction++)
						{
							QToolButton* b = new QToolButton();
							b->setDefaultAction(*itAction);
							(*iterItem)->addButton(b);
						}
						(*iterItem)->setMaximumWidth(mDarWer->getSize().width());
						mMyDarWer[tabName].erase(itdarwer);
					}
				}
			}
			if (isreturn) hidebtn();
		}
		else if (parentSize.width() < mtabItemSize)
		{
			bool isreturn = false;
			for (int groupIndex = groups.size() - 1; groupIndex >= 0; --groupIndex)
			{
				auto iter = mMyDarWer[tabName].find(groups[groupIndex]->title());
				if (iter == mMyDarWer[tabName].end())
				{
					HidemyDar();
					//可以缩放
					std::list<QAction*> mActions = groups[groupIndex]->get_action_all().toStdList();
					//PICRibbonButtonGroup* newGroup = new PICRibbonButtonGroup(parent);
					darWer* newGroup = new darWer(parent);
					for (auto itAction = mActions.begin(); itAction != mActions.end(); itAction++)
					{
						QToolButton* b = new QToolButton;
						b->setDefaultAction(*itAction);
						newGroup->addButton(b);
					}
					//newGroup->resize(groups[groupIndex]->size());
					newGroup->setSize(groups[groupIndex]->size());
					newGroup->setTitle(groups[groupIndex]->title());
					newGroup->resize(DARWER_SIZE+10,30*mActions.size()+5);
					mMyDarWer[tabName][groups[groupIndex]->title()] = dynamic_cast<QWidget*>(newGroup);
					mtabItemSize = mtabItemSize - groups[groupIndex]->size().width();
					mtabItemSize = mtabItemSize + DARWER_SIZE;
					groups[groupIndex]->removeButtons();
					//插入抽屉按钮
					{
						QToolButton* darwerButton = new QToolButton();
						QIcon icon(QString::fromUtf8(":/drawer/icons/shousuo.svg"));
						QSize sizeicon(32,32);
						darwerButton->setIcon(icon);
						darwerButton->setMaximumSize(sizeicon);
						groups[groupIndex]->addButton(darwerButton);
						groups[groupIndex]->resize(DARWER_SIZE,101);
						qToolButtons[tabName][groups[groupIndex]->title()] = darwerButton;
						QObject::connect(darwerButton,SIGNAL(clicked()),this,SLOT(buttomclicked()));
					}
					if (parentSize.width() > mtabItemSize)
						break;
				}
			}
			if (groups.size() == mMyDarWer[tabName].size())
			{
				parent->setMinimumWidth(groups.size() * DARWER_SIZE +100);
			}
		}
	}
}
Ribbon::~Ribbon()
{
	mTabWidget.clear();
	mMyDarWer.clear();
	timer->stop();
}

/**
* @brief Ribbon::hideDar 隐藏抽屉
* @return void
*/
void Ribbon::hideDar(){
	if (mMyDarWer.empty())	return;
	for (auto iter = mMyDarWer.begin(); iter != mMyDarWer.end(); iter++)
	{
		for (auto iter2 = iter->second.begin(); iter2 != iter->second.end(); iter2++)
		{
			if (iter2->second->isVisible())
			{
				auto tabWidget = mTabWidget.find(iter->first);

				iter2->second->hide();
			}
		}
	}
}
/**
* @brief Ribbon::hidebtn 隐藏按钮
* @return void
*/
void Ribbon::hidebtn(){
	for (auto index = qToolButtons.begin(); index != qToolButtons.end(); index++)
		for (auto subIndex = index->second.begin(); subIndex != index->second.end(); subIndex++)
		{
			QIcon icon(QString::fromUtf8(":/drawer/icons/shousuo.svg"));
			subIndex->second->setIcon(icon);
		}
}
