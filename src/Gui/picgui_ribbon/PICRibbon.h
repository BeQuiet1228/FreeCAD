#ifndef RIBBONTABWIDGET_H
#define RIBBONTABWIDGET_H

#include <QTabWidget>
#include <QToolButton>
#include "TabWidgetInterface.hpp"
#include "PICRibbonTabContent.h"

class GuiExport Ribbon : public TabWidgetInterFace
{
  Q_OBJECT
public:
  explicit Ribbon(QWidget *parent = 0);

  /// Add a tab to the ribbon.
  ///
  /// \param[in] tabName Name of the tab
  void addTab(const QString &tabName);

  /// Add a tab to the ribbon.
  ///
  /// \param[in] tabIcon Icon of the tab
  /// \param[in] tabName Name of the tab
  void addTab(const QIcon &tabIcon, const QString &tabName);

  /// Remove a tab from the ribbon.
  ///
  /// \param[in] tabName Name of the tab
  void removeTab(const QString &tabName);

  /// Add a group to the specified tab.
  /// The specified tab is created if it does not exist.
  ///
  /// \param[in] tabName Name of the tab
  /// \param[in] groupName Name of the group
  void addGroup(const QString &tabName, const QString &groupName);

  /// Add a button to the specified group.
  /// The specified group and tab are created if they do not exist.
  ///
  /// \param[in] tabName Name of the tab
  /// \param[in] groupName Name of the group
  /// \param[in] button The button
  void addButton(const QString &tabName, const QString &groupName, QToolButton *button);

  /// Remove a button from the specified group.
  /// Do nothing if the button, group or tab doesn't exist.
  /// The button group and tab are also removed if they become empty due to
  /// the removal of the button.
  ///
  /// \param[in] tabName Name of the tab
  /// \param[in] groupName Name of the group
  /// \param[in] button The button
  void removeButton(const QString &tabName, const QString &groupName, QToolButton *button);


  QList<PICRibbonTabContent *> get_tab_all();
  PICRibbonTabContent * get_tab_by_name(QString& name);
  virtual QSize getunfoldMinSize() override;
  virtual QSize getcurMinSize() override;

  //添加一个action
  void addAction(const QString& tabName, const QString& groupName, QAction* action);
  //清理掉所有的action
  void clearAllAction();
  //清理掉一个tab 包括下面的组、和action-+
  void clearTab(const QString& tabName);
  //清理掉一个组以及下面的action
  void clearGoup(const QString& groupName);
  //获取所有tab的名字
  QList<QString> getTabs();
  //获取所有组的名字
  QList<QString> getGroups();
  //获取特定tab下组的名字
  QList<QString> getGroup(const QString& tabName);
  //获取所有的action
  QList<QAction*> getActions();
  //获取某个tab下所有的action
  QList<QAction*> getTabActions(const QString& tabName);
  //获取某个group下所有的action
  QList<QAction*> getGroupActions(const QString& groupName);
  /*
  改变tab位置，如果older超出最大范围将tab放置到最后。
  如果tab不存在，不做操作。
  */
  virtual void  setTabOlder(const QString& tabName, const int older);
  //判断是否已有该action
  virtual bool hasAction(const QAction* action);

  //1.15 WDT_QL新增接口
  //改变一个分组位置,sequence参数为新的位置,最小为0
  void setGroupSequence(const QString &tabName, const QString &groupName, int sequence);

};

#endif // RIBBONTABWIDGET_H
