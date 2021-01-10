#ifndef RIBBONBUTTONGROUP_H
#define RIBBONBUTTONGROUP_H

#include <QWidget>
#include <QToolButton>
#include <QPaintEvent>
namespace Ui {
class PICRibbonButtonGroup;
}

class GuiExport PICRibbonButtonGroup : public QWidget
{
  Q_OBJECT

public:
  explicit PICRibbonButtonGroup(QWidget *parent = 0);
  virtual ~PICRibbonButtonGroup();

  /// Set the title of the button group.
  /// The title is shown underneath the buttons.
  ///
  /// \param[in] title The title
  void setTitle(const QString &title);

  /// Get the title of the button group.
  ///
  /// \return The title
  QString title() const;

  /// Get the number of buttons in the button group.
  ///
  /// \return The number of buttons
  int buttonCount() const;

  /// Add a button to the group.
  ///
  /// \param[in] button The button
  void addButton(QToolButton *button);

  /// Remove a button from the group.
  ///
  /// \param[in] button The button
  void removeButton(QToolButton *button);
  QList<QAction*> get_action_all();
protected:
	void paintEvent(QPaintEvent *event);
private:
  Ui::PICRibbonButtonGroup *ui;
  QString m_title; ///< Title of the button group
};

#endif // RIBBONBUTTONGROUP_H
