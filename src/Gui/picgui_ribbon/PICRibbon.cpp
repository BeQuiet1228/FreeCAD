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
  // Determine default colors
  QColor bg = qApp->palette().color(QPalette::Background);
  QColor mid = qApp->palette().color(QPalette::Mid);

  // Note: the order in which the background/palette/stylesheet functions are
  // called does matter. Should be same as in Qt designer.
  setAutoFillBackground(true);


  // Set background color
  QPalette pal = palette();
  QColor qcolor = QColor(7,7,7);
  pal.setColor(QPalette::Background, qcolor);
  setPalette(pal);
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
