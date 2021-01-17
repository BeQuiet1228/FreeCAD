#include "PreCompiled.h"
#include "PICRibbonTabContent.h"
#include "ui_PICRibbonTabContent.h"
#include "PICRibbonButtonGroup.h"
#include "picgui_ribbon/moc_PICRibbonTabContent.cpp"
#include <iostream>
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
  ui->contentLayout->addWidget(ribbonButtonGroup);
}

void PICRibbonTabContent::removeGroup(const QString &groupName)
{
  // Find ribbon group
	for (int i = 0; i < ui->contentLayout->count(); i++)
  {
		PICRibbonButtonGroup *group = static_cast<PICRibbonButtonGroup*>(ui->contentLayout->itemAt(i)->widget());
    if (group->title().toLower() == groupName.toLower())
    {
		ui->contentLayout->removeWidget(group); /// \todo :( No effect
      delete group;
      break;
    }
  }

  /// \todo  What if the group still contains buttons? Delete manually?
  // Or automaticly deleted by Qt parent() system.
}

int PICRibbonTabContent::groupCount() const
{
	return ui->contentLayout->count();
}

void PICRibbonTabContent::addButton(const QString &groupName, QToolButton *button)
{
  // Find ribbon group
  PICRibbonButtonGroup *ribbonButtonGroup = nullptr;
  for (int i = 0; i < ui->contentLayout->count(); i++)
  {
	  PICRibbonButtonGroup *group = static_cast<PICRibbonButtonGroup*>(ui->contentLayout->itemAt(i)->widget());
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
  for (int i = 0; i < ui->contentLayout->count(); i++)
  {
	  PICRibbonButtonGroup *group = static_cast<PICRibbonButtonGroup*>(ui->contentLayout->itemAt(i)->widget());
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

QList<PICRibbonButtonGroup *> PICRibbonTabContent::get_group_all()
{
	QList<PICRibbonButtonGroup *> list;
	for (int i = 0; i < ui->contentLayout->count(); i++)
	{
		PICRibbonButtonGroup *group = static_cast<PICRibbonButtonGroup*>(ui->contentLayout->itemAt(i)->widget());
		list.append(group);

	}
	return list;
}

void PICRibbonTabContent::paintEvent(QPaintEvent *event)
{
	QWidget::paintEvent(event);
	QStyleOption opt;

	opt.init(this);
	QPainter p(this);

	style()->drawPrimitive(QStyle::PE_Widget, &opt, &p, this);
}

//1.15WDT_QL新增函数
//新增分组
void PICRibbonTabContent::addGroup(PICRibbonButtonGroup * group)
{
	ui->contentLayout->addWidget(group);
}

//清除tabContent下所有分组
void PICRibbonTabContent::clearGroups()
{
	for (int i = 0; i<ui->contentLayout->count(); i++)
	{
		PICRibbonButtonGroup *group = static_cast<PICRibbonButtonGroup*>(ui->contentLayout->itemAt(i)->widget());
		ui->contentLayout->removeWidget(group);
		i--;
	}
}

