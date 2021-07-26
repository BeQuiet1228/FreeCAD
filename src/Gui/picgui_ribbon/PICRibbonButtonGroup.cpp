#include "PreCompiled.h"
#include "PICRibbonButtonGroup.h"
#include "ui_PICRibbonButtonGroup.h"

#include <QToolButton>
#include <QDebug>
#include <QGridLayout>
#include "picgui_ribbon/moc_PICRibbonButtonGroup.cpp"
PICRibbonButtonGroup::PICRibbonButtonGroup(QWidget *parent)
  : QWidget(parent)
  , ui(new Ui::PICRibbonButtonGroup)
  , m_title(tr(""))
{
  ui->setupUi(this);
  setCursor(Qt::ArrowCursor);//设置鼠标样式
  gridLayout_btn = ui->gridLayout_btn;
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
  button->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Preferred);
  button->setMinimumSize(24, 24);
  button->setAutoRaise(true);
  button->setIconSize(QSize(20,20));
  button->setToolButtonStyle(Qt::ToolButtonTextBesideIcon);
  int btnCount = buttonCount();

  int xPos = btnCount % 3;
  int yPos = btnCount / 3;
  ui->gridLayout_btn->addWidget(button, xPos, yPos);
}
void PICRibbonButtonGroup::addButton2(QToolButton *button)
{
	button->setSizePolicy(QSizePolicy::Preferred, QSizePolicy::Preferred);
	button->setMinimumSize(24, 24);
	button->setAutoRaise(true);
	button->setIconSize(QSize(20, 20));
	button->setToolButtonStyle(Qt::ToolButtonTextBesideIcon);
	int btnCount = buttonCount();
	int xPos = btnCount % 3;
	int yPos = btnCount / 3;
	ui->gridLayout_btn->addWidget(button, xPos, yPos);
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
