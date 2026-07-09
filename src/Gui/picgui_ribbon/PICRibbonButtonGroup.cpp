#include "PreCompiled.h"
#include "PICRibbonButtonGroup.h"
#include "ui_PICRibbonButtonGroup.h"

#include <QToolButton>
#include <QDebug>
#include <QGridLayout>
#include "picgui_ribbon/moc_PICRibbonButtonGroup.cpp"

namespace {

const int RibbonSmallRowCount = 3;
const int RibbonSmallRowHeight = 20;
const int RibbonSmallButtonHeight = 20;
const int RibbonSmallButtonMinWidth = 92;
const int RibbonLargeButtonMinWidth = 60;
const int RibbonLargeButtonHeight = 68;

bool isRibbonCellFree(QGridLayout* layout, int row, int column, int rowSpan)
{
  for (int i = 0; i < rowSpan; ++i) {
    if (layout->itemAtPosition(row + i, column))
      return false;
  }
  return true;
}

void findRibbonButtonPosition(QGridLayout* layout, bool largeButton, int& row, int& column, int& rowSpan)
{
  row = 0;
  column = 0;
  rowSpan = largeButton ? 3 : 1;

  if (largeButton) {
    while (!isRibbonCellFree(layout, 0, column, rowSpan))
      ++column;
    return;
  }

  while (true) {
    for (int i = 0; i < RibbonSmallRowCount; ++i) {
      if (isRibbonCellFree(layout, i, column, 1)) {
        row = i;
        return;
      }
    }
    ++column;
  }
}

void setupRibbonGridLayout(QGridLayout* layout)
{
  layout->setContentsMargins(12, 2, 12, 3);
  layout->setHorizontalSpacing(8);
  layout->setVerticalSpacing(5);
  layout->setSizeConstraint(QLayout::SetMinimumSize);

  for (int i = 0; i < RibbonSmallRowCount; ++i) {
    layout->setRowMinimumHeight(i, RibbonSmallRowHeight);
    layout->setRowStretch(i, 0);
  }
}

QAction* ribbonActionObject(QToolButton* button)
{
  QObject* object = button->property("RibbonActionObject").value<QObject*>();
  return qobject_cast<QAction*>(object);
}

QString ribbonButtonSizeProperty(QToolButton* button)
{
  QString ribbonButtonSize = button->property("RibbonButtonSize").toString();
  if (!ribbonButtonSize.isEmpty())
    return ribbonButtonSize;

  QAction* action = button->defaultAction();
  if (!action)
    action = ribbonActionObject(button);
  if (!action && !button->actions().isEmpty())
    action = button->actions().first();
  if (action)
    ribbonButtonSize = action->property("RibbonButtonSize").toString();

  if (!ribbonButtonSize.isEmpty())
    button->setProperty("RibbonButtonSize", ribbonButtonSize);
  return ribbonButtonSize;
}

}

PICRibbonButtonGroup::PICRibbonButtonGroup(QWidget *parent)
  : QWidget(parent)
  , ui(new Ui::PICRibbonButtonGroup)
  , m_title(tr(""))
{
  ui->setupUi(this);
  setCursor(Qt::ArrowCursor);//设置鼠标样式
  gridLayout_btn = ui->gridLayout_btn;
  ui->verticalLayout->setContentsMargins(0, 0, 0, 0);
  setupRibbonGridLayout(gridLayout_btn);
  ui->verticalLayout->setSpacing(5);
  ui->labelGroupName->setMinimumHeight(18);
  ui->labelGroupName->setStyleSheet(QString::fromLatin1(
    "QLabel {"
    " color: #5f6872;"
    " font-size: 11px;"
    " font-weight: normal;"
    " padding-top: 2px;"
    "}"));
}

PICRibbonButtonGroup::~PICRibbonButtonGroup()
{
  delete ui;
}

void PICRibbonButtonGroup::setTitle(const QString &title)
{
  m_title = title;
  ui->labelGroupName->setText(m_title);
}

QString PICRibbonButtonGroup::title() const
{
  return m_title;
}

int PICRibbonButtonGroup::buttonCount() const
{
  return ui->gridLayout_btn->count();
}

void PICRibbonButtonGroup::addButton(QToolButton *button)
{
  button->setParent(this);
  button->setAutoRaise(true);

  QString ribbonButtonSize = ribbonButtonSizeProperty(button);
  bool largeButton = ribbonButtonSize == QString::fromLatin1("large")
      || ribbonButtonSize == QString::fromLatin1("dropdown");

  if (ribbonButtonSize == QString::fromLatin1("large")) {
    button->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Preferred);
    button->setMinimumSize(RibbonLargeButtonMinWidth, RibbonLargeButtonHeight);
    button->setMaximumHeight(RibbonLargeButtonHeight);
    button->setIconSize(QSize(32,32));
    button->setToolButtonStyle(Qt::ToolButtonTextUnderIcon);
    button->setStyleSheet(QString());
  }
  else if (ribbonButtonSize == QString::fromLatin1("dropdown")) {
    button->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Preferred);
    button->setMinimumSize(RibbonLargeButtonMinWidth, RibbonLargeButtonHeight);
    button->setMaximumHeight(RibbonLargeButtonHeight);
    button->setIconSize(QSize(32,32));
    button->setToolButtonStyle(Qt::ToolButtonTextUnderIcon);
    button->setPopupMode(QToolButton::InstantPopup);
    button->setStyleSheet(QString());
  }
  else {
    button->setSizePolicy(QSizePolicy::MinimumExpanding, QSizePolicy::Fixed);
    button->setMinimumSize(RibbonSmallButtonMinWidth, RibbonSmallButtonHeight);
    button->setMaximumHeight(RibbonSmallButtonHeight);
    button->setIconSize(QSize(18,18));
    button->setToolButtonStyle(Qt::ToolButtonTextBesideIcon);
    button->setStyleSheet(QString::fromLatin1("QToolButton { text-align: left; }"));
  }

  int xPos = 0;
  int yPos = 0;
  int rowSpan = 1;
  findRibbonButtonPosition(ui->gridLayout_btn, largeButton, xPos, yPos, rowSpan);
  ui->gridLayout_btn->addWidget(button, xPos, yPos, rowSpan, 1, Qt::AlignLeft | Qt::AlignVCenter);
}

void PICRibbonButtonGroup::removeButton(QToolButton *button)
{
  /// \todo What happens if button is not part of the layout?
  ui->gridLayout_btn->removeWidget(button);
}

QList<QAction *> PICRibbonButtonGroup::get_action_all()
{
	QList<QToolButton*> list_b = this->findChildren<QToolButton*>();
	QList<QAction*> list;
	for (int i = 0; i<list_b.count(); i++) {
		QAction* ribbonAction = ribbonActionObject(list_b.at(i));
		if (ribbonAction)
			list.append(ribbonAction);
		else
			list.append(list_b.at(i)->actions());
	}
	return list;
}

void PICRibbonButtonGroup::paintEvent(QPaintEvent *event)
{
	QWidget::paintEvent(event);
	QStyleOption opt;

	opt.init(this);
	QPainter p(this);

	style()->drawPrimitive(QStyle::PE_Widget, &opt, &p, this);
}
void PICRibbonButtonGroup::removeButtons()
{
	//全部清理
	std::list<QToolButton*> list_b = this->findChildren<QToolButton*>().toStdList();
	for each (auto var in list_b)
	{
		removeButton(var);
		delete var;
	}
}
