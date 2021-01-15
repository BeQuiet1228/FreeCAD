#ifndef RIBBONTABCONTENT_H
#define RIBBONTABCONTENT_H

#include <QWidget>
#include <QToolButton>
#include "PICRibbonButtonGroup.h"
#include <QPaintEvent>
namespace Ui {
class PICRibbonTabContent;
}

class GuiExport PICRibbonTabContent : public QWidget
{
  Q_OBJECT

public:
  explicit PICRibbonTabContent(QWidget *parent = 0);
  virtual ~PICRibbonTabContent();

  /// Add a group to the tab content.
  ///
  /// \param[in] groupName Name of the group
  void addGroup(const QString &groupName);

  /// Remove a group from the tab content.
  ///
  /// \param[in] groupName Name of the group
  void removeGroup(const QString &groupName);

  /// Get the number of button groups in this tab content.
  ///
  /// \return The number of button groups
  int groupCount() const;

  /// Add a button to the specified group.
  /// The group is created if it does not exist.
  ///
  /// \param[in] groupName Name of the group
  /// \param[in] button The button
  void addButton(const QString &groupName, QToolButton *button);

  /// Remove a button from the specified group.
  /// The group is also removed if it's empty.
  ///
  /// \param[in] groupName Name of the group
  /// \param[in] button The button
  void removeButton(const QString &groupName, QToolButton *button);
  QList<PICRibbonButtonGroup *> get_group_all();

  //1.15WDT_QL新增函数

  //新增分组
  void addGroup(PICRibbonButtonGroup *group);

  //清除TabContent下的所有分组
  void clearGroups();

protected:
	void paintEvent(QPaintEvent *event);
private:
  Ui::PICRibbonTabContent *ui;
};

#endif // RIBBONTABCONTENT_H
