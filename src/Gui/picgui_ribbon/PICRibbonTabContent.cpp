#include "PreCompiled.h"
#include "PICRibbonTabContent.h"
#include "ui_PICRibbonTabContent.h"
#include "PICRibbonButtonGroup.h"
#include "picgui_ribbon/moc_PICRibbonTabContent.cpp"
PICRibbonTabContent::PICRibbonTabContent(QWidget *parent)
  : QWidget(parent)
  , ui(new Ui::PICRibbonTabContent)
{
  ui->setupUi(this);
}

PICRibbonTabContent::~PICRibbonTabContent()
{
  delete ui;
}

void PICRibbonTabContent::addGroup(const QString &groupName)
{
  PICRibbonButtonGroup *ribbonButtonGroup = new PICRibbonButtonGroup;
  ribbonButtonGroup->setTitle(groupName);

  ui->ribbonHorizontalLayout->addWidget(ribbonButtonGroup);
}

void PICRibbonTabContent::removeGroup(const QString &groupName)
{
  // Find ribbon group
  for (int i = 0; i < ui->ribbonHorizontalLayout->count(); i++)
  {
    PICRibbonButtonGroup *group = static_cast<PICRibbonButtonGroup*>(ui->ribbonHorizontalLayout->itemAt(i)->widget());
    if (group->title().toLower() == groupName.toLower())
    {
      ui->ribbonHorizontalLayout->removeWidget(group); /// \todo :( No effect
      delete group;
      break;
    }
  }

  /// \todo  What if the group still contains buttons? Delete manually?
  // Or automaticly deleted by Qt parent() system.
}

int PICRibbonTabContent::groupCount() const
{
  return ui->ribbonHorizontalLayout->count();
}

void PICRibbonTabContent::addButton(const QString &groupName, QToolButton *button)
{
  // Find ribbon group
  PICRibbonButtonGroup *ribbonButtonGroup = nullptr;
  for (int i = 0; i < ui->ribbonHorizontalLayout->count(); i++)
  {
    PICRibbonButtonGroup *group = static_cast<PICRibbonButtonGroup*>(ui->ribbonHorizontalLayout->itemAt(i)->widget());
    if (group->title().toLower() == groupName.toLower())
    {
      ribbonButtonGroup = group;
      break;
    }
  }

  if (ribbonButtonGroup != nullptr)
  {
    // Group found
    // Add ribbon button
    ribbonButtonGroup->addButton(button);
  }
  else
  {
    // Group not found
    // Add ribbon group
    addGroup(groupName);

    // Add ribbon button
    addButton(groupName, button);
  }
}

void PICRibbonTabContent::removeButton(const QString &groupName, QToolButton *button)
{
  // Find ribbon group
  PICRibbonButtonGroup *ribbonButtonGroup = nullptr;
  for (int i = 0; i < ui->ribbonHorizontalLayout->count(); i++)
  {
    PICRibbonButtonGroup *group = static_cast<PICRibbonButtonGroup*>(ui->ribbonHorizontalLayout->itemAt(i)->widget());
    if (group->title().toLower() == groupName.toLower())
    {
      ribbonButtonGroup = group;
      break;
    }
  }

  if (ribbonButtonGroup != nullptr)
  {
    // Group found
    // Remove ribbon button
    ribbonButtonGroup->removeButton(button);

    if (ribbonButtonGroup->buttonCount() == 0)
    {
      // Empty button group
      // Remove button group
      removeGroup(groupName);
    }
  }
}
