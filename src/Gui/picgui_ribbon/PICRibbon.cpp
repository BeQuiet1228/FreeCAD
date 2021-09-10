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
#define DEBUGINNG 0
Ribbon::Ribbon(QWidget *parent)
  : QTabWidget(parent)
{
	mydarWer.clear();
	setCursor(Qt::ArrowCursor);
	QTabWidget* widget = dynamic_cast<QTabWidget*>(this);
	QObject::connect(widget, SIGNAL(currentChanged(int)), this, SLOT(SlotcurrentChanged(int)));
	timer = new QTimer(this);
	QObject::connect(timer,SIGNAL(timeout()),this,SLOT(slotTimerOut()));
	timer->start(300);
}

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
#if DEBUGINNG
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
#else
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
#endif
}

void Ribbon::addButton(const QString &tabName, const QString &groupName, QToolButton *button)
{
  // Find ribbon tab
#if DEBUGINNG
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
#else
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
	}
	else if (tab!=nullptr && !isbreak)
	{
		delete tab;
		mTabWidget.erase(iter);
		auto iterDarwer = mMyDarWer.find(tabName);
		if (iterDarwer != mMyDarWer.end())
		{
			mMyDarWer.erase(mMyDarWer.find(tabName));
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
#endif
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
void Ribbon::addAction(const QString &tabName, const QString &groupName, QAction *action)
{
	QToolButton *b = new QToolButton;
	b->setDefaultAction(action);
	this->addButton(tabName, groupName, b);
}

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
}

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


void Ribbon::setTabOlder(const QString &tabName, const int older)
{
	QString name_t = tabName;
	PICRibbonTabContent * t = get_tab_by_name(name_t);
	QTabWidget::insertTab(older, t, name_t);
}

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
* @brief Ribbon::setScale
* @param QSize & size
* @param bool state
* @return void
*/
void Ribbon::setScale(QSize& size, bool state) {
	int curindex = QTabWidget::currentIndex();
	if (state)
	{
	//	//for (auto index = 0; index < count(); index++)
	//	//	unFold(index, size);
		unFold(curindex, size);
	}
	else
	{
	//	//for (auto index = 0; index < count(); index++)
	//	//	toScale(index, size);
		toScale(curindex, size);
	}
	//QTabWidget::setCurrentIndex(curindex);
}
/**
* @brief  Ribbon::toScale 具体缩放
* @param  unsigned int index  
* @param  QSize & size  
* @return bool  
*/
bool Ribbon::toScale(unsigned int index,QSize& size)
{
	HidemyDar();
	//收缩
	//step1:获取tab页
	QString tabName = QTabWidget::tabText(index);
	auto iter = mTabWidget.find(tabName);
	if (iter == mTabWidget.end()) return false;
	//step2:获取各组件的大小
	//PICRibbonTabContent* mtab = dynamic_cast<PICRibbonTabContent*>(tab);
	PICRibbonTabContent* mtab = dynamic_cast<PICRibbonTabContent*>(iter->second);
	float widthmax = 0;
	std::vector<PICRibbonButtonGroup*> groups;
	for (auto groupindex=0;groupindex<mtab->contentLayout->count();groupindex++)
	{
		PICRibbonButtonGroup* groupbutton = dynamic_cast<PICRibbonButtonGroup*>
			(mtab->contentLayout->itemAt(groupindex)->widget());
		groups.push_back(groupbutton);
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
			PICRibbonButtonGroup* newgroup = new PICRibbonButtonGroup(parent);
			for (auto iteraction = mActions.begin(); iteraction != mActions.end(); iteraction++)
			{
				QToolButton* b = new QToolButton;
				b->setDefaultAction(*iteraction);
				newgroup->addButton(b);
			}
			//QSize size = groups[groupindex]->size();
			//newgroup->setMaximumSize(groups[groupindex]->size());
			newgroup->resize(groups[groupindex]->size());
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
				//groups[groupindex]->setMaximumWidth(118);
				groups[groupindex]->resize(QSize(118,101));
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
	//step0:
	if (mydarWer.empty()) return true;
	//关闭相关的抽屉
	HidemyDar();
	//step1:设置当前页面
	//QTabWidget::setCurrentIndex(index);
	//step2:获取tab页
	//QWidget* tab = QTabWidget::widget(index);
	QString tabName = QTabWidget::tabText(index);
	auto iter = mTabWidget.find(tabName);
	if (iter == mTabWidget.end()) return false;
	//step3:获取个组件的大小
	PICRibbonTabContent* mtab = dynamic_cast<PICRibbonTabContent*>(iter->second);
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
		//QWidget* tab = QTabWidget::widget(index);
		QString tabName = QTabWidget::tabText(index);
		auto iter = mTabWidget.find(tabName);
		PICRibbonTabContent* picribbontabcontent = dynamic_cast<PICRibbonTabContent*>(iter->second);
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
	//auto iter = mydarWer.find(GroupName);
	QString tabName = QTabWidget::tabText(QTabWidget::currentIndex());
	auto iter = mMyDarWer[tabName].find(GroupName);
	if (iter!=mMyDarWer[tabName].end())
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
			pal.setColor(QPalette::Background, QColor(189,193,196,255));
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
	for (auto index = mMyDarWer[tabName].begin(); index != mMyDarWer[tabName].end(); index++)
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

	//调整收缩
	//toScale(index, this->size());
	//setZoominfo(index,this->size());
}
/**
* @brief Ribbon::HidemyDar 隐藏抽屉
* @return void
* @Time 2021/7/29
*/
void Ribbon::HidemyDar()
{
	if (mMyDarWer.empty())	return;
	for(auto iter=mMyDarWer.begin();iter!=mMyDarWer.end();iter++)
	{
		for (auto iter2 = iter->second.begin(); iter2 != iter->second.end(); iter2++)
		{
			iter2->second->hide();
		}
	}
}
void Ribbon::setZoominfo(unsigned int index, QSize& size)
{
	//step1:先全部展开
	QString tabName = QTabWidget::tabText(index);
	auto iter = mTabWidget.find(tabName);
	if (iter == mTabWidget.end())	return;
	PICRibbonTabContent* tab = dynamic_cast<PICRibbonTabContent*>(iter->second);
	for (int i=0;i<tab->contentLayout->count();i++)
	{
		PICRibbonButtonGroup* group = dynamic_cast<PICRibbonButtonGroup*>
			(tab->contentLayout->itemAt(i)->widget());
		auto iter = mydarWer.find(group->title());
		if (iter == mydarWer.end()) continue;
		group->removeButtons();
		std::list<QAction*> actions=dynamic_cast<PICRibbonButtonGroup*>
			(iter->second)->get_action_all().toStdList();
		for (auto iteraction=actions.begin();iteraction!=actions.end();iteraction++)
		{
			QToolButton* b = new QToolButton();
			b->setDefaultAction(*iteraction);
			group->addButton(b);
		}
		mydarWer.erase(iter);
	}
	//step2:收缩
	//toScale(index, size);
}
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
			if (386 == groupButton->size().width())
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
				if (itdarwer != mMyDarWer[tabName].end())
				{
					mtabItemSize = mtabItemSize - (*iterItem)->size().width();
					mtabItemSize = mtabItemSize + itdarwer->second->size().width();
					if (parentSize.width() > mtabItemSize)
					{
						(*iterItem)->removeButtons();
						PICRibbonButtonGroup* curGroup = dynamic_cast<PICRibbonButtonGroup*>(itdarwer->second);
						std::list<QAction*> mActions = curGroup->get_action_all().toStdList();
						for (auto itAction=mActions.begin();itAction!=mActions.end();itAction++)
						{
							QToolButton* b = new QToolButton();
							b->setDefaultAction(*itAction);
							(*iterItem)->addButton(b);
						}
						(*iterItem)->setMaximumWidth(curGroup->size().width());
						mMyDarWer[tabName].erase(itdarwer);
						isreturn = true;
					}
				}
			}
			if (isreturn)
				HidemyDar();
		}
		else if (parentSize.width() < mtabItemSize)
		{
			bool isreturn = false;
			for (int groupIndex = groups.size() - 1; groupIndex >= 0; --groupIndex)
			{
				auto iter = mMyDarWer[tabName].find(groups[groupIndex]->title());
				if (iter == mMyDarWer[tabName].end())
				{
					//可以缩放
					std::list<QAction*> mActions = groups[groupIndex]->get_action_all().toStdList();
					PICRibbonButtonGroup* newGroup = new PICRibbonButtonGroup(parent);
					for (auto itAction = mActions.begin(); itAction != mActions.end(); itAction++)
					{
						QToolButton* b = new QToolButton;
						b->setDefaultAction(*itAction);
						newGroup->addButton(b);
					}
					newGroup->resize(groups[groupIndex]->size());
					newGroup->setTitle(groups[groupIndex]->title());
					mMyDarWer[tabName][groups[groupIndex]->title()] = dynamic_cast<QWidget*>(newGroup);
					mtabItemSize = mtabItemSize - groups[groupIndex]->size().width();
					mtabItemSize = mtabItemSize + 118;
					groups[groupIndex]->removeButtons();
					//插入抽屉按钮
					{
						QToolButton* darwerButton = new QToolButton();
						QIcon icon(QString::fromUtf8(":/drawer/icons/darwer.svg"));
						QSize sizeicon(32,32);
						darwerButton->setIcon(icon);
						darwerButton->setMaximumSize(sizeicon);
						groups[groupIndex]->addButton(darwerButton);
						groups[groupIndex]->resize(118,101);
						QObject::connect(darwerButton,SIGNAL(clicked()),this,SLOT(buttomclicked()));
					}
					if (parentSize.width() > mtabItemSize)
						break;
				}
			}
			HidemyDar();
			if (groups.size() == mMyDarWer[tabName].size())
			{
				parent->setMinimumWidth(groups.size() * 118+100);
			}
		}
	}
}