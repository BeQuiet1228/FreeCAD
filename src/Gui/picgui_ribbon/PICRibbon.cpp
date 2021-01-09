#include "PreCompiled.h"
#include "PICRibbon.h"
#include "PICRibbonTabContent.h"

#include <QApplication>
#include <QStyleOption>
#include <QPainter>
#include "picgui_ribbon/moc_PICRibbon.cpp"
Ribbon::Ribbon(QWidget *parent)
  : QTabWidget(parent)
{

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









void Ribbon::addAction(const QString &tabName, const QString &groupName, QAction *action)
{
	QToolButton *b = new QToolButton;
	b->setDefaultAction(action);
	this->addButton(tabName, groupName, b);
}

void Ribbon::clearAllAction()
{
	for (int i = 0; i < count(); i++)
	{
		QWidget *tab = QTabWidget::widget(i);
		QTabWidget::removeTab(i);
		delete tab;
	}
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






